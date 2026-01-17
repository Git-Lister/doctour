# Contributing to Doctour

Thank you for your interest in contributing to Doctour! This project aims to bridge medieval medical wisdom with modern evidence-based practices for educational purposes.

## Code of Conduct

By participating in this project, you agree to:
- Treat all contributors with respect
- Focus on educational and research goals
- Never provide actual medical advice
- Maintain scientific rigor and historical accuracy

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check existing issues to avoid duplicates
2. Use the issue template (if available)
3. Provide clear reproduction steps for bugs
4. Include system information (OS, Python version, etc.)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test thoroughly**:
   ```bash
   pytest tests/
   ```
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push to your fork**
7. **Open a Pull Request**

## Development Setup

```bash
# Clone repository
git clone https://github.com/Git-Lister/doctour.git
cd doctour

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings (Google style)

### Example:
```python
def process_remedy(name: str, ingredients: List[str]) -> Dict[str, Any]:
    """Process a medieval herbal remedy.
    
    Args:
        name: The remedy name in Middle English
        ingredients: List of herbal ingredients
    
    Returns:
        Dictionary with processed remedy data
    """
    pass
```

## Testing

- Write tests for new features
- Maintain >80% code coverage
- Test both positive and negative cases
- Include safety filter tests

## Historical Accuracy

When adding historical content:
1. **Cite sources** (pre-1410 only)
2. **Verify translations** of Middle English
3. **Cross-reference** with multiple medieval texts
4. **Document** any modern interpretations

## Safety Requirements

**CRITICAL**: All contributions must:
- Pass safety filter checks
- Include contraindication warnings
- Reference modern scientific validation where available
- Never recommend dangerous practices

### Safety Checklist
- [ ] No toxic substances
- [ ] No emergency medical scenarios
- [ ] Includes "not medical advice" disclaimer
- [ ] Cross-referenced with WHO/Cochrane databases

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Update `docs/` for architectural changes
- Include usage examples

## Areas for Contribution

### High Priority
- [ ] Historical text preprocessing
- [ ] Safety filter improvements
- [ ] Middle English language model fine-tuning
- [ ] Test coverage expansion

### Medium Priority
- [ ] UI/CLI enhancements
- [ ] Additional remedy database entries
- [ ] Performance optimizations
- [ ] Documentation improvements

### Research Contributions
- Medieval medical text analysis
- Historical linguistics research
- Cross-cultural medicine studies
- Evidence-based validation of traditional remedies

## Questions?

Open a discussion or reach out to the maintainers. We're happy to help!

---

**Remember**: This is an educational project. Never use it for actual medical advice.
