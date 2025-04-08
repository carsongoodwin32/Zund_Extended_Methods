import os
import datetime

def timestamp_as_string():
    timestamp = datetime.datetime.now().strftime("%m-%d_%H-%M-%S")
    return f"[{timestamp}] "

class logger:
    def __init__(self,log_active=False,log_behavior=None,path_to_log=None):
        self.lA = log_active
        self.lB = log_behavior
        self.pTL = path_to_log

    def log_string(self,lS):
        try:
            log_str = str(lS.lstrip().rstrip())
            if self.lA:
                f = open(self.pTL,'a')
                f.write(timestamp_as_string()+log_str+'\n')
            print("[LOGGER]: "+log_str)
        except Exception as e:
            print("logger.log_string() hit an exception: "+str(e))
        return
    
    def activate_logger(self,path_to_log,log_behavior):
        f_o = 'w'
        l_B = log_behavior.strip().lower()

        if(l_B == 'append'):
            f_o = 'a'

        try:
            f = open(path_to_log,f_o)
            f.close()
        except Exception as e:
            print("logger.activate_logger() hit an exception: "+str(e))
            return
        
        self.lA = True
        self.lB = l_B
        self.pTL = path_to_log
        return

#Define a global logObject that everyone can access.
logObject = logger()

def initLogs(path,log_behavior):
    new_path_to_log = None

    if path[-1] == os.sep or path[-1] == '/' or path[-1] == '\\':
        new_path_to_log = path+os.sep+"log.txt"
    else:
        new_path_to_log = path

    logObject.activate_logger(new_path_to_log,log_behavior)
    return