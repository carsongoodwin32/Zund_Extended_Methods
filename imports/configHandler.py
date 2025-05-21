import configparser
import os
import ast

class materialConfig:
    def __init__(self,material=None,method_file_path=None,change_type_on=None,delete_layers=None,post_process_cmd=None):
        self.mat = material
        self.mFP = method_file_path
        self.cTO = change_type_on
        self.dL = delete_layers
        self.pPC = post_process_cmd

    def validateMaterial(self):
        if (self.mFP != None):
            mfpExist = False

            #Check if the path is a file
            if os.path.isfile(self.mFP):
                mfpExist = True

            if(not mfpExist):
                print("settings.cfg validation failed for config '"+self.mat+"': method_file "+self.mFP+" is inaccessible. Check that the provided file exists.")
                exit(-1)
        return

    def parseMaterial(self,mat,matDict):
        self.mat = mat
        #Check if method_file even exists in this dict
        if 'method_file' in matDict:
            #Basic checks to see if it's actually a file
            try:
                if isinstance(matDict['method_file'],str) and len(matDict['method_file'])>0 and matDict['method_file'][-4:] == '.xml':
                    self.mFP = matDict['method_file']
            except Exception as e:
                print("Error parsing 'method_file' for config "+mat+". Exception recieved: '"+str(e)+"'")
                self.mFP = None

        #Check if change_type_on even exists in this dict
        if 'change_type_on' in matDict:
            #I don't think this needs to be wrapped in a try except, but whatever
            try:
                if isinstance(matDict['change_type_on'],str):
                    self.cTO = matDict['change_type_on']
            except Exception as e:
                print("Error parsing 'change_type_on' for config "+mat+". Exception recieved: '"+str(e)+"'")
                self.cTO = None
        
        #Check if delete_layers even exists in this dict
        if 'delete_layers' in matDict:
            #configparser handles arrays nicely.
            #This is undocumented, but we'll also handle just a straight string
            try:
                if isinstance(matDict['delete_layers'],str):
                    self.dL = [matDict['delete_layers']]
                elif isinstance(matDict['delete_layers'],list):
                    self.dL = matDict['delete_layers']
            except Exception as e:
                print("Error parsing  'delete_layers' for config "+mat+". Exception recieved: '"+str(e)+"'")
                self.dL = None

        #Check if post_process_cmd even exists in this dict
        if 'post_process_cmd' in matDict:
            #I dont think this one needs try except either
            try:
                if (isinstance(matDict['post_process_cmd'],str) and len(matDict['method_file'])>0):
                    self.pPC = matDict['post_process_cmd']
            except Exception as e:
                print("Error parsing 'post_process_cmd' for config "+mat+". Exception recieved: '"+str(e)+"'")
                self.pPC = None

