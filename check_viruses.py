import requests
import json

# Config
API_BASE = 'https://data.ca.gov/api/3/action'
RESOURCE_ID = '49a3fc6f-e52d-4e4a-a9ee-9c9e4a5cc771'
QUERY = 'San Francisco'

def check_viruses():
    print(f"Fetching unique viruses for: '{QUERY}'...")
    # Fetch a large chunk to ensure we see all targets
    url = f"{API_BASE}/datastore_search?resource_id={RESOURCE_ID}&q={QUERY}&limit=10000"
    
    try:
        r = requests.get(url)
        data = r.json()
        
        if not data['success']:
            print("API Error:", data.get('error'))
            return

        records = data['result']['records']
        print(f"Fetched {len(records)} records.")
        
        # Find the virus column (likely 'pcr_target' or similar)
        if not records:
            print("No records.")
            return

        keys = records[0].keys()
        # Better column detection
        virus_col = next((k for k in keys if 'pcr_target' in k.lower() and 'unit' not in k.lower() and 'avg' not in k.lower()), None)
        if not virus_col:
             virus_col = next((k for k in keys if 'target' in k.lower() and 'unit' not in k.lower() and 'rec_eff' not in k.lower() and 'hum_frac' not in k.lower()), None)
        
        if not virus_col:
            print("Could not identify virus column.")
            print("Keys:", keys)
            return

        # Extract unique values
        unique_viruses = set()
        for row in records:
            # Filter for "Southeast" just to match user's context, or check all SF
            # Let's check ALL SF to be thorough
            if row.get(virus_col):
                unique_viruses.add(row[virus_col])

        print(f"\nUnique Viruses Found in CDPH Data ({len(unique_viruses)}):")
        for v in sorted(unique_viruses):
            print(f"- {v}")

        # Check specifically for Adenovirus
        ade_matches = [v for v in unique_viruses if 'adeno' in v.lower()]
        if ade_matches:
            print(f"\nMatch found for Adenovirus: {ade_matches}")
        else:
            print("\nNo direct match found for 'Adenovirus' or 'Group F'")

    except Exception as e:
        print(f"Script failed: {e}")

if __name__ == "__main__":
    check_viruses()
