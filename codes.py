
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
    CODES[name] = op
    hasname.append(op)

def jrel_op(name, op):
    CODES[name] = op
    hasjrel.append(op)

def jabs_op(name, op):
    CODES[name] = op
    hasjabs.append(op)

# DEFINIÇÃO DOS CÓDIGOS ASSEMBLY

CODES['POP_TOP'] = 1
CODES['ROT_TWO'] = 2
CODES['ROT_THREE'] = 3
CODES['DUP_TOP'] = 4
CODES['DUP_TOP_TWO'] = 5
CODES['ROT_FOUR'] = 6

CODES['NOP'] = 9
CODES['UNARY_POSITIVE'] = 10
CODES['UNARY_NEGATIVE'] = 11
CODES['UNARY_NOT'] = 12

CODES['UNARY_INVERT'] = 15

CODES['BINARY_MATRIX_MULTIPLY'] = 16
CODES['INPLACE_MATRIX_MULTIPLY'] = 17

CODES['BINARY_POWER'] = 19
CODES['BINARY_MULTIPLY'] = 20

CODES['BINARY_MODULO'] = 22
CODES['BINARY_ADD'] = 23
CODES['BINARY_SUBTRACT'] = 24
CODES['BINARY_SUBSCR'] = 25
CODES['BINARY_FLOOR_DIVIDE'] = 26
CODES['BINARY_TRUE_DIVIDE'] = 27
CODES['INPLACE_FLOOR_DIVIDE'] = 28
CODES['INPLACE_TRUE_DIVIDE'] = 29

CODES['GET_AITER'] = 50
CODES['GET_ANEXT'] = 51
CODES['BEFORE_ASYNC_WITH'] = 52
CODES['BEGIN_FINALLY'] = 53
CODES['END_ASYNC_FOR'] = 54
CODES['INPLACE_ADD'] = 55
CODES['INPLACE_SUBTRACT'] = 56
CODES['INPLACE_MULTIPLY'] = 57

CODES['INPLACE_MODULO'] = 59
CODES['STORE_SUBSCR'] = 60
CODES['DELETE_SUBSCR'] = 61
CODES['BINARY_LSHIFT'] = 62
CODES['BINARY_RSHIFT'] = 63
CODES['BINARY_AND'] = 64
CODES['BINARY_XOR'] = 65
CODES['BINARY_OR'] = 66
CODES['INPLACE_POWER'] = 67
CODES['GET_ITER'] = 68
CODES['GET_YIELD_FROM_ITER'] = 69

CODES['PRINT_EXPR'] = 70
CODES['LOAD_BUILD_CLASS'] = 71
CODES['YIELD_FROM'] = 72
CODES['GET_AWAITABLE'] = 73

CODES['INPLACE_LSHIFT'] = 75
CODES['INPLACE_RSHIFT'] = 76
CODES['INPLACE_AND'] = 77
CODES['INPLACE_XOR'] = 78
CODES['INPLACE_OR'] = 79
CODES['WITH_CLEANUP_START'] = 81
CODES['WITH_CLEANUP_FINISH'] = 82
CODES['RETURN_VALUE'] = 83
CODES['IMPORT_STAR'] = 84
CODES['SETUP_ANNOTATIONS'] = 85
CODES['YIELD_VALUE'] = 86
CODES['POP_BLOCK'] = 87
CODES['END_FINALLY'] = 88
CODES['POP_EXCEPT'] = 89

HAVE_ARGUMENT =  90              # Opcodes from here have an argument:

CODES['UNPACK_SEQUENCE'] = 92   # Number of tuple items
jrel_op('FOR_ITER', 93)
CODES['UNPACK_EX'] = 94

CODES['LOAD_CONST'] = 100       # Index in const list
hasconst.append(100)
CODES['BUILD_TUPLE'] = 102    # Number of tuple items
CODES['BUILD_LIST'] = 103       # Number of list items
CODES['BUILD_SET'] = 104        # Number of set items
CODES['BUILD_MAP'] = 105        # Number of dict entries
CODES['COMPARE_OP'] = 107       # Comparison operator
hascompare.append(107)

jrel_op('JUMP_FORWARD', 110)    # Number of bytes to skip
jabs_op('JUMP_IF_FALSE_OR_POP', 111) # Target byte offset from beginning of code
jabs_op('JUMP_IF_TRUE_OR_POP', 112)  # ""
jabs_op('JUMP_ABSOLUTE', 113)        # ""
jabs_op('POP_JUMP_IF_FALSE', 114)    # ""
jabs_op('POP_JUMP_IF_TRUE', 115)     # ""

set_name('LOAD_GLOBAL', 116)     # Index in name list

jrel_op('SETUP_FINALLY', 122)   # Distance to target address

CODES['LOAD_FAST'] = 124        # Local variable number
haslocal.append(124)
CODES['STORE_FAST'] = 125       # Local variable number
haslocal.append(125)
CODES['DELETE_FAST'] = 126      # Local variable number
haslocal.append(126)

CODES['RAISE_VARARGS'] = 130    # Number of raise arguments (1] = 2] = or 3
CODES['CALL_FUNCTION'] = 131    # #args
CODES['MAKE_FUNCTION'] = 132    # Flags
CODES['BUILD_SLICE'] = 133      # Number of items
CODES['LOAD_CLOSURE'] = 135
hasfree.append(135)
CODES['LOAD_DEREF'] = 136
hasfree.append(136)
CODES['STORE_DEREF'] = 137
hasfree.append(137)
CODES['DELETE_DEREF'] = 138
hasfree.append(138)

CODES['CALL_FUNCTION_KW'] = 141  # #args + #kwargs
CODES['CALL_FUNCTION_EX'] = 142  # Flags

jrel_op('SETUP_WITH',  143)

CODES['LIST_APPEND'] = 145
CODES['SET_ADD'] = 146
CODES['MAP_ADD'] =  147

CODES['LOAD_CLASSDEREF'] = 148
hasfree.append(148)

CODES['EXTENDED_ARG'] = 144
EXTENDED_ARG =  144

CODES['BUILD_LIST_UNPACK'] = 149
CODES['BUILD_MAP_UNPACK'] = 150
CODES['BUILD_MAP_UNPACK_WITH_CALL'] = 151
CODES['BUILD_TUPLE_UNPACK'] = 152
CODES['BUILD_SET_UNPACK'] = 153

jrel_op('SETUP_ASYNC_WITH', 154)

CODES['FORMAT_VALUE'] = 155
CODES['BUILD_CONST_KEY_MAP'] = 156
CODES['BUILD_STRING'] = 157
CODES['BUILD_TUPLE_UNPACK_WITH_CALL'] = 158

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


CODES['CALL_METHOD'] = 161
jrel_op('CALL_FINALLY', 162)
CODES['POP_FINALLY'] = 163