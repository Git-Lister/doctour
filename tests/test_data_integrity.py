from pathlib import Path
from doctour.data_loader import load_herbs_csv

def test_herbs_csv_is_valid():
    path = Path("data/herbs/herbs.csv")
    herbs = load_herbs_csv(path)

    # Basic guarantees
    assert len(herbs) > 0
    names = {h.name for h in herbs}
    assert len(names) == len(herbs)  # no duplicate herb names

    # No obviously unsafe placeholders
    for h in herbs:
        assert "TODO" not in h.indications
        assert "FIXME" not in h.safety_notes
