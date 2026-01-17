"""Pytest configuration and fixtures for Doctour tests."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def mock_safety_blocklist(tmp_path_factory):
    """Create a mock safety blocklist for testing."""
    import json
    
    blocklist = {
        "blocked_substances": [
            "arsenic",
            "mercury",
            "lead",
            "cyanide"
        ],
        "warning_substances": [
            "belladonna",
            "hemlock",
            "wolfsbane"
        ]
    }
    
    temp_dir = tmp_path_factory.mktemp("test_data")
    blocklist_file = temp_dir / "safety_blocklist.json"
    
    with open(blocklist_file, 'w') as f:
        json.dump(blocklist, f)
    
    return blocklist_file


@pytest.fixture
def mock_config(mock_safety_blocklist):
    """Provide mock configuration for testing."""
    from doctour.config import Config
    
    return Config(
        model_name="test-model",
        safety_blocklist_path=mock_safety_blocklist,
        log_level="DEBUG"
    )


@pytest.fixture
def sample_historical_texts():
    """Provide sample historical medical texts for testing."""
    return [
        {
            "text": "Chamomile is good for calming the stomach and aiding sleep.",
            "source": "Mock Herbal",
            "date": "1400"
        },
        {
            "text": "Lavender oil soothes headaches and nervous tension.",
            "source": "Mock Pharmacopoeia",
            "date": "1395"
        },
        {
            "text": "Peppermint aids digestion and relieves nausea.",
            "source": "Mock Medical Text",
            "date": "1410"
        }
    ]
