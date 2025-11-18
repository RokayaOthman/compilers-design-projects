import sys
import os
# Add the parent directory to Python path so it can find the scanner module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.lex_scanner import Lexer
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class AST:
    pass

class BinOp:
    # constructor
    def __init__(self, left, op, right) :
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return str(self.token)

class UnaryOp():
    def __init__(self, op, expr):
        self.token = self.op = op 
        self.expr = expr # represents an AST node


class Num:
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
        ## (Accept as Valid) the current token and assign the next token to the self.current_token,
        ## otherwise raise an exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            
        else:
            self.error()
    
    def factor(self):
        """OLD : factor : INTEGER | (expr)"""
        """ UPDATED : factor : (plus | minus) factor | integer | (expr)"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN: # ( 
            self.eat(LPAREN)
            node = self.expr() # expr
            self.eat(RPAREN) # )
            return node
        
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        # factor * factor | factor / factor
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())
            #Example : node = BinOp(left=Num(3), op=*, right=Num(4))
            # this represents (3 * 4)

        return node
    

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node
    
    def parse(self):
        return self.expr()


class NodeVisitor:
    # This class is to traverse or visit nodes in AST using the visitor design pattern  
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser 
   
    def visit_BinOp(self, node):
        # Post-order: Visit children → process node
        print(f"Visiting BinOp with op: {node.op.type}")
        left_val = (self.visit(node.left))
        print(f"left value: {left_val} ")
        right_val = (self.visit(node.right))
        print(f"right value: {right_val}")
        # if node.op.type == PLUS:
        #     return left_val + right_val
        # elif node.op.type == MINUS:
        #     return left_val - right_val
        # elif node.op.type == MUL:
        #     return left_val * right_val
        # elif node.op.type == DIV:
        #     return left_val / right_val
        operations = {
                PLUS: lambda x , y : x + y,
                MINUS: lambda x , y : x - y ,
                MUL : lambda x , y : x * y,
                DIV : lambda x , y : x / y
        }
        result = operations[node.op.type](left_val, right_val)
        print(f"BinOp result: {result}")
        return result
    
    def visit_UnaryOp(self, node):
        print(f"Visiting UnaryOp with op: {node.op.type}")
        op = node.op.type
        if op == PLUS :
            result =  +1 * self.visit(node.expr)
        elif op == MINUS:
            result =  -1 * self.visit(node.expr)
        print(f"UnaryOp result: {result}")
        return result
                
    
    def visit_Num(self, node):
        print(f"Visiting Num: {node.value}")
        result = int(node.value)
        print(f"Num result: {result}")
        return result
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():

    while True:
        try:
                text = input('input> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()










