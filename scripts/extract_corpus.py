#!/usr/bin/env python3
"""
Doctour Corpus Automated Extraction Script v2
===============================================
Extracts candidate passages from raw medieval texts (PDF, EPUB, TXT)
for three corpora:
- Corpus A: The Voice (ME syntax, idiom, register)
- Corpus B: The Knowledge (structured medical facts)
- Corpus C: The Bridge (doctor-patient dialogue seeds)

Usage:
    python extract_corpus_v2.py --input-dir ./data/corpus --output-dir ./extracted

Requirements:
    pip install pymupdf ebooklib spacy tqdm lxml
    python -m spacy download en_core_web_sm
"""

import argparse
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Optional dependencies
try:
    import pymupdf as fitz  # PyMuPDF

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from ebooklib import epub

    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False

try:
    import spacy

    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    nlp.add_pipe("sentencizer")
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iterable, **kwargs):
        return iterable


try:
    from lxml import html

    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================


@dataclass
class ExtractionConfig:
    min_passage_tokens: int = 15
    max_passage_tokens: int = 300
    window_size: int = 200
    window_step: int = 150

    register_markers = {
        "formal_medical": [
            "leech",
            "physician",
            "doctor",
            "surgeon",
            "medicine",
            "remedy",
            "herb",
            "potion",
            "salve",
            "cure",
            "treatment",
            "disease",
            "malady",
            "affliction",
            "ailment",
            "complexion",
            "humour",
            "phlegm",
            "choler",
            "melancholy",
            "bloodletting",
            "purgation",
            "regimen",
            "diet",
            "infirmary",
            "patient",
            "sick",
            "fever",
        ],
        "colloquial": [
            "quoth",
            "said",
            "spake",
            "cried",
            "called",
            "answered",
            "replied",
            "swore",
            "laughed",
            "japed",
            "jested",
            "mocked",
            "drank",
            "ate",
            "rode",
            "went",
            "came",
            "saw",
        ],
        "advisory_religious": [
            "counsel",
            "advice",
            "teach",
            "instruct",
            "warn",
            "beseech",
            "pray",
            "exhort",
            "admonish",
            "commandment",
            "virtue",
            "vice",
            "sin",
            "penance",
            "confession",
            "salvation",
            "soul",
            "spirit",
            "god",
            "christ",
            "holy",
            "blessed",
        ],
        "intimate_embodied": [
            "heart",
            "soul",
            "body",
            "flesh",
            "blood",
            "bone",
            "limb",
            "pain",
            "sorrow",
            "woe",
            "joy",
            "bliss",
            "comfort",
            "weep",
            "tears",
            "sigh",
            "groan",
            "touch",
            "feel",
            "see",
            "hear",
        ],
    }

    direct_address_pronouns = [
        "i ",
        "my ",
        "mine ",
        "me ",
        "we ",
        "our ",
        "us ",
        "thou ",
        "thee ",
        "thy ",
        "thine ",
        "ye ",
        "you ",
        "your ",
    ]

    imperative_starters = [
        "take",
        "give",
        "make",
        "put",
        "let",
        "set",
        "hold",
        "keep",
        "look",
        "hear",
        "go",
        "come",
        "tell",
        "say",
        "speak",
        "read",
        "write",
        "know",
        "wit",
        "think",
        "believe",
        "trust",
        "hope",
        "pray",
        "beseech",
        "command",
        "bid",
        "ask",
        "require",
    ]

    normalization_map = {
        "ȝe": "ye",
        "ȝou": "you",
        "ȝour": "your",
        "ȝeue": "give",
        "ȝit": "yet",
        "ȝong": "young",
        "ȝer": "year",
        "þe": "the",
        "þat": "that",
        "þis": "this",
        "þese": "these",
        "þose": "those",
        "þer": "there",
        "þen": "then",
        "þus": "thus",
        "þough": "though",
        "þrough": "through",
        "wiþ": "with",
        "ðe": "the",
        "ðat": "that",
        "schal": "shall",
        "schulde": "should",
        "scho": "she",
        "mikel": "mickle",
        "ilk": "each",
        "kirk": "church",
        "gang": "go",
        "bairn": "child",
        "hame": "home",
        "nane": "none",
        "ony": "any",
        "wyn": "wine",
        "wynter": "winter",
        "swete": "sweet",
        "dere": "dear",
        "ferre": "far",
        "werre": "war",
        "perfit": "perfect",
        "vertu": "virtue",
        "pacient": "patient",
        "medecine": "medicine",
        "diete": "diet",
        "complexioun": "complexion",
        "&": "and",
        "+": "and",
    }

    exclude_files = {
        "Extrasensory_Perception_Research_Finding.txt",
        "readme.md",
        "README.md",
        ".gitignore",
    }


