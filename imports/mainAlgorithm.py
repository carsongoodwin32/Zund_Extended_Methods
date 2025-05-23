import xml.etree.ElementTree as et
import os
from os.path import isfile, join
import shutil
import time
import datetime
import ast

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
    # Consolidate all of the method files into one array
    newMethods = []

    for i in range(len(method_files)):
        methodTree = et.parse(method_files[i])
        methodRoot = methodTree.getroot()
        for child in methodRoot:
            newMethods.append(child)

    return newMethods

def clearMethods(root):
    # Find the methods tag and remove all of the method attributes under it
    methods = root.find("./Methods")
    if methods != None:
        for method in methods.findall("Method"):
            methods.remove(method)

def addMethods(root,newMethods):
    # Append our new methods under the methods tag
    methods = root.find("./Methods")

    for method in newMethods:
        methods.append(method)

def findBestMethodMatch(method,methods):
    # Generally speaking we can just rely on the fact that methods
    # have names that match their geometry operation
    curr_method_name = method.attrib['Name']

    for child in methods:
        try:
            if child.attrib['Name'] == curr_method_name:
                return child.attrib['Type']
        except:
            continue

    return method.attrib['Type']

def renameTypes(root,cTO):
    # We run through every operation in the Geometry tag
    # If change type on has items that match the ones 
    # in the Geometry operations Type field
    # we can find the next best match and rename it.
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
    # Remove any operation in the Geometry tag that has a Name
    # field that matches an item in Delete Layers
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
    # Write the tree to the specified filepath
    tree.write(outputFile)

def postProcess(outputFile,pPCs):
    if pPCs:
        print("post process not implemented yet.")
    return

def algoEngine(inputFile,outputFile,method_files,overwrite_methods,change_type_on,delete_layers,post_process_cmds):
    # Parse the xml file into its root
    tree = et.parse(inputFile)
    root = tree.getroot()[0]

    # Setup file to be saved as .tmp
    outputFile+=".tmp"

    # Do all our method manipulation in these 3 functions
    newMethods = consolidateMethods(method_files)
    if len(newMethods) > 0:
        if overwrite_methods:
            clearMethods(root)
        addMethods(root,newMethods)

    # We can do our layer delete stuff here
    removeLayers(root,delete_layers)

    # We need to do our find and replace here if change_type_on is set
    renameTypes(root,change_type_on)

    # Write out our new file after modifications
    writeNewFile(tree,outputFile)

    # Run our post process command(s) if they exist
    postProcess(outputFile,post_process_cmds)

    # Return the name of the temp file
    return outputFile

def getOutputName(inputFile,appendExtensionString,outputDir):
    return outputDir+inputFile.split(".")[0]+appendExtensionString+"."+"".join(inputFile.split(".")[1:])

def parseFileForMaterial(inputFile,hotfolderDir):
    try:
        # Parse the xml file into its root
        tree = et.parse(os.path.join(hotfolderDir,inputFile))
        root = tree.getroot()[0]

        # We're looking for the name property of the Material tag
        material = root.find("./Material")
        materialStr = material.attrib['Name']
        
    except Exception as e:
        if "permission denied".lower() in str(e).lower():
            # We could be getting permission denied because we're still copying the file
            # It would be nice to have a max retries before it goes to do not reprocess
            return False
        else:
            # All other errors, lets just exit over. Clearly something is wrong.
            return None

    # Return what we've found
    return materialStr

def retrieveMatHits(inputFile,hotfolderDir,materialConfig):
    # Setup the holder for our hits
    matHits = []
    defaultMat = None

    # Parse the file for what material it contains
    materialStr = parseFileForMaterial(inputFile,hotfolderDir)

    # If we recieve False, from parsing the file, 
    # We're just gonna skip it and come back.
    # If we recieve None, we will error out.
    if materialStr == False:
        return False,False,False,False
    if materialStr == None:
        return None,None,None,None

    # Check if any materials match the materialStr
    for mat in materialConfig:
        if (materialStr.lower() in mat.mat.lower()) or (mat.mat.lower() == "COMMON".lower()) or (mat.mat.lower() in materialStr.lower()):
            matHits.append(mat)
        if (mat.mat.lower()=="DEFAULT".lower()):
            defaultMat = mat
    
    # In the case where we have a default mat
    if defaultMat != None:
        # Check if we have less than or equal to one hit
        if len(matHits) <= 1:
            # Check if the mat is common, if it is, we add our default mat
            try:
                if matHits[0].mat.lower() == "COMMON".lower():
                    matHits.append(defaultMat)
            except:
                matHits.append(defaultMat)

    # Setup the containers for our outputs
    method_files = []
    change_type_on = []
    delete_layers = []
    post_process_cmds = []

    # Loops through mats in what we've found in the file
    for mats in matHits:
        if mats.mFP != None:
            method_files.append(mats.mFP)
            change_type_on.append(mats.cTO)
            if mats.dL != None:
                for item in mats.dL:
                    delete_layers.extend(ast.literal_eval(item))
            post_process_cmds.append(mats.pPC)

    return method_files, change_type_on, delete_layers, post_process_cmds

