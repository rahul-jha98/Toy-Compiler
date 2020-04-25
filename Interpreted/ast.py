class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        try:
            return int(self.value)
        except ValueError:
            return float(self.value)

class Bool():
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        return self.value

class String():
    def __init__(self, value, trim = True):
        if trim: 
            self.value = value[1:-1]
        else:
            self.value = value
    
    def eval(self):
        return self.value





class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

class Mod(BinaryOp):
    def eval(self):
        return self.left.eval() % self.right.eval()




class RelOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def truthvalue(self):
        return True 


    def eval(self):
        return self.truthvalue()


class Equals(RelOp):
    def truthvalue(self):
        return self.left.eval() == self.right.eval()


class Greater(RelOp):
    def truthvalue(self):
        return self.left.eval() > self.right.eval()

class Less(RelOp):
    def truthvalue(self):
        return self.left.eval() < self.right.eval()

class LessEq(RelOp):
    def truthvalue(self):
        return self.left.eval() <= self.right.eval()

class GreatEq(RelOp):
    def truthvalue(self):
        return self.left.eval() >= self.right.eval()


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() and self.right.eval()

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() or self.right.eval()

class Not:
    def __init__(self, express):
        self.express = express
    
    def eval(self):
        return self.express.eval()





class Write():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval(), end = '')


class Line():
    def __init__(self, value):
        self.value = value
        

    def eval(self):
        if type(self.value) == list:
            for value in self.value:
                value.eval()
        else:
            return self.value.eval()

class Statements():
    def __init__(self, value):
        self.value = value
        

    def eval(self):
        for val in self.value:
            val.eval()

variables = {}

class Var():
    def __init__(self, lvalue):
        self.lvalue = lvalue

    
    def eval(self):
        return variables.get(self.lvalue)

class Assign():
    def __init__(self, lvalue, rvalue = Number(0)):
        self.lvalue = lvalue
        self.rvalue = rvalue

    
    def eval(self):
        if variables.get(self.lvalue, -1) == -1:
            variables[self.lvalue] = self.rvalue.eval()
        else:
            variables[self.lvalue] = self.rvalue.eval()
        return variables.get(self.lvalue)


class IfElse():
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def eval(self):
        if self.condition.eval():
            self.then.eval()
        else:
            self.otherwise.eval()

class If():
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    
    def eval(self):
        if self.condition.eval():
            return self.then.eval()
