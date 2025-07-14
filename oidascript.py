#!/usr/bin/env python3
"""
OidaScript - Die österreichische Programmiersprache
Command Line Interface for the Austrian Programming Language

Usage:
    oidascript <file.oida>        # Run OidaScript file
    oidascript --version          # Show version
    oidascript --help             # Show help
    oidascript --demo             # Run demo
    oidascript --bootstrap        # Test bootstrap capabilities
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_file
from interpreter import run_code

VERSION = "1.0.0"
BANNER = """
🇦🇹 OidaScript v{version} - Die österreichische Programmiersprache
   Servus! Welcome to Austrian Programming!
   
   "Programmieren auf Österreichisch - weil's einfach leiwand ist!"
""".format(version=VERSION)

def show_help():
    print(BANNER)
    print(__doc__)
    print("\nExamples:")
    print("  oidascript hello.oida           # Run your Austrian program")
    print("  oidascript --demo               # See OidaScript in action")
    print("  oidascript --bootstrap          # Test self-hosting capabilities")
    print("\nFile Extensions:")
    print("  .oida                           # OidaScript source files")
    print("\nWebsite: https://github.com/yourusername/oidascript")

def show_version():
    print(f"OidaScript {VERSION}")
    print("Die erste österreichische Programmiersprache")

def run_demo():
    """Run the coffee shop demo"""
    demo_file = Path(__file__).parent / "examples" / "sauber.oida"
    if demo_file.exists():
        print("🇦🇹 Running OidaScript Demo - Coffee Shop Simulation...")
        print("=" * 60)
        try:
            ast = parse_file(str(demo_file))
            run_code(ast)
        except Exception as e:
            print(f"Demo error: {e}")
    else:
        print("Demo file not found. Please check examples/sauber.oida")

def run_bootstrap():
    """Test bootstrap capabilities"""
    bootstrap_file = Path(__file__).parent / "final_bootstrap.oida"
    if bootstrap_file.exists():
        print("🚀 Testing OidaScript Bootstrap Capabilities...")
        print("=" * 60)
        try:
            ast = parse_file(str(bootstrap_file))
            run_code(ast)
        except Exception as e:
            print(f"Bootstrap error: {e}")
    else:
        print("Bootstrap file not found. Please check final_bootstrap.oida")

def main():
    if len(sys.argv) < 2:
        print("Error: No file specified.")
        print("Use 'oidascript --help' for usage information.")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg in ['--help', '-h']:
        show_help()
    elif arg in ['--version', '-v']:
        show_version()
    elif arg in ['--demo', '-d']:
        run_demo()
    elif arg in ['--bootstrap', '-b']:
        run_bootstrap()
    else:
        # Run the specified file
        if not os.path.exists(arg):
            print(f"Error: File '{arg}' not found.")
            sys.exit(1)
        
        if not arg.endswith('.oida'):
            print("Warning: File doesn't have .oida extension. Continuing anyway...")
        
        try:
            print(f"🇦🇹 Running {arg}...")
            print("-" * 40)
            ast = parse_file(arg)
            run_code(ast)
        except Exception as e:
            print(f"Fehler: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
