########################
# Calculator Memento Tests - Complete Coverage
########################

import datetime
from decimal import Decimal
import pytest
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation


class TestCalculatorMemento:
    """
    Test suite for CalculatorMemento class to achieve 100% coverage.
    
    Tests the Memento pattern implementation for undo/redo functionality,
    including state storage, serialization, and deserialization.
    """

    def test_memento_creation_empty_history(self):
        """Test creating memento with empty history."""
        empty_history = []
        memento = CalculatorMemento(history=empty_history)
        
        assert memento.history == []
        assert isinstance(memento.timestamp, datetime.datetime)

    def test_memento_creation_with_history(self):
        """Test creating memento with calculation history."""
        calc1 = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        calc2 = Calculation(
            operation="Subtraction",
            operand1=Decimal("10"),
            operand2=Decimal("4")
        )
        
        history = [calc1, calc2]
        memento = CalculatorMemento(history=history)
        
        assert len(memento.history) == 2
        assert memento.history[0] == calc1
        assert memento.history[1] == calc2

    def test_memento_custom_timestamp(self):
        """Test creating memento with custom timestamp."""
        custom_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
        history = []
        
        memento = CalculatorMemento(
            history=history,
            timestamp=custom_time
        )
        
        assert memento.timestamp == custom_time

    def test_to_dict_empty_history(self):
        """Test serialization of memento with empty history - Targets Line 34."""
        memento = CalculatorMemento(history=[])
        result_dict = memento.to_dict()
        
        assert 'history' in result_dict
        assert 'timestamp' in result_dict
        assert result_dict['history'] == []
        assert isinstance(result_dict['timestamp'], str)

    def test_to_dict_with_calculations(self):
        """Test serialization of memento with calculations - Targets Line 34."""
        calc = Calculation(
            operation="Multiplication",
            operand1=Decimal("4"),
            operand2=Decimal("5")
        )
        
        memento = CalculatorMemento(history=[calc])
        result_dict = memento.to_dict()
        
        assert len(result_dict['history']) == 1
        assert result_dict['history'][0]['operation'] == "Multiplication"
        assert result_dict['history'][0]['operand1'] == "4"
        assert result_dict['history'][0]['operand2'] == "5"

    def test_from_dict_empty_history(self):
        """Test deserialization of memento with empty history - Targets Line 53."""
        data = {
            'history': [],
            'timestamp': '2024-01-01T12:00:00'
        }
        
        memento = CalculatorMemento.from_dict(data)
        
        assert memento.history == []
        assert memento.timestamp == datetime.datetime(2024, 1, 1, 12, 0, 0)

    def test_from_dict_with_calculations(self):
        """Test deserialization of memento with calculations - Targets Line 53."""
        calc_data = {
            'operation': 'Division',
            'operand1': '15',
            'operand2': '3',
            'result': '5',
            'timestamp': '2024-01-01T10:00:00'
        }
        
        data = {
            'history': [calc_data],
            'timestamp': '2024-01-01T12:00:00'
        }
        
        memento = CalculatorMemento.from_dict(data)
        
        assert len(memento.history) == 1
        assert memento.history[0].operation == "Division"
        assert memento.history[0].operand1 == Decimal("15")
        assert memento.history[0].operand2 == Decimal("3")
        assert memento.history[0].result == Decimal("5")

    def test_round_trip_serialization(self):
        """Test serialization and deserialization round trip."""
        # Create original memento with calculations
        calc1 = Calculation(
            operation="Power",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        calc2 = Calculation(
            operation="Root",
            operand1=Decimal("8"),
            operand2=Decimal("3")
        )
        
        original_memento = CalculatorMemento(history=[calc1, calc2])
        
        # Serialize to dict
        serialized = original_memento.to_dict()
        
        # Deserialize back to memento
        restored_memento = CalculatorMemento.from_dict(serialized)
        
        # Verify restoration
        assert len(restored_memento.history) == 2
        assert restored_memento.history[0].operation == "Power"
        assert restored_memento.history[1].operation == "Root"
        assert restored_memento.timestamp == original_memento.timestamp

    def test_memento_history_reference(self):
        """Test that memento stores reference to history list."""
        original_calc = Calculation(
            operation="Addition",
            operand1=Decimal("1"),
            operand2=Decimal("1")
        )
        
        original_history = [original_calc]
        memento = CalculatorMemento(history=original_history)
        
        # Verify memento has the calculation
        assert len(memento.history) == 1
        assert memento.history[0].operation == "Addition"

    def test_multiple_mementos_different_timestamps(self):
        """Test creating multiple mementos have different timestamps."""
        import time
        
        memento1 = CalculatorMemento(history=[])
        time.sleep(0.001)  # Small delay to ensure different timestamps
        memento2 = CalculatorMemento(history=[])
        
        assert memento1.timestamp != memento2.timestamp
        assert memento1.timestamp < memento2.timestamp

    def test_memento_with_complex_calculations(self):
        """Test memento with various calculation types."""
        calculations = [
            Calculation("Addition", Decimal("1"), Decimal("2")),
            Calculation("Subtraction", Decimal("10"), Decimal("5")),
            Calculation("Multiplication", Decimal("3"), Decimal("4")),
            Calculation("Division", Decimal("20"), Decimal("4")),
            Calculation("Power", Decimal("2"), Decimal("4")),
        ]
        
        memento = CalculatorMemento(history=calculations)
        
        # Test serialization with complex history
        serialized = memento.to_dict()
        assert len(serialized['history']) == 5
        
        # Test deserialization
        restored = CalculatorMemento.from_dict(serialized)
        assert len(restored.history) == 5
        
        # Verify all operations preserved
        operations = [calc.operation for calc in restored.history]
        expected_ops = ["Addition", "Subtraction", "Multiplication", "Division", "Power"]
        assert operations == expected_ops

    def test_memento_timestamp_format(self):
        """Test timestamp is properly formatted in serialization."""
        memento = CalculatorMemento(history=[])
        serialized = memento.to_dict()
        
        # Should be ISO format string
        timestamp_str = serialized['timestamp']
        assert isinstance(timestamp_str, str)
        
        # Should be parseable back to datetime
        parsed_time = datetime.datetime.fromisoformat(timestamp_str)
        assert parsed_time == memento.timestamp