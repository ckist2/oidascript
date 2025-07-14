# parser.py
def tokenize_line(line):
    tokens = []
    current_token = ""
    in_string = False
    in_comment = False
    string_char = None
    i = 0
    
    line = line.strip()
    while i < len(line):
        char = line[i]
        
        # Handle comments
        if char == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string:
            in_comment = True
            break
            
        if in_comment:
            break
            
        # String handling - both " and '
        if char in ['"', "'"] and not in_comment:
            if not in_string:
                # String begins
                in_string = True
                string_char = char
                current_token += char
            elif char == string_char:
                # String ends
                in_string = False
                current_token += char
                tokens.append(current_token)
                current_token = ""
                string_char = None
            else:
                # Different quote in string
                current_token += char
        elif in_string:
            # In string - add everything
            current_token += char
        elif char == ' ' and not in_string and not in_comment:
            # Whitespace outside strings
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in '(){}[],:' and not in_string and not in_comment:
            # Special characters
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            # Normal character
            current_token += char
        
        i += 1
    
    if current_token and not in_comment:
        tokens.append(current_token)
    
    return tokens

def parse_expression(tokens):
    if not tokens:
        return None
    
    # List access behandeln: variable[index]
    if len(tokens) >= 4 and tokens[1] == '[' and tokens[-1] == ']':
        var_name = tokens[0]
        index_tokens = tokens[2:-1]  # Alles zwischen [ und ]
        index = parse_expression(index_tokens)
        return {
            "type": "index",
            "object": {"type": "var", "name": var_name},
            "index": index
        }
        
    # Funktionsaufrufe behandeln: func_name ( arg1 , arg2 )
    if len(tokens) >= 3 and tokens[1] == '(' and tokens[-1] == ')':
        func_name = tokens[0]
        arg_tokens = tokens[2:-1]  # Alles zwischen ( und )
        
        if not arg_tokens:  # Keine Argumente
            return {
                "type": "call",
                "name": func_name,
                "args": []
            }
        else:
            # Argumente durch Komma aufteilen - aber respektiere verschachtelte Klammern
            args = []
            current_arg = []
            paren_depth = 0
            
            for token in arg_tokens:
                if token == ',' and paren_depth == 0:
                    if current_arg:
                        args.append(parse_expression(current_arg))
                        current_arg = []
                else:
                    if token == '(':
                        paren_depth += 1
                    elif token == ')':
                        paren_depth -= 1
                    current_arg.append(token)
            
            # Das letzte Argument hinzufügen
            if current_arg:
                args.append(parse_expression(current_arg))
            
            return {
                "type": "call",
                "name": func_name,
                "args": args
            }
    
    # Mehrfache Infix-Operationen durch Finden von Operatoren und Links-nach-Rechts-Parsing behandeln
    operators = {"+", "-", "*", "/", ">", "<", "==", "!=", ">=", "<=", "und", "oda"}
    unary_operators = {"ned"}
    
    # Unäre Operatoren zuerst behandeln (wie "ned")
    if len(tokens) >= 2 and tokens[0] in unary_operators:
        return {
            "type": "call",
            "name": tokens[0],
            "args": [parse_expression(tokens[1:])]
        }
    
    # Operator-Positionen finden
    op_positions = []
    for i, token in enumerate(tokens):
        if token in operators:
            op_positions.append(i)
    
    if len(op_positions) == 1 and len(tokens) == 3:
        # Einzelne Infix-Operation: a > 10  =>  call(">", a, 10)
        return {
            "type": "call",
            "name": tokens[1],
            "args": [
                parse_expression([tokens[0]]),
                parse_expression([tokens[2]])
            ]
        }
    elif len(op_positions) > 1:
        # Mehrfache Infix-Operationen - links nach rechts parsen
        # "Hello," + " " + name wird zu (("Hello," + " ") + name)
        
        # Mit dem ersten Operanden beginnen
        result = parse_expression([tokens[0]])
        
        # Jeden Operator und Operanden verarbeiten
        for i, op_pos in enumerate(op_positions):
            op = tokens[op_pos]
            if i == len(op_positions) - 1:
                # Letzte Operation - alles nach diesem Operator
                right = parse_expression(tokens[op_pos + 1:])
            else:
                # Den Operanden zwischen diesem und dem nächsten Operator holen
                right = parse_expression([tokens[op_pos + 1]])
            
            result = {
                "type": "call",
                "name": op,
                "args": [result, right]
            }
        
        return result

    # Function call or var
    if len(tokens) == 1:
        # Prüfen auf positive oder negative Ganzzahlen und Dezimalzahlen
        token = tokens[0]
        # Check for strings first
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]  # Remove quotes and return string content directly
        elif token.startswith("'") and token.endswith("'"):
            return token[1:-1]  # Remove quotes and return string content directly
        elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            return int(token)
        elif '.' in token and not token.startswith('"') and not token.startswith("'"):
            try:
                return float(token)
            except ValueError:
                pass
        # Prüfen auf Funktionsaufruf mit leeren Klammern
        elif tokens[0].endswith('()'):
            return {
                "type": "call",
                "name": tokens[0][:-2],
                "args": []
            }
        # Lambda Ausdrücke prüfen: lambda x, y => x + y
        elif tokens[0] == "lambda":
            arrow_index = tokens.index("=>")
            params = []
            for i in range(1, arrow_index):
                if tokens[i] != ",":
                    params.append(tokens[i])
            
            body_tokens = tokens[arrow_index + 1:]
            body = parse_expression(body_tokens)
            
            return {
                "type": "lambda",
                "params": params,
                "body": body
            }
        # Boolean Werte prüfen (OidaScript)
        elif tokens[0] == "woahr":
            return True
        elif tokens[0] == "ned_woahr":
            return False
        elif '(' in tokens[0] and tokens[0].endswith(')'):
            paren_start = tokens[0].index('(')
            func_name = tokens[0][:paren_start]
            args_part = tokens[0][paren_start+1:-1]
            
            if args_part:
                # Durch Komma trennen und jedes Argument parsen
                arg_strs = args_part.split(',')
                args = []
                for arg_str in arg_strs:
                    arg_tokens = tokenize_line(arg_str.strip())
                    args.append(parse_expression(arg_tokens))
                
                return {
                    "type": "call",
                    "name": func_name,
                    "args": args
                }
            else:
                return {
                    "type": "call",
                    "name": func_name,
                    "args": []
                }
        else:
            return { "type": "var", "name": tokens[0] }

    # Listen-Literale [1, 2, 3] behandeln
    if len(tokens) >= 3 and tokens[0] == '[' and tokens[-1] == ']':
        items = []
        if len(tokens) > 2:  # Ned leere Liste
            # Komma-getrennte Elemente parsen
            item_tokens = []
            for token in tokens[1:-1]:  # Skip [ and ]
                if token == ',':
                    if item_tokens:
                        items.append(parse_expression(item_tokens))
                        item_tokens = []
                else:
                    item_tokens.append(token)
            # Des letzte Element hinzufügen
            if item_tokens:
                items.append(parse_expression(item_tokens))
        
        return {
            "type": "list",
            "items": items
        }

    # Wörterbuch-Literale {key: value, key2: value2} behandeln
    if len(tokens) >= 3 and tokens[0] == '{' and tokens[-1] == '}':
        pairs = []
        if len(tokens) > 2:  # Ned leeres Wörterbuch
            # Komma-getrennte key:value Paare parsen
            current_pair = []
            key_tokens = []
            value_tokens = []
            in_value = False
            
            for token in tokens[1:-1]:  # Skip { and }
                if token == ',':
                    if in_value and value_tokens:
                        pairs.append([parse_expression(key_tokens), parse_expression(value_tokens)])
                        key_tokens = []
                        value_tokens = []
                        in_value = False
                elif token == ':':
                    in_value = True
                else:
                    if in_value:
                        value_tokens.append(token)
                    else:
                        key_tokens.append(token)
            
            # Des letzte Paar hinzufügen
            if in_value and value_tokens:
                pairs.append([parse_expression(key_tokens), parse_expression(value_tokens)])
        
        return {
            "type": "dict",
            "pairs": pairs
        }

    # Prüfen obs a Funktionsaufruf is (erstes Token is Funktionsname, Rest san Argumente)
    # Oba erst prüfen obs Operatoren enthält - wenn jo, is es a Expression, koa einfacher Funktionsaufruf
    if any(token in operators for token in tokens[1:]) or any(token in unary_operators for token in tokens[1:]):
        # Des enthält Operatoren, also is ned a einfacher Funktionsaufruf
        # Gib's zruck wies is und lass'n Aufrufer damit umgehen
        return {
            "type": "call",
            "name": tokens[0],
            "args": [parse_expression(tokens[1:])]
        }
    
    # Check for simple function calls without parentheses but with multiple args
    if len(tokens) > 1:
        # This is a function call with space-separated arguments
        func_name = tokens[0]
        args = []
        
        # Parse each argument individually
        for token in tokens[1:]:
            args.append(parse_expression([token]))
        
        return {
            "type": "call",
            "name": func_name,
            "args": args
        }
    
    # Prüfen auf spezielle Klammer-Tokens die Datenstrukturen anzeigen
    if any(token in '[]{}' for token in tokens):
        # Indexierung obj[index] behandeln wo obj a Variable is
        if '[' in tokens and ']' in tokens:
            bracket_start = tokens.index('[')
            bracket_end = tokens.index(']')
            if bracket_start > 0 and bracket_end == len(tokens) - 1:
                obj_tokens = tokens[:bracket_start]
                index_tokens = tokens[bracket_start + 1:bracket_end]
                return {
                    "type": "index",
                    "object": parse_expression(obj_tokens),
                    "index": parse_expression(index_tokens)
                }
    
    # If it's a single token that wasn't caught above, check if it's a variable
    if len(tokens) == 1:
        return { "type": "var", "name": tokens[0] }
    
    return {
        "type": "call",
        "name": tokens[0],
        "args": [parse_expression([t]) for t in tokens[1:]]
    }


