from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser
from examples import enhanceone
from examples import ts

# the next line can be removed after installation
#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyverilog
from pyverilog.vparser.parser import parse

def use(filelist):
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python example_parser.py file ..."

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    optparser = OptionParser()
    optparser.add_option("-v","--version",action="store_true",dest="showversion",
                         default=False,help="Show the version")
    optparser.add_option("-I","--include",dest="include",action="append",
                         default=[],help="Include path")
    optparser.add_option("-D",dest="define",action="append",
                         default=[],help="Macro Definition")
    (options, args) = optparser.parse_args()

    # filelist = args
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f): raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    ast, directives = parse(filelist,
                            preprocess_include=options.include,
                            preprocess_define=options.define)
    ast.show()
    A,gnamelist,listvalues,listoneregrank=ast.checksignals()#receive 4 lists
    # enhanceone.changeindex(listoneregrank,filelist)
    # ts.rpt(listoneregrank,filelist)
    # enhanceone.enhanceall(listoneregrank,filelist,1)
    # for lineno, directive in directives:
    #     print('Line %d : %s' % (lineno, directive))
    return A,gnamelist,listvalues,listoneregrank
# if __name__ == '__main__':
#     main()
