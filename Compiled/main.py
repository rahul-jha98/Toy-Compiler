
from Lexer import Lexer
from Parser import Parser
from Codegen import CodeGen
import os



## write takes a series of , separated values and prints them
## writeln is basically write with \n at end
text_input = '''
writeln("Rahul ", "is my name ", 2 == 3);
a = 5;
b = 8 % a;
writeln(b);
writeln(a + b);
'''

## The last output is not correct
## Will change the logic of execution later so that
## Precedence is left associative

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()

codegen.create_ir()
codegen.save_ir("output.ll")

os.system('llc -filetype=obj output.ll -relocation-model=pic')
os.system('gcc output.o -o output')

## After this simply call ./output to see output of the code