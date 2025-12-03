"""Query Neon API to find database connection string."""
import requests
import os

# Neon API key
api_key = os.getenv('NEON_API_KEY')
if not api_key:
    print("ERROR: NEON_API_KEY not found in environment. Set it in .env file.")
    exit(1)
headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}

# List projects
print("Fetching Neon projects...\n")
resp = requests.get('https://console.neon.tech/api/v2/projects', headers=headers)

if resp.status_code == 200:
    projects = resp.json().get('projects', [])
    print(f"Found {len(projects)} Neon project(s):\n")
    
    for p in projects:
        project_id = p.get('id')
        print(f"  Project: {p.get('name', 'unnamed')}")
        print(f"  ID: {project_id}")
        print(f"  Region: {p.get('region_id')}")
        
        # Get connection URI for this project
        conn_resp = requests.get(
            f'https://console.neon.tech/api/v2/projects/{project_id}/connection_uri',
            headers=headers,
            params={'database_name': 'neondb', 'role_name': 'neondb_owner'}
        )
        
        if conn_resp.status_code == 200:
            uri = conn_resp.json().get('uri', 'Not found')
            # Mask password for display
            if '@' in uri:
                parts = uri.split('@')
                masked = parts[0].rsplit(':', 1)[0] + ':****@' + parts[1]
                print(f"  Connection URI: {masked}")
            print(f"\n  ✅ Full URI retrieved - ready to add to .env")
        else:
            print(f"  Connection URI: Could not retrieve ({conn_resp.status_code})")
        
        print()
else:
    print(f"Error: {resp.status_code}")
    print(resp.text)

