# Desktop Claude Setup Guide

This guide is specifically for using Desktop Claude (not VS Code Claude) with the FRAMES-Python project.

## Connection Status

### ✅ Neon Database - CONNECTED
- **Status**: Successfully connected
- **Database URL**: `postgresql://[USERNAME]:[PASSWORD]@[HOST]/neondb?sslmode=require`
- **Current Tables**: 1 table (`playing_with_neon`)
- **Next Step**: Bootstrap the full database schema

### ✅ Notion API - CONNECTED
- **Status**: Successfully connected
- **API Key**: `[REDACTED - See .env file]`
- **Workspace Users**: 3 users found
- **Current Databases**: 0 (workspace is empty)
- **Next Step**: Set up Notion databases for FRAMES data

## Quick Test

To verify connections at any time:

```bash
cd C:\Users\LizO5\Frames-Python\FRAMES-Python
python test_connections.py
```

## Next Steps

### 1. Bootstrap Neon Database

The Neon database currently has minimal schema. To set up the full FRAMES schema:

```bash
cd C:\Users\LizO5\Frames-Python\FRAMES-Python
python scripts/bootstrap_db.py
```

This will create all necessary tables:
- universities
- teams
- students
- faculty
- projects
- modules
- interfaces
- audit_logs
- And 30+ more tables for the full FRAMES system

### 2. Set Up Notion Sync (Optional)

To create Notion databases for team lead interface:

```bash
# First, create a page in Notion and share it with your integration
# Then run:
python backend/setup_notion_sync.py --parent-page-id <YOUR_NOTION_PAGE_ID>
```

See `backend/NOTION_SYNC_README.md` for detailed instructions.

### 3. Seed Sample Data (Optional)

To populate the database with sample data for testing:

```bash
python backend/seed_multi_university.py
```

## Environment Configuration

Your `.env` file is already configured with:
- ✅ Neon database URL
- ✅ Notion API key
- ✅ Neon API key (for project management)

## Key Differences: Desktop Claude vs VS Code Claude

### Desktop Claude (This Environment)
- Runs on your local machine
- Has direct access to your file system
- Can run Python scripts directly
- Better for database operations and API testing
- Good for data migration, setup, and admin tasks

### VS Code Claude
- Runs inside VS Code
- Integrated with your editor
- Better for code editing and development
- Good for feature development and debugging

## Available Scripts

### Database Operations
- `test_connections.py` - Test Neon and Notion connections
- `check_neon_data.py` - Inspect Neon database contents
- `scripts/bootstrap_db.py` - Create database schema
- `scripts/check_db_tables.py` - List all database tables
- `backend/seed_multi_university.py` - Load sample data

### Notion Operations
- `backend/setup_notion_sync.py` - Set up Notion databases
- `backend/notion_sync_service.py` - Sync service (import for use)
- `scripts/notion_continuous_sync.py` - Continuous sync daemon
- `scripts/create_notion_workspace.py` - Create workspace structure

### Migration Scripts
- `backend/run_migration.py` - Run database migrations
- `apps/research-analytics/backend/migrate_to_postgres.py` - Migrate from SQLite

## Common Tasks

### Check Database Schema
```bash
python scripts/check_db_tables.py
```

### View Database Data
```bash
python check_neon_data.py
```

### Test API Endpoints
```bash
python backend/test_endpoints.py
```

### Start Flask Backend
```bash
cd backend
python app.py
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're in the correct directory:
```bash
cd C:\Users\LizO5\Frames-Python\FRAMES-Python
```

### Database Connection Errors
- Verify `.env` file exists and has DATABASE_URL
- Test connection with `python test_connections.py`
- Check Neon console for database status

### Notion API Errors
- Verify NOTION_API_KEY in `.env`
- Ensure integration has access to pages/databases
- Test connection with `python test_connections.py`

## Documentation

Key documentation files:
- `README.md` - Project overview
- `backend/NOTION_SYNC_README.md` - Notion integration guide
- `backend/LMS_API_README.md` - API documentation
- `canon/DATABASE_SCHEMA.md` - Database schema details
- `docs/IMPLEMENTATION_ROADMAP.md` - Development roadmap

## Contact

For issues or questions about this setup, check the project documentation or the scripts in the `scripts/` directory.

---

**Last Updated**: 2025-12-03
**Environment**: Desktop Claude on Windows
**Project**: FRAMES-Python (Educational platform for aerospace engineering teams)
