def exportEnvironmentReport(basedir,testResults):
    return True

def rwdTestAtPath(path):
    return [True]

def testLogDir(path):
    return path,[True]

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

    if(metaConfig.dFAP):
        #Reading, Writing, Deleting from the original files dir
        testResults.extend(rwdTestAtPath(metaConfig.oFD))
    else:
        testResults.extend([None,None,None])
    return exportEnvironmentReport(basedir,testResults)