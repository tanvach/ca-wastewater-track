import ckan

# Config
QUERY = 'San Francisco'


def check_viruses():
    print(f"Fetching unique viruses for: '{QUERY}'...")
    try:
        # Every matching row, but only the target column (a few bytes a row,
        # instead of ~100 columns).
        records = ckan.search(QUERY, fields=['pcr_target'])
        print(f"Fetched {len(records)} records.")

        unique_viruses = {row['pcr_target'] for row in records if row.get('pcr_target')}

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
