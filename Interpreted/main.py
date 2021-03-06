from Preprocessor import Preprocessor
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

raw_input_text = """
a = 2;
function apple(a, b, c) {
    a = 2;
}
if a == 2 {
    nothing; ## This to show that we are doing nothing here
}
## This is also a raw input file
else if a == 3 {
    writeln(5 == 4, "Rahul", 3);
} 
writeln("hello ", 5);
"""

preprocessor = Preprocessor(raw_input_text)
text_input = preprocessor.get_processed_input()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

# for token in tokens:
#     print(token)

pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
