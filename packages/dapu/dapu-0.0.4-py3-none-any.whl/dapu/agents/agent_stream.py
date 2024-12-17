from dapu.agents.agent import AgentGeneric
from dapu.process import logging
from typing import Callable
from dapu.perks import split_task_id
from dapu.perks import make_replacements, read_sql_from_file

class Agent(AgentGeneric):
    '''
    stream - uses dbpoint/dbhub copy feature
    '''
       
    def do_action(self) -> bool:
        _, target_schema, target_table = split_task_id(self.task_id)

        file_element = 'file'
        existing_files = self.collect_files(file_element)
        if not existing_files:
            logging.error(f"No files for tag {file_element} in {self.task_dir}")
            return False
        full_file_name = existing_files[0]

        sql: str = read_sql_from_file(full_file_name) # no replacements here (reason is...?)
        
        map_columns: dict = None # FIXME
        
        # columns tuleb lähtebaasi päringust
        #truncate_table = True
        #create_table = True
        full_table_name = f"{target_schema}.{target_table}"
        temp_name = 'juu'
        logging.debug(f"STREAMING...from {self.route_alias}")
        
        if sql: # empty sql is ok and returns True
            logging.debug(f"{self.task_id} stream import step")
            #print(f"striiming... from {self.route_alias}")
            #flow : Iterable = self.context.hub.get_driver(self.route_alias).stream
            
            fn_once : Callable = self.fn_once()
            fn_prep_cmd : Callable = self.fn_prepare_insert_to_target(target_schema, target_table)
            fn_before : Callable = self.fn_side_effects_truncate_target(target_schema, target_table)
            fn_save : Callable = self.fn_save()
            
            cnt = self.context.hub.copy_to(sql, self.route_alias, fn_once, fn_before, fn_prep_cmd, fn_save)
            if cnt < 0:
                logging.error(f"{self.task_id} has error on import")
                if cnt < -1: # at least one row was saved (-2 means that error was in second row)
                    # we may want save pointer (last ts, last id etc)
                    ...
                    logging.warning(f"{self.task_id} failed, but some rows were imported, {(-cnt) -1}")
                return False
            if cnt == 0:
                logging.warning(f"{self.task_id} did not import rows!")
            else:
                logging.info(f"{self.task_id} imported {cnt} rows")
        
        self.context.disconnect_alias(self.route_alias)
        logging.debug(f"STREAMING anyway ended and {self.route_alias} is disconnected now")
        return True

    
    def fn_once(self):
        def do_once():
            route_alias = self.route_alias
            cols_def = self.context.hub.get_columns_definition(route_alias) # last query, was just executed..
            map_columns = None # FIXME
            if map_columns is None:
                list_columns = ', '.join([col_def['name'] for col_def in cols_def])
                posinfo = [jrk for jrk, col_def in enumerate(cols_def)]
            else:
                list_columns = ', '.join([map_columns[col_def['name']] for col_def in cols_def if col_def['name'] in map_columns and map_columns[col_def['name']] != ''])
                posinfo = [jrk for jrk, col_def in enumerate(cols_def) if col_def['name'] in map_columns and map_columns[col_def['name']] != '']
            typeinfo = [(col_def['class'], col_def['needs_escape']) for col_def in cols_def]
            #logging.debug(f"Columns are {list_columns}")
            return {"columns" : list_columns, "pos" : posinfo, "type" : typeinfo}
        return do_once

    
    def fn_side_effects_drop_temp(self, temp_name) -> Callable:
        def do_side_effects():
            sql = f"DROP TABLE IF EXISTS {temp_name}"
            self.context.target(sql, False)
            return True
        return do_side_effects


    def fn_side_effects_truncate_target(self, target_schema, target_table) -> Callable:
        def do_side_effects():
            sql = f"TRUNCATE TABLE {target_schema}.{target_table}"
            self.context.target(sql, False)
            return True
        return do_side_effects


    def fn_side_effects_drop_target(self, target_schema, target_table) -> Callable:
        def do_side_effects():
            sql = f"DROP TABLE IF EXISTS {target_schema}.{target_table}"
            self.context.target(sql, False)
            return True
        return do_side_effects
    
    
    def fn_side_effects_truncate_temp(self, temp_name) -> bool:
        def do_side_effects():
            sql = f"TRUNCATE TABLE {temp_name}"
            self.context.target(sql, False)
            return True
        return do_side_effects
    
    
    def fn_save(self) -> Callable: # one save command (usually on row insert)
        def do_save(cmd, pos):
            try:
                self.context.target(cmd, False)
            except Exception as e1:
                logging.error(f"Pos {pos} has error")
                logging.error(f"{cmd}")
                return False
            return True # if not exception
        return do_save


    def fn_escape(self) -> Callable :
        def do_escape(cell_value, v2, v3):
            # v2 = typeinfo[cell_pos][0]
            # v3 = typeinfo[cell_pos][1]
            return self.context.hub.escape(self.context.TARGET_ALIAS, cell_value, v2, v3)
        return do_escape

    
    def fn_prepare_insert_to_temp(self, temp_table):
        def prepare_row_for_insert(row : list | tuple, perma : dict) -> str:
            list_columns = perma.get('columns')
            if list_columns is None:
                logging.error = f"No columns ?!?!"
                return ''
            posinfo = perma['pos']
            typeinfo = perma['type']
            esca = self.fn_escape()
            row_insert_values = ", ".join([esca(cell_value, typeinfo[cell_pos][0], typeinfo[cell_pos][1]) for cell_pos, cell_value in enumerate(row) if cell_pos in (posinfo)])
            cmd = f"INSERT INTO {temp_table} ({list_columns}) VALUES ({row_insert_values})"
            return cmd
        return prepare_row_for_insert


    def fn_prepare_insert_to_target(self, target_schema, target_table):
        def prepare_row_for_insert(row : list | tuple, perma : dict) -> str:
            if perma is None:
                logging.error = f"No no no ??!"
                return ''
            list_columns = perma.get('columns')
            if list_columns is None:
                logging.error = f"No columns ?!?!"
                return ''
            posinfo = perma['pos']
            typeinfo = perma['type']
            esca = self.fn_escape()
            row_insert_values = ", ".join([esca(cell_value, typeinfo[cell_pos][0], typeinfo[cell_pos][1]) for cell_pos, cell_value in enumerate(row) if cell_pos in (posinfo)])
            cmd = f"INSERT INTO {target_schema}.{target_table} ({list_columns}) VALUES ({row_insert_values})"
            return cmd
        return prepare_row_for_insert
