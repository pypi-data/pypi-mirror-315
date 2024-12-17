from typing import Any
from dbpoint.dbpoint import Hub
from dapu.perks import read_package_file, interpret_string_as_yaml

class DapuContext():
    """
    One central class which have one instance what can be given as starting point to all next Dapu-sh components
    (Workers inits Job and Job inits Manager, using context, context values are calculated in very first process in sequence)
    """
    def __init__(self) -> None:

        self.work_dir: str | None = None # target directory (=src in source code, see "layout"), must be initialized
        self.flags: list = [] # clear known arguments (eg. debug)
        self.more_args: list = [] # and other unclear arguments
        self.LOG_LEVEL : int = 20 # don't use here enums directly from logging (cycle will occur!)

        # Critical version: myversion vs meta.stopper.allowed_version
        self.MYVERSION = 2 # int, increment it every time if needed to prevent previous code to start any more

        self.CONF_SUB_DIR: str = 'conf' # fixed! this folder may have conf.yaml for overriding default hard-coded here
        self.CONF_FILE_NAME: str = 'conf.yaml' # if not existing defaults are used (application level fine tuning)

        self.PACKAGE_NAME : str = 'dapu' # for dynamic loading
        self.PACKAGE_VER_SUB_DIR: str = 'ver' # has meaning of "submodule" under module above, keeps core versioning files

        self.PROJECT_VER_SUB_DIR: str = 'ver' # sub dir for custom versioning 
        self.CHANGES_INDEX_FILE_NAME = 'changes.yaml' # same name for both core and custom versioning
        self.TABLE_VER_SUB_DIR: str = 'ver' # for target tables versioning (last part in path /mytarget/ver), here no index file (just numbers)

        self.ROUTES_SUB_DIR: str = 'routes' # for target tables definitions (last part in path mytarget/routes)
        self.ROUTE_FILE_NAME = 'route.yaml' # inside dir directly under pull (mytarget/pull/from_asjur5/route.yaml)

        self.APP_NAME : str = 'dapu' # for logging and temp dir under system-wide temp dir (don't use spaces, don't live complicated life)
        
        self.TARGET_ALIAS: str = 'target' # main connection name/reference (to database where meta tables reside)
        self.CONF_SQL_FILE_NAME: str = 'sql.yaml' # inside conf directory
        self.DAPU_SCHEMA = 'meta' # the latest idea: lets call schema this way, just "meta"
        self.DAPU_PREFIX = '' # and lets prefix all tables in above mentioned schema this way (no prefix)

        self.CONF_API_FILE_NAME: str = 'api.yaml' # inside conf directory
        self.CONF_FILE_FILE_NAME: str = 'file.yaml' # inside conf directory        

        self.list_of_profiles : list[dict] # profiles for rdbms (must think, where to keep api and file access profiles)
        self.hub: Hub | None = None # multidatabase (aka hub)
        self.agents: dict[str, dict] = {} # agents meta will be loaded on first call of get_agents
        self.agents_loaded = False

        # Cleaner:
        self.DELETE_LOGS_OLDER_THEN: str = "2 months"
        self.DELETE_TRACE_LOGS_OLDER_THEN: str = "15 days"
        self.DELETE_AGENDA_OLDER_THEN: str = "14 months" # PROD keskkonnas soovituslik vähemalt aasta, nt 14 months

        # Registrar:
        self.FILENAME_DEFINITION_FILE: str = 'haulwork.yaml' # NB! lowercase!!
        self.FILENAME_FOR_DELETION = 'tasks_to_delete.txt' # file inside conf (mytarget/conf/tasks_to_delete.txt)
        
        # Manager
        self.FAILURE_LIMIT : int = 3
        self.DEFAULT_MANAGER_INTERVAL: str = '4 hours'
        self.DEFAULT_KEEP_GOING_INTERVAL: str = '5 hours' # '2 minutes' # '2 days' # valid PG interval, 

        # Worker
        self.worker_id : int = None
        self.WORKER_NO_NEW_HAUL_AFTER_MINUTES: int = 27
        self.AGENTS_INDEX_FILE_NAME = 'agents.yaml' # in root of dapu, in the target dir (work_dir) if custom are needed


    def get_agent_definition(self, agent_alias: str) -> dict | None:
        """
        For dynamical load of module which will do action we need all allowed packages/modules defined.  
        We trust our own modules (built-in dapu.agents.agent_...) and may-be some external.
        """
        if not agent_alias:
            return None
        if not self.agents_loaded:
            self.load_agents_index()
        agent: dict | None = self.agents.get(agent_alias) # või None
        return agent


    def load_agents_index(self):
        """
        If agents definitions (alias -> package & module) are not loaded yet, lets do it.
        Definitions can be locally built in or current loading project ones.
        """
        core_agents = interpret_string_as_yaml(read_package_file(self.PACKAGE_NAME, self.AGENTS_INDEX_FILE_NAME))
        custom_agents = {}
        try:
            with open(self.full_name_from_root(self.AGENTS_INDEX_FILE_NAME), 'r', encoding='utf-8') as file:
                content = file.read()
            custom_agents = interpret_string_as_yaml(content) or {}
        except Exception as e1:
            pass # custom agents listing file don't need to exists
        self.agents = core_agents | custom_agents # | needs 3.9+
        self.agents_loaded = True
        

    def run(self, *args: list, **kwargs: dict) -> Any:
        """ Wrapper """
        return self.hub.run(*args, **kwargs)


    def target(self, *args: list, **kwargs: dict) -> Any:
        """ Wrapper """
        return self.hub.run(self.TARGET_ALIAS, *args, **kwargs)
    

    def disconnect_target(self):
        """ Wrapper """
        self.hub.disconnect(self.TARGET_ALIAS)


    def disconnect_all(self):
        """ Wrapper """
        self.hub.disconnect_all()


    def disconnect_alias(self, profile_name: str):
        """ Wrapper """
        self.hub.disconnect(profile_name)


    def full_name_from_root(self, inner_part: str | list[str]):
        return self._full_name(inner_part)
    

    def full_name_from_pull(self, inner_part: str | list[str]):
        """ Project level routes root, usually mytarget/routes (old way: mytarget/pull) """
        if isinstance(inner_part, str):
            inner_part = [inner_part]
        return self._full_name([self.ROUTES_SUB_DIR, *inner_part])
    

    def full_name_from_ver(self, inner_part: str | list[str]): 
        """ Custom overall versioning, usually mytarget/ver """
        return self._full_name([self.PROJECT_VER_SUB_DIR, inner_part])
    

    def full_name_from_conf(self, inner_part: str | list[str]): 
        """ Custom overall versioning, usually mytarget/ver """
        return self._full_name([self.CONF_SUB_DIR, inner_part])


    def _full_name(self, inner_part: str | list[str]) -> str | None:
        """
        Returns full name of inside file object (dir or file) short name (or list of part components).
        Don't use it directly! Private function ;)
        """
        import os
        if not self.work_dir:
            raise Exception("work_dir don't have value")
        if not inner_part:
            raise Exception("inner part is missing")
        if isinstance(inner_part, str):
            return os.path.join(self.work_dir, inner_part)
        if isinstance(inner_part, list):
            return os.path.join(self.work_dir, *inner_part)
        raise Exception(f"inner part type is wrong {type(inner_part)}")


    #@lru_cache(maxsize=120, typed=False) -> CacheInfo(hits=24, misses=19, maxsize=120, currsize=19) 
    # not very helpful: there are max 7 different arguments (table_short_name), why 19 misses?
    #@cache # now it may have point to use cache (now = after remaking this as context own function)
    def find_registry_table_full_name(self, table_short_name: str) -> str:
        #logging.debug(f"Usage of {table_short_name}")
        """
        from short name makes full table name according to system global setup (compatibility with historical ideas)
        "agenda" -> "meta.bis_agenda" or "bis.agenda" or "bis.bis_agenda"
        """
        schema_part = ''
        if self.DAPU_SCHEMA is not None and self.DAPU_SCHEMA.strip() > '': # if schema name is present
            schema_part = self.DAPU_SCHEMA.strip() + '.' # dot at end as seperator between schema name and table name
        
        table_prefix = ''
        if self.DAPU_PREFIX is not None and self.DAPU_PREFIX.strip() > '':
            table_prefix = self.DAPU_PREFIX.strip()
        
        return ('').join([schema_part, table_prefix, table_short_name])


    def find_loaded_profile(self, profile_name: str) -> dict:
        name_key: str='name'
        profile: dict = {}
        for one_profile in self.list_of_profiles:
            if isinstance(one_profile, dict) and one_profile.get(name_key) == profile_name:
                profile = one_profile.copy()
                break
        return profile


    def replace_compatibility(self, sql: str, local_replacements : list[tuple] = []) -> str:
        """
        Owner is nice trick here (so each new schema can be created with minimal effort (copy-paste))
        """
        replacements = []
        replacements.append(('{schema}', self.DAPU_SCHEMA))
        replacements.append(('{prefix}', self.DAPU_PREFIX))
        replacements.append(('{owner}', self.hub.get_profile(self.TARGET_ALIAS)['username'])) # after schema create
        for local_replacement in local_replacements: # orvuke tegelt (orphan, never assigned yet)
            replacements.append(local_replacement) # tuple[str, str]
        
        for replacement in replacements:
            sql = sql.replace(replacement[0], replacement[1])
        return sql
   