class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        try:
            return int(self.value)
        except ValueError:
            return float(self.value)


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



class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())


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

        if variables.get(lvalue, -1) == -1:
            variables[lvalue] = self.rvalue.eval()
        
    
    def eval(self):
        return variables.get(self.lvalue)