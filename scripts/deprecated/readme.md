# Deprecated Scripts

These scripts are from the original Doctour scaffolding and have been superseded by the new corpus extraction pipeline.

| Script | Replaced By | Reason |
|--------|-------------|--------|
| `convert_pdfs.py` | `extract_corpus.py` | New script handles PDF/EPUB/TXT natively |
| `translate_texts.py` | — | Not needed; we train on ME directly, not via translation |
| `index_corpus.py` | `extract_corpus.py` + future RAG indexer | New corpus structure requires different indexing |

Do not use these for v0.1. Kept for reference only.