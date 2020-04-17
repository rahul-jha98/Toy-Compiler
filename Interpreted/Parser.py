from rply import ParserGenerator
from ast import *


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB','MUL','DIV','MOD', 'VAR', 'ASSIGN'],
            
            precedence = [
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['MOD'])
            ]

        )

    def parse(self):


        @self.pg.production('program : statements')
        def program(p):
            return Statements(p)


        @self.pg.production('statements : printstatement')
        @self.pg.production('statements : assignmentstatement')
        @self.pg.production('statements : statements printstatement')
        @self.pg.production('statements : statements assignmentstatement')
        def statements(p):
            return Line(p)

        
        @self.pg.production('assignmentstatement : VAR ASSIGN expression SEMI_COLON')
        def assignmentstatement(p):
            return Assign(p[0].value, p[2])


        @self.pg.production('printstatement : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def printstatement(p):
            return Print(p[2])


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
                return Sum(left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(left, right)
            elif operator.gettokentype() == 'MUL':
                return Mul(left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(left, right)
            elif operator.gettokentype() == 'MOD':
                return Mod(left, right)

        @self.pg.production('expression : NUMBER')
        @self.pg.production('expression : VAR')
        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def stopexpression(p):
            if p[0].gettokentype() == 'NUMBER':
                return Number(p[0].value)

            elif p[0].gettokentype() == 'VAR':
                return Var(p[0].value)
            
            elif p[0].gettokentype() == 'OPEN_PAREN':
                return Line(p[1])

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()