# -*- coding: UTF-8 -*-

__all__ = ["cmp_op", "hasconst", "hasname", "hasjrel", "hasjabs",
           "haslocal", "hascompare", "hasfree", "opname", "opmap",
           "HAVE_ARGUMENT", "EXTENDED_ARG", "hasnargs"]


cmp_op = ('<', '<=', '==', '!=', '>', '>=', 'in', 'not in', 'is',
        'is not', 'exception match', 'BAD')

hasconst = []
hasname = []
hasjrel = []
hasjabs = []
haslocal = []
hascompare = []
hasfree = []
hasnargs = [] # unused
CODES = {}
opname = ['<%r>' % (op,) for op in range(256)]

def set_name(name, op):
    CODES[op] = name
    hasname.append(op)

def jrel_op(name, op):
    CODES[op] = name
    hasjrel.append(op)

def jabs_op(name, op):
    CODES[op] = name
    hasjabs.append(op)

# DEFINIÇÃO DOS CÓDIGOS ASSEMBLY

CODES[1] = 'POP_TOP'
CODES[2] = 'ROT_TWO'
CODES[3] = 'ROT_THREE'
CODES[4] = 'DUP_TOP'
CODES[5] = 'DUP_TOP_TWO'
CODES[6] = 'ROT_FOUR'

CODES[9] = 'NOP'
CODES[10] = 'UNARY_POSITIVE'
CODES[11] = 'UNARY_NEGATIVE'
CODES[12] = 'UNARY_NOT'

CODES[15] = 'UNARY_INVERT'

CODES[16] = 'BINARY_MATRIX_MULTIPLY'
CODES[17] = 'INPLACE_MATRIX_MULTIPLY'

CODES[19] = 'BINARY_POWER'
CODES[20] = 'BINARY_MULTIPLY'

CODES[22] = 'BINARY_MODULO'
CODES[23] = 'BINARY_ADD'
CODES[24] = 'BINARY_SUBTRACT'
CODES[25] = 'BINARY_SUBSCR'
CODES[26] = 'BINARY_FLOOR_DIVIDE'
CODES[27] = 'BINARY_TRUE_DIVIDE'
CODES[28] = 'INPLACE_FLOOR_DIVIDE'
CODES[29] = 'INPLACE_TRUE_DIVIDE'

CODES[50] = 'GET_AITER'
CODES[51] = 'GET_ANEXT'
CODES[52] = 'BEFORE_ASYNC_WITH'
CODES[53] = 'BEGIN_FINALLY'
CODES[54] = 'END_ASYNC_FOR'
CODES[55] = 'INPLACE_ADD'
CODES[56] = 'INPLACE_SUBTRACT'
CODES[57] = 'INPLACE_MULTIPLY'

CODES[59] = 'INPLACE_MODULO'
CODES[60] = 'STORE_SUBSCR'
CODES[61] = 'DELETE_SUBSCR'
CODES[62] = 'BINARY_LSHIFT'
CODES[63] = 'BINARY_RSHIFT'
CODES[64] = 'BINARY_AND'
CODES[65] = 'BINARY_XOR'
CODES[66] = 'BINARY_OR'
CODES[67] = 'INPLACE_POWER'
CODES[67] = 'GET_ITER'
CODES[69] = 'GET_YIELD_FROM_ITER'

CODES[70] = 'PRINT_EXPR'
CODES[71] = 'LOAD_BUILD_CLASS'
CODES[72] = 'YIELD_FROM'
CODES[73] = 'GET_AWAITABLE'

CODES[75] = 'INPLACE_LSHIFT'
CODES[76] = 'INPLACE_RSHIFT'
CODES[77] = 'INPLACE_AND'
CODES[78] = 'INPLACE_XOR'
CODES[79] = 'INPLACE_OR'
CODES[81] = 'WITH_CLEANUP_START'
CODES[82] = 'WITH_CLEANUP_FINISH'
CODES[83] = 'RETURN_VALUE'
CODES[84] = 'IMPORT_STAR'
CODES[85] = 'SETUP_ANNOTATIONS'
CODES[86] = 'YIELD_VALUE'
CODES[87] = 'POP_BLOCK'
CODES[88] = 'END_FINALLY'
CODES[89] = 'POP_EXCEPT'

