"""
Export LMS modules from Notion to JSON files.

This script fetches module data from the Notion Module Library database,
transforms it into the JSON schema format, validates it, and saves each
module as a separate JSON file in data/modules/

Usage:
    python scripts/export_modules_from_notion.py
    python scripts/export_modules_from_notion.py --module-id <notion_page_id>

Environment variables required:
    NOTION_API_KEY - Notion integration API key
    NOTION_MODULE_DB_ID - Notion Module Library database ID
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from notion_client import Client
    import jsonschema
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install notion-client jsonschema")
    sys.exit(1)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_MODULE_DB_ID = os.getenv('NOTION_MODULE_DB_ID')
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'modules'
SCHEMA_FILE = PROJECT_ROOT / 'schemas' / 'module_schema.json'

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def validate_config():
    """Validate required configuration"""
    if not NOTION_API_KEY:
        print("Error: NOTION_API_KEY not found in .env file")
        return False

    if not NOTION_MODULE_DB_ID:
        print("Error: NOTION_MODULE_DB_ID not found in .env file")
        print("Run: python scripts/get_notion_db_ids.py to get your database IDs")
        return False

    if not SCHEMA_FILE.exists():
        print(f"Error: Schema file not found at {SCHEMA_FILE}")
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
        print(f"Validation error: {e.message}")
        print(f"Path: {' -> '.join(str(p) for p in e.path)}")
        return False


def extract_notion_text(rich_text: List[Dict]) -> str:
    """Extract plain text from Notion rich text array"""
    if not rich_text:
        return ""
    return "".join([block.get('plain_text', '') for block in rich_text])


def extract_select_value(select_prop: Optional[Dict]) -> Optional[str]:
    """Extract value from Notion select property"""
    if not select_prop or 'select' not in select_prop:
        return None
    select = select_prop['select']
    return select['name'] if select else None


def extract_multi_select_values(multi_select_prop: Optional[Dict]) -> List[str]:
    """Extract values from Notion multi-select property"""
    if not multi_select_prop or 'multi_select' not in multi_select_prop:
        return []
    return [item['name'] for item in multi_select_prop['multi_select']]


def fetch_notion_page_content(notion: Client, page_id: str) -> Dict:
    """
    Fetch full Notion page content including blocks.
    Returns the recordMap structure for react-notion-x rendering.
    """
    try:
        # Fetch the page
        page = notion.pages.retrieve(page_id=page_id)

        # Fetch all blocks (content) from the page
        blocks = []
        has_more = True
        start_cursor = None

        while has_more:
            response = notion.blocks.children.list(
                block_id=page_id,
                start_cursor=start_cursor,
                page_size=100
            )
            blocks.extend(response['results'])
            has_more = response['has_more']
            start_cursor = response.get('next_cursor')

        # Build a simplified recordMap structure
        # Note: This is a simplified version. For full react-notion-x compatibility,
        # you may need to use the official Notion API or notion-client package
        record_map = {
            'block': {
                page_id: {
                    'value': page
                }
            },
            'collection': {},
            'collection_view': {},
            'notion_user': {}
        }

        # Add all blocks to the recordMap
        for block in blocks:
            block_id = block['id']
            record_map['block'][block_id] = {
                'value': block
            }

        return record_map

    except Exception as e:
        print(f"Error fetching page content for {page_id}: {str(e)}")
        return {}


def convert_notion_page_to_module(notion: Client, page: Dict, schema: Dict) -> Optional[Dict]:
    """
    Convert a Notion database page to module JSON format.

    Args:
        notion: Notion client
        page: Notion page object from database query
        schema: JSON schema for validation

    Returns:
        Module data dict or None if conversion fails
    """
    try:
        props = page['properties']
        page_id = page['id'].replace('-', '')

        # Extract properties from Notion database
        title = extract_notion_text(props.get('Title', {}).get('title', []))
        if not title:
            title = extract_notion_text(props.get('Name', {}).get('title', []))

        description = extract_notion_text(props.get('Description', {}).get('rich_text', []))
        category = extract_select_value(props.get('Category'))
        status = extract_select_value(props.get('Status'))
        target_audience = extract_select_value(props.get('Target Audience'))

        # Extract numeric properties
        estimated_minutes = None
        if 'Estimated Time (min)' in props:
            est_time = props['Estimated Time (min)'].get('number')
            if est_time:
                estimated_minutes = int(est_time)

        # Extract tags
        tags = extract_multi_select_values(props.get('Tags'))

        # Extract relations
        prerequisites = []
        if 'Prerequisites' in props and 'relation' in props['Prerequisites']:
            prerequisites = [rel['id'].replace('-', '') for rel in props['Prerequisites']['relation']]

        related_modules = []
        if 'Related Modules' in props and 'relation' in props['Related Modules']:
            related_modules = [rel['id'].replace('-', '') for rel in props['Related Modules']['relation']]

        # Extract ownership
        created_by_id = None
        if 'Team Lead' in props and 'people' in props['Team Lead']:
            people = props['Team Lead']['people']
            if people:
                created_by_id = people[0].get('id', '')

        university_id = extract_select_value(props.get('University'))

        # Generate module_id from title
        module_id = title.lower().replace(' ', '-').replace('/', '-')
        # Remove special characters
        module_id = ''.join(c for c in module_id if c.isalnum() or c == '-')

        # Fetch full page content
        print(f"  Fetching content for: {title}")
        record_map = fetch_notion_page_content(notion, page['id'])

        # Create module data structure
        module_data = {
            'module_id': module_id,
            'title': title,
            'description': description or f"Learn about {title}",
            'category': category or 'fundamentals',
            'estimated_minutes': estimated_minutes or 30,
            'target_audience': target_audience or 'all',
            'status': status or 'draft',
            'notion_page_id': page_id,
            'content_source': 'notion',
            'tags': tags,
            'prerequisites': prerequisites,
            'related_modules': related_modules,
            'sections': []
        }

        if university_id:
            module_data['university_id'] = university_id

        if created_by_id:
            module_data['created_by_id'] = created_by_id

        # Create a single section with the full Notion page content
        section = {
            'section_number': 1,
            'section_type': 'notion_page',
            'title': title,
            'content': f"Notion page: {title}",
            'record_map': record_map
        }

        module_data['sections'].append(section)

        # Validate against schema
        if validate_module_data(module_data, schema):
            return module_data
        else:
            print(f"  Validation failed for: {title}")
            return None

    except Exception as e:
        print(f"Error converting page to module: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def export_modules(module_id: Optional[str] = None):
    """
    Export modules from Notion to JSON files.

    Args:
        module_id: Optional specific Notion page ID to export
    """
    # Validate configuration
    if not validate_config():
        sys.exit(1)

    # Load JSON schema
    print(f"Loading schema from: {SCHEMA_FILE}")
    schema = load_json_schema()

    # Initialize Notion client
    print("Connecting to Notion...")
    notion = Client(auth=NOTION_API_KEY)

    try:
        if module_id:
            # Export specific module
            print(f"\nExporting specific module: {module_id}")
            page = notion.pages.retrieve(page_id=module_id)
            module_data = convert_notion_page_to_module(notion, page, schema)

            if module_data:
                output_file = OUTPUT_DIR / f"{module_data['module_id']}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(module_data, f, indent=2, ensure_ascii=False)
                print(f"✓ Exported to: {output_file}")
            else:
                print("✗ Export failed")
                sys.exit(1)

        else:
            # Export all modules from database
            print(f"Fetching modules from database: {NOTION_MODULE_DB_ID}")

            # Query the database
            results = []
            has_more = True
            start_cursor = None

            while has_more:
                response = notion.databases.query(
                    database_id=NOTION_MODULE_DB_ID,
                    start_cursor=start_cursor,
                    page_size=100
                )
                results.extend(response['results'])
                has_more = response['has_more']
                start_cursor = response.get('next_cursor')

            print(f"Found {len(results)} modules in database")

            # Convert and export each module
            exported_count = 0
            failed_count = 0

            for i, page in enumerate(results, 1):
                print(f"\nProcessing {i}/{len(results)}...")
                module_data = convert_notion_page_to_module(notion, page, schema)

                if module_data:
                    output_file = OUTPUT_DIR / f"{module_data['module_id']}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(module_data, f, indent=2, ensure_ascii=False)
                    print(f"  ✓ Exported to: {output_file}")
                    exported_count += 1
                else:
                    failed_count += 1

            print(f"\n{'='*60}")
            print(f"Export complete!")
            print(f"  Exported: {exported_count}")
            print(f"  Failed: {failed_count}")
            print(f"  Output directory: {OUTPUT_DIR}")
            print(f"{'='*60}")

    except Exception as e:
        print(f"\nError during export: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Export LMS modules from Notion to JSON files'
    )
    parser.add_argument(
        '--module-id',
        help='Export specific module by Notion page ID'
    )

    args = parser.parse_args()

    print("="*60)
    print("LMS Module Export from Notion")
    print("="*60)

    export_modules(module_id=args.module_id)


if __name__ == '__main__':
    main()
