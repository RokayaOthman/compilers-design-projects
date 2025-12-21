<expr>    ::= <term> ( ("+" | "-") <term> )*
<term>    ::= <factor> ( ("*" | "/" | "%") <factor> )*
<factor>  ::= ("+" | "-") <factor>
            | <integer>
            | "(" <expr> ")"


The parser builds an Abstract Syntax Tree (AST) using these nodes:
BinOp(left, op, right)
UnaryOp(op, expr)
Num(token)