from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('WRITELN', r'writeln')
        self.lexer.add('WRITE', r'write')     
        self.lexer.add('TRUE', r'True')
        self.lexer.add('FALSE', r'False')
        self.lexer.add('FUNCTION', r'function')

        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('NOPS', r'nothing')

        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_CURLY', r'\{')
        self.lexer.add('CLOSE_CURLY', r'\}')

        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')


        # Arithmatic Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('MOD', r'\%')


        ## Logical Operators
        self.lexer.add('AND', r'and')
        self.lexer.add('OR', r'or')
        self.lexer.add('NOT', r'not')

        ## Relational Operators
        self.lexer.add('EQUALS', r'==')
        self.lexer.add('LESS', r'<')
        self.lexer.add('GREATER', r'>')
        self.lexer.add('LESS_EQ', r'<=')
        self.lexer.add('GREAT_EQ', r'>=')

        # Number
        #self.lexer.add('INT', r'^[-+]?\d+$')
        self.lexer.add('NUMBER',r'[-+]?[0-9]*\.?[0-9]+')
        self.lexer.add('STRING', r'\"(\\.|[^\"])*\"')

        # Variable
        self.lexer.add('VAR', r'[A-Za-z_][A-Za-z0-9_]*')


        #Assign
        self.lexer.add('ASSIGN', r'\=')
        self.lexer.add('COMMA', r',')


        # Ignore spaces
        self.lexer.ignore('\s+')
        #self.lexer.ignore('\n+')
        #self.lexer.ignore('\\*.*?\\*/')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()