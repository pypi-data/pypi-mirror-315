import logging
import os
import sys
from jinja2 import Environment #Template, select_autoescape, 
from jinja2.loaders import FileSystemLoader
import contextlib # for contextmanager decorator
import zipfile, tempfile, hashlib
import binascii
import yaml
from typing import Callable, Any
import pathlib
import psutil
#from dapu.placeholder import Placeholder
from enum import Enum


def reconf_logging(level=logging.DEBUG):
    """
    Once you can redefine logging globally -- before first use! (correction: or using force=True flag)
    Let's add timestamp in begginning (if no time is displayed by default (you cannot tell the bees))
    ADV: make these adaptions controlled by some env.var (not by Conf class, which may itself already use logging)
    
    https://docs.python.org/3/library/logging.html#logrecord-attributes
    %(message)s
    %(asctime)s
    %(lineno)d
    %(module)s
    %(name)s
    %(levelname)s
    """
    frm = "%(asctime)s:%(levelname)8s:%(lineno)5d:%(module)-15s:%(name)-6s:%(message)s"
    logging.basicConfig(format=frm, level=level, force=True) # Force=True is very import here for us!
    

def get_custom_logger(solution_name):
    """
    Read https://docs.python.org/3/library/logging.html
    """
    return logging.getLogger(solution_name)


def halt(code: int, message: str):
    """
    Shortcut (only for serious error situations) for logging message and do quick exit 
    Be aware: for Airflow any return code (incl 0) means that task is failed (don't use halt on normal flow!)
    For other running systems (bash script etc) You can control flow using exit code (regular end is code 0 automatically)
    Exit code must by between 0 and 255. Any other cases we will map to 255 
    """
    code = code if code >= 0 and code <= 255 else 255
    logging.error(f"{code} {message}")
    sys.exit(code)


def init_cache_intervals() -> dict[str]:
    """
    Registering some expressions what don't need to be validated using DBMS
    Called only from INIT
    """
    cached_intervals = {}
    cached_intervals['23 hours'] = True # we take responsibility that this one is correct expression
    cached_intervals['24 hours'] = True
    cached_intervals['1 days'] = True
    return cached_intervals


def real_path_from_list(args: list[str], idx:int = 0) -> str | None:
    """
    First (or idx-th, 0-started) argument will be taken as project/working directory as ultimate truth for all work
    if it is missing the run of app must be considered as totally failed
    normally returns full path which will assigned to dapuProcess self.work_dir
    """
    if len(args) <= idx:
        logging.error(f"To few arguments ({idx+1}. argument must be working directory)")
        return None
    if not os.path.exists(args[idx]) or not os.path.isdir(args[idx]):
        logging.error(f"The {idx+1}. argument must point to existing directory")
        return None
    return os.path.realpath(args[idx]) # without backslash at end


def split_task_id(task_id) -> tuple[str, str, str] | tuple[None, None, None]:
    """
    Out task_id has to be dot-seprated 3-parted string
    Actually not concern of split, but just for ease --> make all strings lowercase and through away apostrophes
    """
    id_parts = task_id.split('.')
    if len(id_parts) != 3:
        logging.error(f"Task id {task_id} is non-conformant")
        return (None, None, None) # since usually consumer unpacks it
    return (part.replace("'", "").lower() for part in id_parts) # tulpe of three strings (no apostrophes!)


