
import io
from codes import CODES
from helpper import handle_compile, get_code_object, find_line_starts, get_instructions_bytes, _disassemble_bytes, pretty_flags

class GenerateBytecode:
    def __init__(self, x, *, first_line=None, current_offset=None):
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
        return get_instructions_bytes(co.co_code, co.co_varnames, co.co_names,
                                       co.co_consts, self._cell_names,
                                       self._linestarts,
                                       line_offset=self._line_offset)

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
            self.get_assemble_bytes(varnames=co.co_varnames,
                               names=co.co_names, constants=co.co_consts,
                               cells=self._cell_names,
                               linestarts=,
                               line_offset=self._line_offset,
                               file=output,
                               lasti=offset)
            return output.getvalue()
    
    def get_assemble_bytes(self, lasti=-1, file=None):
        # Omit the line number column entirely if we have no line number info
        show_lineno = self._linestarts is not None
        if show_lineno:
            maxlineno = max(linestarts.values()) + self._line_offset
            if maxlineno >= 1000:
                lineno_width = len(str(maxlineno))
            else:
                lineno_width = 3
        else:
            lineno_width = 0
        maxoffset = len(self.codeobj) - 2
        if maxoffset >= 10000:
            offset_width = len(str(maxoffset))
        else:
            offset_width = 4
        for instr in self.get_instructions_bytes():
            new_source_line = (show_lineno and
                            instr.starts_line is not None and
                            instr.offset > 0)
            if new_source_line:
                print(file=file)
            is_current_instr = instr.offset == lasti
            print(instr._disassemble(lineno_width, is_current_instr, offset_width),
                file=file)

    def get_instructions_bytes(self):
        """Iterate over the instructions in a bytecode string.

        Generates a sequence of Instruction namedtuples giving the details of each
        opcode.  Additional information about the code's runtime environment
        (e.g. variable names, constants) can be specified using optional
        arguments.

        """
        labels = findlabels(self.codeobj)
        starts_line = None
        for offset, op, arg in _unpack_opargs(self.codeobj):
            if linestarts is not None:
                starts_line = linestarts.get(offset, None)
                if starts_line is not None:
                    starts_line += line_offset
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
                    argval = cmp_op[arg]
                    argrepr = argval
                elif op in hasfree:
                    argval, argrepr = get_name_info(arg, cells)
                elif op == FORMAT_VALUE:
                    argval, argrepr = FORMAT_VALUE_CONVERTERS[arg & 0x3]
                    argval = (argval, bool(arg & 0x4))
                    if argval[1]:
                        if argrepr:
                            argrepr += ', '
                        argrepr += 'with format'
            #     elif op == MAKE_FUNCTION:
            #         argrepr = ', '.join(s for i, s in enumerate(MAKE_FUNCTION_FLAGS)
            #                             if arg & (1<<i))
            # yield Instruction(opname[op], op,
            #                   arg, argval, argrepr,
            #                   offset, starts_line, is_jump_target)

   
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


def myfunc(alist):
    return len(alist)

if __name__ == "__main__":
    bytecode = GenerateBytecode(myfunc)
    bytecode.info()
    bytecode.dis()