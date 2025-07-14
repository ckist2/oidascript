# OidaScript Syntax Guide 🇦🇹

## Grundlagen (Basics)

### Variablen (Variables)
```oida
// Variable declaration
loss name = "Franz"
loss alter = 25
loss preis = 12.50
loss ist_aktiv = wohr
loss ist_inaktiv = falsch
```

### Kommentare (Comments)
```oida
// Das ist ein Kommentar
// This is a comment

// Mehrere Zeilen:
// Das ist Zeile 1
// Das ist Zeile 2
```

### Datentypen (Data Types)

#### Strings
```oida
loss greeting = "Servus!"
loss name = 'Franz'
loss message = "Servus " + name + "!"
```

#### Zahlen (Numbers)
```oida
// Ganzzahlen (Integers)
loss count = 42
loss negative = -15

// Dezimalzahlen (Floats)
loss pi = 3.14159
loss temperature = -5.5
```

#### Booleans
```oida
loss ist_wahr = wohr     // true
loss ist_falsch = falsch // false
```

#### Listen (Lists)
```oida
loss cities = ["Wien", "Graz", "Salzburg"]
loss numbers = [1, 2, 3, 4, 5]
loss mixed = ["Text", 42, wohr]

// Zugriff (Access)
loss first_city = cities[0]  // "Wien"
loss second_number = numbers[1]  // 2
```

#### Dictionaries
```oida
loss person = {
    "name": "Franz",
    "alter": 30,
    "stadt": "Wien"
}

// Zugriff
loss name = person["name"]
```

## Funktionen (Functions)

### Funktions-Definition
```oida
// Einfache Funktion
tuas greet => {
    "Servus!"
}

// Funktion mit Parametern
tuas greet_person name => {
    "Servus " + name + "!"
}

// Funktion mit mehreren Parametern
tuas berechne_preis menge preis_pro_stueck => {
    menge * preis_pro_stueck
}

// Funktion mit lokalen Variablen
tuas komplexe_berechnung x y => {
    loss zwischenergebnis = x * 2
    loss ergebnis = zwischenergebnis + y
    ergebnis
}
```

### Funktions-Aufrufe
```oida
loss greeting = greet()
loss personal_greeting = greet_person("Maria")
loss total_cost = berechne_preis(5, 12.50)
```

## Kontrollstrukturen (Control Structures)

### Bedingungen (Conditionals)
```oida
// Einfache if-Anweisung
wenn (alter >= 18) {
    debugg("Volljährig!")
}

// if-else
wenn (ist_wiener) {
    hawara("Ein echter Wiener!")
} andernfalls {
    debugg("Auch schön!")
}

// Verschachtelte Bedingungen
wenn (alter >= 65) {
    debugg("Pensionist")
} andernfalls wenn (alter >= 18) {
    debugg("Erwachsen")
} andernfalls {
    debugg("Minderjährig")
}
```

### Vergleichsoperatoren
```oida
// Gleichheit
wenn (name == "Franz") { ... }
wenn (alter != 25) { ... }

// Größer/Kleiner
wenn (preis > 100) { ... }
wenn (count < 10) { ... }
wenn (score >= 50) { ... }
wenn (temperature <= 0) { ... }

// Logische Operatoren
wenn (ist_aktiv und alter >= 18) { ... }
wenn (ist_student oda ist_pensionist) { ... }
wenn (ned ist_gesperrt) { ... }
```

### Schleifen (Loops)
```oida
// While-Schleife
loss i = 0
solang (i < 10) {
    debugg("Zählung: " + str(i))
    i = i + 1
}

// Schleife mit Bedingung
loss running = wohr
solang (running) {
    // Code hier
    running = falsch  // Schleife beenden
}
```

## Operatoren (Operators)

### Arithmetische Operatoren
```oida
loss addition = 5 + 3      // 8
loss subtraktion = 10 - 4  // 6
loss multiplikation = 6 * 7 // 42
loss division = 15 / 3     // 5

// Mit Variablen
loss a = 10
loss b = 5
loss summe = a + b
```

### String-Operationen
```oida
loss vor_name = "Franz"
loss nach_name = "Mueller"
loss full_name = vor_name + " " + nach_name

// String-Funktionen
loss length = len("Servus")
loss upper = obazieh("servus")     // "SERVUS"
loss lower = untazieh("SERVUS")    // "servus"
loss trimmed = zammrauma("  text  ") // "text"
```

## Module System

### Exportieren
```oida
// math_helpers.oida
exportier("addier", tuas a b => a + b)
exportier("PI", 3.14159)
exportier("kreis_flaeche", tuas radius => PI * radius * radius)
```

### Importieren
```oida
// main.oida
importier("math_helpers.oida")

loss summe = addier(5, 3)
loss flaeche = kreis_flaeche(10)
```

## Built-in Funktionen

### Debug & Output
```oida
debugg("Debug message")
trace("Trace information")
warnung("Warning message")
hawara("Servus Hawara!")
oida("Oida! Something happened!")
baba()  // Goodbye message
```

### String-Manipulation
```oida
loss words = aufteila("Wien,Graz,Salzburg", ",")
loss joined = zammfug(words, " - ")
loss substring = rausschneid("Servus", 0, 4)  // "Serv"
loss replaced = austausch("Servus Welt", "Welt", "Austria")
```

### Type Checking
```oida
loss is_text = is_string("Servus")
loss is_number = is_numma(42)
loss is_list = is_listn([1, 2, 3])
loss is_function = is_funktion(greet)
```

### File Operations
```oida
// Datei schreiben
schreib_datei("test.txt", "Servus Austria!")

// Datei lesen
loss content = lies_datei("test.txt")

// Aktueller Pfad
loss current_path = hol_aktueller_pfad()
```

## Österreichische Besonderheiten

### Kulturelle Funktionen
```oida
oida("Das ist ja unglaublich!")     // Austrian exclamation
hawara("Servus mein Freund!")       // Greeting
baba()                              // Goodbye
leiwand(5, 10, 3)                   // Returns max value (10)
```

### Österreichische Begriffe
- `loss` = let/var (variable declaration)
- `tuas` = function (function definition)  
- `wenn` = if
- `andernfalls` = else
- `solang` = while
- `wohr` = true
- `falsch` = false
- `ned` = not
- `und` = and
- `oda` = or

### Authentizität
> **Wichtig**: Es ist "österreichisch", nicht "wienerisch"!
> OidaScript repräsentiert ganz Österreich, nicht nur Wien.

## Beispiel-Programme

### Einfaches Programm
```oida
loss name = "Maria"
loss greeting = "Servus " + name + "!"
hawara(greeting)
```

### Funktion mit Berechnung
```oida
tuas berechne_sachertorte portionen => {
    loss basis_preis = 8.50
    loss gesamt_preis = portionen * basis_preis
    gesamt_preis
}

loss kosten = berechne_sachertorte(4)
debugg("Sachertorte für 4 Personen: €" + str(kosten))
```

### Schleife mit Liste
```oida
loss staedte = ["Wien", "Graz", "Salzburg", "Innsbruck"]
loss i = 0

solang (i < len(staedte)) {
    loss stadt = staedte[i]
    debugg("Stadt " + str(i + 1) + ": " + stadt)
    i = i + 1
}
```
