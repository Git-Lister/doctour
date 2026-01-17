# Doctour - System Architecture

**Version**: 0.1.0  
**Last Updated**: January 17, 2026  
**Status**: Initial Design

---

## Overview

This document defines the technical architecture for the Doctour project - a medieval medical AI that bridges historical medical texts with modern evidence-based herbal remedies.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Web UI     │  │   CLI Tool   │  │   REST API         │   │
│  │  (Gradio/    │  │   (Direct    │  │   (FastAPI)        │   │
│  │   Streamlit) │  │   Terminal)  │  │                    │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LOGIC LAYER                      │
│  • Conversation Manager (session state, multi-turn dialogue)    │
│  • Doctour Core Engine (symptom analyzer, humoral diagnosis)    │
│  • Safety & Validation Layer (toxic filter, emergency detector) │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        MODEL LAYER                               │
│  • Fine-tuned LLM (DeepSeek-R1 or Llama-3.1-8B + LoRA)         │
│  • RAG System (ChromaDB/FAISS + evidence validation)            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  • Medieval Corpus (Hippocratic, Galen, Dioscorides, Avicenna)  │
│  • Modern Evidence Database (Cochrane, WHO)                      │
│  • User Sessions (SQLite/PostgreSQL)                             │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Processing Pipeline
- **Input**: Raw medieval texts (PDF/TXT/EPUB from Internet Archive)
- **Processing**: 
  - Text extraction & normalization
  - Medical content extraction (remedies, symptoms, diagnoses)
  - Evidence cross-referencing with modern databases
  - Instruction dataset generation (symptom → diagnosis → remedy)
- **Output**: Training data in JSONL format + knowledge base

### 2. Model Architecture
- **Base Model**: DeepSeek-R1 (7B) or Llama-3.1-8B
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation via PEFT)
- **Training Corpus**:
  - Medical: Hippocratic Corpus, Galen, Dioscorides, Avicenna (~500K tokens)
  - Literary: Canterbury Tales, Sir Gawain, Julian of Norwich (~200K tokens)
- **RAG Integration**: 
  - Vector store: ChromaDB or FAISS
  - Embeddings: SentenceTransformers
  - Purpose: Real-time evidence validation and safety checks

### 3. Safety System (Multi-Layer)

**Layer 1: Toxic Substance Blocklist**
```json
{
  "mercury": {"status": "blocked", "reason": "Heavy metal poisoning"},
  "hemlock": {"status": "blocked", "reason": "Lethal neurotoxin"},
  "arsenic": {"status": "blocked", "reason": "Carcinogen, acute toxicity"}
}
```

**Layer 2: Drug Interaction Checker**
- Cross-references herbal remedies with modern pharmaceuticals
- Mandatory warning: "If thou takest draughts from a modern leech, consult them ere mixing remedies"

**Layer 3: Emergency Symptom Detector**
- Flags life-threatening conditions (chest pain → heart attack, severe headache → stroke)
- Immediately recommends professional medical attention

**Layer 4: Evidence Validator**
- Every remedy must have:
  - Modern scientific validation (Cochrane/WHO), OR
  - Clear safety record + historical use, OR
  - Explicit "experimental/unvalidated" tag

### 4. Conversation Flow

```
User Input → Symptom Analyzer
     ↓
Humoral Diagnostician (map to medieval framework)
     ↓
Remedy Prescriber (select evidence-based herbs)
     ↓
Safety Filters (check toxic/interactions/emergency)
     ↓
LLM Generation (medieval English response)
     ↓
Output with disclaimers
```

## Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Language** | Python 3.10+ | ML ecosystem, type hints |
| **LLM Framework** | Transformers, PEFT | Industry standard, LoRA support |
| **RAG** | ChromaDB + SentenceTransformers | Lightweight, fast retrieval |
| **API** | FastAPI | Async, auto-documentation |
| **UI** | Gradio (initial) → Streamlit | Rapid prototyping → polished UI |
| **Database** | SQLite → PostgreSQL | Local dev → production scale |
| **Testing** | Pytest + custom safety suite | Safety-critical validation |

## File Structure

See [project root](../../README.md#-getting-started) for complete directory tree.

Key directories:
- `src/` - All Python source code
- `data/` - Raw corpus, processed training data, knowledge bases
- `models/` - Fine-tuned models and checkpoints (gitignored)
- `tests/` - Comprehensive test suite including safety tests
- `docs/` - Design documents, research notes
- `scripts/` - Automation for data processing, training, deployment

## Deployment Architecture (Future)

**Local Development (v0.1)**
```
User → Gradio Web UI → Local Python Server → Local Model (GGUF/PyTorch)
```

**Production (v1.0+)**
```
User → Web Frontend → FastAPI (Docker)
       ↓
Model Service (GPU Server) + RAG Database (Vector Store)
       ↓
PostgreSQL (Sessions) + Object Storage (Corpus)
```

## Security & Privacy Considerations

1. **No Medical Data Storage**: User symptoms are not persisted beyond session
2. **Local-First**: Designed to run entirely offline on user's machine
3. **Open Source**: All code, models, and training data are transparent
4. **Disclaimers**: Every interaction includes medical disclaimer
5. **Safety Logging**: Track but don't store safety flag triggers for monitoring

## Performance Requirements

| Metric | Target (v0.1) | Target (v1.0) |
|--------|--------------|---------------|
| Response Latency | < 5s (local GPU) | < 2s (server) |
| Model Size | < 10GB (base + adapters) | < 5GB (optimized) |
| RAM Usage | 16GB (inference) | 8GB (quantized) |
| Training Time | < 12h (RTX 3060) | < 6h (A100) |

## Success Criteria

**Technical**:
- [ ] Fine-tuned model achieves 90%+ language authenticity score
- [ ] Safety filters block 100% of known toxic substances
- [ ] Emergency detector flags 95%+ of critical symptoms
- [ ] Remedy recommendations have ≥80% evidence backing

**User Experience**:
- [ ] Medieval voice is convincing and consistent
- [ ] Responses feel educational, not dangerous
- [ ] Disclaimers are clear and prominent
- [ ] Interface is intuitive for non-technical users

## Next Steps

See [Development Roadmap](../../README.md#-development-roadmap) in main README.

## References

- [Design Document](design_doc.md) - High-level project vision
- [Safety Requirements](safety_requirements.md) - Detailed safety specifications
- [Medieval Sources](../research/medieval_sources.md) - Corpus bibliography
- [Evidence Validation](../research/evidence_validation.md) - Modern scientific backing

---

**For questions or clarifications, see**: [GitHub Issues](https://github.com/Git-Lister/doctour/issues)
