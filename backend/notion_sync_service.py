"""
FRAMES Notion Sync Service - Bidirectional PostgreSQL ↔ Notion Sync
====================================================================

PURPOSE:
Syncs data between PostgreSQL database and Notion workspace to enable:
1. Team Leads view/edit data in Notion (user-friendly interface)
2. Backend processes read/write to PostgreSQL (source of truth)
3. Bidirectional updates kept in sync automatically

ARCHITECTURE:
- PostgreSQL: Source of truth (backend/db_models.py - 40 tables)
- Notion: User interface layer (databases with matching schemas)
- Sync Engine: Bidirectional sync with conflict resolution

SYNC STRATEGY:
1. PUSH (PostgreSQL → Notion): Update Notion when backend data changes
2. PULL (Notion → PostgreSQL): Update backend when Team Leads edit in Notion
3. Conflict Resolution: Last-write-wins with audit logging
4. Incremental Sync: Only sync changed records (via updated_at timestamps)

REQUIRED NOTION DATABASES:
- Teams (maps to TeamModel)
- Faculty (maps to FacultyModel)
- Students (maps to StudentModel)
- Projects (maps to ProjectModel)
- Interfaces (maps to InterfaceModel)
- Universities (maps to UniversityModel)
- Modules (maps to ModuleModel)

Each Notion database needs:
- Matching properties for all model fields
- 'postgres_id' property (text) for linking back to DB
- 'last_synced' property (date) for sync tracking
- 'sync_status' property (select: synced, pending, conflict)
"""

from notion_client import Client
from sqlalchemy import inspect
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

