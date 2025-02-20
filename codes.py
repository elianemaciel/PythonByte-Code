# -*- coding: UTF-8 -*-

OPERADORES = ['<', '<=', '==', '!=', '>', '>=', 'in', 'is', 'is not']

CODES = {}
HAVE_ARGUMENT =  90

# DEFINIÇÃO DOS CÓDIGOS ASSEMBLY
CODES[20] = 'BINARY_MULTIPLY'

CODES[23] = 'BINARY_ADD'
CODES[24] = 'BINARY_SUBTRACT'
CODES[27] = 'BINARY_TRUE_DIVIDE'
CODES[29] = 'INPLACE_TRUE_DIVIDE'

CODES[55] = 'INPLACE_ADD'
CODES[56] = 'INPLACE_SUBTRACT'
CODES[57] = 'INPLACE_MULTIPLY'

CODES[67] = 'GET_ITER'

CODES[70] = 'PRINT_EXPR'

CODES[92] = 'UNPACK_SEQUENCE'   # Number of tuple items
CODES[93] = 'FOR_ITER'
CODES[94] = 'UNPACK_EX'

CODES[100] = 'LOAD_CONST'
CODES[107] = 'COMPARE_OP'       # Comparison operator

CODES[110] = 'JUMP_FORWARD'
CODES[113] = 'JUMP_ABSOLUTE'
CODES[114] = 'POP_JUMP_IF_FALSE'

CODES[116] = 'LOAD_GLOBAL'

CODES[124] = 'LOAD_FAST'        # Local variable number
CODES[125] = 'STORE_FAST'       # Local variable number

CODES[131] = 'CALL_FUNCTION'    # #args

CODES[144] = 'EXTENDED_ARG'
EXTENDED_ARG =  144

CODES[155] = 'FORMAT_VALUE'

CODES[160] = 'LOAD_METHOD'
CODES[90] = 'STORE_NAME'
CODES[101] = 'LOAD_NAME'