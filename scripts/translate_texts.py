#!/usr/bin/env python3
"""Identify and translate non-English texts in corpus.

This script:
1. Detects language of each text file
2. Identifies which need translation
3. Provides options for translation (manual or assisted)
"""

import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def detect_language(text: str) -> str:
    """Simple language detection based on character patterns.
    
    Returns:
        str: Detected language code (en, la, ar, etc.)
    """
    # Basic heuristics
    if not text.strip():
        return "unknown"
    
    # Check for Arabic script
    arabic_chars = sum(1 for c in text[:1000] if '\u0600' <= c <= '\u06FF')
    if arabic_chars > 50:
        return "ar"  # Arabic
    
    # Check for Latin patterns
    latin_patterns = ['et', 'de', 'ad', 'in', 'per', 'cum', 'ex']
    text_lower = text[:2000].lower()
    latin_count = sum(1 for pattern in latin_patterns if pattern in text_lower.split())
    
    # Check for Middle English patterns
    me_patterns = ['þ', 'ȝ', 'thou', 'thee', 'thy', 'hath', 'doth']
    me_count = sum(1 for pattern in me_patterns if pattern in text_lower)
    
    if me_count > 5:
        return "enm"  # Middle English
    elif latin_count > 10:
        return "la"  # Latin
    elif any(c.isalpha() and c.isascii() for c in text[:100]):
        return "en"  # Modern English
    
    return "unknown"


def analyze_corpus(corpus_dir: Path):
    """Analyze all text files in corpus for language."""
    
    txt_files = list(corpus_dir.glob("*.txt"))
    
    if not txt_files:
        logger.warning(f"No .txt files found in {corpus_dir}")
        logger.info("Run convert_pdfs.py first to extract text from PDFs")
        return
    
    logger.info(f"Analyzing {len(txt_files)} text files...\n")
    
    results = {
        "en": [],      # Modern English
        "enm": [],     # Middle English
        "la": [],      # Latin
        "ar": [],      # Arabic
        "unknown": []  # Unknown/mixed
    }
    
    for txt_file in txt_files:
        try:
            text = txt_file.read_text(encoding='utf-8')[:5000]  # Sample first 5000 chars
            lang = detect_language(text)
            results[lang].append(txt_file.name)
            
        except Exception as e:
            logger.error(f"Error reading {txt_file.name}: {e}")
            results["unknown"].append(txt_file.name)
    
    # Report findings
    print("=" * 70)
    print("CORPUS LANGUAGE ANALYSIS")
    print("=" * 70)
    print()
    
    if results["en"]:
        print(f"✅ MODERN ENGLISH ({len(results['en'])} files) - Ready to use:")
        for name in results["en"]:
            print(f"   • {name}")
        print()
    
    if results["enm"]:
        print(f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 MIDDLE ENGLISH ({len(results['enm'])} files) - Keep as-is (authentic):")
        for name in results["enm"]:
            print(f"   • {name}")
        print()
    
    if results["la"]:
        print(f"📚 LATIN ({len(results['la'])} files) - NEED TRANSLATION:")
        for name in results["la"]:
            print(f"   • {name}")
        print()
        print("   OPTIONS:")
        print("   1. Search Internet Archive for English translations")
        print("   2. Use existing English versions if available")
        print("   3. Machine translation (mark as 'assisted translation')")
        print()
    
    if results["ar"]:
        print(f"🕌 ARABIC ({len(results['ar'])} files) - NEED TRANSLATION:")
        for name in results["ar"]:
            print(f"   • {name}")
        print()
        print("   OPTIONS:")
        print("   1. Search for 19th-century English translations (public domain)")
        print("   2. Check if Canon of Medicine English volumes cover this content")
        print()
    
    if results["unknown"]:
        print(f"❓ UNKNOWN/MIXED ({len(results['unknown'])} files) - REVIEW NEEDED:")
        for name in results["unknown"]:
            print(f"   • {name}")
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Ready to use: {len(results['en']) + len(results['enm'])}")
    print(f"Need translation: {len(results['la']) + len(results['ar'])}")
    print(f"Need review: {len(results['unknown'])}")
    print()
    
    # Save detailed report
    report_file = corpus_dir / "language_analysis.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("CORPUS LANGUAGE ANALYSIS REPORT\n")
        f.write("=" * 70 + "\n\n")
        for lang, files in results.items():
            if files:
                f.write(f"{lang.upper()}: {len(files)} files\n")
                for name in files:
                    f.write(f"  - {name}\n")
                f.write("\n")
    
    logger.info(f"Detailed report saved to: {report_file}")


def main():
    """Main function."""
    corpus_dir = Path(__file__).parent.parent / "data" / "corpus"
    
    if not corpus_dir.exists():
        logger.error(f"Corpus directory not found: {corpus_dir}")
        return 1
    
    analyze_corpus(corpus_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