def parse(lines):
    ast = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("//"):
            i += 1
            continue

        tokens = tokenize_line(line)
        if not tokens:  # Skip empty token lists
            i += 1
            continue
        
        if tokens[0] == "loss":
            ast.append({
                "type": "let",
                "name": tokens[1],
                "value": parse_expression(tokens[3:])
            })
            
        elif tokens[0] == "solang":
            # Den => Trenner finden
            arrow_index = tokens.index("=>")
            cond = parse_expression(tokens[1:arrow_index])
            i += 1
            body = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("sonscht =>", "wenn", "solang", "tuas")):
                parsed = parse_line(lines[i])
                if parsed is not None:
                    body.append(parsed)
                i += 1
            ast.append({
                "type": "while",
                "cond": cond,
                "body": body
            })
            continue

        elif tokens[0] == "tuas":
            name = tokens[1]
            params = tokens[2:-1]  # vor =>
            body = []
            i += 1
            while i < len(lines):
                line = lines[i].strip()
                if line == "":
                    i += 1
                    continue
                
                # Abbrechen wenn ma a ander Top-Level Konstrukt antreffen (ned eingerückt)
                if (line and not lines[i].startswith("  ") and 
                    tokenize_line(line) and len(tokenize_line(line)) > 0 and
                    tokenize_line(line)[0] in ["tuas", "loss"] and
                    tokenize_line(line)[0] != "gib"):
                    break
                
                parsed = parse_line(lines[i])
                if parsed is not None:
                    body.append(parsed)
                i += 1
                
            ast.append({
                "type": "fn",
                "name": name,
                "params": params,
                "body": body
            })
            continue  # habma scho i bewegt

        elif tokens[0] == "gib":
            ast.append({
                "type": "return",
                "value": parse_expression(tokens[2:])  # skip "gib zruck"
            })

        elif tokens[0] == "versuchs":
            # Try-Block parsen
            i += 1
            try_body = []
            while i < len(lines) and not lines[i].strip().startswith("fang"):
                if lines[i].strip():
                    parsed = parse_line(lines[i])
                    if parsed is not None:
                        try_body.append(parsed)
                i += 1
            
            catch_body = []
            error_var = None
            
            # Catch-Block parsen wanns existiert
            if i < len(lines) and lines[i].strip().startswith("fang"):
                catch_line = lines[i].strip()
                catch_tokens = tokenize_line(catch_line)
                
                # Prüfen ob catch a Error-Variable hat: fang auf e =>
                if len(catch_tokens) >= 4 and catch_tokens[3] == "=>":
                    error_var = catch_tokens[2]
                
                i += 1
                while i < len(lines) and lines[i].strip():
                    parsed = parse_line(lines[i])
                    if parsed is not None:
                        catch_body.append(parsed)
                    i += 1
            
            try_catch_node = {
                "type": "try",
                "try_body": try_body
            }
            
            if catch_body:
                try_catch_node["catch_body"] = catch_body
                if error_var:
                    try_catch_node["error_var"] = error_var
            
            ast.append(try_catch_node)
            continue

        elif tokens[0] == "schmeiss":
            ast.append({
                "type": "throw",
                "message": parse_expression(tokens[1:])
            })

        elif tokens[0] == "wenn":
            cond = parse_expression(tokens[1:-1])  # vor =>
            i += 1
            then_branch = []
            while i < len(lines) and not lines[i].strip().startswith("sonscht =>"):
                parsed = parse_line(lines[i])
                if parsed is not None:
                    then_branch.append(parsed)
                i += 1
            i += 1  # 'sonscht =>' überspringen
            else_branch = []
            while i < len(lines):
                parsed = parse_line(lines[i])
                if parsed is not None:
                    else_branch.append(parsed)
                i += 1
            ast.append({
                "type": "if",
                "cond": cond,
                "then": then_branch,
                "else": else_branch
            })
            break

        else:
            parsed = parse_line(line)
            if parsed is not None:
                ast.append(parsed)

        i += 1

    return ast

