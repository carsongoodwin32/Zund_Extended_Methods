import os
import datetime

def timestamp_as_string():
    timestamp = datetime.datetime.now().strftime("%m-%d_%H-%M-%S")
    return f"[{timestamp}] "

def exportEnvironmentReport(basedir,testResults):
    testStrings = [
    "Writing to basedir", "Reading from basedir", "Deleting in basedir",
    "Writing to logfile", "Reading from logfile", "Deleting logfile",
    "Writing to logdir", "Reading from logdir", "Deleting in logdir",
    "Writing to hotfolder", "Reading from hotfolder", "Deleting in hotfolder",
    "Writing to processing_dir", "Reading from processing_dir", "Deleting in processing_dir",
    "Writing to output_dir", "Reading from output_dir", "Deleting in output_dir",
    "Writing to original_files_dir", "Reading from original_files_dir", "Deleting in original_files_dir"
    ]

    if len(testResults) < len(testStrings):
        print("Some tests not run! Exiting due to critical error!")
        return False
    if None in testResults:
        print("Some tests skipped due to 'META' config settings!")

    # Output the file here now that we've shown all warnings and we know we have all test results
    env_file = basedir+os.sep+"environment_report.txt"

    try:
        f = open(env_file, "w")
    except Exception as e:
        print("Could not open "+env_file+" for writing. Recieved Exception: "+str(e)+". Exiting due to critical error!")
        return False
    
    try:
        for i in range(len(testStrings)):
            res = ""
            if testResults[i] == True:
                res = "Passed"
            elif testResults[i] == False:
                res = "Failed"
            else:
                res = "Skipped"

            f.write(timestamp_as_string()+testStrings[i]+" - "+res+'\n')
    except Exception as e:
        print("Could not write to file "+env_file+". Recieved Exception: "+str(e)+". Exiting due to critical error!")
        return False

    try:
        f.close()
    except Exception as e:
        print("Could not close "+env_file+" after writing. Recieved Exception: "+str(e)+". Exiting due to critical error!")
        return False

    if False in testResults:
        print("Some tests failed! Check environment_report.txt for details! Exiting due to critical error!")
        return False
    else:
        print("All run tests passed successfully! Continuing...")
        return True

def rwdTestAtPath(path):
    testResults = []
    try:
        f = open(path+os.sep+"tmp.tmp","a")
        f.write("\ntest")
        f.close()

        testResults.append(True)
    except Exception as e:
        print("Fatal error opening tempfile for writing in "+path+" : "+str(e))
        return [False,None,None]

    try:
        f = open(path+os.sep+"tmp.tmp","r")
        f.readlines()
        f.close()
        
        testResults.append(True)
    except Exception as e:
        print("Fatal error opening tempfile for reading in "+path+" : "+str(e))
        return [testResults[0],False,None]

    try:
        os.remove(path+os.sep+"tmp.tmp")
        testResults.append(True)
    except Exception as e:
        print("Fatal error deleting tempfile in "+path+" : "+str(e))
        return [testResults[0],testResults[1],False]

    return testResults

def testLogDir(path):
    testResults = []
    basedir = os.path.dirname(path)

    file_exist = os.path.isfile(path)
    lines = None

    try:
        if path[-1] == os.sep or path[-1] == '/' or path[-1] == '\\':
            f = open(path+os.sep+"log.txt","a")
        else:
            f = open(path,"a")
        f.write("\ntest")
        f.close()

        testResults.append(True)
    except Exception as e:
        print("Fatal error opening logfile for writing: "+str(e))
        return os.path.dirname(path),[False,None,None]

    try:
        if path[-1] == os.sep or path[-1] == '/' or path[-1] == '\\':
            f = open(path+os.sep+"log.txt","r")
        else:
            f = open(path,"r")
        lines = f.readlines()
        f.close()
        
        testResults.append(True)
    except Exception as e:
        print("Fatal error opening logfile for reading: "+str(e))
        return os.path.dirname(path),[testResults[0],False,None]

    try:
        if file_exist:
            f = open(path,"w")
            f.writelines(lines[:-1])
            f.close()

            testResults.append(None)
        else:
            if path[-1] == os.sep or path[-1] == '/' or path[-1] == '\\':
                os.remove(path+os.sep+"log.txt")
            else:
                os.remove(path)
            testResults.append(True)
    except Exception as e:
        print("Fatal error deleting logfile: "+str(e))
        return os.path.dirname(path),[testResults[0],testResults[1],False]

    return basedir,testResults

def initTests(basedir,metaConfig):
    testResults = []
    # Tests we need to run:
    # Reading, Writing, Deleting from basedir
    testResults.extend(rwdTestAtPath(basedir))

    if(metaConfig.lTF):
        # Reading, Writing, Deleting the log file
        logDir,result = testLogDir(metaConfig.pTL)
        testResults.extend(result)
        # Reading, Writing, Deleting the log dir
        testResults.extend(rwdTestAtPath(logDir))
    else:
        testResults.extend([None,None,None,None,None,None])

    if(metaConfig.wH):
        # Reading, Writing, Deleting from the hotfolder
        testResults.extend(rwdTestAtPath(metaConfig.hD))
    else:
        testResults.extend([None,None,None])

    if(metaConfig.mTPD):
        # Reading, Writing, Deleting from the hotfolder
        testResults.extend(rwdTestAtPath(metaConfig.pD))
    else:
        testResults.extend([None,None,None])

    # Reading, Writing, Deleting from the output dir
    testResults.extend(rwdTestAtPath(metaConfig.oD))

    if(not metaConfig.dFAP):
        # Reading, Writing, Deleting from the original files dir
        testResults.extend(rwdTestAtPath(metaConfig.oFD))
    else:
        testResults.extend([None,None,None])
        
    # Flip bool for return, we expect True when we've failed.
    return not exportEnvironmentReport(basedir,testResults)