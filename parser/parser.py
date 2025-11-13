class AST:
    pass

class BinOp(AST):
    # constructor
    def __init__(self, left, op, right) :
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self,token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        ##compare current token type with 
        ## the passed token type if they match :
        ## eat (Accept as Valid) the current token and assign the next token to the self.current_token,
        ## otherwise raise an exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
