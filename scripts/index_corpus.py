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

from doctour.config import DoctourConfig
from doctour.rag import RAGSystem

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
        help="Directory containing corpus text files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild of index even if it exists",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (currently unused)",
    )

    args = parser.parse_args()

    # Initialize configuration
    logger.info("Initializing Doctour configuration")
    config = DoctourConfig()

    # Initialize RAG system with paths from config + CLI override
    logger.info("Initializing RAG system")
    corpus_path = args.corpus_dir if args.corpus_dir else config.corpus_dir
    rag = RAGSystem(
        corpus_path=corpus_path,
        embeddings_path=Path("./data/embeddings"),
        embedding_model=config.embedding_model,
        top_k=config.top_k_retrieval,
    )

    # Check if corpus directory exists
    if not corpus_path.exists():
        logger.error(f"Corpus directory not found: {corpus_path}")
        logger.info("Please add historical medical texts to the corpus directory")
        return 1

    # Index the corpus
    logger.info(f"Indexing corpus from {corpus_path}")
    rag.index_corpus(force_reindex=args.force)

    logger.info("✓ Corpus indexing completed (stub implementation)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
