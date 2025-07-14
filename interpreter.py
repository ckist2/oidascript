# interpreter.py
import os
from pathlib import Path

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Fehler: De Variable '{name}' is ned definiert. Hast vielleicht an Tippfehler gmacht?")

    def set(self, name, value):
        self.vars[name] = value


class Interpreter:
    def __init__(self):
        self.env = Environment()
        self.returning = None  # Für return Statements
        self.exception = None  # Für Exception Handling

        # Eingebaute Funktionen (OidaScript)
        self.env.set("druck", print)
        self.env.set("hol_eingab", lambda: input("Oida, gib was ein> "))

        # Rechenoperatoren (gleiche Symbole)
        self.env.set("+", lambda a, b: str(a) + str(b) if isinstance(a, str) or isinstance(b, str) else a + b)
        self.env.set("-", lambda a, b: a - b)
        self.env.set("*", lambda a, b: a * b)
        self.env.set("/", lambda a, b: a / b)

        # Vergleichsoperatoren (gleiche Symbole)
        self.env.set(">", lambda a, b: a > b)
        self.env.set("<", lambda a, b: a < b)
        self.env.set("==", lambda a, b: a == b)
        self.env.set("!=", lambda a, b: a != b)
        self.env.set(">=", lambda a, b: a >= b)
        self.env.set("<=", lambda a, b: a <= b)

        # Logische Operatoren (OidaScript)
        self.env.set("und", lambda a, b: a and b)
        self.env.set("oda", lambda a, b: a or b)
        self.env.set("ned", lambda a: not a)

        # Boolean Werte (OidaScript)
        self.env.set("woahr", True)
        self.env.set("ned_woahr", False)

        # Listen Operationen (OidaScript)
        self.env.set("listn", lambda *args: list(args))
        self.env.set("dranhaeng", lambda lst, item: lst.append(item) or lst)
        self.env.set("hol", lambda obj, key: obj[key])
        self.env.set("setz", lambda obj, key, value: obj.__setitem__(key, value) or obj)
        self.env.set("laeng", len)

        # Dictionary Operationen (OidaScript)
        self.env.set("dict", lambda: {})
        self.env.set("schluessel", lambda d: list(d.keys()))
        self.env.set("werte", lambda d: list(d.values()))

        # Fehlerbehandlung Funktionen (OidaScript)
        self.env.set("schmeiss", lambda msg: self._throw_error(msg))
        self.env.set("fehler", lambda msg: RuntimeError(str(msg)))
        self.env.set("is_fehler", lambda obj: isinstance(obj, Exception))

        # Datei I/O Operationen (OidaScript)
        self.env.set("lies_datei", lambda filename: open(filename, 'r', encoding='utf-8').read())
        self.env.set("schreib_datei", lambda filename, content: open(filename, 'w', encoding='utf-8').write(content) or True)
        
        # Module System (OidaScript)
        self.env.set("importier", lambda filename: self._import_module(filename))
        self.env.set("hol_aktueller_pfad", lambda: os.getcwd())
        
        # Österreichische Hilfsfunktionen für Development
        self.env.set("debugg", lambda msg: print(f"🐛 Debug: {msg}"))
        self.env.set("trace", lambda msg: print(f"📍 Trace: {msg}"))
        self.env.set("warnung", lambda msg: print(f"⚠️  Warnung: {msg}"))
        
        # String Manipulation (OidaScript)
        self.env.set("aufteila", lambda text, delim: text.split(delim))
        self.env.set("zammfug", lambda lst, sep: sep.join(lst))
        self.env.set("rausschneid", lambda text, start, end: text[start:end])
        self.env.set("austausch", lambda text, old, new: text.replace(old, new))
        self.env.set("fangt_au", lambda text, prefix: text.startswith(prefix))
        self.env.set("endet_mit", lambda text, suffix: text.endswith(suffix))
        self.env.set("zammrauma", lambda text: text.strip())
        self.env.set("untazieh", lambda text: text.lower())
        self.env.set("obazieh", lambda text: text.upper())
        
        # Typ Checking (OidaScript)
        self.env.set("is_string", lambda obj: isinstance(obj, str))
        self.env.set("is_numma", lambda obj: isinstance(obj, (int, float)))
        self.env.set("is_listn", lambda obj: isinstance(obj, list))
        self.env.set("is_dict", lambda obj: isinstance(obj, dict))
        self.env.set("is_funktion", lambda obj: callable(obj))
        self.env.set("is_woahr", lambda obj: isinstance(obj, bool))
        
        # Typ Umwandlung (OidaScript)
        self.env.set("zu_string", lambda obj: str(obj))
        self.env.set("zu_int", lambda obj: int(obj))
        self.env.set("zu_float", lambda obj: float(obj))
        self.env.set("zu_woahr", lambda obj: bool(obj))
        
        # Hilfsfunktionen (OidaScript)
        self.env.set("reihe", lambda start, end: list(range(start, end)))
        self.env.set("minimum", lambda *args: min(args))
        self.env.set("maximum", lambda *args: max(args))
        self.env.set("betrag", lambda x: abs(x))
        self.env.set("rundung", lambda x: round(x))
        
        # Wienerische Hilfsfunktionen
        self.env.set("oida", lambda msg: print(f"Oida! {msg}"))  # Austrian exclamation
        self.env.set("leiwand", lambda *args: max(args))  # "awesome" -> max
        self.env.set("hawara", lambda msg: print(f"Servus Hawara! {msg}"))  # greeting
        self.env.set("baba", lambda: print("Baba und foi ned!"))  # goodbye
        self.env.set("pfiati", lambda: print("Pfiati!"))  # another goodbye
        
        # Bootstrap Parser Helper Functions
        self.env.set("len", lambda obj: len(obj) if hasattr(obj, '__len__') else 0)
        self.env.set("substring", lambda text, start, end: str(text)[start:end])
        self.env.set("append", lambda lst, item: (lst + [item]) if isinstance(lst, list) else [item])
        self.env.set("trim", lambda text: str(text).strip())
        self.env.set("split", lambda text, delim: str(text).split(str(delim)))
        self.env.set("int", lambda obj: int(obj) if obj else 0)
        self.env.set("float", lambda obj: float(obj) if obj else 0.0)
        self.env.set("str", lambda obj: str(obj) if obj is not None else "")
        self.env.set("startswith", lambda text, prefix: str(text).startswith(str(prefix)))
        self.env.set("endswith", lambda text, suffix: str(text).endswith(str(suffix)))
        self.env.set("contains", lambda text, search: str(search) in str(text))
        self.env.set("slice", lambda lst, start, end: lst[start:end] if isinstance(lst, list) else [])
        
        # Special values for bootstrap
        self.env.set("ned_definiert", None)
        self.env.set("wohr", True)
        self.env.set("falsch", False)

    def _import_module(self, filename):
        """Importiert a ander oidascript-Datei als Modul"""
        try:
            # Add .oida extension if not present
            if not filename.endswith('.oida'):
                filename += '.oida'
            
            # Try relative to current file first, then absolute
            if not os.path.isabs(filename):
                current_dir = os.getcwd()
                full_path = os.path.join(current_dir, filename)
                if not os.path.exists(full_path):
                    # Try in examples directory
                    examples_path = os.path.join(current_dir, 'examples', filename)
                    if os.path.exists(examples_path):
                        full_path = examples_path
            else:
                full_path = filename
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Modul '{filename}' ned gfunden")
            
            # Read and parse the module
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            from parser import parse
            module_ast = parse(lines)
            
            # Create new environment for module
            module_env = Environment(parent=self.env)
            old_env = self.env
            self.env = module_env
            
            try:
                # Execute module
                self.run(module_ast)
                # Return module's variables as dictionary
                return dict(module_env.vars)
            finally:
                self.env = old_env
                
        except Exception as e:
            raise RuntimeError(f"Fehler beim Importieren von '{filename}': {str(e)}")

    def _throw_error(self, message):
        """Schmeiss an Fehler der durch versuchs-fang Blöcke gfangt werdn kann"""
        self.exception = RuntimeError(str(message))
        return None

    def run(self, nodes):
        for node in nodes:
            result = self.eval(node)
            if self.returning is not None:
                return self.returning
            if self.exception is not None:
                return result
        return result

    def eval(self, node):
        if isinstance(node, (int, float, str)):
            return node
        
        if node is None:
            return None

        node_type = node.get("type")

        if node_type == "let":
            value = self.eval(node["value"])
            self.env.set(node["name"], value)

        elif node_type == "var":
            return self.env.get(node["name"])

        elif node_type == "call":
            func = self.env.get(node["name"])
            args = [self.eval(arg) for arg in node["args"]]
            return func(*args)

        elif node_type == "index":
            obj = self.eval(node["object"])
            index = self.eval(node["index"])
            if isinstance(obj, (list, str, dict)):
                return obj[index]
            else:
                raise TypeError(f"Fehler: Kann ned auf '{type(obj).__name__}' zugreifen. Nur Listen, Strings und Dicts san unterstützt.")

        elif node_type == "fn":
            # Capture the current environment for closure
            closure_env = self.env
            
            def fn_impl(*args):
                # Neue Umgebung mit Closure Environment als Parent erstellen
                local_env = Environment(parent=closure_env)
                for param, arg in zip(node["params"], args):
                    local_env.set(param, arg)

                # Aktuellen Interpreter mit neuer Umgebung verwenden
                old_env = self.env
                old_returning = self.returning
                self.env = local_env
                self.returning = None
                
                try:
                    result = self.run(node["body"])
                    return_value = self.returning
                finally:
                    # Originale Umgebung und returning state wiederherstellen
                    self.env = old_env
                    self.returning = old_returning
                
                return return_value

            self.env.set(node["name"], fn_impl)

        elif node_type == "return":
            self.returning = self.eval(node["value"])

        elif node_type == "if":
            condition = self.eval(node["cond"])
            if condition:
                return self.run(node["then"])
            else:
                return self.run(node["else"])
        
        elif node_type == "while":
            while self.eval(node["cond"]):
                result = self.run(node["body"])
                if self.returning is not None:
                    return result

        elif node_type == "list":
            return [self.eval(item) for item in node["items"]]

        elif node_type == "dict":
            result = {}
            for key_node, value_node in node["pairs"]:
                key = self.eval(key_node)
                value = self.eval(value_node)
                result[key] = value
            return result

        elif node_type == "index":
            obj = self.eval(node["object"])
            index = self.eval(node["index"])
            return obj[index]

        elif node_type == "lambda":
            # Aktuelle Umgebung für Closure erfassen
            closure_env = self.env
            
            def lambda_impl(*args):
                # Neue Umgebung mit Closure Environment als Parent erstellen
                local_env = Environment(parent=closure_env)
                for param, arg in zip(node["params"], args):
                    local_env.set(param, arg)

                # Aktuellen Interpreter mit neuer Umgebung verwenden
                old_env = self.env
                old_returning = self.returning
                self.env = local_env
                self.returning = None
                
                try:
                    result = self.eval(node["body"])
                    return_value = result  # Lambda gibt das Expressions-Ergebnis zurück
                finally:
                    # Originale Umgebung und returning state wiederherstellen
                    self.env = old_env
                    self.returning = old_returning
                
                return return_value
            
            return lambda_impl

        elif node_type == "try":
            # Try Block ausführen
            try:
                self.exception = None
                result = self.run(node["try_body"])
                
                # Wenn eine Exception durch throw() geworfen wurde, behandeln
                if self.exception:
                    if "catch_body" in node:
                        # Error Variable setzen falls angegeben
                        if "error_var" in node:
                            self.env.set(node["error_var"], str(self.exception))
                        
                        # Catch Block ausführen
                        self.exception = None
                        result = self.run(node["catch_body"])
                    else:
                        # Re-raise wenn kein catch block
                        raise self.exception
                
                return result
                
            except Exception as e:
                # Python Exceptions behandeln
                if "catch_body" in node:
                    # Error Variable setzen falls angegeben
                    if "error_var" in node:
                        self.env.set(node["error_var"], str(e))
                    
                    # Catch Block ausführen
                    self.exception = None
                    return self.run(node["catch_body"])
                else:
                    # Re-raise wenn kein catch block
                    raise e

        elif node_type == "throw":
            self.exception = RuntimeError(str(self.eval(node["message"])))
            return None

        else:
            raise Exception(f"SyntaxFehler: Den Knotn-Typ '{node_type}' kenn i ned. Is des vielleicht a Tippfehler?")


def run_code(ast):
    interpreter = Interpreter()
    interpreter.run(ast)