HAVE_ARGUMENT =  90              # Opcodes from here have an argument:

CODES[92] = 'UNPACK_SEQUENCE'   # Number of tuple items
jrel_op('FOR_ITER', 93)
CODES[94] = 'UNPACK_EX'

CODES[100] = 'LOAD_CONST'       # Index in const list
hasconst.append(100)
CODES[102] = 'BUILD_TUPLE'    # Number of tuple items
CODES[103] = 'BUILD_LIST'       # Number of list items
CODES[104] = 'BUILD_SET'        # Number of set items
CODES[105] = 'BUILD_MAP'        # Number of dict entries
CODES[107] = 'COMPARE_OP'       # Comparison operator
hascompare.append(107)

jrel_op('JUMP_FORWARD', 110)    # Number of bytes to skip
jabs_op('JUMP_IF_FALSE_OR_POP', 111) # Target byte offset from beginning of code
jabs_op('JUMP_IF_TRUE_OR_POP', 112)  # ""
jabs_op('JUMP_ABSOLUTE', 113)        # ""
jabs_op('POP_JUMP_IF_FALSE', 114)    # ""
jabs_op('POP_JUMP_IF_TRUE', 115)     # ""

set_name('LOAD_GLOBAL', 116)     # Index in name list

jrel_op('SETUP_FINALLY', 122)   # Distance to target address

CODES[124] = 'LOAD_FAST'        # Local variable number
haslocal.append(124)
CODES[125] = 'STORE_FAST'       # Local variable number
haslocal.append(125)
CODES[126] = 'DELETE_FAST'      # Local variable number
haslocal.append(126)

CODES[130] = 'RAISE_VARARGS'    # Number of raise arguments (1] = 2] = or 3
CODES[131] = 'CALL_FUNCTION'    # #args
CODES[132] = 'MAKE_FUNCTION'    # Flags
CODES[133] = 'BUILD_SLICE'      # Number of items
CODES[135] = 'LOAD_CLOSURE'
hasfree.append(135)
CODES[136] = 'LOAD_DEREF'
hasfree.append(136)
CODES[137] = 'STORE_DEREF'
hasfree.append(137)
CODES[138] = 'DELETE_DEREF'
hasfree.append(138)

CODES[141] = 'CALL_FUNCTION_KW'  # #args + #kwargs
CODES[142] = 'CALL_FUNCTION_EX'  # Flags

jrel_op('SETUP_WITH',  143)

CODES[145] = 'LIST_APPEND'
CODES[146] = 'SET_ADD'
CODES[147] = 'MAP_ADD'

CODES[148] = 'LOAD_CLASSDEREF'
hasfree.append(148)

CODES[144] = 'EXTENDED_ARG'
EXTENDED_ARG =  144

CODES[149] = 'BUILD_LIST_UNPACK'
CODES[150] = 'BUILD_MAP_UNPACK'
CODES[151] = 'BUILD_MAP_UNPACK_WITH_CALL'
CODES[152] = 'BUILD_TUPLE_UNPACK'
CODES[153] = 'BUILD_SET_UNPACK'

jrel_op('SETUP_ASYNC_WITH', 154)

CODES[155] = 'FORMAT_VALUE'
CODES[156] = 'BUILD_CONST_KEY_MAP'
CODES[157] = 'BUILD_STRING'
CODES[158] = 'BUILD_TUPLE_UNPACK_WITH_CALL'

set_name('LOAD_METHOD', 160)

set_name('STORE_NAME', 90)       # Index in name list
set_name('DELETE_NAME', 91)      # ""

set_name('LOAD_NAME', 101)    # Index in name list
set_name('LOAD_ATTR', 106)       # Index in name list

set_name('IMPORT_NAME', 108)     # Index in name list
set_name('IMPORT_FROM', 109)     # Index in name list

set_name('STORE_ATTR', 95)      # Index in name list
set_name('DELETE_ATTR', 96)      # ""
set_name('STORE_GLOBAL', 97)     # ""
set_name('DELETE_GLOBAL', 98)    # ""


CODES[161] = 'CALL_METHOD'
jrel_op('CALL_FINALLY', 162)
CODES[163] = 'POP_FINALLY'