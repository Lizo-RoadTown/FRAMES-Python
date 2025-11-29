#!/usr/bin/env python3
"""Audit module exports and summarize completeness."""

import json
from pathlib import Path

EXPORT_DIR = Path("modules/exports")
OUTPUT_PATH = Path("module_library_audit.json")


def load_modules():
    modules = []
    for path in sorted(EXPORT_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
            data["__file"] = path.name
            modules.append(data)
    return modules


def classify(module):
    sections = module.get("sections") or []
    objectives = module.get("learning_objectives") or module.get("learningObjectives") or []
    has_description = bool(module.get("description"))
    has_metadata = bool(module.get("category") and module.get("difficulty") and module.get("estimated_minutes"))
    if len(sections) >= 3 and objectives and has_description and has_metadata:
        return "complete"
    if sections and has_description:
        return "partial"
    return "stub"


def section_stats(sections):
    types = {}
    for section in sections:
        stype = section.get("type") or "unknown"
        types[stype] = types.get(stype, 0) + 1
    return types


def audit():
    modules = load_modules()
    summary = {
        "total_modules": len(modules),
        "complete": 0,
        "partial": 0,
        "stub": 0,
        "missing_description": 0,
        "missing_sections": 0,
        "missing_metadata": 0,
        "missing_objectives": 0,
    }
    details = []
    for module in modules:
        sections = module.get("sections") or []
        classification = classify(module)
        summary[classification] += 1
        if not module.get("description"):
            summary["missing_description"] += 1
        if not sections:
            summary["missing_sections"] += 1
        if not (module.get("category") and module.get("difficulty") and module.get("estimated_minutes")):
            summary["missing_metadata"] += 1
        objectives = module.get("learning_objectives") or []
        if not objectives:
            summary["missing_objectives"] += 1
        details.append(
            {
                "title": module.get("title"),
                "file": module["__file"],
                "classification": classification,
                "section_count": len(sections),
                "section_types": section_stats(sections),
                "has_description": bool(module.get("description")),
                "has_metadata": bool(module.get("category") and module.get("difficulty") and module.get("estimated_minutes")),
                "has_objectives": bool(objectives),
            }
        )
    report = {"summary": summary, "modules": details}
    OUTPUT_PATH.write_text(json.dumps(report, indent=2))
    print(f"Audit complete. Summary saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    audit()
