#!/usr/bin/env python3
"""Script to index historical medical corpus for RAG retrieval.

This script reads historical medical texts from the data directory
and indexes them using the RAG system for efficient retrieval.
"""

import sys
import logging
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from doctour.config import Config
from doctour.rag import RAGSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main indexing function."""
    parser = argparse.ArgumentParser(
        description="Index historical medical corpus for Doctour"
    )
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=Path("data/corpus"),
        help="Directory containing corpus text files"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild of index even if it exists"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Initialize configuration
    logger.info("Initializing Doctour configuration")
    config = Config()
    
    # Initialize RAG system
    logger.info("Initializing RAG system")
    rag = RAGSystem(config)
    
    # Check if corpus directory exists
    if not args.corpus_dir.exists():
        logger.error(f"Corpus directory not found: {args.corpus_dir}")
        logger.info("Please add historical medical texts to the corpus directory")
        return 1
    
    # Index the corpus
    logger.info(f"Indexing corpus from {args.corpus_dir}")
    success = rag.index_corpus(force_reindex=args.force)
    
    if success:
        logger.info("✓ Corpus indexed successfully")
        logger.info(f"Index saved to: {rag.config.corpus_index_path}")
        return 0
    else:
        logger.error("✗ Failed to index corpus")
        return 1


if __name__ == "__main__":
    sys.exit(main())
