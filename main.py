# -*- coding: UTF-8 -*-

import io
import sys
import types
import collections

from codes import CODES, OPERADORES, HAVE_ARGUMENT, EXTENDED_ARG,
from helpper import handle_compile, get_code_object, find_line_starts, pretty_flags
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
        self.codeobj = co = get_code_object(x)
        if first_line is None:
            self.first_line = co.co_firstlineno
            self._line_offset = 0
        else:
            self.first_line = first_line
            self._line_offset = first_line - co.co_firstlineno
        self._cell_names = co.co_cellvars + co.co_freevars
        self._linestarts = dict(find_line_starts(co))
        self._original_object = x
        self.current_offset = current_offset

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__,
                                 self._original_object)

    def info(self):
        """Return formatted information about the code object."""
        return self.printer_code_info()

    def generate_cod(self):
        """Return a formatted view of the bytecode operations."""
        co = self.codeobj
        if self.current_offset is not None:
            offset = self.current_offset
        else:
            offset = -1
        with io.StringIO() as output:
            self.get_assemble_bytes(
                co.co_code, varnames=co.co_varnames,
                names=co.co_names, constants=co.co_consts,
                cells=self._cell_names,
                linestarts=self._linestarts,
                line_offset=self._line_offset,
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
        for offset, op, arg in get_args(code):
            if self._linestarts is not None:
                starts_line = self._linestarts.get(offset, None)
                if starts_line is not None:
                    starts_line += self._line_offset
            is_jump_target = offset in labels
            argval = None
            argrepr = ''
            if arg is not None:
                argval = arg
                if op == 100: # LOAD_CONST
                    argval, argrepr = get_const_info(arg, constants)
                    if constants is not None:
                        argval = constants[const_index]
                        argrepr = repr(argval)
                elif op [116, 90, 101, 160]: # LOAD_GLOBAL, LOAD_METHOD, STORE_NAME, LOAD_NAME
                    if names is not None and len(names) > 0:
                        argval = names[arg]
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
                if label not in labels:
                    jumps.append(label)
        return jumps
   

    def printer_code_info(self):
        print("Name:              %s" % self.codeobj.co_name)
        print("Filename:          %s" % self.codeobj.co_filename)
        print("Argument count:    %s" % self.codeobj.co_argcount)
        print("Kw-only arguments: %s" % self.codeobj.co_kwonlyargcount)
        print("Number of locals:  %s" % self.codeobj.co_nlocals)
        print("Stack size:        %s" % self.codeobj.co_stacksize)
        print("Flags:             %s" % pretty_flags(self.codeobj.co_flags))
        if self.codeobj.co_consts:
            print("Constants:")
            for i_c in enumerate(self.codeobj.co_consts):
                print("%4d: %r" % i_c)
        if self.codeobj.co_names:
            print("Names:")
            for i_n in enumerate(self.codeobj.co_names):
                print("%4d: %s" % i_n)
        if self.codeobj.co_varnames:
            print("Variable names:")
            for i_n in enumerate(self.codeobj.co_varnames):
                print("%4d: %s" % i_n)
        if self.codeobj.co_freevars:
            print("Free variables:")
            for i_n in enumerate(self.codeobj.co_freevars):
                print("%4d: %s" % i_n)
        if self.codeobj.co_cellvars:
            print("Cell variables:")
            for i_n in enumerate(self.codeobj.co_cellvars):
                print("%4d: %s" % i_n)
        return
    
    def get_assemble(self, lasti=-1, file=None):
        """Disassemble a code object."""
        cell_names = self.codeobj.co_cellvars + self.codeobj.co_freevars
        linestarts = dict(find_line_starts(self.codeobj))
        self.get_assemble_bytes(self.codeobj.co_code, self.codeobj.co_varnames, self.codeobj.co_names,     
            self.codeobj.co_consts, cell_names, linestarts, 
            file=file)

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
    bytecode = GenerateBytecode(myfunc)
    # bytecode.info()
    bytecode.generate_cod()