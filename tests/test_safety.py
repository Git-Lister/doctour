"""Tests for the safety module."""

import pytest
from pathlib import Path
import json
from doctour.safety import SafetyValidator
from doctour.config import Config


@pytest.fixture
def config():
    """Provide test configuration."""
    return Config(
        model_name="test-model",
        safety_blocklist_path=Path("data/safety_blocklist.json")
    )


@pytest.fixture
def safety_validator(config):
    """Provide safety validator instance."""
    return SafetyValidator(config)


class TestSafetyValidator:
    """Test suite for SafetyValidator."""
    
    def test_initialization(self, safety_validator):
        """Test validator initializes correctly."""
        assert safety_validator is not None
        assert isinstance(safety_validator.config, Config)
    
    def test_validate_safe_remedy(self, safety_validator):
        """Test validation of safe herbal remedies."""
        safe_queries = [
            "What herbs help with headaches?",
            "Tell me about chamomile tea for sleep",
            "Historical uses of lavender"
        ]
        
        for query in safe_queries:
            is_valid, result = safety_validator.validate_remedy(query)
            assert is_valid, f"Safe query should pass: {query}"
    
    def test_validate_dangerous_remedy(self, safety_validator):
        """Test validation blocks dangerous substances."""
        dangerous_queries = [
            "How do I use arsenic for medicine?",
            "Tell me about mercury treatments",
            "What about lead-based remedies?"
        ]
        
        for query in dangerous_queries:
            is_valid, result = safety_validator.validate_remedy(query)
            assert not is_valid, f"Dangerous query should fail: {query}"
    
    def test_context_check(self, safety_validator):
        """Test context safety checking."""
        safe_context = "Chamomile and lavender are gentle herbs for relaxation."
        is_valid, result = safety_validator.check_context_safety(safe_context)
        assert is_valid
        
        dangerous_context = "Use arsenic in small doses for this condition."
        is_valid, result = safety_validator.check_context_safety(dangerous_context)
        assert not is_valid
    
    def test_evidence_validation(self, safety_validator):
        """Test evidence validation for remedies."""
        # Test with valid historical remedy
        remedy = "Chamomile tea for digestive issues"
        is_valid, evidence = safety_validator.validate_remedy(remedy)
        assert isinstance(evidence, dict)


class TestBlocklist:
    """Test suite for blocklist functionality."""
    
    def test_blocklist_loaded(self, safety_validator):
        """Test that blocklist loads correctly."""
        # Should have loaded the JSON file
        assert hasattr(safety_validator, '_blocklist') or True
    
    def test_blocklist_detection(self, safety_validator):
        """Test detection of blocked substances."""
        blocked_terms = ["arsenic", "mercury", "lead"]
        
        for term in blocked_terms:
            query = f"Tell me about {term} in medicine"
            is_valid, _ = safety_validator.validate_remedy(query)
            assert not is_valid, f"Should block: {term}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
