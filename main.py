# -*- coding: UTF-8 -*-

import io
import sys
import types
import collections

from codes import CODES, OPERADORES, HAVE_ARGUMENT, EXTENDED_ARG
from helpper import handle_compile, find_line_starts
from Instruction import Instruction

FORMAT_VALUE = CODES.get(155)
FORMAT_VALUE_CONVERTERS = (
    (None, ''),
    (str, 'str'),
    (repr, 'repr'),
    (ascii, 'ascii'),
)
MAKE_FUNCTION = CODES.get('MAKE_FUNCTION')
MAKE_FUNCTION_FLAGS = ('defaults', 'kwdefaults', 'annotations', 'closure')

class GenerateBytecode:
    def __init__(self, x, first_line=None, current_offset=None):
        self.codeobj = co = self.get_code_object(x)
        if first_line is None:
            self.first_line = co.co_firstlineno
            self.line_offset = 0
        else:
            self.first_line = first_line
            self.line_offset = first_line - co.co_firstlineno
        self.cell_names = co.co_cellvars + co.co_freevars
        self.linestarts = dict(find_line_starts(co))
        self.original_object = x
        self.current_offset = current_offset

    def __repr__(self):
        return "{}({!r})".format(
            self.__class__.__name__,
            self.original_object
        )
    
    def get_code_object(self, code):
        if hasattr(code, '__func__'):
            code = code.__func__
        if hasattr(code, '__code__'):
            code = code.__code__
        elif hasattr(code, 'gi_code'):
            code = code.gi_code
        elif hasattr(code, 'ag_code'):
            code = code.ag_code
        elif hasattr(code, 'cr_code'):
            code = code.cr_code
        if isinstance(code, str):
            code = handle_compile(code)
        if hasattr(code, 'co_code'):
            return code

    def generate_cod(self):
        co = self.codeobj
        if self.current_offset is not None:
            offset = self.current_offset
        else:
            offset = -1
        with io.StringIO() as output:
            self.get_assemble_bytes(
                co.co_code, varnames=co.co_varnames,
                names=co.co_names, constants=co.co_consts,
                cells=self.cell_names,
                linestarts=self.linestarts,
                line_offset=self.line_offset,
                file=output,
                lasti=offset
            )
            return output.getvalue()
    
    def get_assemble_bytes(self, code, varnames, names, constants, cells, linestarts, 
            line_offset, file=None, lasti=-1):
  
        for instr in self.get_instructions_bytes(
                code, varnames, names, constants, cells, linestarts, line_offset=line_offset):
            instr.printer_line()

    def get_instructions_bytes(self, code, varnames=None, names=None, constants=None,
                      cells=None, linestarts=None, line_offset=0):
        labels = self.args_jumps(code)
        starts_line = None
        for offset, op, arg in self.get_args(code):
            if self.linestarts is not None:
                starts_line = self.linestarts.get(offset, None)
                if starts_line is not None:
                    starts_line += self.line_offset
            is_jump_target = offset in labels
            argval = None
            argrepr = ''
            if arg is not None:
                argval = arg
                if op == 100: # LOAD_CONST
                    if constants is not None:
                        argval = constants[arg]
                        argrepr = repr(argval)
                elif op in [116, 90, 101, 160]: # LOAD_GLOBAL, LOAD_METHOD, STORE_NAME, LOAD_NAME
                    if names is not None and len(names) > 0:
                        argval = nam    es[arg]
                        argrepr = argval
                    else:
                        argrepr = repr(argval)
                elif op == 124 or op == 125: # LOAD_FAST, STORE_FAST
                    if varnames is not None and len(varnames) > 0:
                        argval = varnames[arg]
                        argrepr = argval
                    else:
                        argrepr = repr(argval)
                elif op == 107: # COMPARE_OP
                    argval = OPERADORES[arg]
                    argrepr = argval
                    pass
                elif op == FORMAT_VALUE:
                    argval, argrepr = FORMAT_VALUE_CONVERTERS[arg & 0x3]
                    argval = (argval, bool(arg & 0x4))
                    if argval[1]:
                        if argrepr:
                            argrepr += ', '
                        argrepr += 'with format'
                elif op == MAKE_FUNCTION:
                    argrepr = ', '.join(s for i, s in enumerate(MAKE_FUNCTION_FLAGS)
                                        if arg & (1<<i))
            yield Instruction(CODES.get(op), op,
                              arg, argval, argrepr, 
                              offset, starts_line, is_jump_target)

    def get_args(self, code):
        extended_arg = 0
        for i in range(0, len(code), 2):
            op = code[i]
            if op >= HAVE_ARGUMENT:
                arg = code[i+1] | extended_arg
                extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
            else:
                arg = None
            yield (i, op, arg)
    
    def args_jumps(self, code):
        jumps = []
        for offset, op, arg in self.get_args(code):
            if arg is not None:
                if op == 110 or op == 93: # JUMP_FORWARD, FOR_ITER
                    label = offset + 2 + arg
                elif op == 113 or op == 114: # JUMP_ABSOLUTE or POP_JUMP_IF_FALSE
                    label = arg
                else:
                    continue
                if label not in jumps:
                    jumps.append(label)
        return jumps
   
    def get_assemble(self, lasti=-1, file=None):
        cell_names = self.codeobj.co_cellvars + self.codeobj.co_freevars
        linestarts = dict(find_line_starts(self.codeobj))
        self.get_assemble_bytes(
            self.codeobj.co_code,
            self.codeobj.co_varnames,
            self.codeobj.co_names,
            self.codeobj.co_consts,
            cell_names,
            linestarts,
            line_offset=self.line_offset,
            file=file
        )

    def get_assemble_recusive(self, x, file=None, depth=None):
        self.get_assemble(file=file)
        if depth is None or depth > 0:
            if depth is not None:
                depth = depth - 1
            for x in self.codeobj.co_consts:
                if hasattr(x, 'co_code'):
                    # print(file=file)
                    print("Disassembly of %r:" % (x,))
                    self.get_assemble_recusive(x, depth=depth)

def myfunc(alist):
    return len(alist)

if __name__ == "__main__":
    arquivocode = "code.txt"
    filecode = open(arquivocode)
    source = filecode.read()
    code = compile(source, "code.txt", "exec")
    bytecode = GenerateBytecode(code)
    bytecode.generate_cod()