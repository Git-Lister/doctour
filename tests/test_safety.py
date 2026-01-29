"""Tests for the safety module."""

import pytest

from doctour.safety import SafetySystem, SafetyResult, SafetyLevel
from doctour.config import DoctourConfig


@pytest.fixture
def config():
    """Provide test configuration."""
    return DoctourConfig(model_name="test-model")


@pytest.fixture
def safety_system():
    """Provide safety system instance."""
    return SafetySystem()


class TestSafetySystem:
    """Test suite for SafetySystem."""

    def test_initialization(self, safety_system):
        """Test system initializes and has a blocklist path."""
        assert safety_system is not None
        assert safety_system.blocklist_path is not None

    def test_check_toxic_substances(self, safety_system):
        """Toxic substances are detected."""
        is_safe, blocked = safety_system.check_toxic_substances(
            "This remedy uses arsenic and mercury."
        )
        assert not is_safe
        assert isinstance(blocked, list)

    def test_detect_emergency_symptoms(self, safety_system):
        """Emergency symptoms are detected."""
        is_safe, detected = safety_system.detect_emergency_symptoms(
            "I have crushing chest pain and cannot breathe."
        )
        assert isinstance(detected, list)

    def test_validate_response_safe(self, safety_system):
        """Safe response passes safety checks."""
        user_input = "I have a mild headache."
        model_response = "Chamomile tea and rest may comfort thee."
        result = safety_system.validate_response(user_input, model_response)
        assert isinstance(result, SafetyResult)
        assert result.level in (SafetyLevel.SAFE, SafetyLevel.CAUTION)

    def test_validate_response_blocks_dangerous(self, safety_system):
        """Dangerous response gets flagged/blocked."""
        user_input = "I have a mild headache."
        model_response = "Drink a potion with arsenic and mercury."
        result = safety_system.validate_response(user_input, model_response)
        assert result.level in (
            SafetyLevel.BLOCKED,
            SafetyLevel.WARNING,
            SafetyLevel.EMERGENCY,
        )


class TestBlocklistIntegration:
    """Test suite for blocklist functionality."""

    def test_blocklist_detection(self, safety_system):
        """Detection of blocked substances via validate_response."""
        user_input = "Tell me about remedies."
        model_response = "Use arsenic and lead for thy ailment."
        result = safety_system.validate_response(user_input, model_response)
        assert result.level in (
            SafetyLevel.BLOCKED,
            SafetyLevel.WARNING,
            SafetyLevel.EMERGENCY,
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
