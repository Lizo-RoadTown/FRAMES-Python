# FRAMES Notion Sync Service

## Overview

Bidirectional data synchronization between PostgreSQL (source of truth) and Notion (Team Lead interface).

**Purpose:** Enable Team Leads to view and edit FRAMES data in Notion while maintaining PostgreSQL as the authoritative database for backend operations.

## Architecture

```
PostgreSQL Database (40 tables)
        ↕ Bidirectional Sync
Notion Databases (7 core entities)
        ↓ User-Friendly Interface
    Team Leads
```

### Components

- **`notion_sync_service.py`**: Core sync engine with push/pull operations
- **`setup_notion_sync.py`**: One-time setup script to create Notion databases
- **`notion_sync_config.json`**: Stores database IDs after setup (auto-generated)

## Quick Start

### 1. Prerequisites

```bash
# Ensure .env has NOTION_API_KEY
echo "NOTION_API_KEY=ntn_xxx..." >> .env

# Ensure PostgreSQL database is populated
python check_neon_data.py
```

### 2. Create a Notion Page

1. Go to Notion workspace
2. Create a new page (e.g., "FRAMES Data Sync")
3. Copy the page ID from URL: `https://notion.so/workspace/<PAGE_ID>?...`
4. **CRITICAL:** Share page with integration (click Share → Add integration)

### 3. Run Setup

```bash
cd /workspaces/FRAMES-Python

# Create databases and perform initial sync
python backend/setup_notion_sync.py --parent-page-id <NOTION_PAGE_ID>

# Or skip initial sync (just create empty databases)
python backend/setup_notion_sync.py --parent-page-id <PAGE_ID> --skip-initial-sync
```

**Expected Output:**
```
🚀 FRAMES Notion Sync Setup
================================================================================
1️⃣ Initializing Notion sync service...
   ✅ Service initialized
2️⃣ Creating Notion databases in page abc123...
   ✅ Created 7 databases:
      • Teams              : def456...
      • Faculty            : ghi789...
      • Students           : jkl012...
      • Projects           : mno345...
      • Interfaces         : pqr678...
      • Universities       : stu901...
      • Modules            : vwx234...
3️⃣ Saving database IDs to backend/notion_sync_config.json...
   ✅ Configuration saved
4️⃣ Performing initial data sync (PostgreSQL → Notion)...
   📊 Universities: 8 records in PostgreSQL
      ✅ Synced 8 records (0 failed)
   📊 Teams: 15 records in PostgreSQL
      ✅ Synced 15 records (0 failed)
   ...
================================================================================
✅ Setup complete!
```

### 4. Verify in Notion

Open your Notion page and you should see 7 new databases populated with data from PostgreSQL!

## Usage

### Push Updates (PostgreSQL → Notion)

When backend data changes, push to Notion:

```python
from backend.notion_sync_service import NotionSyncService
from backend.db_models import TeamModel
import json

# Load database IDs from config
with open('backend/notion_sync_config.json') as f:
    config = json.load(f)

# Initialize service
service = NotionSyncService()

# Push single team update
team_id = "team_123"
teams_db_id = config['databases']['Teams']
service.push_to_notion(TeamModel, team_id, teams_db_id)
```

### Pull Updates (Notion → PostgreSQL)

When Team Leads edit in Notion, pull changes:

```python
from backend.notion_sync_service import NotionSyncService
from backend.db_models import StudentModel
import json

# Load config
with open('backend/notion_sync_config.json') as f:
    config = json.load(f)

# Initialize service
service = NotionSyncService()

# Pull all student updates from Notion
students_db_id = config['databases']['Students']
synced_count = service.pull_from_notion(students_db_id, StudentModel)
print(f"Synced {synced_count} students from Notion")
```

### Scheduled Sync

For continuous sync, set up a cron job or Celery task:

```python
# backend/scheduled_sync.py (example)
from notion_sync_service import NotionSyncService
from db_models import TeamModel, StudentModel, FacultyModel
import json

def sync_all_bidirectional():
    """Run full bidirectional sync"""
    with open('backend/notion_sync_config.json') as f:
        config = json.load(f)
    
    service = NotionSyncService()
    
    # Pull changes from Notion
    for model_name, model_class in [
        ('Teams', TeamModel),
        ('Students', StudentModel),
        ('Faculty', FacultyModel),
    ]:
        db_id = config['databases'][model_name]
        count = service.pull_from_notion(db_id, model_class)
        print(f"Pulled {count} {model_name} from Notion")
    
    # Push any PostgreSQL changes to Notion
    # (implement as needed based on updated_at timestamps)

# Run every 5 minutes
if __name__ == "__main__":
    sync_all_bidirectional()
```

**Cron example:**
```bash
*/5 * * * * cd /workspaces/FRAMES-Python && python backend/scheduled_sync.py
```

## Database Schemas

### Teams Database

| Notion Property | Type | Maps to PostgreSQL |
|-----------------|------|-------------------|
| Name | Title | team.name |
| postgres_id | Text | team.id |
| university_id | Text | team.university_id |
| team_type | Select | team.team_type |
| status | Select | team.status |
| project_id | Text | team.project_id |
| created_at | Date | team.created_at |
| last_synced | Date | auto-generated |
| sync_status | Select | auto-managed |

**Select Options:**
- team_type: design, analysis, testing, integration
- status: active, completed, on_hold

### Students Database

