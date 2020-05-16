
## Temporary variable to give unique name to each print statement
print_count = 0

## Variables holidng global reference to string True and False
globalTrue = None
globalFalse = None
globalInt = None

## Functins are list of functions in the language
functions_ir = {}

## Definations contain the raw text of defination of language
function_definations = {}

## In order to bring local scoping in our language we maintaing a stack of scopes
## Whenever a new scope is needed we push in the stack or else pop
allvariables = {}
scopeStack = []
scopeStack.append(allvariables)

variables = scopeStack[0]

def initialize(builder, module, definations):
    global globalTrue, globalFalse, globalInt, function_definations

    function_definations = definations

    if globalTrue == None:
        fmt = "True" + '\0'
        voidptr_ty = ir.IntType(8).as_pointer()

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file with name True
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="True")

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
        globalTrue = fmt_arg


        fmt = "False" + '\0'
        voidptr_ty = ir.IntType(8).as_pointer()

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file with name False
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="False")

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
        globalFalse = fmt_arg


        fmt = "%d\0"
        
        voidptr_ty = ir.IntType(8).as_pointer()

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="int")

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        globalInt = builder.bitcast(global_fmt, voidptr_ty)


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

class NotEquals(RelOp):
    def truthvalue(self):
        return self.builder.icmp_signed('!=', self.left.eval(), self.right.eval())




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
        return self.builder.not_(self.express.eval())


## Statements take a list of statemnts and calls eval on each of them
class Statements():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        for val in self.value:
            val.eval()

## The Line command takes a single statement or list
class Line():
    def __init__(self, builder, module, value):
        self.value = value
        self.builder = builder
        self.module = module

    def eval(self):
        ## If it is list it calls eval on each of them
        if type(self.value) == list:
            for value in self.value:
                value.eval()
        else:
            ## Else return the eval of the single line  
            return self.value.eval()


class Var():
    def __init__(self, builder, module, lvalue):
        self.lvalue = lvalue
        self.builder = builder
        self.module = module
    
    def eval(self):
        try :
            return self.builder.load(variables.get(self.lvalue), name = self.lvalue)
        except Exception:
            raise Exception("The variable named {} was used but never defined".format(self.lvalue))


