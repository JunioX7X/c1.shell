# C1Shell Compiler

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Descripción 📝

**C1Shell** es un compilador educativo escrito en Python que traduce un lenguaje de programación simple (similar a un shell básico) a código ensamblador. Soporta:

- Asignación de variables
- Operaciones aritméticas (`+`, `-`, `*`, `/`, `^`)
- Estructuras condicionales (`if`)
- Comparadores (`>`, `<`)
- Impresión de resultados y cadenas (`print`)

## Características ✨

- **Tokenización**: Analiza el código fuente y lo divide en tokens.
- **Parsing**: Valida la sintaxis del programa.
- **Generación de código**: Produce código ensamblador básico (pendiente de implementación completa).
- **Manejo de errores**: Mensajes detallados con línea y columna.

## Ejemplo de Uso 🚀

### Entrada (`input.c1sh`)
```c1shell
x = 10
y = x + 5 * 2
print(y)

if x > 5 [
    print("x es mayor que 5")
]

Compilación
python c1shell.py prueba-lexica.in prueba-lexica.out

Requisitos 📋
Python 3.x

Instalación 🔧
Clona el repositorio:

bash
git clone https://github.com/tu-usuario/c1shell.git
cd c1shell
Ejecuta el compilador:

bash
python c1shell.py <archivo_entrada> <archivo_salida>


Estructura del Código 🏗️
Tokenización: Clase Token y función tokenizer().

Parsing: Funciones parser(), stmt(), expr(), etc.

Generación de código: Funciones cg_*() (pendientes de implementar).
