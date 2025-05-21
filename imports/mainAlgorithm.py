import xml.etree.ElementTree as et
from os import listdir
from os.path import isfile, join
import time
import datetime

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

def consolidateMethods(method_files):
    newMethods = []

    for i in range(len(method_files)):
        methodTree = et.parse(method_files[i])
        methodRoot = methodTree.getroot()
        for child in methodRoot:
            newMethods.append(child)

    return newMethods

def clearMethods(root):
    methods = root.find("./Methods")
    if methods != None:
        for method in methods.findall("Method"):
            methods.remove(method)

def addMethods(root,newMethods):
    methods = root.find("./Methods")

    for method in newMethods:
        methods.append(method)

def findBestMethodMatch(method,methods):
    curr_method_name = method.attrib['Name']

    for child in methods:
        try:
            if child.attrib['Name'] == curr_method_name:
                return child.attrib['Type']
        except:
            continue

    return method.attrib['Type']

def renameTypes(root,cTO):
    methods = root.find("./Methods")

    geometry = root.find("./Geometry")
    if geometry != None:
        for child in geometry:
            for method in child.findall("Method"):
                try:
                    for item in cTO:
                        if method.attrib['Type'] == item:
                            method.attrib['Type'] = findBestMethodMatch(method,methods)
                except:
                    continue

def removeLayers(root,dL):
    geometry = root.find("./Geometry")
    if geometry != None:
        for outline in geometry.findall("Outline"):
            delete_outline = False
            for method in outline.findall("Method"):
                try:
                    if method.attrib['Name'] in dL:
                        delete_outline = True
                except:
                    continue
            if delete_outline:
                geometry.remove(outline)

def writeNewFile(tree,outputFile):
    tree.write(outputFile)

def postProcess(outputFile,pPCs):
    return

def algoEngine(inputFile,outputFile,method_files,overwrite_methods,change_type_on,delete_layers,post_process_cmds):
    tree = et.parse(inputFile)
    root = tree.getroot()[0]

    #Setup file to be saved as .tmp
    outputFile+=".tmp"

    #Do all our method manipulation in these 3 functions
    newMethods = consolidateMethods(method_files)
    if len(newMethods) > 0:
        if overwrite_methods:
            clearMethods(root)
        addMethods(root,newMethods)

    #We can do our layer delete stuff here
    removeLayers(root,delete_layers)

    #We need to do our find and replace here if change_type_on is set
    renameTypes(root,change_type_on)

    #Write out our new file after modifications
    writeNewFile(tree,outputFile)

    #Run our post process command(s) if they exist
    postProcess(outputFile,post_process_cmds)

    #Return the name of the temp file
    return outputFile

def getOutputName(inputFile,appendExtensionString,outputDir):
    return outputDir+inputFile.split(".")[0]+appendExtensionString+"."+"".join(inputFile.split(".")[1:])

def retrieveMatHits(inputFile,hotfolderDir):
    matHits = []

    for mats in matHits:
    return [],[],[]

def startAlgo(metaConfig,materialConfig,logObject):
    #Show configuration in logs before processing anything
    log_algo_opts(metaConfig,logObject)
    log_mat_opts(materialConfig,logObject)
    #Set Global config options for the processing engine
    overwriteMethods = metaConfig.oM
    #Begin Processing
    try:
        allFiles = [f for f in listdir(metaConfig.hD) if isfile(join(metaConfig.hD, f))]
    except as Exception e:
        logObject.log_string("Could not start main algorithm. Error getting files from hotfolder_dir.")
        logObject.log_string("Error message recieved: "+str(e))
        return 0

    # Valid options could be metaConfig.wH, metaConfig.rP, neither, or both
    while True:
        if metaConfig.rP or metaConfig.wH:
            # Set watch date to now
            watchTime = time.time()
            if metaConfig.rP:
                # If we're retroactively processing, set watchDate to the Unix epoch.
                watchTime = 0
            #Run the algorithm Engine with our specified settings on the found file
            for inFile in allFiles:
                logObject.log_string("Started processing files in hotfolder_dir: "+str(metaConfig.hD))
                creation_time = os.path.getctime(inFile)
                if creation_time >= watchTime and not ".zem" in inFile:
                    logObject.log_string("Started processing file: "+str(inFile))
                    outFile = getOutputName(inFile,metaConfig.aES,metaConfig.hD,metaConfig.oD)
                    # methodFiles, change_type_on, delete_layers, postProcessCMDs = retrieveMatHits(inFile)
                    tempFile = algoEngine(inFile,outFile,methodFiles,overwriteMethods,changeTypeOn,deleteLayers,postProcessCMDs)
                    logObject.log_string("Saved processed file as: "+str(tempFile))
                    if metaConfig.dFAP:
                        logObject.log_string("Deleting original file: "+str(inFile))
                        deleteFile(inFile,metaConfig.hD)
                    else:
                        logObject.log_string("Moving original file from: "+str(metaConfig.hD)+ "to "+str(metaConfig.oFD))
                        moveFile(inFile,metaConfig.hD,metaConfig.oFD)
                    logObject.log_string("Renaming processed file from: "+str(inFile)+ "to "+str(outFile))
                    renameFile(tempFile,outFile)
                    logObject.log_string("Finished processing file: "+str(inFile))
            if not metaConfig.wH:
                logObject.log_string("Finished processing all  files in hotfolder_dir: "+str(metaConfig.hD)+" Exiting program...")
                break
            else:
                allFiles = [f for f in listdir(metaConfig.hD) if isfile(join(metaConfig.hD, f))]
        else:
            logObject.log_string("Current settings prevent any files from being processed. Exiting program...")
            break

    return 0