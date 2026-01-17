# Doctour 🏥🏰

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Pre-Alpha](https://img.shields.io/badge/status-pre--alpha-red)](https://github.com/Git-Lister/doctour)

A medieval medical AI trained on pre-1410 historical texts (Hippocratic Corpus, Galen, Dioscorides, Avicenna), providing evidence-based herbal remedy recommendations through an authentic Middle English interface. Named after "Lud's Chapel" in the Peak District.

> ⚠️ **CRITICAL DISCLAIMER**: This is an **educational/experimental project only**. It is **NOT medical advice**. Always consult qualified healthcare professionals for medical concerns. Do not use this to diagnose or treat any medical condition.

## 🎯 Project Vision

Doctour bridges medieval medical wisdom with modern evidence, creating an AI that:
- Speaks in authentic Middle English (pre-1410 language)
- Uses humoral theory as a diagnostic framework that resonates with subjective experience
- Prescribes **only** herbal remedies with modern scientific validation
- Maintains strict safety filters to prevent dangerous recommendations
- Acknowledges its limitations as a "cautious leech" focused on gentle herbal counsel

## ✨ Features (Planned for v0.1)

- **Authentic Medieval Voice**: Fine-tuned on Canterbury Tales, Sir Gawain, and medical texts
- **Humoral Diagnosis**: Translates symptoms into medieval framework (choleric, melancholic, etc.)
- **Evidence-Based Remedies**: Cross-referenced with Cochrane reviews and WHO traditional medicine database
- **Multi-Layer Safety**: 
  - Toxic substance blocklist
  - Drug interaction warnings
  - Emergency symptom detection
  - Dosage and preparation specifications
- **RAG Integration**: Real-time evidence validation against modern research
- **Web Interface**: Gradio/Streamlit UI with "modern translation" toggle

## 📚 Training Corpus

### Medical Texts
1. **Hippocratic Corpus** (c. 400 BCE) - The Genuine Works of Hippocrates (trans. Francis Adams, 1849)
2. **Galen** (c. 200 CE) - On the Natural Faculties
3. **Dioscorides** (c. 50-70 CE) - The Greek Herbal (1959 English translation)
4. **Avicenna** (c. 1025) - The Canon of Medicine (4 volumes)

### Literary Corpus (for Language Authenticity)
5. **Geoffrey Chaucer** - The Canterbury Tales (c. 1387-1400)
6. **Sir Gawain and the Green Knight** (c. 1390)
7. **Julian of Norwich** - Revelations of Divine Love (c. 1395)
8. **[In progress]** Bald's Leechbook, John of Arderne

## 🏗️ Technical Architecture

### Stack
- **Language**: Python 3.10+
- **Base Model**: DeepSeek-R1 or Llama-3.1-8B
- **Fine-tuning**: LoRA (PEFT library)
- **RAG**: ChromaDB/FAISS + SentenceTransformers
- **API**: FastAPI
- **UI**: Gradio (initial) / Streamlit
- **Database**: SQLite (session storage)

### System Layers
1. **UI Layer**: Web interface, CLI
2. **Application Logic**: Conversation manager, Doctour engine
3. **Safety Layer**: Toxic filter, emergency detector, evidence validator
4. **Model Layer**: Fine-tuned LLM + RAG retrieval
5. **Data Layer**: Medieval corpus, modern evidence base

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- 16GB RAM minimum (32GB recommended for training)
- GPU recommended (RTX 3060+ or equivalent)
- 50GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/Git-Lister/doctour.git
cd doctour

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download historical corpus
python scripts/download_corpus.py

# Process training data
python scripts/prepare_training_data.py
```

### Quick Start (Coming Soon)

```bash
# Run the Doctour interface
python -m src.ui.gradio_interface

# Or use CLI
python -m src.ui.cli
```

## 📖 Documentation

- [Design Document](docs/design/design_doc.md)
- [System Architecture](docs/design/system_architecture.md)
- [Safety Requirements](docs/design/safety_requirements.md)
- [Medieval Sources](docs/research/medieval_sources.md)
- [Evidence Validation](docs/research/evidence_validation.md)

## 🗺️ Development Roadmap

### Phase 0: Project Setup ✅
- [x] Initialize repository
- [x] Define architecture
- [x] Document design specifications

### Phase 1: Data Acquisition (Weeks 1-2)
- [ ] Download all medieval texts
- [ ] Build text processing pipeline
- [ ] Compile modern evidence database
- [ ] Create validated herbs list with safety ratings

### Phase 2: Instruction Dataset (Week 3)
- [ ] Generate symptom scenarios
- [ ] Map symptoms → humoral diagnoses → remedies
- [ ] Include safety edge cases
- [ ] Create 500-1000 training examples

### Phase 3: Model Fine-tuning (Week 4)
- [ ] Configure LoRA hyperparameters
- [ ] Run fine-tuning on base model
- [ ] Validate on test set
- [ ] Save best checkpoint

### Phase 4: Core Logic (Weeks 5-6)
- [ ] Symptom analyzer
- [ ] Humoral diagnostician
- [ ] Remedy prescriber
- [ ] Safety filters (toxic/emergency/interactions)

### Phase 5: Interface (Week 7)
- [ ] CLI implementation
- [ ] Gradio web UI
- [ ] Modern translation toggle

### Phase 6: Testing & Safety (Week 8)
- [ ] Medical accuracy evaluation
- [ ] Language authenticity review
- [ ] Safety compliance testing
- [ ] Emergency detection validation

### Phase 7: Documentation & Release (Week 9)
- [ ] Comprehensive README
- [ ] API documentation
- [ ] User guide with examples
- [ ] v0.1.0 release

## 🤝 Contributing

Contributions are welcome! This project needs:
- Medical historians to validate authenticity
- Herbalists/pharmacologists to verify safety
- Medieval English scholars for language review
- ML engineers for model optimization
- Safety testers for edge cases

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⚖️ License

MIT License - see [LICENSE](LICENSE) for details.

Historical texts used are in the public domain.

## 🙏 Acknowledgments

- Internet Archive for digitized medieval texts
- Cochrane Collaboration for herbal medicine reviews
- WHO Traditional Medicine Programme
- Perplexity AI for development assistance
- The medieval physicians who preserved this knowledge

## 📧 Contact

- **Repository**: [Git-Lister/doctour](https://github.com/Git-Lister/doctour)
- **Issues**: [Bug reports & feature requests](https://github.com/Git-Lister/doctour/issues)

---

*"I am but a counsel-giver, learned in the safer arts of herbes and regimen. For the weightier remedies—the lance, the cuppe, the purge—thou must seek a leech with hands trained in those perilous crafts."*
