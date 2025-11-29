#!/usr/bin/env python3
"""Generate enhanced OAtutor-style modules from exports."""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from textwrap import shorten

EXPORT_DIR = Path("modules/exports")
OUTPUT_DIR = Path("modules/enhanced")
MAX_READING_CHARS = 1200


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_modules():
    modules = []
    for path in sorted(EXPORT_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
            data["__file"] = path
            modules.append(data)
    return modules


def extract_sentences(text: str) -> list[str]:
    if not text:
        return []
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def generate_objectives(module) -> list[dict]:
    sentences = extract_sentences(module.get("description") or "")
    objectives = []
    for sentence in sentences[:3]:
        objectives.append({
            "statement": sentence,
            "bloom_level": "Understand",
        })
    if not objectives:
        title = module.get("title", "Module")
        objectives = [
            {"statement": f"Describe the purpose of {title}.", "bloom_level": "Remember"},
            {"statement": f"Apply the workflow described in {title} to a realistic scenario.", "bloom_level": "Apply"},
        ]
    return objectives


def build_reading_section(module):
    content = module.get("raw_markdown") or module.get("description") or module.get("sections", [{}])[0].get("content_markdown")
    content = (content or "This module introduces key concepts.")
    snippet = shorten(content, MAX_READING_CHARS, placeholder="...")
    return {
        "title": "Overview",
        "type": "reading",
        "content_markdown": snippet,
        "assets": []
    }


def build_practice_steps(module):
    title = module.get("title", "the module")
    return [
        {
            "instruction": f"Review the resources associated with {title} and note key dependencies.",
            "check": "Did you capture the primary goals and blockers?",
            "hint": "Summarize the main objective in one sentence before proceeding.",
            "expected_duration_minutes": 10,
            "requires_review": False,
        },
        {
            "instruction": f"Apply the documented workflow on a realistic scenario related to {title}.",
            "check": "Can you demonstrate the workflow end-to-end?",
            "hint": "Start with a simplified scenario before scaling up.",
            "expected_duration_minutes": 15,
            "requires_review": True,
        }
    ]


def build_quiz(title):
    return [
        {
            "question": f"What is the primary objective of {title}?",
            "type": "multiple_choice",
            "options": ["To document context", "To apply procedures", "To track resources"],
            "correct": "To apply procedures",
            "explanation": "Each CADENCE module focuses on actionable procedures that support mission success.",
            "concept_tags": [slugify(title)],
            "difficulty": "Beginner"
        },
        {
            "question": f"Which artifact should you produce after completing {title}?",
            "type": "short_answer",
            "options": [],
            "correct": "A concise summary of actions, blockers, and next steps.",
            "explanation": "Every module concludes with documentation that feeds onboarding and analytics.",
            "concept_tags": ["documentation"],
            "difficulty": "Intermediate"
        }
    ]


def build_sections(module):
    title = module.get("title", "Module")
    sections = [build_reading_section(module)]
    sections.append(
        {
            "title": "Hands-on Practice",
            "type": "practice",
            "steps": build_practice_steps(module),
        }
    )
    sections.append(
        {
            "title": "Knowledge Check",
            "type": "quiz",
            "questions": build_quiz(title),
        }
    )
    sections.append(
        {
            "title": "Reflection",
            "type": "reflection",
            "prompts": [
                f"What worked well when completing {title}?",
                "What would you change for the next iteration?",
            ]
        }
    )
    return sections


def merge_metadata(module):
    data = module.copy()
    slug = module.get("slug") or slugify(module.get("title", str(uuid.uuid4())))
    module_id = module.get("module_id") or str(uuid.uuid5(uuid.NAMESPACE_URL, slug))
    return {
        "module_id": module_id,
        "title": module.get("title"),
        "slug": slug,
        "description": module.get("description") or "",
        "category": module.get("category") or "Getting Started",
        "discipline": module.get("discipline") or "General",
        "target_audience": module.get("target_audience") or module.get("targetAudience") or "Mixed",
        "estimated_minutes": module.get("estimated_minutes") or 45,
        "difficulty": module.get("difficulty") or "Beginner",
        "status": module.get("status") or "Draft",
        "source_type": module.get("source_type") or "Markdown",
        "source_file": module.get("source_file") or str(data.get("__file", "")),
        "tags": module.get("tags") or [],
        "prerequisites": module.get("prerequisites") or [],
        "record_source": module.get("record_source") or {"type": "enhanced"},
        "notion_page_id": module.get("notion_page_id"),
        "github_file": f"modules/enhanced/{slug}.json",
    }


def enhance_module(module):
    metadata = merge_metadata(module)
    enhanced = metadata.copy()
    enhanced["learning_objectives"] = generate_objectives(module)
    enhanced["concepts"] = metadata.get("tags", [])
    enhanced["sections"] = build_sections(module)
    enhanced["reflection_prompts"] = [
        "What insight will you share with your team?",
        "Which follow-up tasks should you track?",
    ]
    enhanced["race_metadata"] = {
        "ghost_data": [],
        "time_targets": {
            "beginner": metadata["estimated_minutes"] * 1.5,
            "intermediate": metadata["estimated_minutes"],
            "advanced": int(metadata["estimated_minutes"] * 0.75),
        },
        "checkpoints": [
            {"name": "Plan", "order": 1},
            {"name": "Execute", "order": 2},
            {"name": "Document", "order": 3},
        ],
    }
    return enhanced


def save_module(module):
    path = OUTPUT_DIR / f"{module['slug']}.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(module, handle, indent=2, ensure_ascii=False)
    return path


def main():
    ensure_output_dir()
    modules = load_modules()
    for module in modules:
        enhanced = enhance_module(module)
        out_path = save_module(enhanced)
        print(f"Enhanced {module.get('title')} -> {out_path}")


if __name__ == "__main__":
    main()
