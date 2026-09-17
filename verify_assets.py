import os
import sys
import re

project_dir = os.path.dirname(os.path.abspath(__file__))

def get_exact_files_on_disk(dir_path):
    if not os.path.exists(dir_path):
        return set()
    files = set()
    for root, dirs, fnames in os.walk(dir_path):
        for fn in fnames:
            rel = os.path.relpath(os.path.join(root, fn), dir_path)
            # normalize to forward slash
            files.add(rel.replace('\\', '/'))
    return files

assets_disk = get_exact_files_on_disk(os.path.join(project_dir, 'assets'))
public_disk = get_exact_files_on_disk(os.path.join(project_dir, 'public'))

print(f"[VERIFY] Found {len(assets_disk)} files in assets/")
print(f"[VERIFY] Found {len(public_disk)} files in public/")

files_to_check = ['index.html', 'thank-you.html']
missing_count = 0

for fname in files_to_check:
    fpath = os.path.join(project_dir, fname)
    if not os.path.exists(fpath):
        print(f"[ERROR] Missing file: {fname}")
        missing_count += 1
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all /assets/... references
    pattern = r'/(assets/[a-zA-Z0-9_\-\./\+]+)'
    matches = re.findall(pattern, content)
    
    for ref in set(matches):
        # strip query parameters or srcset multipliers if captured
        clean_ref = ref.split()[0].split('?')[0].split('#')[0]
        subpath = clean_ref.replace('assets/', '', 1)
        
        # Check case-sensitive match against assets_disk
        if subpath not in assets_disk:
            print(f"[FAIL] {fname} references '/{clean_ref}' but '{subpath}' is NOT found in assets/ with exact casing!")
            missing_count += 1
        else:
            print(f"[OK] {fname} -> /{clean_ref}")

if missing_count > 0:
    print(f"\n[VERIFY FAILED] Total missing/casing errors: {missing_count}")
    sys.exit(1)

print("\n[VERIFY PASSED] All referenced assets exist on disk with exact case matching!")
sys.exit(0)
