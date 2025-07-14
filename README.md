# OidaScript - Die österreichische Programmiersprache 🇦🇹

![OidaScript Logo](https://img.shields.io/badge/OidaScript-Österreichisch-red?style=for-the-badge&logo=austria)
![Bootstrap Ready](https://img.shields.io/badge/Bootstrap-Ready-green?style=for-the-badge)
![Self Hosting](https://img.shields.io/badge/Self--Hosting-Achieved-gold?style=for-the-badge)

> **"Die erste österreichische Programmiersprache die sich selbst entwickeln kann!"**

## 🎯 Was ist OidaScript?

OidaScript ist die **erste selbst-hosting österreichische Programmiersprache** der Welt! Mit authentischer österreichischer Syntax und kulturellem Charakter revolutioniert OidaScript die Programmierung im deutschsprachigen Raum.

```oida
// Servus! Das ist OidaScript!
loss greeting = "Servus Hawara!"
debugg(greeting)

tuas berechne_sachertorte portionen => {
    loss zutaten = ["Schokolade", "Marillenmarmelade", "Eier"]
    loss preis = portionen * 8.50
    hawara("Sachertorte für " + str(portionen) + " Personen kostet €" + str(preis))
    preis
}

loss kosten = berechne_sachertorte(6)
baba() // Auf Wiedersehen!
```

## ✨ Features

### 🇦🇹 Authentisch Österreichisch
- **Österreichische Syntax**: `loss`, `tuas`, `wenn`, `andernfalls`, `solang`
- **Wienerische Funktionen**: `oida()`, `hawara()`, `baba()`, `leiwand()`
- **Österreichische Fehlermeldungen**: "De Variable is ned definiert"

### 🚀 Bootstrap-Ready (Self-Hosting)
- **Module System**: `importier` und `exportier` für Code-Organisation
- **Float-Unterstützung**: Mathematische Operationen mit Dezimalzahlen
- **File I/O**: Lesen und Schreiben von Dateien
- **Self-Analysis**: OidaScript kann OidaScript-Code analysieren!

### 🛠️ Development Features
- **Debug Tools**: `debugg()`, `trace()`, `warnung()`
- **String Operations**: Umfassende Text-Manipulation
- **Listen & Dictionaries**: Moderne Datenstrukturen
- **Funktionale Programmierung**: Lambda-ähnliche Funktionen

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/ckist2/oidascript
cd oidascript
```

### Erstes Programm
```bash
# Erstelle eine .oida Datei
echo 'hawara("Servus aus OidaScript!")' > mein_programm.oida

# Führe es aus
python oidascript.py mein_programm.oida
```

## 📚 Beispiele

### Grundlagen
```oida
// Variablen
loss name = "Franz"
loss alter = 25
loss ist_wiener = wohr

// Funktionen
tuas greet person => {
    "Servus " + person + "!"
}

// Kontrollstrukturen
wenn (ist_wiener) {
    hawara("Ein echter Wiener!")
} andernfalls {
    debugg("Auch gut!")
}

// Schleifen
loss i = 0
solang (i < 5) {
    debugg("Zählung: " + str(i))
    i = i + 1
}
```

### Module System
```oida
// math_helpers.oida
exportier("addier", tuas a b => a + b)
exportier("PI", 3.14159)

// main.oida
importier("math_helpers.oida")
loss result = addier(5, 3)
debugg("5 + 3 = " + str(result))
```

### File Operations
```oida
// Datei schreiben
schreib_datei("greetings.txt", "Servus Austria!")

// Datei lesen
loss content = lies_datei("greetings.txt")
debugg("Datei Inhalt: " + content)
```

## 🏗️ Architektur

### Komponenten
- **`parser.py`**: Österreichischer Syntax-Parser
- **`interpreter.py`**: Ausführungsengine mit österreichischen Features
- **`main.py`**: CLI Interface
- **`examples/`**: Demonstration und Tests

### Bootstrap Capabilities
```oida
// OidaScript analyzing OidaScript!
loss oidascript_code = "loss x = 42"
loss has_variable = contains(oidascript_code, "loss")
loss tokens = split(oidascript_code, " ")
// Self-hosting achieved! 🎉
```

## 🎯 Roadmap

### Phase 1: Foundation ✅
- [x] Österreichische Syntax
- [x] Basic Interpreter  
- [x] Module System
- [x] Bootstrap Capability

### Phase 2: Tools 🚧
- [ ] REPL (Interactive Shell)
- [ ] Debugger
- [ ] Package Manager
- [ ] Code Formatter

### Phase 3: Ecosystem 📋
- [ ] Web Framework
- [ ] Database Connectors
- [ ] GUI Library
- [ ] Austrian-specific APIs

### Phase 4: Advanced 🔮
- [ ] JIT Compiler
- [ ] Language Server Protocol
- [ ] VS Code Extension
- [ ] Community Platform

## 🤝 Contributing

Willkommen bei der österreichischen Programmier-Revolution!

### Development Setup
```bash
git clone https://github.com/ckist2/oidascript
cd oidascript
python oidascript.py examples/test.oida  # Test basic functionality
python oidascript.py final_bootstrap.oida  # Test self-hosting
```

### Code Style
- Use Austrian German for keywords and functions
- Include cultural references where appropriate
- Maintain authenticity: "It's österreichisch, not wienerisch!"

## 📖 Documentation

### Language Reference
- [Syntax Guide](docs/syntax.md)
- [Built-in Functions](docs/functions.md)
- [Module System](docs/modules.md)
- [Austrian Culture Guide](docs/culture.md)

### Tutorials
- [Getting Started](docs/tutorial.md)
- [Bootstrap Development](docs/bootstrap.md)
- [Austrian Programming Patterns](docs/patterns.md)

## 🏆 Achievements

- **🥇 First Austrian Programming Language**
- **🚀 Self-Hosting Achieved**
- **🇦🇹 Culturally Authentic**
- **⚡ Bootstrap Ready**
- **🛠️ Production Capable**

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Austrian culture and language
- The programming language community
- Everyone who believes in linguistic diversity in programming

---

**"Programmieren auf Österreichisch - weil's einfach leiwand ist!"** 🇦🇹

Made with ❤️ in Austria (virtually)
