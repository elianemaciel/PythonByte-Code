
#!/usr/bin/env python
# # # # # # # # # # # # #
# Create a code object  #
# # # # # # # # # # # # #

from types import CodeType
import dis
import sys

import teste
# if sys.version_info.major < 3:
#     print("You need python 3 to run this code.")
#     sys.exit(1)

# co_code = bytes([101, 0, 0,    #Load print function
#                  101, 1, 0,    #Load name 'a'
#                  101, 2, 0,    #Load name 'b'
#                  23,           #Take first two stack elements and store their sum
#                  131, 1, 0,    #Call first element in the stack with one positional argument
#                  1,            #Pop top of stack
#                  101, 0, 0,    #Load print function
#                  101, 1, 0,    #Load name 'a'
#                  101, 2, 0,    #Load name 'b'
#                  20,           #Take first two stack elements and store their product
#                  131, 1, 0,    #Call first element in the stack with one positional argument
#                  1,            #Pop top of stack
#                  100, 0, 0,    #Load constant None
#                  83])          #Return top of stack

# lnotab = bytes([14,1])

# my_code = CodeType(
#             0,
#             0,
#             0,
#             3,
#             64,
#             co_code,
#             (None,),
#             ('print', 'a', 'b'),
#             (),
#             'my_code_filename',
#             'my_code',
#             1,
#             lnotab,
#             freevars=(),
#             cellvars=() )


def main():

    dis.dis(teste) # disassemble the code


if __name__ == '__main__':
    main()