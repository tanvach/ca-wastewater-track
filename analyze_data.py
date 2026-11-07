import requests
import json
import collections

# Config
API_BASE = 'https://data.chhs.ca.gov/api/3/action'
RESOURCE_ID = '2742b824-3736-4292-90a9-7fad98e94c06'
QUERY = 'San Francisco'

def analyze_data():
    print(f"Fetching data for query: '{QUERY}'...")
    url = f"{API_BASE}/datastore_search?resource_id={RESOURCE_ID}&q={QUERY}&limit=100"
    
    try:
        r = requests.get(url)
        data = r.json()
        
        if not data['success']:
            print("API Error:", data.get('error'))
            return

        records = data['result']['records']
        print(f"Fetched {len(records)} records.\n")
        
        if not records:
            print("No records found.")
            return

        # 1. Inspect Columns
        print("--- Column Names Found ---")
        keys = list(records[0].keys())
        print(keys)
        print("\n")

        # 2. Inspect 'Sewershed' candidates
        potential_loc_cols = [k for k in keys if any(x in k.lower() for x in ['sewer', 'plant', 'facility', 'wwtp', 'name', 'loc'])]
        print("--- Potential Location Columns ---")
        for col in potential_loc_cols:
            unique_vals = set(r.get(col) for r in records)
            print(f"{col}: {unique_vals}")
        print("\n")

        # 3. Inspect 'Virus' and 'Value' candidates
        print("--- Value/Virus Columns ---")
        # Prefer the known column names; the substring guesses below would
        # otherwise match earlier keys such as rec_eff_target_name or
        # concentration_method.
        virus_col = 'pcr_target' if 'pcr_target' in keys else next((k for k in keys if 'target' in k.lower() and 'unit' not in k.lower()), None)
        value_col = 'pcr_target_avg_conc' if 'pcr_target_avg_conc' in keys else next((k for k in keys if 'conc' in k.lower() or 'copy' in k.lower()), None)
        
        if virus_col:
            print(f"Virus Column Candidate: {virus_col}")
            print(f"Sample Values: {list(set(r.get(virus_col) for r in records))[:5]}")
        
        if value_col:
            print(f"Value Column Candidate: {value_col}")
            print(f"Sample Values: {list(set(r.get(value_col) for r in records))[:5]}")

    except Exception as e:
        print(f"Script failed: {e}")

if __name__ == "__main__":
    analyze_data()