def get_dirs_with_definition(dir_path: str, filename_pattern: str = None, depth: int = 1, depth_limit: int = 5) -> list[str] | None:
    """
    Leida kõik alamkaustad (täispikad nimed), kus on olemas definitsioonifail (nt 'haulwork.yaml')
    Sellised kaustad on täiemõõdulised definitsioonid (haulwork.yaml + erinevad sql-failid)
    Kaustapuu peaks olema kolmetasemeline: allikas, tulemskeem, tulemtabel
    Alustada täispika nimega kaustast
    Ülevalpool seda puud on kas lihtsalt juurikas või tulemandmebaas (kui on iga ODS omas baasis)
    Aga see, mis üleval ei puutu asjasse. Käivitatu peab ise teadma oma juurikat.
    Depth on praegune sügavus, rekursiooni korduse hoidja (NB! ja mitte sügevuse limiit)
    """

    dir_list = []

    if depth > depth_limit:  # mingi mõtestatud sügavuskontroll rekursiooni tõttu
        return dir_list

    if not os.path.exists(dir_path):
        return dir_list

    for sub_name in os.listdir(dir_path):   # sub_name on lühike nimi (st ilma pathita)
        full_name = os.path.join(dir_path, sub_name)
        if os.path.exists(full_name): # selle eitust ei saa hästi olla
            if os.path.isdir(full_name): # kui on kaust, siis kaevame edasi
                # liidame listid kokku:
                dir_list += get_dirs_with_definition(full_name, filename_pattern, depth=depth + 1, depth_limit=depth_limit) 
            else:   # on fail
                # kas on soovitud mustriga fail (kui on, siis lisame tema kausta vastusesse)
                if sub_name == filename_pattern or filename_pattern is None:
                    dir_list.append(dir_path) # pikk kaustanimi (nt ....../ods_dwh/vesi/t_mv_naitaja_curr), kus on fail meta.yaml (vms)
                    #' continue    # tahaks katkestada, aga tegelt võib olla alamkaustu, kus on ka sama def fail ? või ei luba sellist mustrit??
    return dir_list


