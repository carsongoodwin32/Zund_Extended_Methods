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
        if cmdArs[basedir] != None:
            # We have our basedir, lets set it and use it
            basedir = cmdArs[basedir]

    # Find the config and handle all initialization of variables.
    metaConfig,materialConfig = cH.initialize()

    # Initialize and run the tests if configInfo calls for it.
    if run_tests:
        # This will kill the program if the tests fail
        fail = tH.initTests()
        if fail:
            exit(0)

    # Initialize the logger if configInfo calls for it.
    if use_logger:
        lH.initLogs()

    return 0

if __name__ == "__main__":
    main()