def is_delimiter(ch):
    delimiters = ' +-*/ ,;><=()\[\]{}'
    return ch in delimiters

def is_operator(ch):
    return ch in '+-*/><=' 

def valid_identifier(str):
    if not str or str[0].isdigit() or is_delimiter(str[0]):
        return False
    return True

def is_keyword(str):
    keywords = ["if", "else", "while", "do", "break", "continue", "int", "double", "float", "return", "char", "case", "sizeof", "long", "short", "typedef", "switch", "unsigned", "void", "static", "struct", "goto"]
    return str in keywords

def is_integer(str):
    if not str:
        return False
    for i in range(len(str)):
        if not str[i].isdigit() and not (str[i] == '-' and i == 0):
            return False
    return True

def is_real_number(str):
    if not str:
        return False
    has_decimal = False
    for i in range(len(str)):
        if not str[i].isdigit() and str[i] != '.' and not (str[i] == '-' and i == 0):
            return False
        if str[i] == '.':
            has_decimal = True
    return has_decimal

def sub_string(str, left, right):
    return str[left:right + 1]

def parse(str):
    left = 0
    right = 0
    len_str = len(str)

    while right <= len_str and left <= right:
        if right < len_str and not is_delimiter(str[right]):
            right += 1

        if right< len_str and is_delimiter(str[right]) and left == right:
            if is_operator(str[right]):
                print(f"'{str[right]}' IS AN OPERATOR")

            right += 1
            left = right
        elif right < len_str and is_delimiter(str[right]) and left != right or (right == len_str and left != right):
            sub_str = sub_string(str, left, right - 1)

            if is_keyword(sub_str):
                print(f"'{sub_str}' IS A KEYWORD")

            elif is_integer(sub_str):
                print(f"'{sub_str}' IS AN INTEGER")

            elif is_real_number(sub_str):
                print(f"'{sub_str}' IS A REAL NUMBER")

            elif valid_identifier(sub_str) and not is_delimiter(str[right - 1]):
                print(f"'{sub_str}' IS A VALID IDENTIFIER")

            elif not valid_identifier(sub_str) and not is_delimiter(str[right - 1]):
                print(f"'{sub_str}' IS NOT A VALID IDENTIFIER")

            left = right

if __name__ == '__main__':
    str = 'int a = b + 1c; )'
    parse(str)