# =============================================================================
# TEXT NORMALIZATION
# =============================================================================


class TextNormalizer:
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.patterns = []
        for old, new in config.normalization_map.items():
            pattern = re.compile(r"\b" + re.escape(old) + r"\b", re.IGNORECASE)
            self.patterns.append((pattern, new))

    def normalize(self, text: str) -> str:
        for pattern, replacement in self.patterns:
            text = pattern.sub(replacement, text)
        return text

    def normalize_passage(self, passage: str) -> Tuple[str, List[Tuple[str, str]]]:
        changes = []
        normalized = passage
        for pattern, replacement in self.patterns:
            matches = pattern.findall(normalized)
            for match in matches:
                changes.append((match, replacement))
            normalized = pattern.sub(replacement, normalized)
        return normalized, changes


# =============================================================================
# FILE READERS
# =============================================================================


class FileReader:
    """Reads text from PDF, EPUB, TXT, and HTML files."""

    @staticmethod
    def read_pdf(filepath: Path) -> str:
        """Extract text from PDF using PyMuPDF."""
        if not PDF_AVAILABLE:
            logger.error("PyMuPDF not installed. Run: pip install pymupdf")
            return ""

        text_parts = []
        try:
            doc = fitz.open(str(filepath))
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
            doc.close()
        except Exception as e:
            logger.error(f"Failed to read PDF {filepath}: {e}")
            return ""

        return "\n".join(text_parts)

    @staticmethod
    def read_epub(filepath: Path) -> str:
        """Extract text from EPUB using ebooklib."""
        if not EPUB_AVAILABLE:
            logger.error("ebooklib not installed. Run: pip install ebooklib")
            return ""

        text_parts = []
        try:
            book = epub.read_epub(str(filepath))
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    content = item.get_content().decode("utf-8", errors="ignore")
                    # Strip HTML tags
                    if LXML_AVAILABLE:
                        tree = html.fromstring(content)
                        text = tree.text_content()
                    else:
                        # Fallback regex strip
                        text = re.sub(r"<[^>]+>", " ", content)
                    text_parts.append(text)
        except Exception as e:
            logger.error(f"Failed to read EPUB {filepath}: {e}")
            return ""

        return "\n".join(text_parts)

    @staticmethod
    def read_txt(filepath: Path) -> str:
        """Read plain text file."""
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read {filepath}: {e}")
            return ""

    @classmethod
    def read_file(cls, filepath: Path) -> str:
        """Dispatch to appropriate reader based on extension."""
        suffix = filepath.suffix.lower()

        if suffix == ".pdf":
            return cls.read_pdf(filepath)
        elif suffix == ".epub":
            return cls.read_epub(filepath)
        elif suffix in (".txt", ".md", ".text"):
            return cls.read_txt(filepath)
        elif suffix in (".html", ".htm"):
            content = cls.read_txt(filepath)
            if LXML_AVAILABLE:
                tree = html.fromstring(content)
                return tree.text_content()
            return re.sub(r"<[^>]+>", " ", content)
        else:
            logger.warning(f"Unknown file type: {suffix} for {filepath}")
            return ""


# =============================================================================
# PASSAGE EXTRACTOR
# =============================================================================


