MAX_OPERATOR_WIDTH = 20
MAX_ARGS_WIDTH = 5

class Instruction:

    def __init__(self, opname="", opcode="", arg="", argval="", argrepr="", offset="", starts_line="",      is_jump_target=""):

        self.opname = opname
        self.opcode = opcode
        self.arg = arg
        self.argval = argval
        self.argrepr = argrepr
        self.offset = offset
        self.starts_line = starts_line
        self.is_jump_target = is_jump_target
    
    def __repr__(self):
        return "opname = " + str(self.opname) + ", opcode = " + str(self.opcode) + ", arg = " + str(self.arg) + ", len= " + str(self.argval) + ", argrepr = " + str(self.argrepr) + ", offset = " + str(self.offset) + ", starts_line = " + str(self.starts_line) 

    def printer_line(self, offset_width=4):
        line = []
        if self.starts_line is not None:
            line.append("%3d" % self.starts_line)
        else:
            line.append('   ')
        line.append(str(self.offset).rjust(4))
        if (self.opname):     
            line.append(str(self.opname).ljust(20))
        else:
            line.append(' '.ljust(20))
        if self.arg is not None:
            line.append(str(self.arg).rjust(5))
            if self.argrepr:
                line.append('(' + self.argrepr + ')')
        print(" ".join(line))