class metaConfig:
    def __init__(self, test_environment=False, log_to_file=False, path_to_log=None, log_behavior='append', watch_hotfolder=False, 
             retroactively_process=False, overwrite_methods=True, delete_file_after_processing=False, append_extension_string='.zem', 
             hotfolder_dir=None, output_dir=None, original_files_dir=None):
        self.tE = test_environment
        self.lTF = log_to_file
        self.pTL = path_to_log
        self.lB = log_behavior
        self.wH = watch_hotfolder
        self.rP = retroactively_process
        self.oM = overwrite_methods
        self.dFAP = delete_file_after_processing
        self.aES = append_extension_string
        self.hD = hotfolder_dir
        self.oD = output_dir
        self.oFD = original_files_dir

    def validateMeta(self):
        #Validate dependency rules of META config
        if(self.lTF):
            if(self.pTL == None):
                print("settings.cfg validation failed: path_to_log not set while log_to_file = true")
                exit(-1)

        if(self.wH):
            if(self.hD == None):
                print("settings.cfg validation failed: hotfolder_dir not set while watch_hotfolder = true")
                exit(-1)

        if(self.aES.lower() == ".zcc"):
            print("settings.cfg validation failed: append_extension_string cannot be '.zcc'")
            exit(-1)

        if(self.oD == None):
            print("settings.cfg validation failed: output_dir not set")
            exit(-1)
        
        if(not self.dFAP):
            if(self.oFD == None):
                print("settings.cfg validation failed: original_files_dir not set while delete_files_after_processing = false")
                exit(-1)           
            else:
                if(self.oFD == self.hD or self.oFD == self.oD):  
                    print("settings.cfg validation failed: original_files_dir is equal to hotfolder_dir or output_dir")
                    exit(-1)

        #Validate paths and files defined in META config
        if(self.lTF):
            logExist = False

            #Check if the path is a file
            if os.path.isfile(self.pTL):
                logExist = True

            #Check if the path containing the file exists
            dir_path = os.path.dirname(self.pTL)
            if os.path.isdir(dir_path):
                logExist = True

            #Check if the path is a directory
            if os.path.isdir(self.pTL):
                logExist = True
            
            if(not logExist):
                print("settings.cfg validation failed: path_to_log directory inaccessible. Check that the provided directory exists.")
                exit(-1)
        
        if(self.wH):
            hotfolderExist = False

            #Check if the path is a directory
            if os.path.isdir(self.hD):
                hotfolderExist = True
            
            if(not hotfolderExist):
                print("settings.cfg validation failed: hotfolder_dir directory inaccessible. Check that the provided directory exists.")
                exit(-1)

        if(not self.dFAP):
            ofdExist = False

            #Check if the path is a directory
            if os.path.isdir(self.oFD):
                ofdExist = True
            
            if(not ofdExist):
                print("settings.cfg validation failed: original_files_dir directory inaccessible. Check that the provided directory exists.")
                exit(-1)

        outputExist = False
        
        #Check if the path is a directory
        if os.path.isdir(self.oD):
            outputExist = True
        
        if(not outputExist):
            print("settings.cfg validation failed: output_dir directory inaccessible. Check that the provided directory exists.")
            exit(-1)
        


    def parseMeta(self,metaDict):
        if 'test_environment' in metaDict:
            try:
                if metaDict['test_environment'].lower() == "true":
                    self.tE = True
                else:
                    self.tE = False
            except Exception as e:
                print("Error parsing 'test_environment' for config: META. Exception recieved: '"+str(e)+"'")
                self.tE = False
        
        if 'log_to_file' in metaDict:
            try:
                if metaDict['log_to_file'].lower() == "true":
                    self.lTF = True
                else:
                    self.lTF = False
            except Exception as e:
                print("Error parsing 'log_to_file' for config: META. Exception recieved: '"+str(e)+"'")
                self.lTF = False
        
        if 'path_to_log' in metaDict:
            try:
                self.pTL = metaDict['path_to_log']
            except Exception as e:
                print("Error parsing 'path_to_log' for config: META. Exception recieved: '"+str(e)+"'")
                self.pTL = None

        if 'log_behavior' in metaDict:
            try:
                if metaDict['log_behavior'].lower() == "overwrite":
                    self.lB = "overwrite"
                else:
                    self.lB = "append"
            except Exception as e:
                print("Error parsing 'log_behavior' for config: META. Exception recieved: '"+str(e)+"'")
                self.lB = "append"

        if 'watch_hotfolder' in metaDict:
            try:
                if metaDict['watch_hotfolder'].lower() == "true":
                    self.wH = True
                else:
                    self.wH = False
            except Exception as e:
                print("Error parsing 'watch_hotfolder' for config: META. Exception recieved: '"+str(e)+"'")
                self.wH = False

        if 'retroactively_process' in metaDict:
            try:
                if metaDict['retroactively_process'].lower() == "true":
                    self.rP = True
                else:
                    self.rP = False
            except Exception as e:
                print("Error parsing 'retroactively_process' for config: META. Exception recieved: '"+str(e)+"'")
                self.rP = False

        if 'overwrite_methods' in metaDict:
            try:
                if metaDict['overwrite_methods'].lower() == "true":
                    self.oM = True
                else:
                    self.oM = False
            except Exception as e:
                print("Error parsing 'overwrite_methods' for config: META. Exception recieved: '"+str(e)+"'")
                self.oM = True

        if 'delete_file_after_processing' in metaDict:
            try:
                if metaDict['delete_file_after_processing'].lower() == "true":
                    self.dFAP = True
                else:
                    self.dFAP = False
            except Exception as e:
                print("Error parsing 'delete_file_after_processing' for config: META. Exception recieved: '"+str(e)+"'")
                self.dFAP = False

        if 'append_extension_string' in metaDict:
            try:
                self.aES = metaDict['append_extension_string']
            except Exception as e:
                print("Error parsing 'append_extension_string' for config: META. Exception recieved: '"+str(e)+"'")
                self.aES = '.zem'

        if 'hotfolder_dir' in metaDict:
            try:
                self.hD = metaDict['hotfolder_dir']
            except Exception as e:
                print("Error parsing 'hotfolder_dir' for config: META. Exception recieved: '"+str(e)+"'")
                self.hD = None

        if 'output_dir' in metaDict:
            try:
                self.oD = metaDict['output_dir']
            except Exception as e:
                print("Error parsing 'output_dir' for config: META. Exception recieved: '"+str(e)+"'")
                self.oD = None

        if 'original_files_dir' in metaDict:
            try:
                self.oFD = metaDict['original_files_dir']
            except Exception as e:
                print("Error parsing 'original_files_dir' for config: META. Exception recieved: '"+str(e)+"'")
                self.oFD = None


def initialize(basedir):
    config = configparser.ConfigParser()

    #Check if the config exists. if not, print what's wrong and exit.
    filepath = basedir+os.sep+"settings.cfg"
    if not os.path.exists(filepath) and not os.path.isfile(filepath):
        print(str(filepath)+" does not exist! Exiting.")
        exit(-1)

    #Read the config for further processing
    try:
        config.read(filepath)
    except:
        print("Fatal error proccessing config: " +str(filepath))
        exit(-1)
    
    #Make sure the config has some readable section in it
    if not len(config.sections()) > 0:
        print("Empty or corrupt config: " +str(filepath))
        exit(-1)

    #Make sure META exists. It's one of the only required sections
    if not 'META' in config:
        print("Missing META section in config: " +str(filepath))
        exit(-1)

    #Make an empty meta object and parse the META config
    meta = metaConfig()
    meta.parseMeta(config['META'])

    #Validate meta for errors
    meta.validateMeta()

    #Now we can parse all the materials into an array holding their own instances of materialConfig
    materials = []
    #Remove META since we don't want to parse it twice
    matKeys = list(config.keys())
    matKeys.remove("META")
    #Run in loop for the rest of the keys in config
    for i in range(len(matKeys)):
        mat = materialConfig()
        mat.parseMaterial(matKeys[i],config[matKeys[i]])
        mat.validateMaterial()
        materials.append(mat)

    #Return our meta and our material configs
    return meta,materials