| Notion Property | Type | Maps to PostgreSQL |
|-----------------|------|-------------------|
| Name | Title | student.name |
| postgres_id | Text | student.id |
| university_id | Text | student.university_id |
| email | Email | student.email |
| team_id | Text | student.team_id |
| status | Select | student.status |
| terms_remaining | Number | student.terms_remaining |
| created_at | Date | student.created_at |
| last_synced | Date | auto-generated |
| sync_status | Select | auto-managed |

**Select Options:**
- status: incoming, established, outgoing, alumni

### Interfaces Database (NDA Theory)

| Notion Property | Type | Maps to PostgreSQL |
|-----------------|------|-------------------|
| Name | Title | interface.name |
| postgres_id | Text | interface.id |
| from_university | Text | interface.from_university |
| to_university | Text | interface.to_university |
| from_team_id | Text | interface.from_team_id |
| to_team_id | Text | interface.to_team_id |
| bond_type | Select | interface.bond_type |
| energy_loss | Number | interface.energy_loss |
| is_cross_university | Checkbox | interface.is_cross_university |
| created_at | Date | interface.created_at |
| last_synced | Date | auto-generated |
| sync_status | Select | auto-managed |

**Select Options:**
- bond_type: codified-strong, institutional-weak, fragile-temporary

**Energy Loss:** 0-100 (knowledge transfer friction)

### Other Databases

See `notion_sync_service.py` for complete schemas:
- Faculty (email, department, role)
- Projects (description, status, dates)
- Universities (code, full_name)
- Modules (title, category, difficulty)

## Integration with Flask API

Add sync triggers to existing API endpoints:

```python
# backend/app.py

from .notion_sync_service import NotionSyncService
import json

# Load config once at startup
with open('backend/notion_sync_config.json') as f:
    NOTION_CONFIG = json.load(f)

notion_service = NotionSyncService()

@app.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    team = TeamModel.query.get_or_404(team_id)
    data = request.json
    
    # Update PostgreSQL
    team.name = data.get('name', team.name)
    team.status = data.get('status', team.status)
    db.session.commit()
    
    # Sync to Notion (async recommended)
    try:
        teams_db_id = NOTION_CONFIG['databases']['Teams']
        notion_service.push_to_notion(TeamModel, team_id, teams_db_id)
    except Exception as e:
        logger.warning(f"Notion sync failed: {e}")
        # Don't fail the request if Notion sync fails
    
    return jsonify(team.to_dict())
```

## Conflict Resolution

**Strategy:** Last-write-wins

- Each record tracks `last_synced` timestamp
- Updates compare timestamps to detect conflicts
- In case of conflict, most recent edit wins
- All changes logged to `audit_logs` table (existing FRAMES feature)

**Future Enhancement:** Could implement merge strategies or conflict flags for human review.

## Sync Status Tracking

Each Notion record has `sync_status` property:

- **synced** (green): Successfully synced, no pending changes
- **pending** (yellow): Changes made in Notion, not yet pulled to PostgreSQL
- **conflict** (red): Conflicting edits detected, manual review needed

## Limitations & Considerations

### Rate Limits

Notion API: 3 requests/second

**Mitigation:**
- Batch operations where possible
- Implement exponential backoff on rate limit errors
- Use incremental sync (only changed records)

### Data Types

Some PostgreSQL types don't have direct Notion equivalents:

- **JSON fields**: Converted to rich_text (not editable in Notion)
- **Arrays**: Converted to multi_select (limited to predefined options)
- **UUIDs**: Converted to text strings

### University Filtering

Multi-university data model requires filtering:

```python
# Only sync data for specific university
teams = TeamModel.query.filter_by(university_id='CalPolyPomona').all()
for team in teams:
    service.push_to_notion(TeamModel, team.id, teams_db_id)
```

### PROVES Project (Special Case)

PROVES project has `university_id=NULL` (shared collaborative nucleus):

```python
# Sync PROVES data separately
proves_teams = TeamModel.query.filter_by(university_id=None).all()
```

## Troubleshooting

### Error: "Could not find database"

**Cause:** Integration doesn't have access to page/database

**Fix:** Share the parent page with integration in Notion

### Error: "NOTION_API_KEY not found"

**Cause:** Missing environment variable

**Fix:** Add to `.env`:
```bash
NOTION_API_KEY=ntn_xxx...
```

### Sync appears stuck

**Cause:** Rate limiting or large dataset

**Fix:**
- Check Notion API rate limit headers
- Implement batch processing with delays
- Run initial sync in smaller chunks

### Data not appearing in Notion

**Cause:** Property type mismatch or validation error

**Fix:**
- Check logs for specific property errors
- Verify PostgreSQL data matches Notion property types
- Use `_get_notion_property_value()` debug mode

## Future Enhancements

- [ ] Webhook support for real-time Notion → PostgreSQL sync
- [ ] Async sync operations (Celery tasks)
- [ ] Selective field sync (sync only specific properties)
- [ ] Merge conflict UI for manual resolution
- [ ] Sync analytics dashboard
- [ ] Multi-database relation support (link Teams to Projects)
- [ ] Attachment/file syncing
- [ ] Formula properties for calculated fields

## Related Documentation

- **Backend API:** `backend/LMS_API_README.md`
- **Database Models:** `backend/db_models.py`
- **Notion Integration:** `canon/NOTION_INTEGRATION.md`
- **Multi-University Model:** `README.md` (Architecture section)

## Support

For sync issues:
1. Check logs: `backend/notion_sync.log` (if logging configured)
2. Verify database connectivity: `python check_neon_data.py`
3. Test Notion API access: `python -c "from backend.notion_sync_service import NotionSyncService; s = NotionSyncService()"`
4. Review `notion_sync_config.json` for correct database IDs
