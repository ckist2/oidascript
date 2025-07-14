# OidaScript Project Structure

```
oidascript/
├── README.md                 # Main project documentation
├── LICENSE                   # MIT License
├── package.json             # Project metadata
├── oidascript.py            # CLI interface
├── main.py                  # Legacy runner (use oidascript.py)
├── parser.py                # Austrian syntax parser
├── interpreter.py           # Execution engine
├── final_bootstrap.oida     # Bootstrap demonstration
├── LAUNCH.md               # Launch announcement
├── LAUNCH_CHECKLIST.md     # Launch verification
├── docs/
│   └── syntax.md           # Complete syntax guide
└── examples/
    ├── sauber.oida         # Simple demo program
    ├── test.oida           # Comprehensive feature test
    └── math_helpers.oida   # Module system example
```

## Core Files

### Essential Runtime
- `oidascript.py` - **Main CLI** (use this!)
- `parser.py` - Austrian syntax parser
- `interpreter.py` - Execution engine

### Documentation  
- `README.md` - Complete project overview
- `docs/syntax.md` - Language reference
- `LICENSE` - MIT License

### Examples
- `examples/sauber.oida` - Simple demo
- `examples/test.oida` - Full feature showcase  
- `examples/math_helpers.oida` - Module example

### Demonstrations
- `final_bootstrap.oida` - Self-hosting proof

## Usage

```bash
# Run programs
python oidascript.py examples/sauber.oida

# Show help
python oidascript.py --help

# Test bootstrap
python oidascript.py --bootstrap

# Run demo  
python oidascript.py --demo
```

**Clean, production-ready Austrian programming language! 🇦🇹**
