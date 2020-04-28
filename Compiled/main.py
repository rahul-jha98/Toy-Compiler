from Preprocessor import Preprocessor
from Lexer import Lexer
from Parser import Parser
from Codegen import CodeGen

import os


sample_codes = []

## Code 0 : Factorial
## This is a code showing the use of functions in our language
sample_codes.append('''
## This is a function called factorial that takes a value and returns 
## its factorial. This meanwhile is a comment

function factorial(n) {
    product = 1;
    
    ## Running a loop from 1 to n
    repeat_for (i = 1; i <= n; i = i + 1) {
        product = product * i;
    }
    
    ## Returning the product
    return product;
}

writeln("The factorial of ", 4, " is ", factorial(4));

a = 6;
b = factorial(a);
writeln("The factorial of ", a, " is ", b);
''')


## Code : 1 Nested for
## Program showing if else and for in our language
sample_codes.append('''
a = 8;
repeat_for(i = 0; i < a; i = i + 1) {

    repeat_for(j = i; j < a; j  = j + 1) 
        if i % 2 == 0
            write(" @ ");
        else if i % 2 == 1
            write(" * ");
        else {
            writeln("This is show multiple if else stack");
            writeln("This block shouldn't be reachable in code");
        }
    
    writeln(" ");
}
''')


## Code : 2 Static scoping
## The best part is that while making the language we have kept utmost care of 
## scoping and thus function has its own scope
sample_codes.append('''
function updatevalue(a, b) {
    ## We update the value of a and b in function

    a = a * 2;
    b = b / 2;

    ## We also display the values in function
    writeln("The values of a and b in functions is ", a, b);

    return 0;
}

a = 5;
b = 5;

## We call update value passing a and b to it
updatevalue(a, b);

## Although a and b is updated in function it is not in the current scope
writeln("The values of a and b outside function is ", a, b);
''')


## Code 3 : The magic of recursion
## Our language also supports basic recursions
sample_codes.append('''
function fib(a) {
    ## We update the value of a and b in function

    if a == 1 return 1;
    else if a == 2 return 1;
    else {
        return fib(a-1) + fib(a-2);
    }

    return 0;
}

repeat_for(i = 1; i <= 10; i = i + 1)
    writeln("Fibonacci ", i, "is ", fib(i));
''')


sample_codes.append('''
a = 0;
writeln("Enter a number whose table you need");
input(a);
repeat_for(i = 1; i < 11; i = i + 1) {
    writeln(a, " * ", i, " = ", a * i);
}
''')
## Set code no to 0 1 or 2 depending of
code_no = 4

## Firstly we initialize the preprocessor with the input we want to use
preprocessor = Preprocessor(sample_codes[code_no])

## The nwe get the updated text and functions definations
text_input, functions = preprocessor.get_processed_input()
## We get the tokens by initializing the lexer
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

## We initialize the codegenerator the get the ir builder and printf
codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf
scanf = codegen.scanf

## Create the parser with given reference
pg = Parser(module, builder, printf, scanf, functions)
pg.parse()
parser = pg.get_parser()

## Then we parse the text and eval each of it
parser.parse(tokens).eval()

## Uncommenting the below line will print the code generateed
print(pg.module)


## Writing intermediate code to ll file
codegen.create_ir()
codegen.save_ir("output.ll")

## Compiling the ll file using gcc to finally generate the machine code
os.system('llc -filetype=obj output.ll -relocation-model=pic')
os.system('gcc output.o -o output')


## At the end of it in the given directory run ./output to execte code generated