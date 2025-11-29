#!/usr/bin/env python3
"""Rebuild modules whose source files are PDFs into JSON exports."""

from __future__ import annotations

import csv
import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from PyPDF2 import PdfReader


CSV_PATH = Path("data/projects/CADENCE/notion_modules_categorized.csv")
CONTENT_DIR = Path("temp_cadence_extract/content")
EXPORT_DIR = Path("modules/exports")

TARGET_TITLES = {
    "Outlook Calendar Tutorial",
    "Team Management",
    "Mission Definition",
    "UNP Audio Visual Recommendations",
    "CDH and Software",
    "NASA Power Systems for CubeSats",
    "UNP Electrical Power Systems",
    "EPS Design Presentation",
    "Communications Subsystem",
    "UNP COMM Subsystem",
    "UNP Mission Design Course",
    "GMAT Development User Guide",
    "GMAT Users Guide",
    "Satellite Operations",
    "ConOps and Experiment Plan",
    "Systems Engineering Part 1",
    "Systems Engineering Part 2",
    "Systems Engineering Part 3",
    "SCR/SRR Expectations",
    "Mission Assurance",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def read_csv_rows() -> Dict[str, Dict]:
    with CSV_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row["Title"]: row for row in reader}


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        chunks.append(text)
    return "\n".join(chunks)


def chunk_text(text: str, max_sections: int = 8) -> List[Dict[str, str]]:
    clean = re.sub(r"\r\n", "\n", text)
    clean = re.sub(r"\n{3,}", "\n\n", clean)
    paragraphs = [p.strip() for p in clean.split("\n\n") if p.strip()]

    sections = []
    for idx, paragraph in enumerate(paragraphs[:max_sections]):
        lines = [ln.strip() for ln in paragraph.splitlines() if ln.strip()]
        heading = lines[0][:80] if lines else f"Section {idx + 1}"
        sections.append(
            {
                "heading": heading,
                "content_markdown": paragraph,
                "word_count": len(paragraph.split()),
            }
        )
    if not sections:
        sections.append(
            {
                "heading": "Summary",
                "content_markdown": "Refer to the attached PDF for detailed content.",
                "word_count": 9,
            }
        )
    return sections


def build_module_record(row: Dict, text: str) -> Dict:
    title = row["Title"]
    slug = slugify(row["Title"])
    module_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"cadence://{title}".lower()))
    sections = chunk_text(text)

    tags = [tag.strip() for tag in (row.get("Tags") or "").split(";") if tag.strip()]
    prereqs = [req.strip() for req in (row.get("Prerequisites") or "").split(";") if req.strip()]

    return {
        "module_id": module_uuid,
        "slug": slug,
        "title": title,
        "description": row.get("Description", ""),
        "category": row.get("Category"),
        "discipline": row.get("Discipline"),
        "target_audience": row.get("Target Audience"),
        "estimated_minutes": int(row["Estimated Minutes"]) if row.get("Estimated Minutes") else None,
        "status": row.get("Status"),
        "difficulty": row.get("Difficulty"),
        "source_type": row.get("Source Type") or "PDF",
        "source_file": row.get("Source File"),
        "tags": tags,
        "prerequisites": prereqs,
        "sections": sections,
        "raw_markdown": "\n\n".join(section["content_markdown"] for section in sections),
        "record_source": {
            "type": "cadence-pdf-rebuild",
            "file": row.get("Source File"),
        },
    }


def main():
    rows = read_csv_rows()
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    for title in TARGET_TITLES:
        row = rows.get(title)
        if not row:
            print(f"[WARN] {title}: not found in CSV")
            continue

        source_file = row.get("Source File")
        if not source_file:
            print(f"[WARN] {title}: no Source File listed")
            continue

        pdf_path = CONTENT_DIR / source_file
        if not pdf_path.exists():
            stem = Path(source_file).stem
            candidates = list(CONTENT_DIR.glob(f"{stem}*.pdf"))
            if candidates:
                pdf_path = candidates[0]
            else:
                print(f"[WARN] {title}: source file missing ({pdf_path})")
                continue

        print(f"Rebuilding {title} from {source_file} ...", end=" ")
        text = extract_pdf_text(pdf_path)
        record = build_module_record(row, text)

        out_path = EXPORT_DIR / f"{record['slug']}.json"
        with out_path.open("w", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2, ensure_ascii=False)

        print("OK")


if __name__ == "__main__":
    main()