def parse_line_safe(line):
    """A Zeile parsen und des Ergebnis zruckgeben wanns ned None is, sonst nix zruckgeben"""
    result = parse_line(line)
    return result if result is not None else None

def parse_line(line):
    try:
        tokens = tokenize_line(line)
        
        # Leere Zeilen oder Kommentare behandeln
        if not tokens or (len(tokens) > 0 and tokens[0].startswith("//")):
            return None
        
        if tokens[0] == "gib":
            if len(tokens) < 3:
                raise SyntaxError(f"Syntax-Fehler: 'gib zruck' braucht an Wert")
            return {
                "type": "return",
                "value": parse_expression(tokens[2:])  # skip "gib zruck"
            }
        elif tokens[0] == "loss":
            if len(tokens) < 4 or tokens[2] != "=":
                raise SyntaxError(f"Syntax-Fehler: Variable braucht 'loss name = wert' Format")
            return {
                "type": "let",
                "name": tokens[1],
                "value": parse_expression(tokens[3:])
            }
        elif tokens[0] == "schmeiss":
            return {
                "type": "throw",
                "message": parse_expression(tokens[1:])
            }
        else:
            return parse_expression(tokens)
    except Exception as e:
        raise SyntaxError(f"Parser-Fehler in Zeile '{line.strip()}': {str(e)}")

def parse_file(filename):
    """Parse an entire OidaScript file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            return parse(lines)
    except FileNotFoundError:
        raise FileNotFoundError(f"Datei '{filename}' nicht gefunden")
    except Exception as e:
        raise Exception(f"Fehler beim Lesen der Datei '{filename}': {e}")
