from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('MOD', r'\%')
        # Number
        #self.lexer.add('INT', r'^[-+]?\d+$')
        self.lexer.add('NUMBER',r'[-+]?[0-9]*\.?[0-9]+')
        # Variable
        self.lexer.add('VAR', r'[A-Za-z_][A-Za-z0-9_]*')
        #Assign
        self.lexer.add('ASSIGN', r'\=')
        # Ignore spaces
        self.lexer.ignore('\s+')
        #self.lexer.ignore('\n+')
        #self.lexer.ignore('\\*.*?\\*/')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()