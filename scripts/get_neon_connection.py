"""Get Neon database connection string for a specific project."""
import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('NEON_API_KEY')
if not api_key:
    print("ERROR: NEON_API_KEY not found. Set it in .env file.")
    exit(1)
project_id = os.getenv('NEON_PROJECT_ID', 'spring-surf-23419787')

headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# Get project details
print(f"Fetching connection details for project: {project_id}\n")

# Try to get connection URI
conn_resp = requests.get(
    f'https://console.neon.tech/api/v2/projects/{project_id}/connection_uri',
    headers=headers,
    params={'database_name': 'neondb', 'role_name': 'neondb_owner'}
)

if conn_resp.status_code == 200:
    data = conn_resp.json()
    uri = data.get('uri', '')
    print("✅ Got connection string!")
    print(f"\nFull URI:\n{uri}\n")
    
    # Also show masked version
    if '@' in uri:
        parts = uri.split('@')
        creds = parts[0].rsplit(':', 1)
        masked = creds[0] + ':****@' + parts[1]
        print(f"Masked: {masked}")
else:
    print(f"Error getting connection URI: {conn_resp.status_code}")
    print(conn_resp.text)
    
    # Try listing branches to get more info
    print("\nTrying to get branch info...")
    branches_resp = requests.get(
        f'https://console.neon.tech/api/v2/projects/{project_id}/branches',
        headers=headers
    )
    if branches_resp.status_code == 200:
        branches = branches_resp.json().get('branches', [])
        for b in branches:
            print(f"  Branch: {b.get('name')} (ID: {b.get('id')})")
    else:
        print(f"  Branch error: {branches_resp.status_code}")
        print(f"  {branches_resp.text}")

