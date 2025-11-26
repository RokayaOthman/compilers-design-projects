import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tokens import TokenType as T

class Token:
    def __init__(self, lexeme: str, token_type):
        self.lexeme = lexeme 
        self.type = token_type
        # handle numbers
        if token_type == 'integer':
            self.value = int(lexeme)
        elif token_type == 'real number':
            self.value = float(lexeme)
        else:
            self.value = lexeme

    def __str__(self):
        return f"({self.lexeme} => {self.token_type})"

class Scanner:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def is_delimiter(ch):
        delimiters = ' +-*/ ,;><=()[]{}\n\t%'
        return ch in delimiters

    @staticmethod
    def is_keyword(s):
        keywords = [
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "inline", "int", "long", "register", "restrict", "return", "short",
            "signed", "sizeof", "static", "struct", "switch", "typedef", "union",
            "unsigned", "void", "volatile", "while",
            "_Bool", "_Complex", "_Imaginary"
        ]
        return s in keywords

    @staticmethod
    def is_operator(ch):
        operators = '+-*/><=%'
        return ch in operators

    @staticmethod
    def valid_identifier(text):
        if not text or text[0].isdigit() or Scanner.is_delimiter(text[0]):
            return False
        return True

    @staticmethod
    def is_integer(text):
        if not text:
            return False
        for i in range(len(text)):
            if not text[i].isdigit() and not (text[i] == '-' and i == 0):
                return False
        return True

    @staticmethod
    def is_real_number(text):
        if not text:
            return False
        try:
            float(text)
            return '.' in text  # this ensures it has a '.' in it
        except ValueError:
            return False

    @staticmethod
    def sub_string(text, left, right):
        return text[left: right + 1]

    # returns a list of objects (lexeme , tokenType)
    @staticmethod
    def scan_tokens(stringCode):
        left = 0
        right = 0
        len_str = len(stringCode)
        tokens = []
        double_ops = ['==', '<=', '>=', '!=', '&&', '||']

        # the main loop
        while right < len_str:
            # Handle comments before anything else
            if stringCode[right] == '/' and right + 1 < len_str:
                # Single-line comment //
                if stringCode[right + 1] == '/':
                    right += 2
                    while right < len_str and stringCode[right] != '\n':
                        right += 1
                    # move left pointer to after the comment
                    left = right
                    continue

                # Multi-line comment /* ... */
                elif stringCode[right + 1] == '*':
                    right += 2
                    while right + 1 < len_str and not (stringCode[right] == '*' and stringCode[right + 1] == '/'):
                        right += 1
                    right += 2  # skip the closing */
                    left = right
                    continue

            if not Scanner.is_delimiter(stringCode[right]):
                right += 1
                continue

            # We hit a delimiter or end of token
            if left != right:
                sub_str = Scanner.sub_string(stringCode, left, right - 1).strip()

                if Scanner.is_keyword(sub_str):
                    important_keywords = {'int' : 'int keyword',
                                          'return' : 'return keyword'}
                    token_type = important_keywords.get(sub_str, 'keyword')
                    tokens.append(Token(sub_str, token_type))
                elif Scanner.is_integer(sub_str):
                    tokens.append(Token(sub_str, 'integer'))
                elif Scanner.is_real_number(sub_str):
                    tokens.append(Token(sub_str, 'real number'))
                elif Scanner.valid_identifier(sub_str):
                    tokens.append(Token(sub_str, 'identifier'))

            ch = stringCode[right]
            next_ch = stringCode[right + 1] if right + 1 < len_str else ''

            if ch + next_ch in double_ops:
                tokens.append(Token(ch + next_ch, 'operator'))
                right += 2
                left = right
                continue
            elif Scanner.is_operator(ch):
                tokens.append(Token(ch, 'operator'))
                right += 1
                left = right
                continue
            else:
                delimiter_types = {
                    '{': 'open brace',
                    '}': 'close brace',
                    '(': 'open parenthesis',
                    ')': 'close parenthesis',
                    '[': 'open bracket',
                    ']': 'close bracket',
                    ',': '`comm`a',
                    ';': 'semicolon',
                    '\n': 'newline',
                    '\t': 'tab',
                }
                token_type = delimiter_types.get(ch, 'delimiter')
                if ch.strip():  # ignore whitespace
                    tokens.append(Token(ch, token_type))
                right += 1
                left = right


         # Handle any remaining content after the loop ends
        if left < len_str:
            remaining_sub_str = Scanner.sub_string(stringCode, left, len_str - 1).strip()
            if remaining_sub_str:
                if Scanner.is_keyword(remaining_sub_str):
                    important_keywords = {'int' : 'int keyword',
                                        'return' : 'return keyword'}
                    token_type = important_keywords.get(remaining_sub_str, 'keyword')
                    tokens.append(Token(remaining_sub_str, token_type))
                elif Scanner.is_integer(remaining_sub_str):
                    tokens.append(Token(remaining_sub_str, 'integer'))
                elif Scanner.is_real_number(remaining_sub_str):
                    tokens.append(Token(remaining_sub_str, 'real number'))
                elif Scanner.valid_identifier(remaining_sub_str):
                    tokens.append(Token(remaining_sub_str, 'identifier'))

        return tokens

class Lexer :
    
    def __init__(self, text):
            tokens = Scanner.scan_tokens(text)
            print(f"Scanner tokens: {[(t.lexeme, t.type) for t in tokens]}")  # DEBUG
            self.tokens = []
            for token in tokens:
                # Map the scanner token types to parser token types
                if token.type == 'integer':
                    self.tokens.append(Token(token.lexeme, T.INTEGER))
                elif token.lexeme == '+':
                    self.tokens.append(Token(token.lexeme, T.PLUS))
                elif token.lexeme == '-':
                    self.tokens.append(Token(token.lexeme, T.MINUS))
                elif token.lexeme == '*':
                    self.tokens.append(Token(token.lexeme, T.MUL))
                elif token.lexeme == '/':
                    self.tokens.append(Token(token.lexeme, T.DIV))
                elif token.lexeme == '%':
                    self.tokens.append(Token(token.lexeme, T.MOD))
                elif token.lexeme == '(':
                    self.tokens.append(Token(token.lexeme, T.LPAREN))
                elif token.lexeme == ')':
                    self.tokens.append(Token(token.lexeme, T.RPAREN))
                
            
            # Add end-of-file token
            self.tokens.append(Token('', T.EOF))
            self.pos = 0


    def get_next_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]   
            self.pos += 1
            return token
        else:
            # Return EOF token if we've reached the end
            return Token('', T.EOF)
