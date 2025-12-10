from enum import Enum

class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    EOF = 'EOF'
    MOD = 'MOD'
    POWER = 'POWER'
    GREATER = 'GREATER'
    INT = 'INT'
    RETURN = 'RETURN'
    SEMI = 'SEMI'
    IDENTIFIER = 'IDENTIFIER'
    ASSIGN = '='


TOKEN_DESCRIPTIONS = {
    TokenType.INT: "keyword",
    TokenType.RETURN: "keyword",
    TokenType.IDENTIFIER: "identifier",
    TokenType.INTEGER: "integer",
    TokenType.PLUS: "operator",
    TokenType.MINUS: "operator",
    TokenType.MUL: "operator",
    TokenType.DIV: "operator",
    TokenType.MOD: "operator",
    TokenType.POWER: "operator",
    TokenType.LPAREN: "left parenthesis",
    TokenType.RPAREN: "right parenthesis",
    TokenType.LBRACE: "left brace",
    TokenType.RBRACE: "right brace",
    TokenType.SEMI: "semicolon",
    TokenType.ASSIGN: "assignment operator",
    TokenType.EOF: "end of file"
}