def load_task_id_list_from_file(file_path: str, delete_afterwards: bool=False) -> list[str] | None:
    """
    Loads text file lines as list items assuming they are task_id's and thus taking only valid lines.
    Deletes file if asked.
    """
    simple_list = []
    
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        logging.debug(f"File does not exist {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as handle:
        for line in handle:
            candidate_task_id = line.strip().lower()
            if candidate_task_id == '' or ' ' in candidate_task_id:
                continue # the most simple cases lets elimiate immediatelly
            _, _, tester = split_task_id(candidate_task_id)
            if tester is not None:
                simple_list.append(candidate_task_id)

    logging.debug(f"Found {len(simple_list)} tasks in file {file_path}")
    
    if delete_afterwards:
        os.remove(file_path)
        logging.debug(f"File {file_path} deleted")
    
    return simple_list


def load_yaml_list_of_dicts(file_full_name: str, may_miss: bool = False) -> list[dict] | None:
    """
    Loads specific yaml file with list of dicts
    File must be UTF-8 encoded
    If problems return None
    Param may_miss controls only logging level (error vs info)
    """
    if not os.path.exists(file_full_name) or not os.path.isfile(file_full_name):
        if not may_miss:
            logging.error(f"Missing needed yaml-file {file_full_name}")
        else:
            logging.info(f"Missing optional yaml-file {file_full_name}")
        return None
    
    list_of_profiles = yaml.load(open(file_full_name, encoding="utf-8"), Loader=yaml.Loader)
    if not list_of_profiles: # any kind of emptiness
        logging.info(f"Empty yaml-file {file_full_name}")
        return None
    
    if not isinstance(list_of_profiles, list):
        logging.error(f"Not list/array in yaml-file {file_full_name}")
        return None
    
    if len(list_of_profiles) == 0:
        return None
    
    # cycle for information only
    for pos, item in enumerate(list_of_profiles, 1): # pos is info for human
        if not isinstance(item, dict):
            logging.warning(f"Item no {pos} is not dict in yaml-file {file_full_name}")
    
    # lets use only connecty ones
    new_list = [item for item in list_of_profiles if isinstance(item, dict)]
    
    if len(new_list) == 0:
        logging.warning(f"Empty list (no dicts in yaml-file {file_full_name})")
        return None
    
    return new_list


# enabler and registrar use it
def load_yaml(yaml_dir: str|None, yaml_file:str, empty_as:any = []) -> any :
    """
    Two way to point to file: 
    a) dir full path and file name, 
    b) None and file full path
    Return type is usually list or dict and depends on content of file
    """
    if yaml_dir is None:
        full_file_name = yaml_file
    else:
        full_file_name = os.path.join(yaml_dir, yaml_file)
    if not os.path.exists(full_file_name):
        msg = f"File {full_file_name} is not existing (it may be fine)"
        logging.warning(msg)
        return empty_as
    
    try:
        return yaml.load(open(full_file_name, encoding="utf-8"), Loader=yaml.Loader) or empty_as
    except Exception as e1:
        logging.error(str(e1))
        logging.error(f"Some error happenes while reading {full_file_name} as YAML")
        return empty_as


def interpret_string_as_yaml(yaml_content_string: str) -> dict | None:
    """
    Transform yaml string content as dict (can we avoid yaml files with arrays at the highest level?)
    """
    import yaml
    if yaml_content_string is None:
        return None
    return yaml.load(yaml_content_string, Loader = yaml.Loader) or None


def replace_dict(input_dict: dict | None) -> dict:
    """
    Recursive funtion to walk over dict and try to replace strings to env.var if string is surrounded by percent marks
    """
    new_dict : dict = {}
    if input_dict is None:
        return new_dict
    
    for key, value in input_dict.items():
        if isinstance(value, dict) :
            new_value = replace_dict(value)
        else:
            if isinstance(value, str):
                new_value = replace_value_from_env(value)
            else:
                new_value = value
        new_dict[key] = new_value
    return new_dict


def replace_value_from_env(value: str) -> str:
    """
    Replaces string with env.var value if string is surrounded with % 
    If env var with that name don't exists then return some stupidness
    """
    if value[0:1] == '%' and value[-1:] == '%':
        var_name: str = value[1:-1]
        return os.getenv(var_name, "uhuuu")
    return value


def generate(data: dict, dir: str, template_name: str) -> str:
    """
    Jinja2 template rendering with data, returning result string
    """
    loader = FileSystemLoader(dir, encoding="utf-8")
    env = Environment(loader = loader)
    template = env.get_template(template_name)
    return template.render(**data)


def compress_with_zip(src_path: str, archive_dir: str, archive_name_without_extension: str, extension: str = 'zip'):
    """
    Simple compressing, keeping structure and names
    scr_path content will be compressed
    """
    archive_path = os.path.join(archive_dir, archive_name_without_extension + "." + extension)
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive_file:
        for dir_path, _, file_names in os.walk(src_path): # subdir_names is not need for now
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                archive_file_path = os.path.relpath(file_path, src_path)
                archive_file.write(file_path, archive_file_path)
    return archive_path


def calculate_dir_hash(task_dir: str) -> str:
    """
    Recursive function to calculate directory content files content hash
    Purpose: to find out if something is changed (but no-change-save is not needed to catch)
    Obviously for that purpose You must save previous hash using same function.
    """
    dir_hash: str = ''
    list_of_items = os.listdir(task_dir) # in arbitrary order.
    for sub_name in list_of_items.sort():
        full_name = os.path.join(task_dir, sub_name)
        if os.path.isdir(full_name):
            file_hash = calculate_dir_hash(full_name) # recursive
        else:
            file_hash = calculate_file_content_hash(full_name)
        dir_hash = dir_hash + file_hash
    # dir_hash is quite long due the lot of files, so lets make it short using same hashing
    bytes_of_hash = dir_hash.encode('utf-8') # md5 wants binary input
    dir_hash = hashlib.md5(bytes_of_hash).hexdigest();
    return dir_hash


def calculate_file_content_hash(full_file_name: str ) -> str:
    """
    Calculates hash of binary file content (to detect changes)
    """
    bytes_from_file = b''
    with open(full_file_name, "rb") as file_handle:
        bytes_from_file = file_handle.read() # read file as bytes
    file_hash = hashlib.md5(bytes_from_file).hexdigest();
    logging.debug(f"Hash {file_hash} was calculated for file {full_file_name}")
    return file_hash


def content_to_file(content : str, dir: str, file_name: str) -> bool:
    """
    Save content to file named file_name into directory dir
    """
    full_name: str = os.path.join(dir, file_name)
    with open_with_missing_dirs(full_name, 'w') as handle:
        handle.write(content)
    logging.debug(f" - content saved to {os.path.realpath(full_name)}")
    return True


def is_interactive():
    """
    To differiate interactive environment (eg jupyter notebook) run from regular (command line) run
    """
    import __main__ as entry_point
    return not hasattr(entry_point, '__file__')


@contextlib.contextmanager
def temporary_dir_context(perma_path: str| None = None):
    """
    Behaves like regular temporary directory context, but if argument is not None then uses that directory as temp dir
    Rationale: to test during developing files which normally will be deleted immediatelly
    """
    if perma_path is None:
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    else:
        os.makedirs(perma_path, exist_ok=True)
        yield perma_path


@contextlib.contextmanager
def open_with_missing_dirs(path, access_mode):
    """
    Open "path" for writing, creating any parent directories as needed.
    Similar to mkdir -p dir & edit file // path = dir + file
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, access_mode, encoding='utf-8') as file_handle:
        yield file_handle


from typing import Callable # for Annotations
def make_column_creation_expression(col: tuple, source_driver_mapper_fn: Callable | None = None) -> str:
    """
    Generates from col.info tuple (col_pos, col_name, col_type, col_width, col_scale, col_primary, col_comment)
    a string to use in CREATE/ALTER TABLE command
    eg. (2, 'size', 'numeric', 10, 2, 0, 'some size') -> "size numeric(10, 2)"
    eg. (3, 'name', 'varchar', 250, 0, 0, 'some name') -> "name text"
    """
    dataclass = col[2].upper()
    if source_driver_mapper_fn is not None:
        dataclass = source_driver_mapper_fn(dataclass) # types map to postgre types (in case of PG mäping to more general PG)
    if dataclass not in ('TEXT', 'INTEGER', 'SMALLINT', 'JSONB', 'BYTEA', 'DATE', 'TIMESTAMP', 'TIME') and col[3] > 0 and col[4] is not None: # and src[4] != 65535:
        details = []
        details.append(f"{col[3]}")
        if col[4] is not None and col[4] != 65535 and dataclass != 'VARCHAR':
            details.append(f"{col[4]}")
        datatype_details = ",".join(details)
        datatype_details = f"({datatype_details})" # sulud ümber
    else:
        datatype_details = ''
    datatype = dataclass + datatype_details
    
    column_definition_for_create_table = col[1] + ' ' + datatype
    #print(column_definition_for_create_table)
    #logging.debug(column_definition_for_create_table)
    return column_definition_for_create_table


def type_mapper_code_2_function(code: str | None) -> Callable:
    """
    Return function which is able to preform maping from given DBS datatypes to PostgreSQL datatype
    Code is some name/alias to use as hint
    Function signature must be: str -> str
    """
    def echo_mapper(dataclass_name: str) -> str:
        return dataclass_name

    if not code: # incl None
        return echo_mapper
    
    if code.beginswith('asa'): # just sample
        from dbpoint.drivers.asa import DataDriver
        return DataDriver().get_mapper()
    
    return echo_mapper # fallback aka echo (typename in = typename out)


def compress_temp_dir(content_temp_dir: str) -> str: # returns hexed bytes
    """
    Compresses whole directory with structure (not sure about empty subdirs, use dummy file if important)
    Returns hex-string of bytes of compressed file
    """
    with temporary_dir_context() as zip_temp_dir:
        archive_name = 'random'
        logging.debug(f"Temporary zip file {archive_name} will be produced into {zip_temp_dir}")
        
        result_file_name = compress_with_zip(content_temp_dir, zip_temp_dir, archive_name)
        if result_file_name:
            logging.debug(f"Zipped archive file long name is {result_file_name}")
            with open(result_file_name, 'rb') as zip:
                all_bytes = zip.read()
            package_file_hex = binascii.hexlify(all_bytes).decode("ascii") # ascii or utf-8 - doesnt matter
            logging.debug(f"Hexed bytes as python binary string length is {len(package_file_hex)}")
        else:
            logging.error(f"Ziping failed")
    return package_file_hex


def version_string_from_timeint(time_int) -> str:
    """
    My own algoritm for time-versioning (human-simplified timestamp)
    Takes time-int (unix time int) 
    Reverse: @see isodate_from_version_string()
    """
    from datetime import datetime
    ts: datetime = datetime.fromtimestamp(time_int)
    seconds_from_midnight: int = (ts.hour * 60 + ts.minute) * 60 + ts.second
    day_number_in_year: int = int(ts.strftime("%j")) # '001' -> 1
    year_number_short: int = ts.year - 2000
    ver: str = f"{year_number_short:0>2d}.{day_number_in_year:0>3d}.{seconds_from_midnight:0>5d}"
    # modifiers: ':0>3'
    #   : 
    #   0 - char for fullfilling empty space (default char is ' ')
    #   > right alignment 
    #   3 - length
    #   d - variable is number (same as 'n' for integers)
    return ver


def version_string_from_time(time: any) -> str:
    """
    Wrapper to version_string_from_timeint - differrent input will casted to int and call version string function
    """
    from datetime import datetime
    if isinstance(time, datetime):
        time_int = time.timestamp()
    elif isinstance(time, str):
        if time == '':
            time_int = datetime.now().timestamp()
        try:
            time_int = datetime.fromisoformat(time).timestamp()
        except Exception as e1:
            print(e1)
            return ''
    elif isinstance(time, int | float):
        time_int = time
    else:
        return ''
    return version_string_from_timeint(time_int)


def isodate_from_version_string(ver_str) -> str:
    """
    Oposite (almost) to my own time-versioning: human-timestamp to official timestamp
    Returns time as ISO string (YYYY-MM-DD hh:mm:ss) 
    Milliseconds are 0.
    """
    from datetime import timedelta, datetime
    
    parts: list[str] = ver_str.split('.')
    years: int = int(parts[0])
    ts: datetime = datetime((2000 if years < 100 else 0) + years, 1, 1) - timedelta(days=1)
    ts
    days: int = int(parts[1])
    secs: int = int(parts[2])
    ts2: datetime = ts + timedelta(days=days, seconds=secs)
    
    return str(ts2)


def convert_to_bool(input) -> bool: # igasuguste anomaaliate vältimiseks (ja uute tekitamiseks, irw)
    """
    Special meaning strings to booleans
    Eg, psycopg2 returns (if no hack made) postgres booleans as 't' and 'f'
    Or, some json/yaml or other human-defined boolean (on/off, true/false, jah/ei, yes/no)
    """
    if isinstance(input, bool):
        return input
    if isinstance(input, str):
        input = input.lower().strip()
        if input in ('true', 'yes', 'jah', 'y', 'j', 't', 'on'):
            return True
        else:
            return False
    if input:
        return True
    return False


def lookup_first(result_set: list[tuple], nth_column: int, equals_to: any, return_col: int) -> any:
    """
    Return value of return_col of first tuple from list where tuples N-th column value equals to equals_to
    """
    for row in result_set:
        if row[nth_column] == equals_to:
            return row[return_col]
    return None
    

def sum_column(result_set: list[tuple], nth_column: int | float ) -> int | float:
    """
    Returns sum of not-null values of nth column of tuples in list
    """
    total = 0
    for row in result_set:
        total += row[nth_column] if row[nth_column] is not None else 0
    return total


def mem_free_now() -> float: 
    """
    Returns free memory in megabytes as float
    Just now psutil is only thing which needs build tools inside lightweight Alpine
    """
    return psutil.virtual_memory().available / (1024 * 1024)


def is_file_inside_git_area(file_or_dir: str | None) -> bool | None:
    """
    To keep developer copy of file we must detect if dev runs code inside git-area 
    and thus file in question is in git (and local deletion of it has bad impact).
    In auto-deployed server we don't have git, so copy of file can be deleted.
    In self-deploy case too (fake deploy in devs comp, eg xcopy in windows).

    Detecting it by existene of '.git' folder somethere upwards.
        May-be's: what if some path up is not readable for python process?

    Alternative is to use gitpython package:
    pip install gitpython
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
      = repo.working_tree_dir
      = repo.working_dir
    ...May-be's: what happenes if git is not installed -> except => return False
    """
    if file_or_dir is None:
        return None # = cannot say :(
    my_parent = fileobject_parent(file_or_dir)
    if my_parent is None: # we are at the top, root, directly below root we don't accept .git dir
        return False
    git_dir_check = os.path.join(my_parent, '.git')
    if os.path.exists(git_dir_check): # this one masks exception and returns False in any case and forcing us to check next (if we could catch error we would stop with False)
        return True
    return is_file_inside_git_area(my_parent)
    

def fileobject_parent(file_or_dir: str | None) -> str | None:
    """
    Find direct parent of file or directory.
    Full path in, full path out
    """
    if file_or_dir is None:
        return None
    path_object = pathlib.Path(file_or_dir)
    if path_object.parent == path_object.parents[-1]: 
        # if parent is the last item in list of parents (maybe next is true as well: parents list lenght is 1)
        return None # parent is root (aka anchor)
    parent_path = path_object.parents[0] # this is full path
    return parent_path  # path_object.parent


def make_replacements(original: str | None, replacements: list[tuple[str | Enum, str]] | None = None) -> str | None:
    """
    One way of two ways to replace markers inside unsafe strings (other way is Jinja, f-strings are not because they consume variables immediatelly)
    """
    if original is None:
        return None
    if not replacements:
        return original
    replaced = original
    for replacement in replacements:
        what_to_replace = replacement[0].value if isinstance(replacement[0], Enum) else str(replacement[0])
        replaced = replaced.replace(what_to_replace, replacement[1])
    return replaced


def read_sql_from_file(file_full_name: str) -> str | None:
    """
    Read utf-8 text-file content.
    File must exists and be readable. If any failure (incl empty file) return None
    """
    sql = ''
    whitespace = " \n\t"
    try:
        with open(file_full_name, 'r', encoding="utf-8") as sf:
            sql = sf.read()
        if sql.strip(whitespace) == '': # if file is sort of empty consider it as no file (smart user can overcome/cheat anyway)
            logging.error("Empty file {file_full_name}")
            return None
    except Exception as e1:
        logging.error(str(e1))
        return None
    return sql # returning all what was in file, including whitespace


def read_package_file(module_name: str, file_name: str) -> str | None:
    """
    Return content of one resource file included into named package. 
    Eg. core versioning scripts, module mappings, ...
    Subdir must have (empty) __init__.py file inside and so it can pointed as module (dot-notation).  
    And dirs/files must be built in during package build (edit pyproject.toml if problems arise).  
    File_name must be flat, no backslashes (must directly sit inside submodule) - up to 3.12
    Reads file with 'r' key (not 'rb'). Returns UTF-8 string
    """
    from importlib.resources import files # needs 3.7+, actually 3.9+
    
    try:
        # old way, deprecated in 3.11:        
        # with importlib.resources.open_text(module_name, file_name, encoding="UTF-8") as file:
        # new way, needs py 3.9, encoding="utf-8" is default (from 3.13 must used as kw-arg)
        with files(module_name).joinpath(file_name).open('r', encoding="utf-8") as handler: # 3.9+ (3.13+ allows multi pathnames)
            content = handler.read()
        return content # utf-8 string
    except Exception as e1:
        logging.error(f"Resource file {file_name} problem: {e1}")
        return None


def clean_log_message(msg: str) -> str:
    """
    No action just now but messages from external sources must go through this function
    """
    return msg.replace(":", " - ")


def task_id_eventlog(flag: str, context) -> Callable: # decorator! very special!
    """
    Decorator will insert worker_log record with desired flag. And return INT (number of rows got).
    Use decorator for function which returns result set (list on tuples) where 1st in tuple is task_id
    """
    flag = flag.upper().replace("'", "").strip()
    def inner(func: Callable[..., list[tuple]]) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> int:
            result_set = func(*args, **kwargs)
            if not result_set:
                return 0
            worker_log = context.find_registry_table_full_name('worker_log')
            for changed_row in result_set:
                changed_row_task_id = changed_row[0]
                sql_reg_log = f"""INSERT INTO {worker_log} (task_id, flag) VALUES ('{changed_row_task_id}', '{flag}')"""
                context.target(sql_reg_log, False)   
            return len(result_set)
        return wrapper
    return inner