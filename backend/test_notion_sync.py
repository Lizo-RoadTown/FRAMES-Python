"""
Test Notion Sync Service
========================

Quick validation tests for the sync service without actually hitting Notion API
Tests schema generation and data conversion logic
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.notion_sync_service import NotionSyncService
from backend.db_models import TeamModel, StudentModel, InterfaceModel
from datetime import datetime


def test_schema_generation():
    """Test that database schemas are generated correctly"""
    print("🧪 Testing Schema Generation...")
    
    service = NotionSyncService()
    
    # Test Teams schema
    teams_schema = service._get_team_schema()
    assert 'Name' in teams_schema, "Teams schema missing Name property"
    assert 'postgres_id' in teams_schema, "Teams schema missing postgres_id"
    assert 'team_type' in teams_schema, "Teams schema missing team_type"
    assert teams_schema['Name']['title'] == {}, "Name should be title type"
    assert 'select' in teams_schema['team_type'], "team_type should be select"
    
    print("   ✅ Teams schema valid")
    
    # Test Students schema
    students_schema = service._get_student_schema()
    assert 'email' in students_schema, "Students schema missing email"
    assert students_schema['email']['email'] == {}, "email should be email type"
    assert 'terms_remaining' in students_schema, "Students schema missing terms_remaining"
    assert students_schema['terms_remaining']['number'] == {}, "terms_remaining should be number"
    
    print("   ✅ Students schema valid")
    
    # Test Interfaces schema
    interfaces_schema = service._get_interface_schema()
    assert 'bond_type' in interfaces_schema, "Interfaces schema missing bond_type"
    assert 'energy_loss' in interfaces_schema, "Interfaces schema missing energy_loss"
    assert 'is_cross_university' in interfaces_schema, "Interfaces schema missing is_cross_university"
    assert interfaces_schema['is_cross_university']['checkbox'] == {}, "is_cross_university should be checkbox"
    
    print("   ✅ Interfaces schema valid")
    
    print("\n✅ All schema tests passed!\n")


def test_model_to_notion_conversion():
    """Test converting SQLAlchemy models to Notion properties"""
    print("🧪 Testing Model → Notion Conversion...")
    
    service = NotionSyncService()
    
    # Create mock team record
    class MockTeam:
        id = "team_123"
        name = "Test Team"
        university_id = "CalPolyPomona"
        team_type = "design"
        status = "active"
        project_id = "project_456"
        created_at = "2025-01-01T00:00:00"
        
        class __class__:
            __name__ = "TeamModel"
    
    # Add columns property for inspection
    class MockColumn:
        def __init__(self, name):
            self.name = name
    
    class MockMapper:
        columns = [
            MockColumn('id'),
            MockColumn('name'),
            MockColumn('university_id'),
            MockColumn('team_type'),
            MockColumn('status'),
            MockColumn('project_id'),
            MockColumn('created_at'),
        ]
    
    # Mock inspect function
    original_inspect = __import__('sqlalchemy', fromlist=['inspect']).inspect
    def mock_inspect(cls):
        return MockMapper()
    
    import sqlalchemy
    sqlalchemy.inspect = mock_inspect
    
    try:
        team = MockTeam()
        properties = service._model_to_notion_properties(team)
        
        # Validate conversions
        assert 'Name' in properties, "Missing Name property"
        assert properties['Name']['title'][0]['text']['content'] == "Test Team", "Name not converted correctly"
        
        assert 'postgres_id' in properties, "Missing postgres_id property"
        assert properties['postgres_id']['rich_text'][0]['text']['content'] == "team_123", "postgres_id not converted"
        
        assert 'team_type' in properties, "Missing team_type property"
        assert properties['team_type']['select']['name'] == "design", "team_type not converted"
        
        assert 'last_synced' in properties, "Missing auto-generated last_synced"
        assert 'sync_status' in properties, "Missing auto-generated sync_status"
        assert properties['sync_status']['select']['name'] == "synced", "sync_status should default to synced"
        
        print("   ✅ Team → Notion conversion valid")
        
    finally:
        sqlalchemy.inspect = original_inspect
    
    print("\n✅ All conversion tests passed!\n")


def test_notion_property_extraction():
    """Test extracting values from Notion property structures"""
    print("🧪 Testing Notion Property Extraction...")
    
    service = NotionSyncService()
    
    # Mock Notion page with various property types
    mock_page = {
        'properties': {
            'Name': {
                'type': 'title',
                'title': [{'plain_text': 'Test Student'}]
            },
            'email': {
                'type': 'email',
                'email': 'test@example.com'
            },
            'status': {
                'type': 'select',
                'select': {'name': 'active'}
            },
            'terms_remaining': {
                'type': 'number',
                'number': 4
            },
            'active': {
                'type': 'checkbox',
                'checkbox': True
            },
            'created_at': {
                'type': 'date',
                'date': {'start': '2025-01-01'}
            }
        }
    }
    
    # Test extraction
    assert service._get_notion_property_value(mock_page, 'Name') == 'Test Student', "Title extraction failed"
    assert service._get_notion_property_value(mock_page, 'email') == 'test@example.com', "Email extraction failed"
    assert service._get_notion_property_value(mock_page, 'status') == 'active', "Select extraction failed"
    assert service._get_notion_property_value(mock_page, 'terms_remaining') == 4, "Number extraction failed"
    assert service._get_notion_property_value(mock_page, 'active') == True, "Checkbox extraction failed"
    assert service._get_notion_property_value(mock_page, 'created_at') == '2025-01-01', "Date extraction failed"
    
    print("   ✅ All property extractions valid")
    
    print("\n✅ All extraction tests passed!\n")


if __name__ == "__main__":
    print("=" * 80)
    print("FRAMES Notion Sync Service - Unit Tests")
    print("=" * 80)
    print()
    
    try:
        test_schema_generation()
        test_model_to_notion_conversion()
        test_notion_property_extraction()
        
        print("=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print("\n📋 Next step: Run setup script with actual Notion page ID")
        print("   python backend/setup_notion_sync.py --parent-page-id <PAGE_ID>")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
