########################
# Calculator Tests - Fixed with Proper Test Isolation
########################

import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

# Fixture to initialize Calculator with a temporary directory for file paths
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch properties to use the temporary directory paths
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file, \
             patch('app.calculator.Calculator.load_history') as mock_load:
            
            # Set return values to use paths within the temporary directory
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            # Return an instance of Calculator with the mocked config
            yield Calculator(config=config)

# ========================
# Original Professor Tests
# ========================

# Test Calculator Initialization
def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Test Logging Setup
@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        
        # Instantiate calculator to trigger logging
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

# Test Adding and Removing Observers
def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test Setting Operations
def test_set_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

# Test Performing Operations
def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(2, 3)
    assert result == Decimal('5')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 3)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

# Test Undo/Redo Functionality
def test_undo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

# Test History Management
@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

# FIXED: Load History Test with Proper Isolation
def test_load_history():
    """Test load_history functionality with proper mocking."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        # Create calculator without loading existing history
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Now test the actual load_history method
        mock_data = pd.DataFrame({
            'operation': ['Addition'],
            'operand1': ['2'],
            'operand2': ['3'],
            'result': ['5'],
            'timestamp': [datetime.datetime.now().isoformat()]
        })
        
        with patch('app.calculator.pd.read_csv', return_value=mock_data), \
             patch('app.calculator.Path.exists', return_value=True):
            calculator.load_history()
            assert len(calculator.history) == 1
            assert calculator.history[0].operation == "Addition"
        
# Test Clearing History
def test_clear_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

# Test REPL Commands (using patches for input/output handling)
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")

# ========================
# Enhanced Coverage Tests - FIXED with Proper Isolation
# ========================

# Test Logging Setup Error Handling - Lines 103-106
@patch('app.calculator.os.makedirs', side_effect=PermissionError("Cannot create directory"))
def test_logging_setup_error(mock_makedirs):
    """Test logging setup when directory creation fails - Lines 103-106."""
    with pytest.raises(PermissionError):
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir:
            mock_log_dir.return_value = Path('/invalid/path/logs')
            Calculator(CalculatorConfig())

@patch('app.calculator.logging.basicConfig', side_effect=Exception("Logging setup failed"))
def test_logging_configuration_error(mock_logging):
    """Test logging configuration error handling - Lines 103-106."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        with pytest.raises(Exception, match="Logging setup failed"):
            Calculator(config=config)

# Test Load History Error Handling - Lines 219
@patch('app.calculator.pd.read_csv', side_effect=Exception("CSV read error"))
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history_csv_error(mock_exists, mock_read_csv):
    """Test load history when CSV reading fails - Line 219."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        with pytest.raises(OperationError, match="Failed to load history"):
            calculator.load_history()

# Test Save History Error Handling - Lines 230-233
@patch('app.calculator.pd.DataFrame.to_csv', side_effect=Exception("CSV write error"))
def test_save_history_csv_error(mock_to_csv):
    """Test save history when CSV writing fails - Lines 230-233."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Add some history
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        calculator.perform_operation(2, 3)
        
        with pytest.raises(OperationError, match="Failed to save history"):
            calculator.save_history()

# FIXED: Test that covers the missing line 344 specifically  
def test_get_history_dataframe_specific_coverage():
    """Test get_history_dataframe method to hit line 344 specifically."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        # Mock load_history to prevent loading existing data
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
            
            # Create calculation with custom timestamp to test dataframe conversion
            operation = OperationFactory.create_operation('add')
            calculator.set_operation(operation)
            calculator.perform_operation(2, 3)
            
            # Get dataframe and verify specific timestamp conversion (line 344)
            df = calculator.get_history_dataframe()
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 1
            assert 'timestamp' in df.columns
            # Verify timestamp is properly converted (this hits line 344)
            assert isinstance(df.iloc[0]['timestamp'], datetime.datetime)

# FIXED: Test History Size Limit - Lines 268-275
def test_history_size_limit():
    """Test history respects maximum size limit - Lines 268-275."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        config.max_history_size = 2  # Set small limit for testing
        
        # Create calculator without loading existing history
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        
        # Add calculations beyond the limit
        calculator.perform_operation(1, 1)
        calculator.perform_operation(2, 2)
        calculator.perform_operation(3, 3)  # This should trigger history trimming
        
        # History should not exceed max size
        assert len(calculator.history) <= config.max_history_size
        # Should keep the most recent calculations
        assert calculator.history[-1].operand1 == Decimal("3")

