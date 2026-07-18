from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "notebook_inventory.csv"


def first_markdown_heading(nb: dict) -> str:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = "".join(cell.get("source", []))
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return ""


def notebook_stats(path: Path) -> dict:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    markdown_cells = [c for c in cells if c.get("cell_type") == "markdown"]
    error_count = 0
    output_count = 0
    executed_count = 0
    for cell in code_cells:
        if cell.get("execution_count") is not None:
            executed_count += 1
        outputs = cell.get("outputs", []) or []
        output_count += len(outputs)
        for output in outputs:
            if output.get("output_type") == "error":
                error_count += 1

    return {
        "file": path.name,
        "size_kb": round(path.stat().st_size / 1024, 1),
        "cells": len(cells),
        "markdown_cells": len(markdown_cells),
        "code_cells": len(code_cells),
        "executed_code_cells": executed_count,
        "outputs": output_count,
        "errors": error_count,
        "title": first_markdown_heading(nb),
    }


def main() -> None:
    rows = [notebook_stats(path) for path in sorted(ROOT.glob("*.ipynb"))]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(rows)} notebooks)")


if __name__ == "__main__":
    main()
