from dapu.agents.agent import AgentGeneric
from dapu.process import logging
from dapu.perks import split_task_id
from dapu.placeholder import Placeholder

class Agent(AgentGeneric):
    """
     - do: run
       file: somefile.sql
     - do: run
       file: 
        - firstfile.sql
        - secondfile.sql
    """
    
    def do_action(self) -> bool:
        """
        Collects files (using element named "file"). If no file exists interprets as error (return False).
        
        
        """
        
        file_element = 'file'
        existing_files = self.collect_files(file_element)
        if not existing_files:
            logging.error(f"No files for tag {file_element} in {self.task_dir}")
            return False
    
        _, schema_name, table_name = split_task_id(self.task_id)
        replacements: list[tuple[str | Placeholder, str]] = []
        replacements.append((Placeholder.TARGET_SCHEMA, f'{schema_name}'))
        replacements.append((Placeholder.TARGET_TABLE, f'{table_name}'))
        
        return self.apply_files_to_target(existing_files, replacements)
    