class PassageExtractor:
    def __init__(self, config: ExtractionConfig):
        self.config = config
        self.normalizer = TextNormalizer(config)

    def segment_sentences(self, text: str) -> List[str]:
        if SPACY_AVAILABLE:
            doc = nlp(text)
            return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
        else:
            sentences = re.split(r"(?<=[.!?;])\s+", text)
            return [s.strip() for s in sentences if len(s.strip()) > 10]

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def has_direct_address(self, text: str) -> bool:
        text_lower = text.lower()
        return any(pronoun.strip() in text_lower for pronoun in self.config.direct_address_pronouns)

    def has_imperative(self, text: str) -> bool:
        text_lower = text.lower()
        return any(text_lower.startswith(imp) for imp in self.config.imperative_starters)

    def has_direct_speech(self, text: str) -> bool:
        return any(q in text for q in ('"', "'", '"', '"'))

    def classify_register(self, text: str) -> List[str]:
        text_lower = text.lower()
        scores = {}
        for register, markers in self.config.register_markers.items():
            score = sum(1 for marker in markers if marker in text_lower)
            scores[register] = score

        if not scores or max(scores.values()) == 0:
            return ["unclassified"]

        max_score = max(scores.values())
        return [reg for reg, score in scores.items() if score == max_score and score > 0]

    def score_voice_candidate(self, text: str) -> float:
        score = 0.0
        if self.has_direct_address(text):
            score += 2.0
        if self.has_imperative(text):
            score += 1.5
        if self.has_direct_speech(text):
            score += 1.0

        registers = self.classify_register(text)
        if "formal_medical" in registers:
            score += 2.5
        if "advisory_religious" in registers:
            score += 1.5
        if "intimate_embodied" in registers:
            score += 1.0
        if "colloquial" in registers:
            score += 0.5

        token_count = self.count_tokens(text)
        if self.config.min_passage_tokens <= token_count <= self.config.max_passage_tokens:
            score += 1.0

        return score

    def clean_extracted_text(self, text: str) -> str:
        """Clean up common OCR/extraction artifacts."""
        # Remove page numbers (standalone numbers)
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)
        # Remove excessive whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        # Remove common header/footer patterns
        text = re.sub(r"\bCHAPTER\s+[IVX]+\b", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\bBOOK\s+[IVX]+\b", "", text, flags=re.IGNORECASE)
        return text.strip()

    def extract_from_file(self, filepath: Path, source_type: str) -> Dict[str, List[Dict]]:
        logger.info(f"Processing {filepath.name} ({source_type})")

        raw_text = FileReader.read_file(filepath)
        if not raw_text:
            logger.warning(f"No text extracted from {filepath}")
            return {"voice": [], "knowledge": [], "bridge_seeds": []}

        text = self.clean_extracted_text(raw_text)

        results = {"voice": [], "knowledge": [], "bridge_seeds": []}

        if source_type == "literary":
            sentences = self.segment_sentences(text)
            for i, sentence in enumerate(sentences):
                score = self.score_voice_candidate(sentence)
                if score >= 3.0:
                    normalized, changes = self.normalizer.normalize_passage(sentence)
                    results["voice"].append(
                        {
                            "source_file": filepath.name,
                            "original": sentence,
                            "normalized": normalized,
                            "score": score,
                            "register": self.classify_register(sentence),
                            "has_direct_address": self.has_direct_address(sentence),
                            "has_imperative": self.has_imperative(sentence),
                            "has_direct_speech": self.has_direct_speech(sentence),
                            "spelling_changes": changes,
                            "token_count": self.count_tokens(sentence),
                            "sentence_index": i,
                        }
                    )

        elif source_type == "medical":
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
            for i, para in enumerate(paragraphs):
                normalized = self.normalizer.normalize(para)
                results["knowledge"].append(
                    {
                        "source_file": filepath.name,
                        "original": para,
                        "normalized": normalized,
                        "token_count": self.count_tokens(para),
                        "paragraph_index": i,
                        "register": self.classify_register(para),
                    }
                )

        elif source_type == "medical_me":
            sentences = self.segment_sentences(text)
            for i, sentence in enumerate(sentences):
                score = self.score_voice_candidate(sentence)
                normalized, changes = self.normalizer.normalize_passage(sentence)

                entry = {
                    "source_file": filepath.name,
                    "original": sentence,
                    "normalized": normalized,
                    "score": score,
                    "register": self.classify_register(sentence),
                    "has_direct_address": self.has_direct_address(sentence),
                    "has_imperative": self.has_imperative(sentence),
                    "spelling_changes": changes,
                    "token_count": self.count_tokens(sentence),
                    "sentence_index": i,
                }

                if score >= 4.0:
                    results["bridge_seeds"].append(entry)
                if score >= 2.0:
                    results["voice"].append(entry)

        return results


# =============================================================================
# SOURCE CLASSIFIER
# =============================================================================


class SourceClassifier:
    LITERARY_KEYWORDS = [
        "chaucer",
        "gower",
        "julian",
        "pearl",
        "canterbury",
        "confessio",
        "revelations",
        "cleanness",
        "patience",
        "gawain",
        "margery",
        "kempe",
    ]
    MEDICAL_KEYWORDS = [
        "hippocrates",
        "galen",
        "dioscorides",
        "avicenna",
        "canon",
        "rerum",
        "britannicarum",
    ]
    MEDICAL_ME_KEYWORDS = [
        "arderne",
        "fistula",
        "leechbook",
        "lanfranc",
        "lanfrank",
        "chirurgia",
        "bald",
        "cockayne",
        "leechdom",
    ]

    @classmethod
    def classify(cls, filename: str) -> Optional[str]:
        name_lower = filename.lower()
        if any(kw in name_lower for kw in cls.MEDICAL_ME_KEYWORDS):
            return "medical_me"
        if any(kw in name_lower for kw in cls.LITERARY_KEYWORDS):
            return "literary"
        if any(kw in name_lower for kw in cls.MEDICAL_KEYWORDS):
            return "medical"
        return None


# =============================================================================
# MAIN PIPELINE
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Extract Doctour training corpora from PDF/EPUB/TXT"
    )
    parser.add_argument("--input-dir", required=True, help="Directory containing raw corpus files")
    parser.add_argument("--output-dir", required=True, help="Directory for extracted output")
    parser.add_argument(
        "--min-score", type=float, default=3.0, help="Minimum score for voice candidates"
    )
    parser.add_argument(
        "--review-batch-size", type=int, default=50, help="Candidates per review file"
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".pdf", ".epub", ".txt", ".md", ".html", ".htm"],
        help="File extensions to process",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check dependencies
    if not PDF_AVAILABLE:
        logger.warning("PyMuPDF not available — PDF files will be skipped")
    if not EPUB_AVAILABLE:
        logger.warning("ebooklib not available — EPUB files will be skipped")

    config = ExtractionConfig()
    extractor = PassageExtractor(config)

    all_voice = []
    all_knowledge = []
    all_bridge_seeds = []

    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in args.extensions]
    files = [f for f in files if f.name not in config.exclude_files]

    logger.info(f"Found {len(files)} files to process")
    logger.info(f"Extensions: {set(f.suffix.lower() for f in files)}")

    for filepath in tqdm(files, desc="Extracting passages"):
        source_type = SourceClassifier.classify(filepath.name)
        if not source_type:
            logger.warning(f"Could not classify {filepath.name}, skipping")
            continue

        results = extractor.extract_from_file(filepath, source_type)
        all_voice.extend(results["voice"])
        all_knowledge.extend(results["knowledge"])
        all_bridge_seeds.extend(results["bridge_seeds"])

    # Sort by score descending
    all_voice.sort(key=lambda x: x["score"], reverse=True)
    all_bridge_seeds.sort(key=lambda x: x["score"], reverse=True)

    # Write review batches
    def write_review_batches(items, prefix, batch_size):
        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            batch_file = output_dir / f"{prefix}_batch_{i // batch_size + 1:03d}.jsonl"
            with open(batch_file, "w", encoding="utf-8") as f:
                for item in batch:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            logger.info(f"Wrote {len(batch)} items to {batch_file.name}")

    write_review_batches(all_voice, "corpus_voice_candidates", args.review_batch_size)
    write_review_batches(all_knowledge, "corpus_knowledge_chunks", args.review_batch_size)
    write_review_batches(all_bridge_seeds, "corpus_bridge_seeds", args.review_batch_size)

    # Write consolidated stats
    stats = {
        "total_files_processed": len(files),
        "voice_candidates": len(all_voice),
        "knowledge_chunks": len(all_knowledge),
        "bridge_seeds": len(all_bridge_seeds),
        "top_voice_score": all_voice[0]["score"] if all_voice else 0,
        "top_bridge_score": all_bridge_seeds[0]["score"] if all_bridge_seeds else 0,
        "file_breakdown": defaultdict(int),
    }

    for item in all_voice:
        stats["file_breakdown"][item["source_file"]] += 1

    with open(output_dir / "extraction_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, default=str)

    logger.info("=" * 60)
    logger.info("EXTRACTION COMPLETE")
    logger.info(f"Files processed: {stats['total_files_processed']}")
    logger.info(f"Voice candidates: {stats['voice_candidates']}")
    logger.info(f"Knowledge chunks: {stats['knowledge_chunks']}")
    logger.info(f"Bridge seeds: {stats['bridge_seeds']}")
    logger.info(f"Review batches written to {output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
