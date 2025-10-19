# Lexical Scanner for C Code

This Python program implements a **simple lexical analyzer (scanner)** for C source code. It reads a C file, identifies each lexeme (token), classifies it (e.g., keyword, identifier, operator, number, delimiter), and prints the result.

## Overview

A **lexical scanner** (or lexer) is the first phase of a compiler.
It reads raw source code and breaks it into **tokens** — the smallest meaningful units such as:

* `int`, `if`, `return` → keywords
* `a`, `b`, `count` → identifiers
* `+`, `==`, `<=` → operators
* `{`, `}`, `;` → delimiters
* `123`, `10.5` → numbers

This project demonstrates how a scanner can be implemented using basic Python logic and string operations.

---

## ⚙️ How It Works

1. **`Token` class**
   Represents a token with two attributes:

   * `lexeme`: the actual string from the source code
   * `token_type`: the category (keyword, operator, identifier, etc.)

2. **`Scanner` class**
   Contains static helper functions to:

   * Detect delimiters, keywords, operators, integers, and real numbers.
   * Extract substrings between delimiters.
   * Tokenize the input code through the `scan_tokens()` method.

3. **`scan_c_file()` function**
   Reads a `.c` file and passes its content to the scanner.

4. **`main()` function**
   Loads a file named `cfile.c` (you can change this), runs the scanner, and prints all tokens in the format:

   ```
   (lexeme => token_type)
   ```

---
**Sample output:**
```
(int => keyword)
(main => identifier)
(() => delimiter)
({ => delimiter)
(int => keyword)
(a => identifier)
(= => operator)
(5 => integer)
(; => delimiter)
(float => keyword)
(b => identifier)
(= => operator)
(10.5 => real number)
(; => delimiter)
(if => keyword)
(a => identifier)
(< => operator)
(b => identifier)
({ => delimiter)
(a => identifier)
(= => operator)
(a => identifier)
(+ => operator)
(1 => integer)
(; => delimiter)
(} => delimiter)
(else => keyword)
({ => delimiter)
(b => identifier)
(= => operator)
(b => identifier)
(- => operator)
(1.0 => real number)
(; => delimiter)
(++ => operator)
(; => delimiter)
(return => keyword)
(0 => integer)
(; => delimiter)
(} => delimiter)
(} => delimiter)
```
---
## ▶️ Running the Program

1. Save your C source code as `cfile.c` in the same directory as the script.
2. Run the Python scanner:

   ```bash
   python lex-scanner.py
   ```
3. View the tokens printed in your terminal.

