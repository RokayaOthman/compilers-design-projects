# Simple C-Like Compiler

A lightweight compiler for a C-inspired language, built from scratch as part of a Compiler Design course.  
This project includes a **lexer**, **recursive descent parser**, **AST**, and **interpreter** — all implemented in Python.

## Features

- **Arithmetic expressions**: `2 + 3 * (4 ** 2)`
- **Variables**: `x = 5; return x * 2;`
- **Function structure**: `int main() { ... }`
- **Operator precedence & associativity** (e.g., `**` is right-associative)
- **Syntax error reporting** with human-readable messages
- **Runtime error handling** (e.g., division by zero, undefined variables)
- **Interactive menu**: tokenize, compile, or exit
- **Human-friendly token output** (e.g., `'(' → left parenthesis`)

## Full grammar rules :

<program>      ::= <function>

<function>     ::= "int" <identifier> "(" ")" "{" <block> "}"

<block>        ::= <statement>+

<statement>    ::= <assignment> | <return_stmt>

<assignment>   ::= <identifier> "=" <expr> ";"

<return_stmt>  ::= "return" <expr> ";"

<expr>         ::= <term> ( ("+" | "-") <term> )*

<term>         ::= <factor> ( ("*" | "/" | "%") <factor> )*

<factor>       ::= ("+" | "-") <factor> | <power>

<power>        ::= <atom> ( "**" <power> )?

<atom>         ::= <integer> | <identifier> | "(" <expr> ")"