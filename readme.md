# Advanced Calculator Application with Design Patterns

A sophisticated calculator application built with Python that integrates advanced design patterns, pandas for data management, and full test automation with GitHub Actions.

**Author:** Pruthul Patel  
**Repository:** https://github.com/Pruthul15/assignment5

## Features

- 6 arithmetic operations: add, subtract, multiply, divide, power, root
- Undo/redo functionality using Memento pattern
- History management with pandas DataFrames
- Auto-save to CSV files using Observer pattern
- Comprehensive error handling (LBYL and EAFP paradigms)
- Configuration through environment variables
- 100% test coverage with 171 tests

## Installation Instructions

### 1. Clone and Setup
```bash
git clone https://github.com/Pruthul15/assignment5.git
cd assignment5
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create Configuration File

Create a `.env` file in the project root:

```env
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### 3. Run the Calculator
```bash
python main.py
```

## Usage Guide

### Available Commands

**Operations:** `add`, `subtract`, `multiply`, `divide`, `power`, `root`  
**History:** `history`, `clear`, `save`, `load`  
**State:** `undo`, `redo`  
**Utility:** `help`, `exit`

### Example Session

```
Enter command: add
First number: 15
Second number: 7
Result: 22

Enter command: power
First number: 2
Second number: 8
Result: 256

Enter command: history
Calculation History:
1. Addition(15, 7) = 22
2. Power(2, 8) = 256

Enter command: undo
Operation undone

Enter command: exit
History saved successfully.
```

## Project Structure

```
assignment5/
├── .github/
│   └── workflows/
│       └── python-app.yml      # GitHub Actions CI/CD configuration
├── app/
│   ├── __init__.py
│   ├── calculation.py          # Calculation value object
│   ├── calculator.py           # Main calculator facade
│   ├── calculator_config.py    # Configuration management
│   ├── calculator_memento.py   # Memento pattern for undo/redo
│   ├── calculator_repl.py      # REPL command-line interface
│   ├── exceptions.py           # Custom exception classes
│   ├── history.py              # Observer pattern for history
│   ├── input_validators.py     # Input validation (LBYL approach)
│   └── operations.py           # Strategy & Factory patterns
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py     # Calculation class tests
│   ├── test_calculator.py      # Calculator tests
│   ├── test_calculator_memento.py  # Memento pattern tests
│   ├── test_calculator_repl.py # REPL interface tests
│   ├── test_config.py          # Configuration tests
│   ├── test_exceptions.py      # Exception handling tests
│   ├── test_history.py         # History observer tests
│   ├── test_operations.py      # Operation tests
│   └── test_validators.py      # Input validation tests
├── history/                     # Auto-created for history CSV files
├── logs/                        # Auto-created for log files
├── .env                         # Environment variables (not in repo)
├── .gitignore
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Design Patterns

1. **Factory Pattern** (`operations.py`): Dynamic operation creation
2. **Observer Pattern** (`history.py`): Auto-save on calculations
3. **Memento Pattern** (`calculator_memento.py`): Undo/redo state management
4. **Strategy Pattern** (`operations.py`): Interchangeable operations
5. **Facade Pattern** (`calculator.py`): Simplified interface

## Error Handling

The application demonstrates both LBYL and EAFP error handling paradigms:

**LBYL (Look Before You Leap):** Validates conditions before execution
```python
"Division": lambda x, y: x / y if y != 0 else self._raise_div_zero()
```

**EAFP (Easier to Ask Forgiveness than Permission):** Try/catch approach
```python
try:
    result = self.operation_strategy.execute(a, b)
except ValidationError as e:
    logging.error(f"Validation error: {str(e)}")
```

### Error Examples

**Division by Zero:**
```
Enter command: divide
First number: 10
Second number: 0
Error: Division by zero is not allowed
```

**Invalid Input:**
```
Enter command: add
First number: abc
Second number: 5
Error: Invalid number format: abc
```

**Root of Negative Number:**
```
Enter command: root
First number: -25
Second number: 2
Error: Cannot calculate root of negative number
```

**Zero Root (Undefined):**
```
Enter command: root
First number: 16
Second number: 0
Error: Zero root is undefined
```

**Negative Exponent:**
```
Enter command: power
First number: 2
Second number: -3
Error: Negative exponents not supported
```

**Unknown Command:**
```
Enter command: xyz
Unknown command: 'xyz'. Type 'help' for available commands.
```

## Testing

### Run Tests
```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=app tests/         # With coverage report
```

### Test Coverage
- **Total Tests:** 171
- **Coverage:** 100%
- **Test Files:** 9 comprehensive test modules

## CI/CD with GitHub Actions

Automated testing runs on every push:
1. Sets up Python 3.12 environment
2. Installs dependencies
3. Runs full test suite with coverage
4. **Fails if coverage < 100%**

View workflow: `.github/workflows/python-app.yml`

Check status: https://github.com/Pruthul15/assignment5/actions

## Data Management with pandas

- History stored in pandas DataFrame
- Auto-saves to CSV: `history/calculator_history.csv`
- Preserves operations, operands, results, timestamps
- Load/save functionality for persistence

## Configuration Options

Set in `.env` file:
- `CALCULATOR_MAX_HISTORY_SIZE`: Max history entries (default: 100)
- `CALCULATOR_AUTO_SAVE`: Auto-save after operations (true/false)
- `CALCULATOR_PRECISION`: Decimal precision (default: 10)
- `CALCULATOR_MAX_INPUT_VALUE`: Max input allowed (default: 1000000)

## Requirements

- Python 3.12
- pandas
- python-dotenv
- pytest
- pytest-cov

## Author

**Pruthul Patel**  
IS 601 - Module 5 Assignment