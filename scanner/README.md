

** grammar ** 

program      : function 
function     : "int" ID "(" ")" "{" block "}"
block        : statement+
statement    : "return" expr ";"

expr         : term ((PLUS | MINUS) term) *
term         : factor ((MUL | DIV | MOD ) factor) *
factor       : (PLUS | MINUS) factor | power 
power        : atom (POWER power) ?
atom         : INTEGER | LPARENTH expr RPAREN
   

---
steps : 

1. change the grammar rule
2. add a new node
3. add a visitor

---
Parser      
   turn flat tokens into a meaningful tree (AST)
   applying grammar rules
   the AST captures operator precedence , program structure (function => return statement => expression)

interpreter 
   walks the AST and computes a result
   by visiting each node recursively (using the visitor pattern)
   performs real computation
   
