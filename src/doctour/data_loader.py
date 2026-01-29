from pathlib import Path
import csv
from typing import List
from pydantic import BaseModel, field_validator


class Herb(BaseModel):
    name: str
    latin_name: str
    qualities: str
    indications: str
    contraindications: str
    safety_notes: str

    @field_validator("qualities")
    @classmethod
    def validate_qualities(cls, v: str) -> str:
        allowed = {"warm_dry", "cool_dry", "cool_moist", "warm_moist"}
        if v not in allowed:
            raise ValueError(f"Unknown qualities: {v}")
        return v


def load_herbs_csv(path: Path) -> List[Herb]:
    herbs: List[Herb] = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip BOM and whitespace from keys
            normalized = {k.strip().lstrip("\ufeff"): v for k, v in row.items()}
            if not normalized.get("name"):
                continue
            herbs.append(Herb.model_validate(normalized))
    return herbs
