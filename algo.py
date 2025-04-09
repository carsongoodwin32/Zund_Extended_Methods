#temporary scratchpad workspace for the algorithm that will be combined with all the code later
import xml.etree.ElementTree as et

mF = [".\\testing\\method_files\\9mm.xml",".\\testing\\method_files\\common.xml"]
cTO = '{none}'
dL = ["#meta-data","none"]
pPC = ""
oM = True

iF = ".\\testing\\test_files\\test.zcc"
oF = ".\\testing\\test_files\\test.zem.zcc"

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
                    if method.attrib['Type'] == cTO:
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

def postProcess(outputFile,pPC):
    return

def algoEngine(inputFile,outputFile,method_files,overwrite_methods,change_type_on,delete_layers,post_process_cmd):
    tree = et.parse(inputFile)
    root = tree.getroot()[0]

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

    #Run our post process command if it exists
    postProcess(outputFile,post_process_cmd)

algoEngine(iF,oF,mF,oM,cTO,dL,pPC)