# Test Perform Operation Error Handling - Lines 305, 309-312
@patch('app.calculator.InputValidator.validate_number', side_effect=ValidationError("Invalid number"))
def test_perform_operation_validation_logging(mock_validate):
    """Test validation error logging in perform_operation - Line 305."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        
        with pytest.raises(ValidationError):
            calculator.perform_operation("invalid", "also_invalid")

@patch('app.calculator.InputValidator.validate_number', side_effect=RuntimeError("Unexpected error"))
def test_perform_operation_unexpected_error(mock_validate):
    """Test unexpected error handling in perform_operation - Lines 309-312."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        
        with pytest.raises(OperationError, match="Operation failed"):
            calculator.perform_operation("1", "2")

# Test Calculator Initialization Error - Lines 324-333
@patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed"))
def test_calculator_initialization_load_error(mock_load):
    """Test calculator initialization when load_history fails - Lines 324-333."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        # Should not raise exception, just log warning
        calculator = Calculator(config=config)
        assert calculator is not None

# FIXED: Test Get History DataFrame - Line 344
def test_get_history_dataframe():
    """Test get_history_dataframe method - Line 344."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        # Create calculator without loading existing history
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Add some calculations
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        calculator.perform_operation(2, 3)
        calculator.perform_operation(4, 5)
        
        df = calculator.get_history_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'operation' in df.columns
        assert 'operand1' in df.columns
        assert 'operand2' in df.columns
        assert 'result' in df.columns
        assert 'timestamp' in df.columns

# FIXED: Test Get History DataFrame Empty
def test_get_history_dataframe_empty():
    """Test get_history_dataframe with empty history - Line 344."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        # Create calculator without loading existing history
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        df = calculator.get_history_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

# Test Undo/Redo Edge Cases - Lines 371, 390
def test_undo_empty_stack():
    """Test undo when undo stack is empty - Line 371."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Try to undo with no operations
        result = calculator.undo()
        assert result is False

def test_redo_empty_stack():
    """Test redo when redo stack is empty - Line 390."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Try to redo with no undone operations
        result = calculator.redo()
        assert result is False

# FIXED: Test Undo/Redo Sequence
def test_undo_redo_sequence():
    """Test complete undo/redo sequence."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        # Create calculator without loading existing history  
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        
        # Perform operations
        calculator.perform_operation(1, 1)
        calculator.perform_operation(2, 2)
        
        assert len(calculator.history) == 2
        
        # Undo operations
        assert calculator.undo() is True
        assert len(calculator.history) == 1
        
        assert calculator.undo() is True
        assert len(calculator.history) == 0
        
        # Try to undo when stack is empty
        assert calculator.undo() is False
        
        # Redo operations
        assert calculator.redo() is True
        assert len(calculator.history) == 1
        
        assert calculator.redo() is True
        assert len(calculator.history) == 2
        
        # Try to redo when stack is empty
        assert calculator.redo() is False

# Test Load History with Empty File
@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history_empty_file(mock_exists, mock_read_csv):
    """Test loading history from empty CSV file."""
    # Mock empty DataFrame
    mock_read_csv.return_value = pd.DataFrame()
    
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        calculator.load_history()
        assert len(calculator.history) == 0

# Test Load History File Not Exists
@patch('app.calculator.Path.exists', return_value=False)
def test_load_history_file_not_exists(mock_exists):
    """Test loading history when file doesn't exist."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        calculator.load_history()  # Should not raise exception
        assert len(calculator.history) == 0

# Test Save History with Empty History
def test_save_history_empty():
    """Test saving empty history creates proper CSV structure."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        calculator.save_history()  # Should not raise exception
        
        # Verify file was created
        assert config.history_file.exists()

# Test Observer Notification
def test_observer_notification():
    """Test that observers are properly notified of calculations."""
    with TemporaryDirectory() as temp_dir:
        config = CalculatorConfig(base_dir=Path(temp_dir))
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=config)
        
        # Create mock observer
        mock_observer = Mock()
        calculator.add_observer(mock_observer)
        
        operation = OperationFactory.create_operation('add')
        calculator.set_operation(operation)
        calculator.perform_operation(2, 3)
        
        # Verify observer was notified
        mock_observer.update.assert_called_once()

# Test Calculator with Custom Config
def test_calculator_with_custom_config():
    """Test calculator initialization with custom configuration."""
    with TemporaryDirectory() as temp_dir:
        custom_config = CalculatorConfig(base_dir=Path(temp_dir))
        custom_config.max_history_size = 50
        
        with patch('app.calculator.Calculator.load_history'):
            calculator = Calculator(config=custom_config)
        
        assert calculator.config.max_history_size == 50
        assert calculator.config.base_dir == Path(temp_dir)

# Test Calculator Default Config
def test_calculator_default_config():
    """Test calculator initialization with default configuration."""
    calculator = Calculator()  # No config provided
    
    assert calculator.config is not None
    assert hasattr(calculator.config, 'max_history_size')
    assert hasattr(calculator.config, 'base_dir')