#!/usr/bin/env python3
"""Convert PDFs in corpus to text files with OCR support."""

import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def convert_pdfs_to_text(corpus_dir: Path):
    """Convert all PDFs in corpus directory to text."""
    
    # Try importing libraries
    try:
        import pypdf
    except ImportError:
        logger.error("pypdf not found. Install with: pip install pypdf")
        return False
    
    try:
        from PIL import Image
        import pytesseract
        has_ocr = True
        logger.info("OCR support available (pytesseract found)")
    except ImportError:
        has_ocr = False
        logger.warning("OCR not available. Install with: pip install pytesseract pillow")
        logger.warning("For scanned PDFs, you'll need OCR support")
    
    pdf_files = list(corpus_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.error(f"No PDF files found in {corpus_dir}")
        return False
    
    logger.info(f"Found {len(pdf_files)} PDF files to convert\n")
    
    success_count = 0
    failed_count = 0
    ocr_needed = []
    
    for pdf_file in pdf_files:
        logger.info(f"Converting: {pdf_file.name}")
        txt_file = pdf_file.with_suffix('.txt')
        
        # Skip if .txt already exists
        if txt_file.exists():
            logger.info(f"  → Skip (already exists: {txt_file.name})")
            continue
        
        try:
            reader = pypdf.PdfReader(pdf_file)
            text = ""
            page_count = len(reader.pages)
            
            logger.info(f"  → {page_count} pages")
            
            # Try extracting text
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n\n"
            
            # Check if we got meaningful text
            if len(text.strip()) < 100:
                logger.warning(f"  ⚠ Very little text extracted ({len(text.strip())} chars)")
                logger.warning(f"  ⚠ This is likely a SCANNED manuscript (needs OCR)")
                ocr_needed.append(pdf_file.name)
                failed_count += 1
                continue
            
            # Add metadata header
            header = f"""---
source: {pdf_file.stem}
format: PDF
extracted: {Path(__file__).parent.parent.name}
---

"""
            
            # Save text file
            txt_file.write_text(header + text, encoding='utf-8')
            logger.info(f"  ✓ Created {txt_file.name} ({len(text)} chars)\n")
            success_count += 1
            
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}\n")
            failed_count += 1
    
    # Summary
    logger.info("=" * 60)
    logger.info(f"CONVERSION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"✓ Successfully converted: {success_count}")
    logger.info(f"✗ Failed/Skipped: {failed_count}")
    
    if ocr_needed:
        logger.info(f"\n⚠ SCANNED MANUSCRIPTS DETECTED ({len(ocr_needed)}):")
        logger.info("These PDFs need OCR or digital transcriptions:")
        for pdf in ocr_needed:
            logger.info(f"  - {pdf}")
        logger.info("\nSee translation options in documentation.")
    
    return True


if __name__ == "__main__":
    corpus_dir = Path(__file__).parent.parent / "data" / "corpus"
    
    if not corpus_dir.exists():
        logger.error(f"Corpus directory not found: {corpus_dir}")
        sys.exit(1)
    
    convert_pdfs_to_text(corpus_dir)
