# mixm_asm.py

# Assembler - one of the parts of MixMachine,
# which assemles mix source code ("*.mix") to
# Mix Assembled code ("*.ma")

# Main module of assembler.
# Read two file names (gets by command line arguments):
# 1) input file (required)
# 2) output file (default "out.ma")

import sys
from errors import *
from parse_file import *
import commands

DEFAULT_OUT_NAME = "out.ma"

	
#def write_ma(file, mem):
  ## do nothing
  
  #mem_str = reduce(lambda x, y: x + "\n" + str(y), mem, str())
  #file.write(mem_str)

def print_syntax_errors(errors):
  for error in errors:
    print "%i: %s" % (error[0], error[1])

def main():
  arg_number = len(sys.argv) - 1
  
  if (arg_number < 1 or arg_number > 2):
    print ERR_INVALID_ARGS[1]
    return ERR_INVALID_ARGS[0]
  
  else:
    try:
      if (arg_number == 2):
        file_out = open(sys.argv[2], "w")
      else:
        file_out = open(DEFAULT_OUT_NAME, "w")

    except IOError, (errno, strerror):
      file_out.close()
      print strerror
      return ERR_INVALID_INPUT_FILE[0]

  try:
    file_in = open(sys.argv[1], "r")
  except IOError, (errno, strerror):
    file_out.close()
    print strerror
    return ERR_FILE[0]

  lines = parse_file(file_in)
  file_in.close()
  if(lines[0] == 0): # we have errors
    print "Syntax errors in source file:"
    print_syntax_errors(lines[1])
    file_out.close()
    return ERR_SYNTAX[0]
  else:
    lines = lines[1]

  #write_ma(file_out, [23,453,124])
  file_out.close()
	
# if we executing module
if __name__ == '__main__':
  main()
