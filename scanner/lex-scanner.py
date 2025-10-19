class Token:
    def __init__(self, lexeme : str, token_type):
        self.lexeme = lexeme
        self.token_type = token_type
    def __str__(self):
        return f"({self.lexeme}, {self.token_type})"

class Scanner:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def is_delimiter(ch):
        delimiters = ' +-*/ ,;><=()[]{}\n\t'
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
        operators = '+-*/><='
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
            if not text[i].isdigit() and not (text[i] == '-' and i == 0) :
                return False
        return True
    
    @staticmethod
    def is_real_number(text):    
        if not text :
            return False
        try:
            float(text)
            return '.' in text #this ensures it has a '.' in it
        except ValueError:
            return False
    
    @staticmethod
    def sub_string(text, left, right):
        return text[left : right + 1]

    
    # returns a list of objects (lexeme , tokenType)
    @staticmethod
    def scan_tokens(stringCode):
        double_ops = ['++', '--', '==', '<=', '>=', '!=', '&&', '||']
        left = 0
        right = 0
        len_str = len(stringCode)
        tokens = []
        
        # the main loop
        while right < len_str and left <= right :
            
            if right < len_str and not Scanner.is_delimiter(stringCode[right]):
                right += 1
            
            if ((right < len_str and Scanner.is_delimiter(stringCode[right])) and left != right) or (right == len_str and left != right):
                sub_str = Scanner.sub_string(stringCode, left, right - 1).strip()

                # choosing the type of this substring
                if Scanner.is_keyword(sub_str):
                    token = Token(sub_str, 'keyword')
                    tokens.append(token)
                
                elif Scanner.is_integer(sub_str):
                    token = Token(sub_str, 'integer')
                    tokens.append(token)
                
                elif Scanner.is_real_number(sub_str):
                    token = Token(sub_str, 'real number')
                    tokens.append(token)

                elif Scanner.valid_identifier(sub_str):
                    token = Token(sub_str, 'identifier')
                    tokens.append(token)

                right += 1
                left = right

            elif right < len_str and Scanner.is_delimiter(stringCode[right]):
                ch = stringCode[right]
                
    
                next_ch = stringCode[right + 1] if right + 1 < len_str else ''
                    
                if ch + next_ch in double_ops :
                    token = Token(ch + next_ch, 'operator')
                    tokens.append(token)
                    right += 2
                    left = right
                    continue

                elif Scanner.is_operator(ch):
                    token = Token(ch, 'operator')
                    tokens.append(token)
                    right += 1
                    left = right
                    continue

        return tokens

def scan_c_file(c_file):
    with open(c_file, "r", encoding="utf-8") as f:
        content = f.read()
    tokens = Scanner.scan_tokens(content)
    return tokens
    
def main():
    c_file = 'cfile.c'  
    tokens = scan_c_file(c_file)
    for token in tokens :
        print(token)
            
if __name__ == "__main__":
    main()




        
        

