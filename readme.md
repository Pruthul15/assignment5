# Advanced Calculator with Design Patterns

A command-line calculator application built with Python that uses advanced design patterns, pandas for data management, and comprehensive testing.

## What This Does

This calculator lets you do math operations through a command-line interface. It saves your calculation history, has undo/redo functionality, and uses several design patterns to make the code maintainable.

## Features

- Basic operations: add, subtract, multiply, divide, power, root
- Undo and redo your calculations 
- History management - see all your past calculations
- Auto-saves your work to CSV files
- Load and save history manually
- Configuration through environment variables
- Comprehensive error handling

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Pruthul15/assignment5.git
cd assignment5
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### 5. Run the Calculator
```bash
python main.py
```

## How to Use

When you start the calculator, you'll see:
```
Calculator started. Type 'help' for commands.
Enter command:
```

### Available Commands

- `add`, `subtract`, `multiply`, `divide`, `power`, `root` - Do math operations
- `history` - Show all your past calculations
- `clear` - Clear the calculation history
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation
- `save` - Save history to file
- `load` - Load history from file
- `help` - Show available commands
- `exit` - Exit the calculator

### Example Usage
```
Enter command: add
Enter numbers (or 'cancel' to abort):
First number: 5
Second number: 3
Result: 8

Enter command: multiply
Enter numbers (or 'cancel' to abort):
First number: 4
Second number: 7
Result: 28

Enter command: history
Calculation History:
1. Addition(5, 3) = 8
2. Multiplication(4, 7) = 28

Enter command: undo
Operation undone

Enter command: history
Calculation History:
1. Addition(5, 3) = 8
```

## Project Structure

```
assignment5/
├── app/
│   ├── __init__.py
│   ├── calculation.py          # Individual calculation logic
│   ├── calculator.py           # Main calculator class
│   ├── calculator_config.py    # Configuration management
│   ├── calculator_memento.py   # Undo/redo functionality
│   ├── calculator_repl.py      # Command-line interface
│   ├── exceptions.py           # Custom exceptions
│   ├── history.py              # History management and observers
│   ├── input_validators.py     # Input validation
│   └── operations.py           # Operation classes and factory
├── tests/
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl.py
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_operations.py
│   └── test_validators.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Design Patterns Used

- **Factory Pattern**: Creates operation objects based on user input
- **Observer Pattern**: Monitors calculation events for logging and auto-saving
- **Memento Pattern**: Saves calculator state for undo/redo functionality
- **Strategy Pattern**: Interchangeable operation execution strategies
- **Facade Pattern**: Simplified interface through the Calculator class

## Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

Current test coverage: **99%** with **171 tests**

## Configuration Options

You can customize the calculator through environment variables in the `.env` file:

- `CALCULATOR_MAX_HISTORY_SIZE` - Maximum number of calculations to keep in history
- `CALCULATOR_AUTO_SAVE` - Whether to automatically save history after each operation
- `CALCULATOR_DEFAULT_ENCODING` - Text encoding for file operations
- `CALCULATOR_PRECISION` - Decimal precision for results
- `CALCULATOR_MAX_INPUT_VALUE` - Maximum allowable input value

## Data Storage

The calculator uses pandas to manage calculation history:
- History is automatically saved to `history/calculator_history.csv`
- Each calculation includes operation, operands, result, and timestamp
- Data persists between sessions

## Error Handling

The calculator handles various error scenarios:
- Invalid input (non-numeric values)
- Division by zero
- Invalid operations
- File I/O errors
- Configuration errors

## Development

If you want to modify or extend the calculator:

1. All application code is in the `app/` directory
2. Tests are in the `tests/` directory
3. Follow the existing patterns for consistency
4. Add tests for any new functionality
5. Update this README if you add new features

## Requirements

- Python 3.x
- pandas
- pytest (for testing)
- python-dotenv (for environment variables)
i wqanted to push to git 