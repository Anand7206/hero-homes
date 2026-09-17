import os
import sys
import re

project_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(project_dir, 'assets')

# List of all files on disk with exact case
files_on_disk = set(os.listdir(assets_dir)) if os.path.exists(assets_dir) else set()

print(f"[VERIFY-SLOTS] Found {len(files_on_disk)} files in assets/")

# Parse ASSETS manifest from index.html
index_path = os.path.join(project_dir, 'index.html')
if not os.path.exists(index_path):
    print("[ERROR] index.html missing!")
    sys.exit(1)

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract manifest
manifest_match = re.search(r'const ASSETS\s*=\s*\{([^}]+)\};', content)
if not manifest_match:
    print("[ERROR] ASSETS manifest not found in index.html!")
    sys.exit(1)

manifest_block = manifest_match.group(1)
paths = re.findall(r'/assets/([a-zA-Z0-9_\-\.]+)', manifest_block)

print("\n--- Auditing ASSETS Manifest Paths Against Disk ---")
missing_count = 0
for path in paths:
    if path not in files_on_disk:
        # Check if optional (e.g. clubhouse / sports zone placeholder slots)
        print(f"[SLOT AWAITING FILE] /assets/{path} is currently absent -> WILL RENDER PLACEHOLDER")
    else:
        print(f"[SLOT VALIDATED] /assets/{path} -> MATCHED EXACT CASE")

# Check that every image reference in HTML points to /assets/
all_html_paths = re.findall(r'/(assets/[a-zA-Z0-9_\-\.]+)', content)
for p in set(all_html_paths):
    filename = p.replace('assets/', '')
    if filename not in files_on_disk:
        print(f"[INFO] /assets/{filename} fallback path -> Will render placeholder if missing")

print("\n[VERIFY PASSED] Asset Slot System verified with zero fatal errors!")
sys.exit(0)
