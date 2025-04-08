import os

import imports.argHandler as aH
import imports.configHandler as cH
import imports.logHandler as lH
import imports.testHandler as tH

basedir = ""

def main():
    # Parse arguments passed to python script
    cmdArgs = aH.validateAndParseArgs()

    # Default basedir to the current dir
    basedir = os.getcwd()

    # We could have no args
    if cmdArgs != None:
        # We could have args, but no basedir
        if cmdArgs["basedir"] != None:
            # We have our basedir, lets set it and use it
            basedir = cmdArgs["basedir"]

    # Find the config and handle all initialization of variables.
    metaConfig,materialConfig = cH.initialize(basedir)

    # Initialize and run the tests if configInfo calls for it.
    if metaConfig.tE:
        # This will kill the program if the tests fail
        fail = tH.initTests(basedir,metaConfig)
        if fail:
            exit(0)

    # Initialize the logger if configInfo calls for it.
    if metaConfig.lTF:
        lH.initLogs(metaConfig.pTL,metaConfig.lB)
        lH.logObject.log_string("Logger set up successfully!")

    #At this point in the code we can now make the assumptions that:
    #'META' config is !syntactically! correct.
    #material specific, common, and default configs are !syntactically! correct.
    #We have all the permissions we want/need for all relevant directories.
    #Everything except for the main code has been initialized (configs, loggers, testers, etc)



    return 0

if __name__ == "__main__":
    main()