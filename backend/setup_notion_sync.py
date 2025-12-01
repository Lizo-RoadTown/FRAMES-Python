"""
Setup Script: Create Notion Databases and Initialize Sync
==========================================================

This script:
1. Creates all required Notion databases for FRAMES data
2. Performs initial sync from PostgreSQL → Notion
3. Saves database IDs for future sync operations
4. Creates a sync configuration file

USAGE:
    python backend/setup_notion_sync.py --parent-page-id <NOTION_PAGE_ID>

REQUIREMENTS:
    - NOTION_API_KEY in .env
    - Parent page must be shared with integration
    - PostgreSQL database must be populated with data
"""

import argparse
import json
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.notion_sync_service import NotionSyncService, sync_all_teams_to_notion
from backend.database import db
from backend.db_models import (
    TeamModel, FacultyModel, StudentModel, ProjectModel,
    InterfaceModel, University
)
from backend.app import app

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Setup Notion databases for FRAMES sync')
    parser.add_argument(
        '--parent-page-id',
        required=True,
        help='ID of Notion page to create databases in (must be shared with integration)'
    )
    parser.add_argument(
        '--config-file',
        default='backend/notion_sync_config.json',
        help='Path to save database ID configuration'
    )
    parser.add_argument(
        '--skip-initial-sync',
        action='store_true',
        help='Skip initial data sync (just create databases)'
    )
    
    args = parser.parse_args()
    
    print("🚀 FRAMES Notion Sync Setup")
    print("=" * 80)
    
    # Initialize service
    print("\n1️⃣ Initializing Notion sync service...")
    try:
        service = NotionSyncService()
        print("   ✅ Service initialized")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        sys.exit(1)
    
    # Create databases
    print(f"\n2️⃣ Creating Notion databases in page {args.parent_page_id}...")
    try:
        created_dbs = service.create_notion_databases(args.parent_page_id)
        print(f"   ✅ Created {len(created_dbs)} databases:")
        for db_name, db_id in created_dbs.items():
            print(f"      • {db_name:20s}: {db_id}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Save configuration
    print(f"\n3️⃣ Saving database IDs to {args.config_file}...")
    config = {
        "parent_page_id": args.parent_page_id,
        "created_at": str(datetime.now()),
        "databases": created_dbs,
        "model_mapping": {
            "TeamModel": created_dbs.get("Teams"),
            "FacultyModel": created_dbs.get("Faculty"),
            "StudentModel": created_dbs.get("Students"),
            "ProjectModel": created_dbs.get("Projects"),
            "InterfaceModel": created_dbs.get("Interfaces"),
            "University": created_dbs.get("Universities"),
        }
    }
    
    try:
        with open(args.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"   ✅ Configuration saved")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        sys.exit(1)
    
    # Initial sync
    if not args.skip_initial_sync:
        print("\n4️⃣ Performing initial data sync (PostgreSQL → Notion)...")
        
        with app.app_context():
            sync_operations = [
                ("Universities", University, created_dbs.get("Universities")),
                ("Projects", ProjectModel, created_dbs.get("Projects")),
                ("Teams", TeamModel, created_dbs.get("Teams")),
                ("Faculty", FacultyModel, created_dbs.get("Faculty")),
                ("Students", StudentModel, created_dbs.get("Students")),
                ("Interfaces", InterfaceModel, created_dbs.get("Interfaces")),
            ]
            
            for name, model_class, db_id in sync_operations:
                if not db_id:
                    print(f"   ⏭️  Skipping {name} (database not created)")
                    continue
                
                try:
                    # Count records in PostgreSQL
                    count = model_class.query.count()
                    print(f"\n   📊 {name}: {count} records in PostgreSQL")
                    
                    if count == 0:
                        print(f"      ⏭️  No data to sync")
                        continue
                    
                    # Sync each record
                    synced = 0
                    failed = 0
                    
                    for record in model_class.query.all():
                        try:
                            service.push_to_notion(model_class, record.id, db_id)
                            synced += 1
                            if synced % 10 == 0:
                                print(f"      ... synced {synced}/{count}")
                        except Exception as e:
                            failed += 1
                            print(f"      ⚠️  Failed to sync {record.id}: {str(e)[:50]}")
                    
                    print(f"      ✅ Synced {synced} records ({failed} failed)")
                    
                except Exception as e:
                    print(f"      ❌ Sync failed: {e}")
                    import traceback
                    traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Open Notion and verify databases were created")
    print("   2. Check that data was synced correctly")
    print("   3. Use sync service to keep data in sync:")
    print("\n      from backend.notion_sync_service import NotionSyncService")
    print("      service = NotionSyncService()")
    print("      # Push updates: service.push_to_notion(TeamModel, team_id, db_id)")
    print("      # Pull updates: service.pull_from_notion(db_id, TeamModel)")
    print("\n   4. Set up scheduled sync job (cron/celery) for continuous sync")


if __name__ == "__main__":
    from datetime import datetime
    main()