## Assignment can either create a new varaible with declaration or 
## update the value of declared varibale
class Assign():
    def __init__(self, builder, module, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.builder = builder
        self.module = module

        
    
    def eval(self):
        val = self.rvalue.eval()
        ## If variable is not in scope create new in given scope
        if variables.get(self.lvalue, -1) == -1:
            ptr = self.builder.alloca(ir.IntType(32), size = 1, name = self.lvalue)
            variables[self.lvalue] = ptr
        
        self.builder.store(val, variables.get(self.lvalue))
        return val


## If block only
class If():
    def __init__(self,builder, module, condition, then):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.then = Line(builder, module, [Scope(1), then, Scope(-1)])
    
    def eval(self):
        predicate = self.condition.eval()
        with self.builder.if_then(predicate) as (then):
            return self.then.eval()


## If with else
class IfElse():
    def __init__(self, builder, module, condition, then, otherwise):
        self.builder = builder
        self.module = module
        self.condition = condition
        self.then = Line(builder, module, [Scope(1), then, Scope(-1)])
        self.otherwise = Line(builder, module, [Scope(1), otherwise, Scope(-1)])

    def eval(self):
        predicate = self.condition.eval()
        with self.builder.if_else(predicate) as (then, otherwise):
            with then:
                self.then.eval()
            with otherwise:
                self.otherwise.eval()



## Scope takes a value 1 or -1 and pushes or pops a new scope in scope stack
class Scope():
    def __init__(self, toPush, copy = True):
        self.toPush = toPush
        self.copy = copy

    def eval(self):
        global variables, scopeStack
        if self.toPush == 1:
            newVariables = {}
            if self.copy:
                for key, value in variables.items():
                    newVariables[key] = variables[key]

            scopeStack.append(newVariables)
            variables = newVariables

        else:
            scopeStack = scopeStack[:-1]
            variables = scopeStack[-1]



## If the value is boolean we print the global String 
## True of False in the console
def print_true_or_false(builder, module, printf, predicate):
    with builder.if_else(predicate) as (then, otherwise):
        with then:
            builder.call(printf, [globalTrue])
        with otherwise:
            builder.call(printf, [globalFalse])




## Write calls the C native printf with the appropriate arguments to print it on the cammand line
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
        elif value.type == ir.IntType(32):
            self.builder.call(self.printf, [globalInt, value])
            return
        elif value.type == ir.FloatType(32):
            fmt = "%f \0"
        else:
            print_true_or_false(self.builder, self.module, self.printf, value)
            return

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



## Write calls the C native printf with the appropriate arguments to print it on the cammand line
class Input():
    def __init__(self, builder, module, scanf, var):
        self.builder = builder
        self.module = module
        self.scanf = scanf
        self.var = var

    def eval(self):
        address = variables.get(self.var, None)
        global print_count

        if address == None:
            raise Exception("Variable with name {} is not defined".format(self.var))

        
        print(address)
        self.builder.call(self.scanf, [globalInt, address])
        

'''
Uptil this point the AST methods were using predefined constructs.
From now we will have to handle the instruction blocks ourselves
'''
for_count = 0
class For():
    def __init__(self,builder, module, initialization, cond, after, block):
        global for_count
        self.builder = builder
        self.module = module
        self.initialization = initialization
        self.cond = cond
        self.after = after
        self.block = Line(builder, module, [Scope(1), block, Scope(-1)])
        self.for_count = for_count
        
        for_count = for_count + 1
    
    def eval(self):
        Scope(1).eval()

        self.initialization.eval()
        loop = self.builder.append_basic_block('loop{}'.format(self.for_count))
        self.builder.branch(loop)
        self.builder.position_at_start(loop)
        
        predicate = self.cond.eval()

        with self.builder.if_then(predicate) as then:
            self.block.eval()

            self.after.eval()

            predicate = self.cond.eval()

            loop_end = self.builder.block
            loop_end_bb = self.builder.append_basic_block('afterloop{}'.format(self.for_count))
            self.builder.cbranch(predicate, loop, loop_end_bb)
            self.builder.position_at_start(loop_end_bb)
        Scope(-1).eval()




class DefineFunction():
    def __init__(self, builder, module, printf, scanf, name, argslist):
        self.builder = builder
        self.module = module
        self.name = name
        self.argslist = argslist
        self.printf = printf
        self.scanf = scanf

    def eval(self):
        ## Creating the function type
        func_type = ir.FunctionType(ir.IntType(32), 
                                [ir.IntType(32)] * len(self.argslist))
        
        if self.name in  functions_ir.keys():
            raise Exception("Function with the name already exists")

        func = ir.Function(self.module, func_type, self.name)

        

        bb_entry = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(bb_entry)

        ## Create a new scope of the function
        Scope(1, False).eval()
        
        ## Populate the scope with default function args
        for i, arg in enumerate(func.args):
            arg.name = self.argslist[i]
            alloca = self.builder.alloca(ir.IntType(32), name=arg.name)
            self.builder.store(arg, alloca)
            variables[arg.name] = alloca

        functions_ir[self.name] = func
        # This part is tricky to fill the function definations ir 
        # in the function so that the instructions are actually filled
        # in the code segment of function and not of main 
        text_input = function_definations[self.name]
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(text_input)

        ## Since the parser fills the block of passed builder so we can't use our previous
        ## builder and thus we create a new parser with new builder
        pg = Parser(self.module, self.builder, self.printf, self.scanf, function_definations)
        pg.parse()
        parser = pg.get_parser()
        parser.parse(tokens).eval()
        
        ## Then we pop the scope stack and return exectution stack to previous state
        Scope(-1).eval()
        
        functions_ir[self.name] = func




class CallFunction():
    def __init__(self, builder, module, name, argslist):
        self.module = module
        self.builder = builder
        self.name = name
        self.argslist = argslist
        if type(self.argslist) != list:
            self.argslist = [argslist]
    
    def eval(self):
        ## First evaluate all the values in the parameters passed
        evaluatedlist = [x.eval() for x in self.argslist]
        return self.builder.call(functions_ir[self.name], evaluatedlist)



class ReturnValue():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value
    
    def eval(self):
        self.builder.ret(self.value.eval())
