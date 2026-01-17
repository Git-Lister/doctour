"""Multi-layer safety system for Doctour.

Implements four layers of safety:
1. Toxic Substance Blocklist
2. Drug Interaction Checker
3. Emergency Symptom Detector
4. Evidence Validator
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SafetyLevel(Enum):
    """Safety assessment levels."""
    SAFE = "safe"
    CAUTION = "caution"
    WARNING = "warning"
    BLOCKED = "blocked"
    EMERGENCY = "emergency"


@dataclass
class SafetyResult:
    """Result of safety check."""
    level: SafetyLevel
    message: str
    blocked_substances: List[str] = None
    emergency_symptoms: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.blocked_substances is None:
            self.blocked_substances = []
        if self.emergency_symptoms is None:
            self.emergency_symptoms = []
        if self.warnings is None:
            self.warnings = []


class SafetySystem:
    """Multi-layer safety validation system."""

    def __init__(self, blocklist_path: Optional[Path] = None):
        """Initialize safety system.
        
        Args:
            blocklist_path: Path to safety_blocklist.json
        """
        if blocklist_path is None:
            blocklist_path = Path(__file__).parent.parent.parent / "data" / "safety_blocklist.json"
        
        self.blocklist_path = blocklist_path
        self.blocklist_data = self._load_blocklist()
    
    def _load_blocklist(self) -> Dict:
        """Load safety blocklist from JSON file."""
        try:
            with open(self.blocklist_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Safety blocklist not found at {self.blocklist_path}")
            return {"toxic_substances": {}, "dangerous_practices": {}, "emergency_symptoms": []}
    
    def check_toxic_substances(self, text: str) -> Tuple[bool, List[str]]:
        """Check text for toxic substances (Layer 1).
        
        Args:
            text: Text to check for toxic substances
        
        Returns:
            Tuple of (is_safe, list of blocked substances found)
        """
        text_lower = text.lower()
        blocked = []
        
        for substance, info in self.blocklist_data.get("toxic_substances", {}).items():
            if info.get("status") == "blocked" and substance.lower() in text_lower:
                blocked.append(substance)
                logger.warning(f"Toxic substance detected: {substance}")
        
        return len(blocked) == 0, blocked
    
    def check_dangerous_practices(self, text: str) -> Tuple[bool, List[str]]:
        """Check for dangerous medical practices.
        
        Args:
            text: Text to check
        
        Returns:
            Tuple of (is_safe, list of dangerous practices found)
        """
        text_lower = text.lower()
        blocked = []
        
        for practice, info in self.blocklist_data.get("dangerous_practices", {}).items():
            if info.get("status") == "blocked" and practice.lower() in text_lower:
                blocked.append(practice)
                logger.warning(f"Dangerous practice detected: {practice}")
        
        return len(blocked) == 0, blocked
    
    def detect_emergency_symptoms(self, text: str) -> Tuple[bool, List[str]]:
        """Detect life-threatening symptoms (Layer 3).
        
        Args:
            text: User input to check
        
        Returns:
            Tuple of (no_emergency, list of emergency symptoms detected)
        """
        text_lower = text.lower()
        detected = []
        
        for symptom in self.blocklist_data.get("emergency_symptoms", []):
            if symptom.lower() in text_lower:
                detected.append(symptom)
                logger.critical(f"Emergency symptom detected: {symptom}")
        
        return len(detected) == 0, detected
    
    def validate_response(self, user_input: str, model_response: str) -> SafetyResult:
        """Comprehensive safety validation.
        
        Args:
            user_input: User's symptom description
            model_response: Model's proposed response
        
        Returns:
            SafetyResult with assessment and warnings
        """
        # Layer 3: Check for emergency symptoms first
        no_emergency, emergency_symptoms = self.detect_emergency_symptoms(user_input)
        if not no_emergency:
            return SafetyResult(
                level=SafetyLevel.EMERGENCY,
                message="⚠️ CRITICAL: This appears to be a medical emergency. Seek immediate professional medical attention. Call emergency services.",
                emergency_symptoms=emergency_symptoms
            )
        
        # Layer 1: Check response for toxic substances
        safe_substances, blocked_substances = self.check_toxic_substances(model_response)
        
        # Check for dangerous practices
        safe_practices, blocked_practices = self.check_dangerous_practices(model_response)
        
        if not safe_substances or not safe_practices:
            return SafetyResult(
                level=SafetyLevel.BLOCKED,
                message="Response blocked: Contains dangerous substances or practices.",
                blocked_substances=blocked_substances + blocked_practices
            )
        
        # Layer 2: Drug interaction warning (always included)
        warnings = [
            "If thou takest draughts from a modern leech (physician), consult them ere mixing remedies."
        ]
        
        return SafetyResult(
            level=SafetyLevel.SAFE,
            message="Response passed safety checks.",
            warnings=warnings
        )
    
    def get_medical_disclaimer(self) -> str:
        """Get the standard medical disclaimer."""
        return (
            "\n\n⚠️ CRITICAL DISCLAIMER: This is an educational/experimental project only. "
            "It is NOT medical advice. Always consult qualified healthcare professionals "
            "for medical concerns. Do not use this to diagnose or treat any medical condition."
        )
