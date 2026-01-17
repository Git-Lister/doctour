"""Configuration management for Doctour."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DoctourConfig:
    """Configuration settings for Doctour application."""
    
    # Model settings
    model_name: str = "mistral-7b-instruct"
    model_path: Optional[Path] = None
    lora_adapter_path: Optional[Path] = None
    
    # Data paths
    data_dir: Path = Path("./data")
    corpus_dir: Path = Path("./data/corpus")
    remedies_db: Path = Path("./data/remedies.json")
    
    # Safety settings
    enable_safety_filter: bool = True
    max_response_length: int = 512
    temperature: float = 0.7
    
    # RAG settings
    enable_rag: bool = True
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k_retrieval: int = 3
    
    # Middle English settings
    middle_english_style: bool = True
    language_era: str = "1350-1410"
    
    @classmethod
    def from_env(cls) -> "DoctourConfig":
        """Create configuration from environment variables."""
        config = cls()
        
        if model_name := os.getenv("DOCTOUR_MODEL_NAME"):
            config.model_name = model_name
        
        if model_path := os.getenv("DOCTOUR_MODEL_PATH"):
            config.model_path = Path(model_path)
        
        if data_dir := os.getenv("DOCTOUR_DATA_DIR"):
            config.data_dir = Path(data_dir)
        
        return config


# Default configuration instance
default_config = DoctourConfig()
