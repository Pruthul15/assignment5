########################
# REPL Tests - Comprehensive Coverage
########################

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError


class TestCalculatorREPL:
    """Test suite for calculator REPL functionality to achieve 100% coverage."""

    def test_help_command(self):
        """Test help command displays all available commands."""
        with patch('builtins.input', side_effect=['help', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    # Verify help text is displayed
                    mock_print.assert_any_call("\nAvailable commands:")
                    mock_print.assert_any_call("  add, subtract, multiply, divide, power, root - Perform calculations")
                    mock_print.assert_any_call("  history - Show calculation history")
                    mock_print.assert_any_call("  clear - Clear calculation history")
                    mock_print.assert_any_call("  undo - Undo the last calculation")
                    mock_print.assert_any_call("  redo - Redo the last undone calculation")
                    mock_print.assert_any_call("  save - Save calculation history to file")
                    mock_print.assert_any_call("  load - Load calculation history from file")
                    mock_print.assert_any_call("  exit - Exit the calculator")

    def test_exit_with_save_success(self):
        """Test normal exit with successful history save."""
        with patch('builtins.input', side_effect=['exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history') as mock_save:
                    calculator_repl()
                    
                    mock_save.assert_called_once()
                    mock_print.assert_any_call("History saved successfully.")
                    mock_print.assert_any_call("Goodbye!")

    def test_exit_with_save_error(self):
        """Test exit when save_history raises an exception - Line 54-55."""
        with patch('builtins.input', side_effect=['exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save error")):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Warning: Could not save history: Save error")
                    mock_print.assert_any_call("Goodbye!")

    def test_history_empty(self):
        """Test history command when no calculations exist."""
        with patch('builtins.input', side_effect=['history', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.show_history', return_value=[]):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("No calculations in history")

    def test_history_with_calculations(self):
        """Test history command when calculations exist."""
        mock_history = ["Addition(2, 3) = 5", "Subtraction(10, 4) = 6"]
        
        with patch('builtins.input', side_effect=['history', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.show_history', return_value=mock_history):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("\nCalculation History:")
                        mock_print.assert_any_call("1. Addition(2, 3) = 5")
                        mock_print.assert_any_call("2. Subtraction(10, 4) = 6")

    def test_clear_history(self):
        """Test clear history command."""
        with patch('builtins.input', side_effect=['clear', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.clear_history') as mock_clear:
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_clear.assert_called_once()
                        mock_print.assert_any_call("History cleared")

    def test_undo_success(self):
        """Test successful undo operation."""
        with patch('builtins.input', side_effect=['undo', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.undo', return_value=True):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Operation undone")

    def test_undo_nothing_to_undo(self):
        """Test undo when nothing to undo."""
        with patch('builtins.input', side_effect=['undo', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.undo', return_value=False):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Nothing to undo")

    def test_redo_success(self):
        """Test successful redo operation."""
        with patch('builtins.input', side_effect=['redo', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.redo', return_value=True):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Operation redone")

    def test_redo_nothing_to_redo(self):
        """Test redo when nothing to redo."""
        with patch('builtins.input', side_effect=['redo', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.redo', return_value=False):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Nothing to redo")

    def test_save_command_success(self):
        """Test save command successful execution."""
        with patch('builtins.input', side_effect=['save', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history') as mock_save:
                    calculator_repl()
                    
                    # save_history called twice: once for save command, once for exit
                    assert mock_save.call_count == 2
                    mock_print.assert_any_call("History saved successfully")

    def test_save_command_error(self):
        """Test save command when exception occurs - Lines 78-82."""
        with patch('builtins.input', side_effect=['save', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save failed")):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Error saving history: Save failed")

    def test_load_command_success(self):
        """Test load command successful execution."""
        with patch('builtins.input', side_effect=['load', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.load_history') as mock_load:
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        # load_history called twice: once during init, once for load command
                        assert mock_load.call_count == 2
                        mock_print.assert_any_call("History loaded successfully")

    def test_load_command_error(self):
        """Test load command when exception occurs - Lines 86-90."""
        with patch('builtins.input', side_effect=['load', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed")):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Error loading history: Load failed")

    def test_arithmetic_operation_success(self):
        """Test successful arithmetic operation."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('5')):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("\nResult: 5")

    def test_operation_cancel_first_number(self):
        """Test canceling operation at first number - Lines 116-117."""
        with patch('builtins.input', side_effect=['add', 'cancel', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Operation cancelled")

    def test_operation_cancel_second_number(self):
        """Test canceling operation at second number - Lines 120-121."""
        with patch('builtins.input', side_effect=['add', '2', 'cancel', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Operation cancelled")

    def test_operation_validation_error(self):
        """Test operation with validation error - Lines 103-108."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.perform_operation', side_effect=ValidationError("Invalid input")):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Error: Invalid input")

    def test_operation_operation_error(self):
        """Test operation with operation error - Lines 103-108."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.perform_operation', side_effect=OperationError("Operation failed")):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Error: Operation failed")

    def test_operation_unexpected_error(self):
        """Test operation with unexpected error - Lines 103-108."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.perform_operation', side_effect=RuntimeError("Unexpected error")):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        mock_print.assert_any_call("Unexpected error: Unexpected error")

    def test_unknown_command(self):
        """Test unknown command handling."""
        with patch('builtins.input', side_effect=['invalid_command', 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Unknown command: 'invalid_command'. Type 'help' for available commands.")

    def test_keyboard_interrupt(self):
        """Test KeyboardInterrupt (Ctrl+C) handling - Lines 135-140."""
        with patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    mock_print.assert_any_call("\nOperation cancelled")

    def test_eof_error(self):
        """Test EOFError (Ctrl+D) handling - Lines 144-163."""
        with patch('builtins.input', side_effect=[EOFError()]):
            with patch('builtins.print') as mock_print:
                calculator_repl()
                
                mock_print.assert_any_call("\nInput terminated. Exiting...")

    def test_unexpected_error_in_loop(self):
        """Test unexpected error in main loop - Lines 144-163."""
        with patch('builtins.input', side_effect=[RuntimeError("Unexpected"), 'exit']):
            with patch('builtins.print') as mock_print:
                with patch('app.calculator.Calculator.save_history'):
                    calculator_repl()
                    
                    mock_print.assert_any_call("Error: Unexpected")

    @patch('app.calculator_repl.logging.error')
    def test_fatal_initialization_error(self, mock_logging_error):
        """Test fatal error during initialization - Lines 154-163."""
        with patch('app.calculator_repl.Calculator', side_effect=Exception("Fatal init error")):
            with patch('builtins.print') as mock_print:
                with pytest.raises(Exception, match="Fatal init error"):
                    calculator_repl()
                    
                mock_print.assert_any_call("Fatal error: Fatal init error")
                mock_logging_error.assert_called_once()

    def test_all_arithmetic_operations(self):
        """Test all arithmetic operations for complete coverage."""
        operations = ['add', 'subtract', 'multiply', 'divide', 'power', 'root']
        
        for op in operations:
            with patch('builtins.input', side_effect=[op, '2', '3', 'exit']):
                with patch('builtins.print'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=1):
                        with patch('app.calculator.Calculator.save_history'):
                            calculator_repl()

    def test_decimal_result_normalization(self):
        """Test Decimal result normalization."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('builtins.print') as mock_print:
                # Return a Decimal that needs normalization
                mock_result = Decimal('5.000')
                with patch('app.calculator.Calculator.perform_operation', return_value=mock_result):
                    with patch('app.calculator.Calculator.save_history'):
                        calculator_repl()
                        
                        # Should normalize 5.000 to 5
                        mock_print.assert_any_call("\nResult: 5")