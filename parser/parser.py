import sys
import os
# Add the parent directory to Python path so it can find the scanner module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tokens import TokenType as T
from scanner.lex_scanner import Lexer
class AST:
    pass

    
# program : function 
class Program:
    def __init__(self, function):
        self.function = function


# function : "int" IDENTIFIER "("  ")"  "{" statement "}" 
class Function:
    def __init__(self, name, body):
        self.name = name
        self.body = body 

# a Block is a node that holds multiple statements
class Block:
    def __init__(self, statements):
        self.statements = statements

class Var:
    def __init__(self, token):
        self.token = token
        self.name = token.value

class Assign:
    def __init__(self, left, right):
        self.left = left # var node
        self.right = right # expr  , Num(5)

class Return:
    def __init__(self, expr):
        self.expr = expr
    

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
    
    def parse_program(self):
        func = self.parse_function()
        return Program(func)

    # every self.eat( ) call is a checkpoint , if the current token doesnt match what is expected
    # the parser should fail immediately with a clear error

    def parse_function(self):
        # expect: "int" IDENTIFIER "(" ")" "{" statement "}"
        self.eat(T.INT)
        token = self.current_token
        self.eat(T.IDENTIFIER)
        func_name = token.value

        self.eat(T.LPAREN)
        self.eat(T.RPAREN)

        self.eat(T.LBRACE)
        
        body = self.parse_block()
        self.eat(T.RBRACE)
        return Function(func_name, body)


    def parse_block(self):
        statements = []
        # this loops until it hits } , collecting all statements
        while self.current_token.type != T.RBRACE:
            # parse one statement and add it to the list
            statements.append(self.parse_statement())
        return Block(statements)


    def parse_statement(self):
        if self.current_token.type == T.RETURN:
            self.eat(T.RETURN)
            expr_node = self.expr()
            self.eat(T.SEMI)
            return Return(expr_node)
        else:
            self.error("Expected 'return' statement")




    def error(self, message=None):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        ##compare current token type with 
        ## the passed token type if they match :
        ## (Accept as Valid) the current token and assign the next token to the self.current_token,
        ## otherwise raise an exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            
        else:
            self.error("there is a syntax error")
            sys.exit(1)
    
    # smallest meaningful building block of an expression , you cant break down any further
    def atom (self) :
        token = self.current_token
        if token.type == T.INTEGER:
            self.eat(T.INTEGER)
            return Num(token)
        elif token.type == T.IDENTIFIER:
            self.eat(T.IDENTIFIER)
            return Var(token)
        elif token.type == T.LPAREN: # ( 
            self.eat(T.LPAREN)
            node = self.expr() # expr
            self.eat(T.RPAREN) # )
            return node


    def power(self):
        node = self.atom()
        token = self.current_token
        if token.type == T.POWER:
            self.eat(T.POWER) # ← Consume the ** operator
            node = BinOp(left=node, op=token, right=self.power())
        return node
    
    def factor(self):
        """OLD : factor : INTEGER | (expr)"""
        """ UPDATED : factor : (PLUS | MINUS) factor | power """
        
        token = self.current_token
        if token.type == T.PLUS:
            self.eat(T.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == T.MINUS:
            self.eat(T.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        else:
            return self.power()
        
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        # factor * factor | factor / factor
        node = self.factor()

        while self.current_token.type in (T.MUL, T.DIV, T.MOD):
            token = self.current_token
            if token.type == T.MUL:
                self.eat(T.MUL)
            elif token.type == T.DIV:
                self.eat(T.DIV)
            elif token.type == T.MOD:
                self.eat(T.MOD)

            node = BinOp(left=node, op=token, right=self.factor())
            #Example : node = BinOp(left=Num(3), op=*, right=Num(4))
            # this represents (3 * 4)

        return node
    

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV | MOD) factor) | power*
        factor : INTEGER | LPAREN expr RPAREN

        power  : handles factor ** factor 
        atom   : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (T.PLUS, T.MINUS):
            token = self.current_token
            if token.type == T.PLUS:
                self.eat(T.PLUS)
            elif token.type == T.MINUS:
                self.eat(T.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node
    
    def parse(self):
        return self.parse_program()


class NodeVisitor:
    # This class is to traverse or visit nodes in AST using the visitor design pattern  
    def visit(self, node):
        # 1. Construct the method name dynamically , (e.g., 'BinOp', 'Num'),
        #    method name becomes a string like 'visit_BinOp', 'visit_Num'
        method_name = 'visit_' + type(node).__name__

        # 2. Return the method object corresbonding to the specific node type
        # if such a method doesn't exist, it returns the default fallback method
        visitor = getattr(self, method_name, self.generic_visit)
        
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser 
   
    def visit_Program(self, node):
        return self.visit(node.function)
    
    def visit_Function(self, node):
        return self.visit(node.body)
    
    def visit_Block(self, node):
        result = None
        for statement in node.statements:
            result = self.visit(statement)
        return result
    
    def visit_Return(self, node):
        return self.visit(node.expr)

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
            T.PLUS: lambda x, y: x + y,
            T.MINUS: lambda x, y: x - y,
            T.MUL: lambda x, y: x * y,
            T.DIV: lambda x, y: x / y,
            T.MOD: lambda x,y: x % y,
            T.POWER: lambda x, y: x ** y
        }
        result = operations[node.op.type](left_val, right_val)
        print(f"BinOp result: {result}")
        return result
    
    def visit_UnaryOp(self, node):
        print(f"Visiting UnaryOp with op: {node.op.type}")
        op = node.op.type
        if op == T.PLUS :
            result =  +1 * self.visit(node.expr)
        elif op == T.MINUS:
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

    filepath = "../scanner/cfile.c"
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
    
    with open(filepath , "r") as f:
        text = f.read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(result)


if __name__ == '__main__':
    main()










