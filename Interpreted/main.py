from Lexer import Lexer
from Parser import Parser

text_input = """
print(4 - 4 + 2);
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

text_input = """
a = 4 - (5 + 1);
print(a);
b = a * 2;
c = b;
print(3 + c);
print(a == b);
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