def startAlgo(metaConfig,materialConfig,logObject):
    # Show configuration in logs before processing anything
    log_algo_opts(metaConfig,logObject)
    log_mat_opts(materialConfig,logObject)

    # Set Global config options for the processing engine
    overwriteMethods = metaConfig.oM
    doNotReprocess = []

    # Begin Processing
    try:
        allFiles = [f for f in os.listdir(metaConfig.hD) if isfile(join(metaConfig.hD, f))]
        # If we're not retroactively processing, we need to not process any files currently in the dir
        if metaConfig.wH and not metaConfig.rP:
            doNotReprocess.extend(allFiles)
    except Exception as e:
        logObject.log_string("Could not start main algorithm. Error getting files from hotfolder_dir.")
        logObject.log_string("Error message recieved: "+str(e))
        return 0

    logObject.log_string("Started processing files in hotfolder_dir: "+str(metaConfig.hD))

    # Valid options could be metaConfig.wH, metaConfig.rP, neither, or both
    while True:
        if metaConfig.rP or metaConfig.wH:
            # Run the algorithm Engine with our specified settings on the found file
            for inFile in allFiles:
                if  not metaConfig.aES in inFile and ".zcc" in inFile and not inFile in doNotReprocess:
                    logObject.log_string("Started processing file: "+str(inFile))
                    # Get the output name of the file
                    # This should be returned as a full path string instead of just a file name
                    outFile = getOutputName(inFile,metaConfig.aES,metaConfig.oD)
                    # Read the files material tag and retrieve all hits for all the different attributes
                    methodFiles, changeTypeOn, deleteLayers, postProcessCMDs = retrieveMatHits(inFile,metaConfig.hD,materialConfig)
                    if methodFiles == False:
                        logObject.log_string("Recieved permission denied error for file: "+str(inFile)+". Retrying...")
                        continue
                    if methodFiles == None:
                        logObject.log_string("Recieved generic fatal error for file: "+str(inFile)+". Exiting program now...")
                        return 0
                    if methodFiles:
                        # Run the main algorithm on the file, saving it as a temp file (so we don't overwrite the original)
                        tempFile = algoEngine(os.path.join(metaConfig.hD,inFile),outFile,methodFiles,overwriteMethods,changeTypeOn,deleteLayers,postProcessCMDs)
                        logObject.log_string("Saved processed file as: "+str(tempFile))
                        if metaConfig.dFAP:
                            # Go ahead and delete the original file
                            logObject.log_string("Deleting original file: "+str(inFile))
                            os.remove(os.path.join(metaConfig.hD,inFile))
                        else:
                            # We will always overwrite a file in the oFD, else we will error out.
                            if(os.path.isfile(os.path.join(metaConfig.oFD,inFile))):
                                os.remove(os.path.join(metaConfig.oFD,inFile))
                            # Move the original file to the oFD dir
                            logObject.log_string("Moving original file from: "+str(metaConfig.hD)+ " to "+str(metaConfig.oFD))
                            shutil.move(os.path.join(metaConfig.hD,inFile),metaConfig.oFD)
                        # Now we can rename the temp file to the output name
                        logObject.log_string("Renaming processed file from: "+str(inFile)+ " to "+str(outFile))
                        # We will always overwrite a file in the output, else we will error out.
                        if(os.path.isfile(outFile)):
                            os.remove(outFile)
                        os.rename(tempFile,outFile)
                    else:
                        # If method files returns [] or None or something like that
                        # mark this file as not to reprocess.
                        doNotReprocess.append(inFile)
                        logObject.log_string("No rules detected for: "+str(inFile))
                    # We've finished running rule on this file, start another loop or exit.
                    logObject.log_string("Finished processing file: "+str(inFile))
            if not metaConfig.wH:
                # We can leave the loop and exit app if we're not watching the hotfolder
                logObject.log_string("Finished processing all  files in hotfolder_dir: "+str(metaConfig.hD))
                break
            else:
                # If we are watching the hotfolder, get the most recent file listing in the directory
                allFiles = [f for f in os.listdir(metaConfig.hD) if isfile(join(metaConfig.hD, f))]

                # Check for files that exist in doNotReprocess that don't exist in allFiles anymore
                # You could have a case where someone moves a file out that existed before ZEM starts
                # and then moves it back in to start processing
                for file in doNotReprocess:
                    if file not in allFiles:
                        try:
                            doNotReprocess.remove(file)
                        except:
                            continue
        else:
            # if wH and rP are false, we can't do anything so we'll exit. 
            logObject.log_string("Current settings prevent any files from being processed.")
            break

    # This should never actually get hit in the wH case.
    return 0