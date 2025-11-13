class AST(object) :
    pass

class BinOp(AST):
    # constructor
    def __init__(self, left, op, right) :
        self.left = left
        self.right = right
        self.token = self.op = op