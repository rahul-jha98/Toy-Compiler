from rply import ParserGenerator
from ast import *

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'WRITE', 'WRITELN', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB','MUL','DIV','MOD', 'VAR', 'ASSIGN',
             'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
             'EQUALS', 'LESS', 'GREATER', 'LESS_EQ', 'GREAT_EQ',
             'COMMA', 'STRING', 'IF', 'ELSE', 'OPEN_CURLY', 'CLOSE_CURLY',
             'NOPS'
             ],
            
             
             precedence = [
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['MOD'])
            ]
        )
        self.module = module
        self.builder = builder
        self.printf = printf

        initialize(builder, module)

    def parse(self):
        @self.pg.production('program : statements')
        def program(p):
            return Statements(self.builder, self.module, p)

        @self.pg.production('statements : onestatement')
        @self.pg.production('statements : statements onestatement')
        def statements(p):
            return Line(self.builder, self.module, p)

        
        @self.pg.production('onestatement : noopsstatement')
        @self.pg.production('onestatement : writestatement')
        @self.pg.production('onestatement : writelnstatement')
        @self.pg.production('onestatement : ifelsestatement')
        @self.pg.production('onestatement : assignmentstatement')
        def onestatement(p):
            return Line(self.builder, self.module, p[0])




        '''
        ------- All Statements in the language -----------
        '''
        @self.pg.production('noopsstatement : NOPS SEMI_COLON')
        def noopsstatement(p):
            return Line([])
            

        @self.pg.production('assignmentstatement : VAR ASSIGN expression SEMI_COLON')
        def assignmentstatement(p):
            return Assign(self.builder, self.module, p[0].value, p[2])
        

        
        @self.pg.production('writestatement : WRITE OPEN_PAREN printstatement CLOSE_PAREN SEMI_COLON')
        def writestatement(p):
            return Line(self.builder, self.module, p[2])

        @self.pg.production('writelnstatement : WRITELN OPEN_PAREN printstatement CLOSE_PAREN SEMI_COLON')
        def writelnstatement(p):
            withnewline = p[2].value
            withnewline.append(Write(self.builder, self.module, self.printf, String("\n", trim = False)))
            return Line(self.builder, self.module, withnewline)

        @self.pg.production('printstatement : oneprintstatement')
        @self.pg.production('printstatement : printstatement COMMA oneprintstatement')
        def printstatement(p):
            return Line(self.builder, self.module, p[::2])

        @self.pg.production('oneprintstatement : allexpression')
        @self.pg.production('oneprintstatement : STRING')
        def oneprintstatement(p):
            try:
                isString = p[0].gettokentype()
                return Write(self.builder, self.module, self.printf, String(p[0].value))
            except AttributeError:
                return Write(self.builder, self.module, self.printf, p[0])
            return Write(self.builder, self.module, self.printf, p[0])


        @self.pg.production('ifelsestatement : IF log_expression block ELSE block')
        @self.pg.production('ifelsestatement : IF log_expression block')
        def ifelsestatement(p):
            if len(p) == 3:
                return If(self.builder, self.module, p[1], p[2])
            else:
                return IfElse(self.builder, self.module, p[1], p[2], p[4])

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
        @self.pg.production('allexpression : expression')
        @self.pg.production('allexpression : log_expression')
        def allexpression(p):
            return Line(self.builder, self.module, p[0])

        

        ## Logical Expressions
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


        @self.pg.production('log_expression : rel_expression')
        def log_expression_relation(p):
            return Line(self.builder, self.module, p[0])


        

        ## Relational expressions
        @self.pg.production('rel_expression : expression EQUALS expression')
        @self.pg.production('rel_expression : expression LESS expression')
        @self.pg.production('rel_expression : expression GREATER expression')
        @self.pg.production('rel_expression : expression LESS_EQ expression')
        @self.pg.production('rel_expression : expression GREAT_EQ expression')
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
