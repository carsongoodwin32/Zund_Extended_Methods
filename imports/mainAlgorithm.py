from lxml import etree

def log_algo_opts(metaConfig,logObject):
    logObject.log_string("Main Algorithm Started!")
    logObject.log_string("[META] Meta Configured with:")
    logObject.log_string("Watch Hotfolder: "+str(metaConfig.wH))
    logObject.log_string("Retroactively Process: "+str(metaConfig.rP))
    logObject.log_string("Delete Files after Processing: "+str(metaConfig.dFAP))
    logObject.log_string("Appended Extension String: "+str(metaConfig.aES))
    logObject.log_string("Hotfolder Dir: "+str(metaConfig.hD))
    logObject.log_string("Output Dir: "+str(metaConfig.oD))
    logObject.log_string("Original Files Dir: "+str(metaConfig.oFD))
    return

def log_mat_opts(materialConfig,logObject):
    logObject.log_string("Found "+str(len(materialConfig))+" material configs!")
    for i in range(len(materialConfig)):
        logObject.log_string("[MATERIAL] Material '"+materialConfig[i].mat+"' configured with:")
        logObject.log_string("Method File: "+str(materialConfig[i].mFP))
        logObject.log_string("Change Type on: "+str(materialConfig[i].cTO))
        if materialConfig[i].dL != None:
            logObject.log_string("Delete Layers: "+', '.join(materialConfig[i].dL))
        logObject.log_string("Post Process Command: "+str(materialConfig[i].pPC))
    return

def startAlgo(metaConfig,materialConfig,logObject):
    #Show configuration in logs before processing anything
    log_algo_opts(metaConfig,logObject)
    log_mat_opts(materialConfig,logObject)
    #Begin Processing

    return 0