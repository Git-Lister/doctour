# Historical Medical Corpus

This directory contains the historical medical texts used by Doctour's RAG system.

## Purpose

The corpus provides the knowledge base for Doctour to generate historically-informed responses about herbal remedies and medieval medical practices.

## Required Content

Place pre-1410 historical medical texts in this directory, including:

### Primary Sources
- **Hippocratic Corpus** (c. 400 BCE) - Greek medical texts
- **Galen's Works** (c. 200 CE) - Roman medical authority
- **Dioscorides' De Materia Medica** (c. 70 CE) - Herbal pharmacology
- **Avicenna's Canon of Medicine** (c. 1025 CE) - Islamic medical encyclopedia

### Medieval English Sources
- Anglo-Saxon herbals
- Medieval English medical manuscripts
- Leechbooks
- Herbal remedy collections

## File Format

Texts should be in plain text format (.txt) with:

```
filename: source_title_date.txt

Format:
---
title: Title of Source
author: Author Name
date: Year/Period
language: Original Language
---

[Text content here]
```

## Metadata

Each text file should include:
- **Title**: Name of the work
- **Author**: Original author if known
- **Date**: Approximate date or period
- **Language**: Original language (Latin, Greek, Arabic, Middle English, etc.)
- **Translation**: Translator if applicable

## Indexing

After adding texts to this directory, run the indexing script:

```bash
python scripts/index_corpus.py --corpus-dir data/corpus
```

This creates a searchable index for the RAG system.

## Sources

### Public Domain Sources

- **Perseus Digital Library**: Ancient Greek and Latin texts
- **Internet Archive**: Medieval manuscripts and translations
- **Wikisource**: Translations of classical medical texts
- **Project Gutenberg**: Historical medical texts

### Academic Resources

- Digital editions from university libraries
- Open access medieval manuscript collections
- Historical medical text databases

## Copyright Compliance

**IMPORTANT**: Only include texts that are:

1. In the public domain (pre-1900 works generally safe)
2. Open access with explicit permission
3. Licensed under Creative Commons or similar

Do NOT include:
- Modern copyrighted translations without permission
- Recently published scholarly editions
- Commercial medical texts

## Data Quality

### Preferred Qualities

- Accurate transcriptions or translations
- Clear attribution and dating
- Focus on herbal remedies and non-dangerous treatments
- Texts from reputable academic sources

### Safety Filtering

The RAG system automatically filters out dangerous remedies using the safety blocklist. However, curate texts to focus on:

- Herbal remedies with modern scientific validation
- Dietary recommendations
- General health advice
- Historical diagnostic frameworks

Avoid texts heavy in:
- Toxic substances (mercury, lead, arsenic)
- Surgical procedures
- Treatments now known to be harmful

## Example Structure

```
data/corpus/
├── hippocrates_aphorisms_400bce.txt
├── galen_hygiene_200ce.txt
├── dioscorides_materia_medica_70ce.txt
├── avicenna_canon_vol1_1025ce.txt
├── bald_leechbook_900ce.txt
└── anonymous_herbal_1400ce.txt
```

## Current Status

**Empty Directory**: Please add historical medical texts to begin using Doctour.

For testing purposes, you can use small sample excerpts from public domain sources.

## Contact

For questions about corpus curation, see CONTRIBUTING.md
