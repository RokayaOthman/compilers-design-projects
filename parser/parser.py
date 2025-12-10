import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tokens import TokenType as T , TOKEN_DESCRIPTIONS
from scanner.lex_scanner import Lexer, Token, Scanner
class AST:
    pass

class ParserError(Exception) :
# exception raised for syntax errors in the parser
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.message)
   
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
        self.op = op # = self.token
        self.right = right

    def __str__(self):
        return str(self.token)

class UnaryOp():
    def __init__(self, op, expr):
        self.token = self.op 
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
        if not statements or not isinstance(statements[-1], Return):
            self.error("Function body must end with a return statement")
        return Block(statements)

    def parse_statement(self):
        token = self.current_token
        
        # Handle assignment: x = expr;
        if token.type == T.IDENTIFIER:
            next_token = self.lexer.peek()
            if next_token and next_token.type == T.ASSIGN:
                var_token = self.current_token  # Save the original token
                self.eat(T.IDENTIFIER)
                self.eat(T.ASSIGN)
                expr_node = self.expr()
                self.eat(T.SEMI)
                return Assign(Var(var_token), expr_node)  # Use saved token
        
        # Handle return statement
        if token.type == T.RETURN:
            self.eat(T.RETURN)
            expr_node = self.expr()
            self.eat(T.SEMI)
            return Return(expr_node)
        
        self.error(f"Unexpected token")


    def error(self, message=None):
        if message is None :
            message = f"Unexpected token"
        raise ParserError(message, self.current_token)
    

    def eat(self, token_type):
        ##compare current token type with 
        ## the passed token type if they match :
        ## (Accept as Valid) the current token and assign the next token to the self.current_token,
        ## otherwise raise an exception

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            
        else:
            self.error(f"Expected '{token_type}', got '{self.current_token.type}'")
            
    
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
    # 2 + 3 ** 4 ** 5 + 1
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
        program_node =  self.parse_program()
        if self.current_token.type != T.EOF:
            self.error("Unexpected tokens after end of program")
        return program_node

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
        self.variables = {}
   
    def visit_Program(self, node):
        return self.visit(node.function)
    
    def visit_Function(self, node):
        return self.visit(node.body)
    
    def visit_Block(self, node):
        #print(f"Block has {len(node.statements)} statements")
        result = None
        for i, statement in enumerate(node.statements):
            #print(f"Visiting statement {i+1}: {type(statement).__name__}")
            result = self.visit(statement)
        return result

    def visit_Assign(self, node):
        print(f"ASSIGN: {node.left.name}")
        var_name = node.left.name
        value = self.visit(node.right)
        self.variables[var_name] = value
        return value

    def visit_Var(self, node):
        var_name = node.name
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise Exception(f"Undefined variable: {var_name}")
           


    def visit_Return(self, node):
        return self.visit(node.expr)

    def visit_BinOp(self, node):
        # Post-order: Visit children → process node
        #print(f"Visiting BinOp with op: {node.op.type}")
        left_val = (self.visit(node.left))
        #print(f"left value: {left_val} ")
        right_val = (self.visit(node.right))
        op_type = node.op.type

        #print(f"right value: {right_val}")
        
        if op_type == T.PLUS:
            return left_val + right_val
        elif op_type == T.MINUS:
            return left_val - right_val
        elif op_type == T.MUL:
            return left_val * right_val
        elif op_type == T.DIV:
            if right_val == 0: 
                raise Exception("Runtime Error: Division by zero")
            return left_val / right_val
        elif op_type == T.MOD:
            if right_val == 0:
                raise Exception("Runtime Error: Modulo by zero")
            return left_val % right_val
        elif op_type == T.POWER:
            return left_val ** right_val
        else:
            raise Exception(f"Unknown operator: {op_type}")
        
        
    
    def visit_UnaryOp(self, node):
        #print(f"Visiting UnaryOp with op: {node.op.type}")
        op = node.op.type
        if op == T.PLUS :
            result =  +1 * self.visit(node.expr)
        elif op == T.MINUS:
            result =  -1 * self.visit(node.expr)
        print(f"UnaryOp result: {result}")
        return result
                
    
    def visit_Num(self, node):
        #print(f"Visiting Num: {node.value}")
        result = int(node.value)
        #print(f"Num result: {result}")
        return result
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def interactie_menu_loop(filepath):
    while True:
        print("1. Print the tokens")
        print("2. Compile the file")
        print("3. Exit")
        choice = input("Enter an option (1-3): ")
        
        if choice == "1" or choice == "2":
            # Both options need to read the file
            if not os.path.exists(filepath):
                print(f"Error: File '{filepath}' not found.")
                continue  # Don't return — stay in menu
            
            with open(filepath, "r") as f:
                text = f.read()
            
            if choice == "1":
                # Use Lexer to get tokens
                lexer = Lexer(text)
                tokens = []
                token = lexer.get_next_token()
                while token.type != T.EOF:
                    tokens.append(token)
                    token = lexer.get_next_token()
                
                print("Scanner tokens:")
                for t in tokens:
                    desc = TOKEN_DESCRIPTIONS.get(t.type, "unknown")
                    print(f" '{t.lexeme}' -> {desc}")
                    
            elif choice == "2":
                try:
                    lexer = Lexer(text)
                    parser = Parser(lexer)
                    interpreter = Interpreter(parser)
                    result = interpreter.interpret()
                    print(f"✅ Compiled successfully! Result: {result}")
                except ParserError as e:
                    print(f"❌ Syntax Error: {e.message}")
                except Exception as e:  # ← Add this to catch runtime errors
                    print(f"💥 Runtime Error: {e}")
                        
        elif choice == "3":
            break
        else:
            print("⚠️  Invalid choice, try again.")

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(project_root, "cfile.txt")
    # if not os.path.exists(filepath):
    #     print(f"Error: File '{filepath}' not found.")
    #     return
    
    # with open(filepath , "r") as f:
    #     text = f.read()

    # lexer = Lexer(text)
    # parser = Parser(lexer)
    # interpreter = Interpreter(parser)
    # result = interpreter.interpret()
    # print(result)
    interactie_menu_loop(filepath)


    
    
    

if __name__ == '__main__':
    main()










