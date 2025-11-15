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
        ## eat (Accept as Valid) the current token and assign the next token to the self.current_token,
        ## otherwise raise an exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        """factor : INTEGER | (expr)"""
        token = self.current_token
        if token.type == INTEGER:
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
    # This class is to traverse or visit nodes in AST
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
        left_val = int(self.visit(node.left))
        right_val = int(self.visit(node.right))
        if node.op.type == PLUS:
            return left_val + right_val
        elif node.op.type == MINUS:
            return left_val - right_val
        elif node.op.type == MUL:
            return left_val * right_val
        elif node.op.type == DIV:
            return left_val / right_val
        
    def visit_Num(self, node):
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
                text = input('spi> ')
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










