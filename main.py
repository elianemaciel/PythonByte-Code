# -*- coding: UTF-8 -*-

import io
import sys
import types
import collections

from codes import CODES
from codes import hasconst, hasname, hasjrel, hasjabs, haslocal, hascompare, hasfree
from helpper import handle_compile, get_code_object, find_line_starts, pretty_flags, findlabels, _unpack_opargs, get_const_info, get_name_info



FORMAT_VALUE = CODES.get(155)
FORMAT_VALUE_CONVERTERS = (
    (None, ''),
    (str, 'str'),
    (repr, 'repr'),
    (ascii, 'ascii'),
)
MAKE_FUNCTION = CODES.get('MAKE_FUNCTION')
MAKE_FUNCTION_FLAGS = ('defaults', 'kwdefaults', 'annotations', 'closure')
_OPNAME_WIDTH = 20
_OPARG_WIDTH = 5

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

    def __iter__(self):
        co = self.codeobj
        return self.get_instructions_bytes()

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__,
                                 self._original_object)

    def info(self):
        """Return formatted information about the code object."""
        return self.printer_code_info()

    def dis(self):
        """Return a formatted view of the bytecode operations."""
        import ipdb; ipdb.set_trace()
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
        # Omit the line number column entirely if we have no line number info
        show_lineno = linestarts is not None
        if show_lineno:
            maxlineno = max(linestarts.values()) + self._line_offset
            if maxlineno >= 1000:
                lineno_width = len(str(maxlineno))
            else:
                lineno_width = 3
        else:
            lineno_width = 0
        maxoffset = len(code) - 2
        if maxoffset >= 10000:
            offset_width = len(str(maxoffset))
        else:
            offset_width = 4
        for instr in self.get_instructions_bytes(code, varnames, names,
                                         constants, cells, linestarts,
                                         line_offset=line_offset):
            new_source_line = (show_lineno and
                            instr.starts_line is not None and
                            instr.offset > 0)
            if new_source_line:
                # pass
                print(file=file)
            is_current_instr = instr.offset == lasti
            print(instr.get_assemble(lineno_width, is_current_instr, offset_width), file=file)

    def get_instructions_bytes(self, code, varnames=None, names=None, constants=None,
                      cells=None, linestarts=None, line_offset=0):
        """Iterate over the instructions in a bytecode string.

        Generates a sequence of Instruction namedtuples giving the details of each
        opcode.  Additional information about the code's runtime environment
        (e.g. variable names, constants) can be specified using optional
        arguments.

        """
        labels = findlabels(code)
        starts_line = None
        for offset, op, arg in _unpack_opargs(code):
            if self._linestarts is not None:
                starts_line = self._linestarts.get(offset, None)
                if starts_line is not None:
                    starts_line += self._line_offset
            is_jump_target = offset in labels
            argval = None
            argrepr = ''
            if arg is not None:
                #  Set argval to the dereferenced value of the argument when
                #  available, and argrepr to the string representation of argval.
                #    _disassemble_bytes needs the string repr of the
                #    raw name index for LOAD_GLOBAL, LOAD_CONST, etc.
                argval = arg
                if op in hasconst:
                    argval, argrepr = get_const_info(arg, constants)
                elif op in hasname:
                    argval, argrepr = get_name_info(arg, names)
                elif op in hasjrel:
                    argval = offset + 2 + arg
                    argrepr = "to " + repr(argval)
                elif op in haslocal:
                    argval, argrepr = get_name_info(arg, varnames)
                elif op in hascompare:
                    # argval = cmp_op[arg]
                    # argrepr = argval
                    pass
                elif op in hasfree:
                    argval, argrepr = get_name_info(arg, cells)
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
            print(op)
            print(CODES.get(op))
            yield Instruction(CODES.get(op), op,
                              arg, argval, argrepr,
                              offset, starts_line, is_jump_target)

   
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
        self.get_assemble_bytes()

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

    def assemble_str(self, source, **kwargs):
        """Compile the source string, then disassemble the code object."""
        self.get_assemble_recusive(handle_compile(source, '<dis>'), **kwargs)

class Instruction:
    """Details for a bytecode operation

       Defined fields:
         opname - human readable name for operation
         opcode - numeric code for operation
         arg - numeric argument to operation (if any), otherwise None
         argval - resolved arg value (if known), otherwise same as arg
         argrepr - human readable description of operation argument
         offset - start index of operation within bytecode sequence
         starts_line - line started by this opcode (if any), otherwise None
         is_jump_target - True if other code jumps to here, otherwise False
    """

    def __init__(self, opname="", opcode="", arg="", argval="", argrepr="", offset="", starts_line="",      is_jump_target=""):

        self.opname = opname
        self.opcode = opcode
        self.arg = arg
        self.argval = argval
        self.argrepr = argrepr
        self.offset = offset
        self.starts_line = starts_line
        self.is_jump_target = is_jump_target

    def get_assemble(self, lineno_width=3, mark_as_current=False, offset_width=4):
        """Format instruction details for inclusion in disassembly output

        *lineno_width* sets the width of the line number field (0 omits it)
        *mark_as_current* inserts a '-->' marker arrow as part of the line
        *offset_width* sets the width of the instruction offset field
        """
        fields = []
        # Column: Source code line number
        if lineno_width:
            if self.starts_line is not None:
                lineno_fmt = "%%%dd" % lineno_width
                fields.append(lineno_fmt % self.starts_line)
            else:
                fields.append(' ' * lineno_width)
        # Column: Current instruction indicator
        if mark_as_current:
            fields.append('-->')
        else:
            fields.append('   ')
        # Column: Jump target marker
        if self.is_jump_target:
            fields.append('>>')
        else:
            fields.append('  ')
        # Column: Instruction offset from start of code sequence
        fields.append(repr(self.offset).rjust(offset_width))
        # Column: Opcode name
        print(self.opname)
        fields.append(self.opname.ljust(_OPNAME_WIDTH))
        # Column: Opcode argument
        if self.arg is not None:
            fields.append(repr(self.arg).rjust(_OPARG_WIDTH))
            # Column: Opcode argument details
            if self.argrepr:
                fields.append('(' + self.argrepr + ')')
        return ' '.join(fields).rstrip()


def myfunc(alist):
    return len(alist)

if __name__ == "__main__":
    bytecode = GenerateBytecode(myfunc)
    bytecode.info()
    bytecode.dis()