# main.py - OidaScript Interpreter
from parser import parse
from interpreter import run_code
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "examples/test.oida"  # Österreichische file extension!

with open(filename, encoding='utf-8') as f:
    lines = f.readlines()

ast = parse(lines)

run_code(ast)
