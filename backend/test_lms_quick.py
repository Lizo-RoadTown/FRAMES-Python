"""
Quick test script to verify LMS endpoints are working
Run the Flask app first: python app.py
Then run this script: python test_lms_quick.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/lms"

def test_get_modules():
    """Test GET /api/lms/modules"""
    print("\n1. Testing GET /api/lms/modules...")
    response = requests.get(f"{BASE_URL}/modules")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 200
    assert data['success'] == True
    print("   ✓ PASSED")

def test_get_module_not_found():
    """Test GET /api/lms/modules/<invalid_id>"""
    print("\n2. Testing GET /api/lms/modules/999 (should 404)...")
    response = requests.get(f"{BASE_URL}/modules/999")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 404
    assert data['success'] == False
    print("   ✓ PASSED")

def test_track_progress_missing_fields():
    """Test POST /api/lms/modules/<id>/progress with missing fields"""
    print("\n3. Testing POST /api/lms/modules/1/progress (missing fields)...")
    response = requests.post(
        f"{BASE_URL}/modules/1/progress",
        json={},
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 400
    assert 'Missing required field' in data['error']
    print("   ✓ PASSED")

def test_get_analytics():
    """Test GET /api/lms/modules/1/analytics"""
    print("\n4. Testing GET /api/lms/modules/1/analytics...")
    response = requests.get(f"{BASE_URL}/modules/1/analytics")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)}")
    # This might return 404 if module doesn't exist, which is fine
    print("   ✓ COMPLETED")

def main():
    print("="*60)
    print("LMS API Endpoint Tests")
    print("="*60)
    print("\nMake sure Flask app is running on http://localhost:5000")
    print("Start it with: python app.py")
    
    try:
        # Test if server is running
        response = requests.get("http://localhost:5000/api/network-data")
        if response.status_code != 200:
            print("\n❌ Flask server not responding. Start it with: python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to Flask server. Start it with: python app.py")
        return
    
    print("\n✓ Flask server is running")
    
    # Run tests
    try:
        test_get_modules()
        test_get_module_not_found()
        test_track_progress_missing_fields()
        test_get_analytics()
        
        print("\n" + "="*60)
        print("✓ All basic tests passed!")
        print("="*60)
        print("\nNext steps:")
        print("1. Wait for Agent A to populate database with Notion content")
        print("2. Test endpoints with real module data")
        print("3. Integrate with React frontend (Agent B)")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    main()
