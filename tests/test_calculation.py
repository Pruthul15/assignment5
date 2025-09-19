########################
# Calculation Tests - Complete Coverage Suite
########################

import datetime
from decimal import Decimal
import pytest
from app.calculation import Calculation
from app.exceptions import OperationError


class TestCalculation:
    """
    Test suite for the Calculation class to achieve comprehensive coverage.
    
    This test class covers all aspects of the Calculation model including:
    - Basic arithmetic operations (Addition, Subtraction, Multiplication, Division)
    - Advanced operations (Power, Root)
    - Error handling and edge cases
    - Data serialization and deserialization
    - String representations and formatting
    - Equality comparisons
    """

    # ========================
    # Basic Operation Tests
    # ========================

    def test_addition_calculation(self):
        """Test basic addition operation."""
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        assert calc.result == Decimal("5")
        assert calc.operation == "Addition"
        assert calc.operand1 == Decimal("2")
        assert calc.operand2 == Decimal("3")

    def test_subtraction_calculation(self):
        """Test basic subtraction operation."""
        calc = Calculation(
            operation="Subtraction",
            operand1=Decimal("10"),
            operand2=Decimal("4")
        )
        assert calc.result == Decimal("6")

    def test_multiplication_calculation(self):
        """Test basic multiplication operation."""
        calc = Calculation(
            operation="Multiplication",
            operand1=Decimal("6"),
            operand2=Decimal("7")
        )
        assert calc.result == Decimal("42")

    def test_division_calculation(self):
        """Test basic division operation."""
        calc = Calculation(
            operation="Division",
            operand1=Decimal("15"),
            operand2=Decimal("3")
        )
        assert calc.result == Decimal("5")

    def test_power_calculation(self):
        """Test power operation with positive exponent."""
        calc = Calculation(
            operation="Power",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        assert calc.result == Decimal("8")

    def test_root_calculation(self):
        """Test root operation with valid inputs."""
        calc = Calculation(
            operation="Root",
            operand1=Decimal("8"),
            operand2=Decimal("3")
        )
        # Cube root of 8 should be approximately 2
        assert abs(calc.result - Decimal("2")) < Decimal("0.0001")

    # ========================
    # Error Handling Tests - Target Missing Coverage Lines
    # ========================

    def test_division_by_zero_error(self):
        """Test division by zero raises appropriate error - Targets Line ~81."""
        with pytest.raises(OperationError, match="Division by zero is not allowed"):
            Calculation(
                operation="Division",
                operand1=Decimal("10"),
                operand2=Decimal("0")
            )

    def test_negative_power_error(self):
        """Test negative power raises appropriate error - Targets Line ~188."""
        with pytest.raises(OperationError, match="Negative exponents are not supported"):
            Calculation(
                operation="Power",
                operand1=Decimal("2"),
                operand2=Decimal("-3")
            )

    def test_root_of_negative_number_error(self):
        """Test root of negative number raises appropriate error - Targets Line ~200."""
        with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
            Calculation(
                operation="Root",
                operand1=Decimal("-4"),
                operand2=Decimal("2")
            )

    def test_zero_root_error(self):
        """Test zero root raises appropriate error - Targets Line ~200."""
        with pytest.raises(OperationError, match="Zero root is undefined"):
            Calculation(
                operation="Root",
                operand1=Decimal("4"),
                operand2=Decimal("0")
            )

    def test_unknown_operation_error(self):
        """Test unknown operation raises appropriate error."""
        with pytest.raises(OperationError, match="Unknown operation: InvalidOp"):
            calc = Calculation(
                operation="InvalidOp",
                operand1=Decimal("2"),
                operand2=Decimal("3")
            )

    # ========================
    # Serialization Tests - Target Missing Coverage Line ~222
    # ========================

    def test_to_dict_serialization(self):
        """Test conversion of calculation to dictionary format."""
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("5"),
            operand2=Decimal("3")
        )
        
        result_dict = calc.to_dict()
        
        assert result_dict['operation'] == "Addition"
        assert result_dict['operand1'] == "5"
        assert result_dict['operand2'] == "3"
        assert result_dict['result'] == "8"
        assert 'timestamp' in result_dict

    def test_from_dict_deserialization(self):
        """Test creation of calculation from dictionary."""
        data = {
            'operation': 'Multiplication',
            'operand1': '4',
            'operand2': '5',
            'result': '20',
            'timestamp': '2024-01-01T12:00:00'
        }
        
        calc = Calculation.from_dict(data)
        
        assert calc.operation == "Multiplication"
        assert calc.operand1 == Decimal("4")
        assert calc.operand2 == Decimal("5")
        assert calc.result == Decimal("20")

    def test_from_dict_missing_key_error(self):
        """Test from_dict with missing required key raises error - Targets Line ~222."""
        invalid_data = {
            'operation': 'Addition',
            # Missing 'operand1' key
            'operand2': '3',
            'result': '5',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        with pytest.raises(OperationError, match="Invalid calculation data"):
            Calculation.from_dict(invalid_data)

    def test_from_dict_invalid_decimal_error(self):
        """Test from_dict with invalid decimal raises error - Targets Line ~222."""
        invalid_data = {
            'operation': 'Addition',
            'operand1': 'not_a_number',  # Invalid decimal
            'operand2': '3',
            'result': '5',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        with pytest.raises(OperationError, match="Invalid calculation data"):
            Calculation.from_dict(invalid_data)

    def test_from_dict_invalid_timestamp_error(self):
        """Test from_dict with invalid timestamp format raises error."""
        invalid_data = {
            'operation': 'Addition',
            'operand1': '2',
            'operand2': '3',
            'result': '5',
            'timestamp': 'invalid_timestamp_format'
        }
        
        with pytest.raises(OperationError, match="Invalid calculation data"):
            Calculation.from_dict(invalid_data)

    # ========================
    # String Representation Tests
    # ========================

    def test_string_representation(self):
        """Test __str__ method returns properly formatted string."""
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("7"),
            operand2=Decimal("3")
        )
        
        expected = "Addition(7, 3) = 10"
        assert str(calc) == expected

    def test_detailed_representation(self):
        """Test __repr__ method returns detailed string representation."""
        calc = Calculation(
            operation="Subtraction",
            operand1=Decimal("10"),
            operand2=Decimal("4")
        )
        
        repr_str = repr(calc)
        assert "Calculation(operation='Subtraction'" in repr_str
        assert "operand1=10" in repr_str
        assert "operand2=4" in repr_str
        assert "result=6" in repr_str
        assert "timestamp=" in repr_str

    # ========================
    # Equality and Comparison Tests
    # ========================

    def test_equality_same_calculations(self):
        """Test equality comparison for identical calculations."""
        calc1 = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        
        calc2 = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        
        # Note: These won't be equal due to different timestamps
        # but we can test the logic by setting same timestamp
        calc2.timestamp = calc1.timestamp
        assert calc1 == calc2

    def test_equality_different_calculations(self):
        """Test equality comparison for different calculations."""
        calc1 = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        
        calc2 = Calculation(
            operation="Subtraction",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        
        assert calc1 != calc2

    def test_equality_with_non_calculation_object(self):
        """Test equality comparison with non-Calculation object."""
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
        
        assert calc != "not a calculation"
        assert calc != 42
        assert calc != None

    # ========================
    # Result Formatting Tests
    # ========================

    def test_format_result_default_precision(self):
        """Test result formatting with default precision."""
        calc = Calculation(
            operation="Division",
            operand1=Decimal("10"),
            operand2=Decimal("3")
        )
        
        formatted = calc.format_result()
        # Should be a string representation of the result
        assert isinstance(formatted, str)

    def test_format_result_custom_precision(self):
        """Test result formatting with custom precision."""
        calc = Calculation(
            operation="Division",
            operand1=Decimal("1"),
            operand2=Decimal("3")
        )
        
        formatted = calc.format_result(precision=2)
        assert isinstance(formatted, str)

    # ========================
    # Timestamp Tests
    # ========================

    def test_timestamp_creation(self):
        """Test that calculation gets a timestamp when created."""
        before_creation = datetime.datetime.now()
        
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("1"),
            operand2=Decimal("1")
        )
        
        after_creation = datetime.datetime.now()
        
        # Timestamp should be between before and after creation
        assert before_creation <= calc.timestamp <= after_creation

    def test_custom_timestamp(self):
        """Test setting a custom timestamp."""
        custom_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
        
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("1"),
            operand2=Decimal("1"),
            timestamp=custom_time
        )
        
        assert calc.timestamp == custom_time

    # ========================
    # Edge Cases and Special Values
    # ========================

    def test_large_numbers(self):
        """Test calculations with large numbers."""
        calc = Calculation(
            operation="Multiplication",
            operand1=Decimal("999999999999"),
            operand2=Decimal("999999999999")
        )
        
        # Should handle large numbers without error
        assert calc.result is not None

    def test_decimal_precision(self):
        """Test calculations maintain decimal precision."""
        calc = Calculation(
            operation="Division",
            operand1=Decimal("1"),
            operand2=Decimal("3")
        )
        
        # Result should be a Decimal type
        assert isinstance(calc.result, Decimal)

    def test_zero_operands(self):
        """Test calculations with zero operands."""
        calc = Calculation(
            operation="Addition",
            operand1=Decimal("0"),
            operand2=Decimal("5")
        )
        
        assert calc.result == Decimal("5")
        
        calc2 = Calculation(
            operation="Multiplication",
            operand1=Decimal("0"),
            operand2=Decimal("100")
        )
        
        assert calc2.result == Decimal("0")

    # ========================
    # Post-Initialization Tests
    # ========================

    def test_post_init_calculation(self):
        """Test that __post_init__ automatically calculates result."""
        # Create calculation without triggering calculate manually
        calc = Calculation.__new__(Calculation)
        calc.operation = "Addition"
        calc.operand1 = Decimal("5")
        calc.operand2 = Decimal("7")
        calc.timestamp = datetime.datetime.now()
        
        # Manually call __post_init__ to test it
        calc.__post_init__()
        
        assert calc.result == Decimal("12")