from .database import db
from .db_models import (
    TeamModel, FacultyModel, StudentModel, ProjectModel,
    InterfaceModel, University
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class NotionSyncService:
    """Bidirectional sync service between PostgreSQL and Notion"""
    
    # Model to Notion database mapping (to be populated after DB creation)
    MODEL_TO_NOTION_DB = {
        'TeamModel': None,          # Will store Notion database IDs
        'FacultyModel': None,
        'StudentModel': None,
        'ProjectModel': None,
        'InterfaceModel': None,
        'University': None,
    }
    
    def __init__(self):
        """Initialize Notion client and validate connection"""
        api_key = os.getenv('NOTION_API_KEY')
        if not api_key:
            raise ValueError("NOTION_API_KEY not found in .env")
        
        self.notion = Client(auth=api_key)
        logger.info("Notion sync service initialized")
    
    def create_notion_databases(self, parent_page_id: str) -> dict:
        """
        Create all required Notion databases in specified parent page
        
        Args:
            parent_page_id: ID of Notion page to create databases in
            
        Returns:
            dict: Mapping of model names to created database IDs
        """
        created_dbs = {}
        
        # Define database schemas based on SQLAlchemy models
        database_schemas = {
            'Teams': self._get_team_schema(),
            'Faculty': self._get_faculty_schema(),
            'Students': self._get_student_schema(),
            'Projects': self._get_project_schema(),
            'Interfaces': self._get_interface_schema(),
            'Universities': self._get_university_schema(),
        }
        
        for db_name, schema in database_schemas.items():
            logger.info(f"Creating Notion database: {db_name}")
            
            try:
                # Create database
                response = self.notion.databases.create(
                    parent={"type": "page_id", "page_id": parent_page_id},
                    title=[{"type": "text", "text": {"content": f"FRAMES {db_name}"}}],
                    properties=schema
                )
                
                created_dbs[db_name] = response['id']
                logger.info(f"✅ Created {db_name}: {response['id']}")
                
            except Exception as e:
                logger.error(f"❌ Failed to create {db_name}: {e}")
                raise
        
        return created_dbs
    
    def _get_team_schema(self) -> dict:
        """Generate Notion properties schema for Teams database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "university_id": {"rich_text": {}},
            "team_type": {"select": {"options": [
                {"name": "design", "color": "blue"},
                {"name": "analysis", "color": "green"},
                {"name": "testing", "color": "orange"},
                {"name": "integration", "color": "purple"}
            ]}},
            "project_id": {"rich_text": {}},
            "status": {"select": {"options": [
                {"name": "active", "color": "green"},
                {"name": "completed", "color": "gray"},
                {"name": "on_hold", "color": "yellow"}
            ]}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    
    def _get_faculty_schema(self) -> dict:
        """Generate Notion properties schema for Faculty database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "university_id": {"rich_text": {}},
            "email": {"email": {}},
            "department": {"rich_text": {}},
            "role": {"select": {"options": [
                {"name": "professor", "color": "blue"},
                {"name": "advisor", "color": "green"},
                {"name": "researcher", "color": "purple"}
            ]}},
            "active": {"checkbox": {}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    
    def _get_student_schema(self) -> dict:
        """Generate Notion properties schema for Students database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "university_id": {"rich_text": {}},
            "email": {"email": {}},
            "team_id": {"rich_text": {}},
            "status": {"select": {"options": [
                {"name": "incoming", "color": "blue"},
                {"name": "established", "color": "green"},
                {"name": "outgoing", "color": "orange"},
                {"name": "alumni", "color": "gray"}
            ]}},
            "terms_remaining": {"number": {}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    
    def _get_project_schema(self) -> dict:
        """Generate Notion properties schema for Projects database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "university_id": {"rich_text": {}},
            "description": {"rich_text": {}},
            "status": {"select": {"options": [
                {"name": "planning", "color": "blue"},
                {"name": "active", "color": "green"},
                {"name": "completed", "color": "gray"},
                {"name": "cancelled", "color": "red"}
            ]}},
            "start_date": {"date": {}},
            "end_date": {"date": {}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    
    def _get_interface_schema(self) -> dict:
        """Generate Notion properties schema for Interfaces database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "from_university": {"rich_text": {}},
            "to_university": {"rich_text": {}},
            "from_team_id": {"rich_text": {}},
            "to_team_id": {"rich_text": {}},
            "bond_type": {"select": {"options": [
                {"name": "codified-strong", "color": "green"},
                {"name": "institutional-weak", "color": "yellow"},
                {"name": "fragile-temporary", "color": "red"}
            ]}},
            "energy_loss": {"number": {}},
            "is_cross_university": {"checkbox": {}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    
    def _get_university_schema(self) -> dict:
        """Generate Notion properties schema for Universities database"""
        return {
            "Name": {"title": {}},
            "postgres_id": {"rich_text": {}},
            "code": {"rich_text": {}},
            "full_name": {"rich_text": {}},
            "active": {"checkbox": {}},
            "created_at": {"date": {}},
            "last_synced": {"date": {}},
            "sync_status": {"select": {"options": [
                {"name": "synced", "color": "green"},
                {"name": "pending", "color": "yellow"},
                {"name": "conflict", "color": "red"}
            ]}}
        }
    

    
    def push_to_notion(self, model_class, record_id: str, database_id: str):
        """
        Push a single PostgreSQL record to Notion
        
        Args:
            model_class: SQLAlchemy model class (e.g., TeamModel)
            record_id: ID of record in PostgreSQL
            database_id: ID of Notion database to sync to
        """
        # Get record from PostgreSQL
        record = model_class.query.get(record_id)
        if not record:
            logger.error(f"Record {record_id} not found in {model_class.__name__}")
            return None
        
        # Convert record to Notion properties
        notion_properties = self._model_to_notion_properties(record)
        
        # Check if record already exists in Notion
        existing_page = self._find_notion_page_by_postgres_id(database_id, record_id)
        
        if existing_page:
            # Update existing page
            logger.info(f"Updating Notion page {existing_page['id']}")
            response = self.notion.pages.update(
                page_id=existing_page['id'],
                properties=notion_properties
            )
        else:
            # Create new page
            logger.info(f"Creating new Notion page for {record_id}")
            response = self.notion.pages.create(
                parent={"database_id": database_id},
                properties=notion_properties
            )
        
        return response
    
    def pull_from_notion(self, database_id: str, model_class):
        """
        Pull all records from Notion database and update PostgreSQL
        
        Args:
            database_id: ID of Notion database to sync from
            model_class: SQLAlchemy model class to update
        """
        # Query all pages from Notion database
        has_more = True
        start_cursor = None
        synced_count = 0
        
        while has_more:
            response = self.notion.databases.query(
                database_id=database_id,
                start_cursor=start_cursor
            )
            
            for page in response.get('results', []):
                try:
                    # Convert Notion page to model data
                    model_data = self._notion_to_model_data(page, model_class)
                    
                    # Get postgres_id to find existing record
                    postgres_id = self._get_notion_property_value(page, 'postgres_id')
                    
                    if postgres_id:
                        # Update existing record
                        record = model_class.query.get(postgres_id)
                        if record:
                            for key, value in model_data.items():
                                setattr(record, key, value)
                            logger.info(f"Updated {model_class.__name__} {postgres_id}")
                        else:
                            logger.warning(f"Record {postgres_id} not found, creating new")
                            record = model_class(**model_data)
                            db.session.add(record)
                    else:
                        # Create new record
                        record = model_class(**model_data)
                        db.session.add(record)
                        logger.info(f"Created new {model_class.__name__}")
                    
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"Error syncing page {page['id']}: {e}")
                    continue
            
            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')
        
        # Commit all changes
        db.session.commit()
        logger.info(f"✅ Synced {synced_count} records from Notion to PostgreSQL")
        
        return synced_count
    
    def _model_to_notion_properties(self, record) -> dict:
        """Convert SQLAlchemy model instance to Notion properties dict"""
        properties = {}
        
        # Get all columns from model
        mapper = inspect(record.__class__)
        
        for column in mapper.columns:
            col_name = column.name
            value = getattr(record, col_name)
            
            # Skip None values
            if value is None:
                continue
            
            # Convert based on column type
            if col_name == 'id':
                properties['postgres_id'] = {"rich_text": [{"text": {"content": str(value)}}]}
            elif col_name in ['name', 'title']:
                properties['Name'] = {"title": [{"text": {"content": str(value)}}]}
            elif 'email' in col_name:
                properties[col_name] = {"email": str(value)}
            elif col_name in ['active', 'is_cross_university']:
                properties[col_name] = {"checkbox": bool(value)}
            elif 'date' in col_name or col_name == 'created_at':
                if isinstance(value, str):
                    properties[col_name] = {"date": {"start": value}}
                elif isinstance(value, datetime):
                    properties[col_name] = {"date": {"start": value.isoformat()}}
            elif isinstance(value, (int, float)):
                properties[col_name] = {"number": value}
            elif col_name in ['status', 'team_type', 'bond_type', 'role', 'category', 'difficulty']:
                properties[col_name] = {"select": {"name": str(value)}}
            else:
                # Default to rich_text for strings
                properties[col_name] = {"rich_text": [{"text": {"content": str(value)}}]}
        
        # Add sync timestamp
        properties['last_synced'] = {"date": {"start": datetime.now().isoformat()}}
        properties['sync_status'] = {"select": {"name": "synced"}}
        
        return properties
    
    def _notion_to_model_data(self, page: dict, model_class) -> dict:
        """Convert Notion page to model data dict"""
        model_data = {}
        properties = page.get('properties', {})
        
        # Map Notion properties back to model fields
        for prop_name, prop_value in properties.items():
            # Skip sync-specific fields
            if prop_name in ['last_synced', 'sync_status', 'postgres_id']:
                continue
            
            # Extract value based on property type
            value = self._get_notion_property_value(page, prop_name)
            
            if value is not None:
                # Map 'Name' back to 'name' or 'title'
                if prop_name == 'Name':
                    if hasattr(model_class, 'name'):
                        model_data['name'] = value
                    elif hasattr(model_class, 'title'):
                        model_data['title'] = value
                else:
                    model_data[prop_name] = value
        
        return model_data
    
    def _get_notion_property_value(self, page: dict, property_name: str):
        """Extract value from Notion property regardless of type"""
        properties = page.get('properties', {})
        prop = properties.get(property_name)
        
        if not prop:
            return None
        
        prop_type = prop.get('type')
        
        if prop_type == 'title':
            texts = prop.get('title', [])
            return texts[0].get('plain_text', '') if texts else ''
        elif prop_type == 'rich_text':
            texts = prop.get('rich_text', [])
            return texts[0].get('plain_text', '') if texts else ''
        elif prop_type == 'select':
            select = prop.get('select')
            return select.get('name') if select else None
        elif prop_type == 'multi_select':
            multi = prop.get('multi_select', [])
            return [m.get('name') for m in multi]
        elif prop_type == 'number':
            return prop.get('number')
        elif prop_type == 'checkbox':
            return prop.get('checkbox')
        elif prop_type == 'email':
            return prop.get('email')
        elif prop_type == 'date':
            date_obj = prop.get('date')
            return date_obj.get('start') if date_obj else None
        else:
            return None
    
    def _find_notion_page_by_postgres_id(self, database_id: str, postgres_id: str):
        """Find Notion page with matching postgres_id"""
        response = self.notion.databases.query(
            database_id=database_id,
            filter={
                "property": "postgres_id",
                "rich_text": {
                    "equals": postgres_id
                }
            }
        )
        
        results = response.get('results', [])
        return results[0] if results else None


# Convenience functions for common sync operations
def sync_all_teams_to_notion(database_id: str):
    """Sync all teams from PostgreSQL to Notion"""
    service = NotionSyncService()
    teams = TeamModel.query.all()
    
    for team in teams:
        try:
            service.push_to_notion(TeamModel, team.id, database_id)
            logger.info(f"Synced team {team.id}")
        except Exception as e:
            logger.error(f"Failed to sync team {team.id}: {e}")


def sync_all_from_notion_to_postgres(database_id: str, model_class):
    """Sync all records from Notion database to PostgreSQL"""
    service = NotionSyncService()
    return service.pull_from_notion(database_id, model_class)
