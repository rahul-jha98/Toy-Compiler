
from Lexer import Lexer
from ast import *
from Preprocessor import Preprocessor
from Codegen import CodeGen
import os



## write takes a series of , separated values and prints them
## writeln is basically write with \n at end
raw_text_input = '''
function product(i, j) {
    return i * j;
}

a = 2;
writeln(a);
b = 5;
writeln(b);

## if a == 2 {
##     writeln(5);
##     b = a;
##     writeln(4 * 8);
##     writeln(b);
## }
## else if a == 3 {
##     b = a + 1;
##     writeln(b);
## } else {
##     writeln("else");
## }

## writeln(2 == 3);
'''


raw_text_input = '''
repeat_for(i = 0; i < 5; i = i + 1) {
    repeat_for(j = i; j < 5; j  = j + 1)
        write(" * ");
    
    writeln(" ");
}
'''
preprocessor = Preprocessor(raw_text_input)
text_input, functions = preprocessor.get_processed_input()
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf


pg = Parser(module, builder, printf, functions)
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()
print(pg.module)
codegen.create_ir()
codegen.save_ir("output.ll")

os.system('llc -filetype=obj output.ll -relocation-model=pic')
os.system('gcc output.o -o output')

## After this simply call ./output to see output of the code