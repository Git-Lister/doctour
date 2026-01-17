# Data Directory

This directory contains the training data and resources for the Doctour medieval medical AI.

## Structure

```
data/
├── corpus/              # Historical medical texts (pre-1410)
│   ├── hippocratic/    # Hippocratic Corpus texts
│   ├── galen/          # Galen's medical writings
│   ├── dioscorides/    # De Materia Medica
│   └── avicenna/       # Canon of Medicine extracts
├── remedies.json       # Curated herbal remedies database
├── safety_blocklist.json  # Substances and practices to avoid
└── embeddings/         # Cached vector embeddings for RAG
```

## Data Sources

### Historical Texts
All texts are from **pre-1410** sources to maintain authentic medieval medical knowledge:

- **Hippocratic Corpus** (c. 400 BCE): Foundation of Western medicine
- **Galen** (129-216 CE): Greek physician, influential throughout Middle Ages  
- **Dioscorides** (c. 40-90 CE): De Materia Medica, herbal medicine encyclopedia
- **Avicenna** (980-1037 CE): Canon of Medicine, synthesis of Greco-Roman and Arabic medicine

### Remedies Database
Structured JSON containing:
- Herbal remedy names (English and Middle English)
- Modern scientific validation references
- Safety information and contraindications
- Cross-references to Cochrane reviews and WHO traditional medicine database

## Setup

1. Download historical texts (links in docs/design/)
2. Run preprocessing scripts to extract and clean text
3. Generate embeddings for RAG system

## Safety

**CRITICAL**: The `safety_blocklist.json` filters out:
- Toxic substances
- Dangerous practices
- Unvalidated treatments
- Emergency medical conditions requiring professional care

## License

Historical texts are in the public domain. Modern curation and safety data are MIT licensed.
