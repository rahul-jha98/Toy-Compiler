
from llvmlite import ir

## Temporary variable to give unique name to each print statement
print_count = 0


class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        ## Setting the length of format to be used
        ## Here we can check the type if we are to set type automatically
        ## Else we can also make number, float as two types
        i = ir.Constant(ir.IntType(32), int(self.value))
        return i


class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class Print():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        global print_count
        value = self.value.eval()

        # Declare argument list

        ## This is type of pointer for string use 
        ## IntType(8) for char
        voidptr_ty = ir.IntType(8).as_pointer()

        ## Statemet to be used in printf
        ## different for float and int
        fmt = "%i \n\0"

        ## Same char pointer dont change
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr{}".format(print_count))
        print_count = print_count + 1

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])


class Line():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        for val in self.value:
            val.eval()

class Statements():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        for val in self.value:
            val.eval()