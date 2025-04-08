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
    "Writing to output_dir", "Reading from output_dir", "Deleting in output_dir",
    "Writing to original_files_dir", "Reading from original_files_dir", "Deleting in original_files_dir"
    ]

    if len(testResults) < len(testStrings):
        print("Some tests not run! Exiting due to critical error!")
        return False
    if None in testResults:
        print("Some tests skipped due to 'META' config settings!")

    #Output the file here now that we've shown all warnings and we know we have all test results
    env_file = basedir+os.sep+"environment_report.txt"

    try:
        f = open(env_file, "w")
    except Exception as e:
        print("Could not open "+env_file+" for writing. Recieved Exception: "+str(e)+". Exiting due to critical error!")
        return False
    
    try:
        for i in range(len(testStrings)):
            res = "N/A"
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
    return [True,True,True]

def testLogDir(path):
    return path,[True,True,True]

def initTests(basedir,metaConfig):
    testResults = []
    #Tests we need to run:
    #Reading, Writing, Deleting from basedir
    testResults.extend(rwdTestAtPath(basedir))

    if(metaConfig.lTF):
        #Reading, Writing, Deleting the log file
        logDir,result = testLogDir(metaConfig.pTL)
        testResults.extend(result)
        #Reading, Writing, Deleting the log dir
        testResults.extend(rwdTestAtPath(logDir))
    else:
        testResults.extend([None,None,None,None,None,None])

    if(metaConfig.wH):
        #Reading, Writing, Deleting from the hotfolder
        testResults.extend(rwdTestAtPath(metaConfig.hD))
    else:
        testResults.extend([None,None,None])

    #Reading, Writing, Deleting from the output dir
    testResults.extend(rwdTestAtPath(metaConfig.oD))

    if(not metaConfig.dFAP):
        #Reading, Writing, Deleting from the original files dir
        testResults.extend(rwdTestAtPath(metaConfig.oFD))
    else:
        testResults.extend([None,None,None])
    return exportEnvironmentReport(basedir,testResults)