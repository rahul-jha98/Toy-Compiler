from rply import ParserGenerator
from ast import *

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB']
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):
        @self.pg.production('program : statements')
        def program(p):
            return Statements(self.builder, self.module, p)

        @self.pg.production('statements : printstatement')
        @self.pg.production('statements : assignmentstatement')
        @self.pg.production('statements : statements printstatement')
        @self.pg.production('statements : statements assignmentstatement')
        def statements(p):
            return Line(self.builder, self.module, p)

        @self.pg.production('assignmentstatement : VAR ASSIGN expression SEMI_COLON')
        def assignmentstatement(p):
            return Assign(p[0].value, p[2])
        
        
        @self.pg.production('printstatement : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def printstatement(p):
            return Print(self.builder, self.module, self.printf, p[2])


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
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
            elif operator.gettokentype() == 'MOD':
                return Mod(left, right)
            

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)
        
        @self.pg.production('expression : VAR')
        def number(p):
            return Var(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
