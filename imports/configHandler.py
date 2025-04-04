import configparser

class materialConfig:
    def __init__(self,material,method_file_path,change_type_on,delete_layers):
        self.mat = material
        self.mFP = method_file_path
        self.cTO = change_type_on
        self.dL = delete_layers

class metaConfig:
    def __init__(self, test_environment, log_to_file, path_to_log, log_behavior, watch_hotfolder, 
             retroactively_process, delete_file_after_processing, append_extension_string, 
             hotfolder_dir, output_dir, original_files_dir):
    self.tE = test_environment
    self.lTF = log_to_file
    self.pTL = path_to_log
    self.lB = log_behavior
    self.wH = watch_hotfolder
    self.rP = retroactively_process
    self.dFAP = delete_file_after_processing
    self.aES = append_extension_string
    self.hD = hotfolder_dir
    self.oD = output_dir
    self.oFD = original_files_dir

def initialize():
    config = configparser.ConfigParser()
    #We must parse meta first

    #Create a metaConfig class with all the info for easy parsing later.
    meta = None

    #Now we can parse all the materials into their own instances of materialConfig   
    materials = []

    #return our meta and our material configs
    return meta,materials