#!/usr/bin/env python3
"""CADENCE export ingestion pipeline for Agent Gamma.

This utility reads the large CADENCE Notion export, extracts module markdown
files listed in ``notion_modules_categorized.csv`` and converts them into the
JSON structure that the GitHub → Postgres pipeline expects.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import zipfile

EXPORT_PATH = Path("temp_cadence_extract/ExportBlock-e881308d-93d4-492e-bdac-6d92e7bb342e-Part-1.zip")
MANIFEST_CSV = Path("data/projects/CADENCE/notion_modules_categorized.csv")
OUTPUT_DIR = Path("modules/exports")


@dataclass
class ModuleMeta:
    title: str
    category: str
    description: str
    target_audience: str
    discipline: str
    estimated_minutes: Optional[int]
    status: str
    difficulty: str
    source_type: str
    source_file: str
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)


def normalize_label(value: str) -> str:
    return (value or "").strip()


def parse_manifest(csv_path: Path) -> List[ModuleMeta]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Manifest missing: {csv_path}")

    modules: List[ModuleMeta] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            estimated_raw = normalize_label(row.get("Estimated Minutes", ""))
            try:
                estimated = int(estimated_raw) if estimated_raw else None
            except ValueError:
                estimated = None

            modules.append(
                ModuleMeta(
                    title=normalize_label(row.get("Title", "")),
                    category=normalize_label(row.get("Category", "")),
                    description=normalize_label(row.get("Description", "")),
                    target_audience=normalize_label(row.get("Target Audience", "")),
                    discipline=normalize_label(row.get("Discipline", "")),
                    estimated_minutes=estimated,
                    status=normalize_label(row.get("Status", "")) or "Draft",
                    difficulty=normalize_label(row.get("Difficulty", "")),
                    source_type=normalize_label(row.get("Source Type", "")),
                    source_file=normalize_label(row.get("Source File", row.get("Title", ""))),
                    tags=[normalize_label(tag) for tag in (row.get("Tags") or "").split(";") if normalize_label(tag)],
                    prerequisites=[
                        normalize_label(req) for req in (row.get("Prerequisites") or "").split(";") if normalize_label(req)
                    ],
                )
            )
    return modules


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_label(value).lower())
    return re.sub(r"-{2,}", "-", slug).strip("-")


def normalize_export_name(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"\s+[0-9a-f]{32}$", "", stem, flags=re.IGNORECASE)
    return slugify(stem)


def parse_markdown_sections(markdown: str) -> List[Dict[str, str]]:
    sections: List[Dict[str, str]] = []
    current_heading = "Overview"
    current_lines: List[str] = []

    heading_pattern = re.compile(r"^(#{1,3})\s+(.*)")

    for line in markdown.splitlines():
        match = heading_pattern.match(line)
        if match:
            if current_lines:
                sections.append(
                    {
                        "heading": current_heading,
                        "content_markdown": "\n".join(current_lines).strip(),
                        "word_count": len(" ".join(current_lines).split()),
                    }
                )
            current_heading = match.group(2).strip() or current_heading
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines or not sections:
        sections.append(
            {
                "heading": current_heading,
                "content_markdown": "\n".join(current_lines).strip(),
                "word_count": len(" ".join(current_lines).split()),
            }
        )

    return sections


def locate_markdown_entry(manifest_source: str, md_index: Dict[str, str]) -> Optional[str]:
    candidates = []
    slug = slugify(Path(manifest_source).stem)
    for normalized_name, zip_entry in md_index.items():
        if normalized_name == slug:
            return zip_entry
        if normalized_name.startswith(slug):
            candidates.append(zip_entry)
    return candidates[0] if candidates else None


def build_md_index(zip_path: Path) -> Dict[str, str]:
    if not zip_path.exists():
        raise FileNotFoundError(f"Export archive missing: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as archive:
        return {
            normalize_export_name(name): name
            for name in archive.namelist()
            if name.lower().endswith(".md")
        }


def create_module_record(meta: ModuleMeta, markdown: str, source_entry: str) -> Dict[str, object]:
    module_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"cadence://{meta.title}".lower()))
    slug = slugify(meta.title) or slugify(meta.source_file)
    sections = parse_markdown_sections(markdown)

    return {
        "module_id": module_uuid,
        "slug": slug,
        "title": meta.title,
        "description": meta.description,
        "category": meta.category,
        "discipline": meta.discipline,
        "target_audience": meta.target_audience,
        "estimated_minutes": meta.estimated_minutes,
        "status": meta.status or "Draft",
        "difficulty": meta.difficulty,
        "source_type": meta.source_type or "Markdown",
        "source_file": meta.source_file,
        "tags": meta.tags,
        "prerequisites": meta.prerequisites,
        "sections": sections,
        "raw_markdown": markdown.strip(),
        "record_source": {
            "type": "cadence-notion-export",
            "archive": str(EXPORT_PATH),
            "entry_name": source_entry,
        },
    }


def ingest_modules(limit: Optional[int] = None, only_titles: Optional[Iterable[str]] = None, overwrite: bool = False):
    modules = parse_manifest(MANIFEST_CSV)
    selected_titles = {title.lower() for title in only_titles} if only_titles else None
    md_index = build_md_index(EXPORT_PATH)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    missing_files: List[str] = []

    with zipfile.ZipFile(EXPORT_PATH, "r") as archive:
        for meta in modules:
            if selected_titles and meta.title.lower() not in selected_titles:
                continue
            entry = locate_markdown_entry(meta.source_file or meta.title, md_index)
            if not entry:
                missing_files.append(meta.title)
                continue

            markdown = archive.read(entry).decode("utf-8")
            record = create_module_record(meta, markdown, entry)
            out_path = OUTPUT_DIR / f"{record['slug']}.json"

            if out_path.exists() and not overwrite:
                print(f"Skipping existing module: {out_path.name}")
            else:
                with out_path.open("w", encoding="utf-8") as handle:
                    json.dump(record, handle, indent=2, ensure_ascii=False)
                print(f"Saved {meta.title} -> {out_path}")
            processed += 1
            if limit and processed >= limit:
                break

    if missing_files:
        print("\nModules missing markdown exports:")
        for title in missing_files:
            print(f" - {title}")

    print(f"\nProcessed {processed} modules. Output directory: {OUTPUT_DIR}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert CADENCE Notion export markdown into module JSON files.")
    parser.add_argument("--limit", type=int, help="Limit the number of modules to ingest.")
    parser.add_argument("--module", action="append", dest="modules", help="Only process modules with matching titles.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing JSON files.")
    return parser


def main():
    args = build_parser().parse_args()
    ingest_modules(limit=args.limit, only_titles=args.modules, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
