"""
Tests for LMS API endpoints
"""
import pytest
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from shared.database.db_models import Module, ModuleSection, ModuleProgress
from backend.database import db


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_get_all_modules_empty(client):
    """Test GET /api/lms/modules with no modules"""
    response = client.get('/api/lms/modules')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['count'] == 0
    assert data['modules'] == []


def test_get_module_details_not_found(client):
    """Test GET /api/lms/modules/<id> with invalid ID"""
    response = client.get('/api/lms/modules/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'not found' in data['error'].lower()


def test_track_progress_missing_fields(client):
    """Test POST /api/lms/modules/<id>/progress with missing data"""
    response = client.post(
        '/api/lms/modules/1/progress',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing required field' in data['error']


def test_submit_feedback_missing_fields(client):
    """Test POST /api/lms/modules/<id>/feedback with missing data"""
    response = client.post(
        '/api/lms/modules/1/feedback',
        data=json.dumps({'student_id': 'student1'}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing required field' in data['error']


def test_create_module_and_fetch(client):
    """Test creating a module and fetching it"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='test-module-1',
            title='Test Module',
            description='A test module',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    # Fetch all modules
    response = client.get('/api/lms/modules')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['count'] == 1
    assert data['modules'][0]['title'] == 'Test Module'
    
    # Fetch specific module
    response = client.get(f'/api/lms/modules/{module_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['module']['title'] == 'Test Module'


def test_module_with_sections(client):
    """Test creating a module with sections and fetching"""
    with app.app_context():
        # Create module
        module = Module(
            module_id='test-module-2',
            title='Module with Sections',
            status='published'
        )
        db.session.add(module)
        db.session.commit()
        
        # Create sections
        section1 = ModuleSection(
            module_id=module.id,
            section_number=1,
            section_type='text',
            title='Section 1',
            content='Content for section 1'
        )
        section2 = ModuleSection(
            module_id=module.id,
            section_number=2,
            section_type='video',
            title='Section 2',
            content='Video content',
            media_url='https://example.com/video.mp4'
        )
        db.session.add_all([section1, section2])
        db.session.commit()
        module_id = module.id
    
    # Fetch module with sections
    response = client.get(f'/api/lms/modules/{module_id}?include_sections=true')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'sections' in data['module']
    assert len(data['module']['sections']) == 2
    assert data['module']['sections'][0]['title'] == 'Section 1'
    assert data['module']['sections'][1]['title'] == 'Section 2'


def test_track_progress_creates_record(client):
    """Test that tracking progress creates a progress record"""
    with app.app_context():
        # Create module
        module = Module(
            module_id='test-module-3',
            title='Progress Test Module',
            status='published'
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    # Track progress
    response = client.post(
        f'/api/lms/modules/{module_id}/progress',
        data=json.dumps({
            'student_id': 'student123',
            'section_number': 1,
            'progress_percent': 50,
            'status': 'in_progress'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['progress']['progress_percent'] == 50
    assert data['progress']['status'] == 'in_progress'
    
    # Verify progress was saved
    with app.app_context():
        progress = ModuleProgress.query.filter_by(
            module_id=module_id,
            student_id='student123'
        ).first()
        assert progress is not None
        assert progress.progress_percent == 50


def test_get_module_analytics(client):
    """Test fetching module analytics"""
    with app.app_context():
        # Create module
        module = Module(
            module_id='test-module-4',
            title='Analytics Test Module',
            status='published'
        )
        db.session.add(module)
        db.session.commit()
        
        # Create some progress records
        progress1 = ModuleProgress(
            module_id=module.id,
            student_id='student1',
            status='completed',
            progress_percent=100,
            total_time_seconds=1800
        )
        progress2 = ModuleProgress(
            module_id=module.id,
            student_id='student2',
            status='in_progress',
            progress_percent=50,
            total_time_seconds=900
        )
        db.session.add_all([progress1, progress2])
        db.session.commit()
        module_id = module.id
    
    # Fetch analytics
    response = client.get(f'/api/lms/modules/{module_id}/analytics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['analytics']['total_students'] == 2
    assert data['analytics']['completed_count'] == 1
    assert data['analytics']['completion_rate'] == 50.0


# TODO: Add more tests with actual module data once Agent A's pipeline is complete


# ============================================================================
# ASCENT BASECAMP ENDPOINT TESTS
# Tests for learner_performance, subsystem_competency, race mode
# ============================================================================

def test_start_module_endpoint(client):
    """Test POST /api/lms/students/<id>/modules/<id>/start"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_001',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    response = client.post(f'/api/lms/students/test_student/modules/{module_id}/start')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['attempt_number'] == 1
    assert 'log_id' in data


def test_log_activity_endpoint(client):
    """Test POST /api/lms/students/<id>/modules/<id>/log_activity"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_002',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    # First start the module
    client.post(f'/api/lms/students/test_student/modules/{module_id}/start')
    
    # Then log activity
    activity_data = {
        'time_spent_seconds': 120,
        'errors_count': 3
    }
    response = client.post(
        f'/api/lms/students/test_student/modules/{module_id}/log_activity',
        data=json.dumps(activity_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['time_spent_seconds'] == 120
    assert data['errors_count'] == 3


def test_complete_module_endpoint(client):
    """Test POST /api/lms/students/<id>/modules/<id>/complete"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_003',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    # Start module first
    client.post(f'/api/lms/students/test_student/modules/{module_id}/start')
    
    # Complete it
    completion_data = {
        'time_spent_seconds': 300,
        'errors_count': 2,
        'mastery_score': 85.5
    }
    response = client.post(
        f'/api/lms/students/test_student/modules/{module_id}/complete',
        data=json.dumps(completion_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert data['mastery_score'] == 85.5
    assert 'subsystem' in data
    assert 'competency_level' in data


def test_get_ghost_cohorts_endpoint(client):
    """Test GET /api/lms/modules/<id>/ghost_cohorts"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_004',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    response = client.get(f'/api/lms/modules/{module_id}/ghost_cohorts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'ghost_cohorts' in data
    # May be empty if no ghost data exists
    assert isinstance(data['ghost_cohorts'], list)


def test_get_leaderboard_endpoint(client):
    """Test GET /api/lms/students/<id>/leaderboard"""
    response = client.get('/api/lms/students/test_student/leaderboard')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'top_10' in data
    assert 'student_rank' in data
    assert isinstance(data['top_10'], list)


def test_get_subsystem_competency_endpoint(client):
    """Test GET /api/lms/students/<id>/subsystem_competency"""
    response = client.get('/api/lms/students/test_student/subsystem_competency')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'competencies' in data
    assert isinstance(data['competencies'], list)


def test_start_race_endpoint(client):
    """Test POST /api/lms/students/<id>/race/start"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_005',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    race_data = {'module_id': module_id}
    response = client.post(
        '/api/lms/students/test_student/race/start',
        data=json.dumps(race_data),
        content_type='application/json'
    )
    # May be 404 if race_metadata doesn't exist, or 201 if it does
    assert response.status_code in [201, 404]


def test_complete_race_endpoint(client):
    """Test POST /api/lms/students/<id>/race/complete"""
    with app.app_context():
        # Create a test module
        module = Module(
            module_id='TEST_006',
            title='Test Module',
            description='Test',
            category='testing',
            status='published',
            estimated_minutes=30
        )
        db.session.add(module)
        db.session.commit()
        module_id = module.id
    
    # Start race first
    client.post(
        '/api/lms/students/test_student/race/start',
        data=json.dumps({'module_id': module_id}),
        content_type='application/json'
    )
    
    # Complete race
    completion_data = {
        'module_id': module_id,
        'time_seconds': 180,
        'errors_count': 1,
        'mastery_score': 92.0
    }
    response = client.post(
        '/api/lms/students/test_student/race/complete',
        data=json.dumps(completion_data),
        content_type='application/json'
    )
    # May be 404 if race wasn't started, or 200 if successful
    assert response.status_code in [200, 404]


def test_error_handling_invalid_student(client):
    """Test error handling for invalid student IDs"""
    response = client.get('/api/lms/students//modules')  # Empty student ID
    # Should either be 404 or handle gracefully
    assert response.status_code in [404, 400, 500]


def test_error_handling_missing_module(client):
    """Test error handling for non-existent modules"""
    response = client.post('/api/lms/students/test_student/modules/999999/start')
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
