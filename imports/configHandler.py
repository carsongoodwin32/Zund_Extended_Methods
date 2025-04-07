import configparser
import os

class materialConfig:
    def __init__(self,material=None,method_file_path=None,change_type_on=None,delete_layers=None,post_process_cmd=None):
        self.mat = material
        self.mFP = method_file_path
        self.cTO = change_type_on
        self.dL = delete_layers
        self.pPC = post_process_cmd

    def parseMaterial(self,matDict):
        return

class metaConfig:
    def __init__(self, test_environment=None, log_to_file=None, path_to_log=None, log_behavior=None, watch_hotfolder=None, 
             retroactively_process=None, delete_file_after_processing=None, append_extension_string=None, 
             hotfolder_dir=None, output_dir=None, original_files_dir=None):
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

    def parseMeta(self,metaDict):
        return

def initialize(basedir):
    config = configparser.ConfigParser()

    #Check if the config exists. if not, print what's wrong and exit.
    filepath = basedir+os.sep+"settings.cfg"
    if not os.path.exists(filepath) and not os.path.isfile(filepath):
        print(str(filepath)+" does not exist! Exiting.")
        exit(0)

    #Read the config for further processing
    try:
        config.read(filepath)
    except:
        print("Fatal error proccessing config: " +str(filepath))
        exit(0)
    
    #Make sure the config has some readable section in it
    if not len(config.sections()) > 0:
        print("Empty or corrupt config: " +str(filepath))
        exit(0)

    #Make sure META exists. It's one of the only required sections
    if not 'META' in config:
        print("Missing META section in config: " +str(filepath))
        exit(0)

    #Make an empty meta object and parse the META config
    meta = metaConfig()
    meta.parseMeta(config['META'])

    #Now we can parse all the materials into an array holding their own instances of materialConfig
    materials = []
    #Remove META since we don't want to parse it twice
    matKeys = list(config.keys())
    matKeys.remove("META")
    #Run in loop for the rest of the keys in config
    for i in range(len(matKeys)):
        mat = materialConfig()
        mat.parseMaterial(config[matKeys[i]])
        materials.append(mat)

    #Return our meta and our material configs
    return meta,materials