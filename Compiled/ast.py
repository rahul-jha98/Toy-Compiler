from llvmlite import ir

## Temporary variable to give unique name to each print statement
print_count = 0


class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        try:
            i = ir.Constant(ir.IntType(32), int(self.value))
        except ValueError:
            i = ir.Constant(ir.FloatType(32), float(self.value))
        return i


class Bool():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value
    
    def eval(self):        
        return ir.Constant(ir.IntType(1), int(self.value))

class String():
    def __init__(self, value, trim = True):
        if trim: 
            self.value = value[1:-1]
        else:
            self.value = value
    
    def eval(self):
        return self.value



class BinaryOp():
    #operations for binary operations
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

class Mul(BinaryOp):
    def eval(self):
        i = self.builder.mul(self.left.eval(), self.right.eval())
        return i

class Div(BinaryOp):
    def eval(self):
        i = self.builder.sdiv(self.left.eval(), self.right.eval())
        return i

class Mod(BinaryOp):
    def eval(self):
        i = self.builder.srem(self.left.eval(), self.right.eval())
        return i



class RelOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right

    def truthvalue(self):
        return True 


    def eval(self):
        return self.truthvalue()



class Equals(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('==', self.left.eval(), self.right.eval())


class Greater(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('>', self.left.eval(), self.right.eval())

class Less(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('<', self.left.eval(), self.right.eval())

class LessEq(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('<=', self.left.eval(), self.right.eval())

class GreatEq(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('>=', self.left.eval(), self.right.eval())






class And:
    def __init__(self, builder, module, left, right):
        self.left = left
        self.right = right
        self.builder = builder
        self.module = module
        
    def eval(self):
        return self.builder.and_(self.left.eval(), self.right.eval())

class Or:
    def __init__(self, builder, module, left, right):
        self.left = left
        self.right = right
        self.builder = builder
        self.module = module

    def eval(self):
        return self.builder.or_(self.left.eval(), self.right.eval())

class Not:
    def __init__(self, builder, module, express):
        self.express = express
        self.builder = builder
        self.module = module
    
    def eval(self):
        return self.builder.sub(ir.Constant(ir.IntType(8), int(1)), self.express.eval())



class Write():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        global print_count



        passvalue = True
        value = self.value.eval()
    
        if isinstance(self.value, String):            
            passvalue = False
            fmt = value + '\0'

        else:
            fmt = "%d \0"

        voidptr_ty = ir.IntType(8).as_pointer()

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
        if passvalue:
            self.builder.call(self.printf, [fmt_arg, value])
        else:
            self.builder.call(self.printf, [fmt_arg])


class Line():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        if type(self.value) == list:
            for value in self.value:
                value.eval()
        else:
            return self.value.eval()

            
class Statements():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        for val in self.value:
            val.eval()


variables = {}

class Var():
    def __init__(self, builder, module, lvalue):
        self.lvalue = lvalue
        self.builder = builder
        self.module = module
    
    def eval(self):
        return self.builder.load(variables.get(self.lvalue), name = self.lvalue)

class Assign():
    def __init__(self, builder, module, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.builder = builder
        self.module = module

        
    
    def eval(self):
        val = self.rvalue.eval()
        if variables.get(self.lvalue, -1) == -1:
            ptr = self.builder.alloca(ir.IntType(32), size = 1, name = self.lvalue)
            variables[self.lvalue] = ptr

        self.builder.store(val, variables.get(self.lvalue))
        return val