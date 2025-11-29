"""
Deploy LMS modules from JSON files to PostgreSQL database.

This script reads module JSON files from data/modules/, validates them,
and inserts/updates them in the PostgreSQL database.

Usage:
    python scripts/deploy_modules_to_db.py
    python scripts/deploy_modules_to_db.py --module-file data/modules/intro-to-research.json
    python scripts/deploy_modules_to_db.py --dry-run  # Test without writing to DB

Environment variables required:
    DATABASE_URL - PostgreSQL connection string (Neon)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema not installed.")
    print("Run: pip install jsonschema")
    sys.exit(1)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import after adding to path
from backend.database import db
from backend.app import app
from shared.database.db_models import Module, ModuleSection

# Configuration
INPUT_DIR = PROJECT_ROOT / 'data' / 'modules'
SCHEMA_FILE = PROJECT_ROOT / 'schemas' / 'module_schema.json'


def validate_config():
    """Validate required configuration"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL not found in .env file")
        return False

    if not INPUT_DIR.exists():
        print(f"Error: Input directory not found: {INPUT_DIR}")
        print("Run: python scripts/export_modules_from_notion.py first")
        return False

    if not SCHEMA_FILE.exists():
        print(f"Error: Schema file not found: {SCHEMA_FILE}")
        return False

    return True


def load_json_schema() -> Dict:
    """Load the module JSON schema"""
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_module_data(module_data: Dict, schema: Dict) -> bool:
    """Validate module data against JSON schema"""
    try:
        jsonschema.validate(instance=module_data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"  ✗ Validation error: {e.message}")
        return False


def load_module_json(file_path: Path) -> Optional[Dict]:
    """Load and validate a module JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return None


def deploy_module_to_db(module_data: Dict, dry_run: bool = False) -> bool:
    """
    Deploy a module to the database.

    Args:
        module_data: Validated module data dict
        dry_run: If True, don't commit to database

    Returns:
        True if successful, False otherwise
    """
    try:
        module_id = module_data['module_id']

        # Check if module already exists
        existing = Module.query.filter_by(module_id=module_id).first()

        if existing:
            print(f"  → Module exists (ID: {existing.id}), updating...")
            module = existing

            # Update fields
            module.title = module_data['title']
            module.description = module_data.get('description')
            module.category = module_data.get('category')
            module.estimated_minutes = module_data.get('estimated_minutes')
            module.target_audience = module_data.get('target_audience')
            module.status = module_data.get('status', 'draft')
            module.notion_page_id = module_data.get('notion_page_id')
            module.content_source = module_data.get('content_source', 'notion')
            module.tags = module_data.get('tags', [])
            module.prerequisites = module_data.get('prerequisites', [])
            module.related_modules = module_data.get('related_modules', [])
            module.university_id = module_data.get('university_id')
            module.created_by_id = module_data.get('created_by_id')
            module.updated_at = datetime.utcnow()

            # Delete existing sections
            ModuleSection.query.filter_by(module_id=module.id).delete()

        else:
            print(f"  → Creating new module...")
            module = Module(
                module_id=module_id,
                title=module_data['title'],
                description=module_data.get('description'),
                category=module_data.get('category'),
                estimated_minutes=module_data.get('estimated_minutes'),
                target_audience=module_data.get('target_audience'),
                status=module_data.get('status', 'draft'),
                notion_page_id=module_data.get('notion_page_id'),
                content_source=module_data.get('content_source', 'notion'),
                tags=module_data.get('tags', []),
                prerequisites=module_data.get('prerequisites', []),
                related_modules=module_data.get('related_modules', []),
                university_id=module_data.get('university_id'),
                created_by_id=module_data.get('created_by_id'),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(module)

        # Flush to get the module.id for sections
        if not dry_run:
            db.session.flush()

        # Add sections
        sections_data = module_data.get('sections', [])
        print(f"  → Adding {len(sections_data)} sections...")

        for section_data in sections_data:
            section = ModuleSection(
                module_id=module.id,
                section_number=section_data['section_number'],
                section_type=section_data['section_type'],
                title=section_data.get('title', ''),
                content=section_data['content'],
                media_url=section_data.get('media_url'),
                duration_seconds=section_data.get('duration_seconds'),
                created_at=datetime.utcnow()
            )

            # Store record_map if present (for react-notion-x)
            if 'record_map' in section_data:
                # Note: You may need to add a record_map JSON column to ModuleSection
                # For now, we'll store it in the content field if section_type is notion_page
                if section_data['section_type'] == 'notion_page':
                    section.content = json.dumps(section_data['record_map'])

            db.session.add(section)

        if dry_run:
            print(f"  ✓ Dry run: Would deploy module '{module_data['title']}'")
            db.session.rollback()
        else:
            db.session.commit()
            print(f"  ✓ Deployed: {module_data['title']} (ID: {module.id})")

        return True

    except Exception as e:
        db.session.rollback()
        print(f"  ✗ Error deploying module: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def deploy_modules(module_file: Optional[str] = None, dry_run: bool = False):
    """
    Deploy modules from JSON files to database.

    Args:
        module_file: Optional path to specific JSON file
        dry_run: If True, validate but don't commit to database
    """
    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Load JSON schema
    print(f"Loading schema from: {SCHEMA_FILE}")
    schema = load_json_schema()

    # Get list of JSON files to process
    if module_file:
        json_files = [Path(module_file)]
        if not json_files[0].exists():
            print(f"Error: File not found: {module_file}")
            sys.exit(1)
    else:
        json_files = list(INPUT_DIR.glob('*.json'))

    if not json_files:
        print(f"No JSON files found in {INPUT_DIR}")
        print("Run: python scripts/export_modules_from_notion.py first")
        sys.exit(1)

    print(f"Found {len(json_files)} module files")
    if dry_run:
        print("⚠️  DRY RUN MODE - No changes will be written to database\n")

    # Process each file
    deployed_count = 0
    failed_count = 0

    with app.app_context():
        for i, file_path in enumerate(json_files, 1):
            print(f"\n[{i}/{len(json_files)}] Processing: {file_path.name}")

            # Load JSON
            module_data = load_module_json(file_path)
            if not module_data:
                failed_count += 1
                continue

            # Validate against schema
            if not validate_module_data(module_data, schema):
                failed_count += 1
                continue

            # Deploy to database
            if deploy_module_to_db(module_data, dry_run=dry_run):
                deployed_count += 1
            else:
                failed_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Deployment {'simulation' if dry_run else 'complete'}!")
    print(f"  Deployed: {deployed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {len(json_files)}")
    print(f"{'='*60}")

    if failed_count > 0:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Deploy LMS modules from JSON files to PostgreSQL'
    )
    parser.add_argument(
        '--module-file',
        help='Deploy specific module JSON file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate files without writing to database'
    )

    args = parser.parse_args()

    print("="*60)
    print("LMS Module Deployment to Database")
    print("="*60)

    deploy_modules(
        module_file=args.module_file,
        dry_run=args.dry_run
    )


if __name__ == '__main__':
    main()
