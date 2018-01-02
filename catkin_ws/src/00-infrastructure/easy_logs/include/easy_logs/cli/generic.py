from abc import abstractmethod
import duckietown_utils as dtu
from duckietown_utils.cli import D8AppWithLogs


class GenericLogDisplay(D8AppWithLogs): 

    def define_options(self, params): 
        params.accept_extra(description='Log query string')
        
        
    @abstractmethod
    def show_info(self, logs):
        pass
    
    def go(self):
        extra = self.options.get_extra()
        if not extra:
            query = '*'
        else:
            if len(extra) > 1:
                msg = 'Expected only one extra argument.'
                raise dtu.DTUserError(msg)
            query = extra[0]
        
        db = self.get_easy_logs_db() 
        logs = db.query(query)
     
        self.info('Found %d logs.' % len(logs))
        self.show_info(logs)
