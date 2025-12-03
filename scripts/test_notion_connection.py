"""Test Notion API connection and list accessible content."""
from dotenv import load_dotenv
load_dotenv()

import os
from notion_client import Client

notion = Client(auth=os.getenv('NOTION_API_KEY'))

# Search for all accessible content
results = notion.search(query='', page_size=20)
print(f"Found {len(results['results'])} items accessible to FRAMES bot:\n")

for item in results['results'][:15]:
    obj_type = item['object']
    item_id = item['id']
    
    if obj_type == 'page':
        # Try to get title from various property formats
        props = item.get('properties', {})
        name = 'Untitled'
        
        for prop_name in ['title', 'Title', 'Name', 'name']:
            if prop_name in props:
                prop = props[prop_name]
                if 'title' in prop and prop['title']:
                    name = prop['title'][0].get('plain_text', 'Untitled')
                    break
        
        print(f"  📄 Page: {name}")
        print(f"     ID: {item_id}")
        
    elif obj_type == 'database':
        title = item.get('title', [])
        name = title[0]['plain_text'] if title else 'Untitled DB'
        print(f"  📊 Database: {name}")
        print(f"     ID: {item_id}")

print(f"\n✅ Notion API connection working!")

