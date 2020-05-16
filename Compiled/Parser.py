from rply import ParserGenerator
from llvmlite import ir
from Lexer import Lexer


'''
    This is the third phase of the compiler. In this case we are parsing the given grammar
    depending on the rules of the language. In case the rule is matched we take the appropriate 
    action.
'''
class Parser():
    def __init__(self, module, builder, printf, scanf, definations = {}):
        self.pg = ParserGenerator(
            # Tokens that can be accepted by our parser
            ['NUMBER', 'WRITE', 'WRITELN', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB','MUL','DIV','MOD', 'VAR', 'ASSIGN',
             'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
             'EQUALS', 'LESS', 'GREATER', 'LESS_EQ', 'GREAT_EQ', 'NOT_EQUALS',
             'COMMA', 'STRING', 'IF', 'ELSE', 'OPEN_CURLY', 'CLOSE_CURLY',
             'NOPS','FUNCTION', 'RETURN', 'FOR', 'INPUT', 'WHILE'
             ],
            
             
             ## Defining the precedence of operators in language
             precedence = [
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['MOD'])
            ]
        )

        ## Setting the module, builder and printf system call reference
        self.module = module
        self.builder = builder
        self.printf = printf
        self.scanf = scanf

        ## Initializing the defaults constructs for our language
        ## Like a global string called True, False etc.
        initialize(builder, module, definations)

        self.constants = {}
        self.constants['false'] = self.builder.bitcast(globalFalse, globalVoidPtr)
        self.constants['true'] = self.builder.bitcast(globalTrue, globalVoidPtr)
        self.constants['int'] = self.builder.bitcast(globalInt, globalVoidPtr)




    '''
        Method that does the actual parsing
    '''
    def parse(self):
        ## a program is a list of statements
        @self.pg.production('program : statements')
        def program(p):
            return Statements(self.builder, self.module, p)


        ## statements is either onestatemnt or statements followed by onestatemnt
        @self.pg.production('statements : onestatement')
        @self.pg.production('statements : statements onestatement')
        def statements(p):
            return Line(self.builder, self.module, p)

        
        ## onestatement represents every single line possible in our code
        ## onestatement consist of two type of constructs
        ##          for and if statement which don't end with semicolon
        ##          semicolon statement followed by SEMI_COLON token. ';'
        @self.pg.production('onestatement : forstatement')
        @self.pg.production('onestatement : ifelsestatement')
        @self.pg.production('onestatement : whilestatement')
        @self.pg.production('onestatement : semicolon SEMI_COLON')
        def onestatement(p):
            return Line(self.builder, self.module, p[0])


        ## These are the group of statemetns that actually require to end with semi colon
        ## Consist of 
        ##          list of all the statemnets constructs in our language
        @self.pg.production('semicolon : noopsstatement')
        @self.pg.production('semicolon : functiondefination')
        @self.pg.production('semicolon : returnstatement')
        @self.pg.production('semicolon : inputstatement')
        @self.pg.production('semicolon : functioncall')
        @self.pg.production('semicolon : writestatement')
        @self.pg.production('semicolon : writelnstatement')
        @self.pg.production('semicolon : assignmentstatement')
        def semicolonstatement(p):
            return p[0]





        '''
        ------- All Statements in the language -----------
        '''

        ## There is a keyword called 'nothing' in our language
        ## The need for this is that sometimes make a if condition 
        ## but don't know what to do as of now. Leaving a block empty throws error.
        ## So, you can write 'nothing;' which is a valid construct and also 
        ## as the name suggests does nothing :)
        @self.pg.production('noopsstatement : NOPS')
        def noopsstatement(p):
            ## Passing empty list thus adding no construct to the code
            return Line(self.builder, self.module, [])
            


        ## Function defination is supposed to be a prototype. 
        ##          it is supposed to be like 
        ##          function name(args*)
        @self.pg.production('functiondefination : FUNCTION VAR OPEN_PAREN argslist CLOSE_PAREN')
        @self.pg.production('functiondefination : FUNCTION VAR OPEN_PAREN CLOSE_PAREN')
        def functiondefination(p):
            if len(p) == 4:
                ## If len is 4 that means we have no arguments in the function
                ## p[1].value is the name of the function
                return DefineFunction(self.builder, self.module, self.printf, self.scanf, p[1].value, [])
            else:
                ## p[3] is supposed to give argslist in the next case
                return DefineFunction(self.builder, self.module, self.printf, self.scanf, p[1].value, p[3])


        
        ## arglist is collection of variable names separated by ,
        ## like a, b, c
        @self.pg.production('argslist : VAR')
        @self.pg.production('argslist : argslist COMMA VAR')
        def argslist(p):
            if len(p) == 1:
                return p[0].value
            
            else:
                ## Flattening the args list
                ## It is used because in case of multpile args the array can be recursive
                ## So, it picks every element to same depth
                values = p[:-1:2]
                if type(values[0]) == list:
                    values[0].append(p[-1].value)
                    return values[0]
                else:
                    values.append(p[-1].value)
                    return values

        
        ## The return statement can be used to return an evaluated expression
        @self.pg.production('returnstatement : RETURN expression')
        def returnstatement(p):
            return ReturnValue(self.builder, self.module, p[1])


        ## assignment statements can be used to assign a value to a variable
        ## Also, not that our language can detect if the variable is declared on not
        ## and declare it for you automatically :)
        @self.pg.production('assignmentstatement : VAR ASSIGN expression')
        @self.pg.production('assignmentstatement : VAR ASSIGN functioncall')
        def assignmentstatement(p):
            return Assign(self.builder, self.module, p[0].value, p[2])





        ## write takes a list of printable statements and prints it one by one
        ## Eg : write(2, 2 == 2, "Rahul")
        ## should print 2 True Rahul in console
        @self.pg.production('writestatement : WRITE OPEN_PAREN printstatement CLOSE_PAREN')
        def writestatement(p):
            return Line(self.builder, self.module, p[2])

        ## writeln is same as write but adds a newline after all values have been printed
        @self.pg.production('writelnstatement : WRITELN OPEN_PAREN printstatement CLOSE_PAREN')
        def writelnstatement(p):
            withnewline = p[2].value
            ## Append a Write commant to print \n at the end of previous list
            withnewline.append(Write(self.builder, self.module, self.printf, String("\n", trim = False), self.constants))
            return Line(self.builder, self.module, withnewline)


        @self.pg.production('inputstatement : INPUT OPEN_PAREN VAR CLOSE_PAREN')
        def inputstatement(p):
            return Input(self.builder, self.module, self.scanf, p[2].value, self.constants)

        ## printstatement is a list of printable statements comma separated
        @self.pg.production('printstatement : oneprintstatement')
        @self.pg.production('printstatement : printstatement COMMA oneprintstatement')
        def printstatement(p):
            return Line(self.builder, self.module, p[::2])


        ## oneprintstatemnet can be any expression or a STRING kind
        @self.pg.production('oneprintstatement : allexpression')
        @self.pg.production('oneprintstatement : STRING')
        def oneprintstatement(p):
            try:
                isString = p[0].gettokentype()
                return Write(self.builder, self.module, self.printf, String(p[0].value), self.constants)
            except AttributeError:
                return Write(self.builder, self.module, self.printf, p[0], self.constants)
            return Write(self.builder, self.module, self.printf, p[0], self.constants)



        ## Function call is when you call a function but don't store the return value
        ## it takes an optional comma separated expression list
        @self.pg.production('functioncall : VAR OPEN_PAREN CLOSE_PAREN')
        @self.pg.production('functioncall : VAR OPEN_PAREN expresslist CLOSE_PAREN')
        def functincall(p):
            if len(p) == 3:
                return CallFunction(self.builder, self.module, p[0].value, [])
            else:
                return CallFunction(self.builder, self.module, p[0].value, p[2])     


        ## Return list of expressions
        @self.pg.production('expresslist : expression')
        @self.pg.production('expresslist : expresslist COMMA expression')
        def expresslist(p):
            if len(p) == 1:
                return p[0]
            
            else:
                values = p[:-1:2]
                if type(values[0]) == list:
                    values[0].append(p[-1])
                    return values[0]
                else:
                    values.append(p[-1])
                    return values   

    

        ## If statement can be a if followed by logical expression then optional else 
        ## each if and else takes a block as next parameter which is the set of statemnets
        @self.pg.production('ifelsestatement : IF log_expression block ELSE block')
        @self.pg.production('ifelsestatement : IF log_expression block')
        def ifelsestatement(p):
            if len(p) == 3:
                return If(self.builder, self.module, p[1], p[2])
            else:
                return IfElse(self.builder, self.module, p[1], p[2], p[4])


        ## For has the syntax like 
        ## for (assignment; logical_expression; assignment2) block
        @self.pg.production('forstatement : FOR OPEN_PAREN assignmentstatement SEMI_COLON log_expression SEMI_COLON assignmentstatement CLOSE_PAREN block')
        def forstatement(p):
            return For(self.builder, self.module, p[2], p[4], p[6], p[8])

        ## While has the syntax like 
        ## while(logical_expression) block
        @self.pg.production('whilestatement : WHILE OPEN_PAREN log_expression CLOSE_PAREN block')
        def whilestatement(p):
            return While(self.builder,self.module,p[2],p[4])

        ## A block is a single statement
        ## In case you need multiple statements you need to enclose it in curly braces
        @self.pg.production('block : onestatement')
        @self.pg.production('block : OPEN_CURLY statements CLOSE_CURLY')
        def block(p):
            if len(p) == 1:
                return Line(self.builder, self.module, p[0])
            else:
                return Line(self.builder, self.module, p[1])





        '''
        ------- All Expressions in the language -----------
        '''

        ## allexpression consist of expression or logical expression
        @self.pg.production('allexpression : expression')
        @self.pg.production('allexpression : log_expression')
        def allexpression(p):
            return Line(self.builder, self.module, p[0])

        

        ## Logical Expressions
        ## logical expressions when operated with and, or, not also give logical expression
        @self.pg.production('log_expression : log_expression OR log_expression')
        @self.pg.production('log_expression : log_expression AND log_expression')
        @self.pg.production('log_expression : NOT log_expression')
        def log_expression(p):

            if len(p) == 3:
                # And Or case
                left = p[0]
                right = p[2]
                operator = p[1]

                if operator.gettokentype() == 'OR':
                    return Or(self.builder, self.module, left, right)
                else:
                    return And(self.builder, self.module, left, right)
            else:
                return Not(self.builder, self.module, p[1])


        
        ## The keyword True, False are logical expression itself
        ## Also, we can enclose a logical expression in () and it is still logical expression
        @self.pg.production('log_expression : TRUE')
        @self.pg.production('log_expression : FALSE')
        @self.pg.production('log_expression : OPEN_PAREN log_expression CLOSE_PAREN')
        def log_expression_value(p):
            if p[0].gettokentype() == 'TRUE':
                return Bool(self.builder, self.module, True)
            elif p[0].gettokentype() == "FALSE":
                return Bool(self.builder, self.module, False)
            else:
                return Line(self.builder, self.module, p[1])


        ## This is the tricky part
        ## Since relational operators give either true or false 
        ## We have wrapped it within logical expression
        @self.pg.production('log_expression : rel_expression')
        def log_expression_relation(p):
            return Line(self.builder, self.module, p[0])


        

        ## Relational expressions
        @self.pg.production('rel_expression : expression EQUALS expression')
        @self.pg.production('rel_expression : expression LESS expression')
        @self.pg.production('rel_expression : expression GREATER expression')
        @self.pg.production('rel_expression : expression LESS_EQ expression')
        @self.pg.production('rel_expression : expression GREAT_EQ expression')
        @self.pg.production('rel_expression : expression NOT_EQUALS expression')
        def arithmatic_relations(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'EQUALS':
                return Equals(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LESS':
                return Less(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'GREATER':
                return Greater(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LESS_EQ':
                return LessEq(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'GREAT_EQ':
                return GreatEq(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'NOT_EQUALS':
                return NotEquals(self.builder, self.module, left, right)


        ## Arithmatic Expressions
        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression MOD expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MOD':
                return Mod(self.builder, self.module, left, right)


        ## A function call is also a valid expression
        @self.pg.production('expression : functioncall')
        def callexpression(p):            
            return p[0]        


        ## A number, variable or (expression) are also expression
        @self.pg.production('expression : NUMBER')
        @self.pg.production('expression : VAR')
        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def stopexpression(p):
            if p[0].gettokentype() == 'NUMBER':
                return Number(self.builder, self.module, p[0].value)

            elif p[0].gettokentype() == 'VAR':
                return Var(self.builder, self.module, p[0].value)
            
            elif p[0].gettokentype() == 'OPEN_PAREN':
                return Line(self.builder, self.module, p[1])

        
        

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()



## Temporary variable to give unique name to each print statement
print_count = 0

## Variables holidng global reference to string True and False
globalTrue = None
globalFalse = None
globalInt = None
globalVoidPtr = None

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
    global globalTrue, globalFalse, globalInt, globalVoidPtr, function_definations

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
        globalTrue = global_fmt


        fmt = "False" + '\0'
        voidptr_ty = ir.IntType(8).as_pointer()

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file with name False
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="False")

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        globalFalse = global_fmt


        fmt = "%d \0"
        
        voidptr_ty = ir.IntType(8).as_pointer()

        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))

        ## Setting global variable for the file
        global_fmt = ir.GlobalVariable(module, c_fmt.type, name="int")

        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        globalInt = global_fmt

        globalVoidPtr = voidptr_ty
    



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
def print_true_or_false(builder, module, printf, predicate, constants):
    with builder.if_else(predicate) as (then, otherwise):
        with then:
            builder.call(printf, [constants['true']])
        with otherwise:
            builder.call(printf, [constants['false']])




## Write calls the C native printf with the appropriate arguments to print it on the cammand line
class Write():
    def __init__(self, builder, module, printf, value, constants = {}):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value
        self.constants = constants

    def eval(self):
        global print_count

        
        passvalue = True
        value = self.value.eval()
        if isinstance(self.value, String):            
            passvalue = False
            fmt = value + '\0'
        elif value.type == ir.IntType(32):
            self.builder.call(self.printf, [self.constants['int'], value])
            return
        else:
            print_true_or_false(self.builder, self.module, self.printf, value, self.constants)
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
    def __init__(self, builder, module, scanf, var, constants):
        self.builder = builder
        self.module = module
        self.scanf = scanf
        self.var = var
        self.constants = constants

    def eval(self):
        address = variables.get(self.var, None)
        global print_count

        if address == None:
            raise Exception("Variable with name {} is not defined".format(self.var))

        
        print(address)
        self.builder.call(self.scanf, [self.constants['int'], address])
        

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


## While loop is almost same as for loop
class While():
    def __init__(self,builder,module,cond,block):
        global for_count
        self.builder = builder
        self.module = module
        self.cond = cond
        self.block = Line(builder,module,[Scope(1), block, Scope(-1)])
        self.while_count = for_count
        for_count += 1

    def eval(self):
        
        loop = self.builder.append_basic_block(f'while_loop{self.while_count}')

        self.builder.branch(loop)
        self.builder.position_at_start(loop)

        predicate = self.cond.eval()

        with self.builder.if_then(predicate) as then:
            Scope(1).eval()
            self.block.eval()

            predicate = self.cond.eval()

            loop_end = self.builder.block
            loop_end_bb = self.builder.append_basic_block(f'afterloop{self.while_count}')
            self.builder.cbranch(predicate,loop,loop_end_bb)
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
