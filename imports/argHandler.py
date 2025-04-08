import argparse as ap

def createArgs(parser):
    parser.add_argument('-b','--basedir', help='Specify a directory that ZEM will pull its files from instead of its default.')
    return

def validateAndParseArgs():
    parser = ap.ArgumentParser(prog="ZEM.py")
    createArgs(parser)
    cmdArgs = vars(parser.parse_args())
    return cmdArgs