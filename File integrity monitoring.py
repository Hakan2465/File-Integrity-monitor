import argparse
import json
import os
import hashlib

# hier setzen wir die hashlib library ein, geben der hashlib.sha256() ein neuen namen.   
def hash_file(file_path):
    sha256 = hashlib.sha256()
    try:
        # In Z.10 öffnen wir die Datei, lesen sie in binär
        with open(file_path, "rb") as f:
            # hier gehen wir einen loop durch, lesen durch die Datei in chunks (4kb), nutzen lambda um die nächsten chunks zu starten. 
            # [b""] nutzen wir als stoppzeichen, damit iter weiß, wann es stoppen muss.
            for chunk in iter(lambda: f.read (4096), b""):
                # hier nutzen sha256.updte(chunk) um die chunks(4096b) zu aktualisieren, um die gemeinsam zu verbinden.
                sha256.update(chunk)
                # output ist sha256.hexdigest(), was die zusammengestellten chunks in einen hash verschlüsselt.
            return sha256.hexdigest()
        # except ist genutzt, damit der Code weiß was zu tun ist, wenn die try: Funktion nicht klappt (permission, korrupten Daten,etc.)
    except:
        # wenn es nicht klappt, wird None returned, was den Code zum stoppen bringt.
        return None
    
def fetch_all_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.join(root,file)

def save_hashes(hash_dict, filename="hashes.json"):
    with open(filename, "w") as f:
        json.dump(hash_dict, f, indent=2)

def load_hashes(filename="hashes.json"):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

# hier nutze ich argparse als CLI Setup, da ich das CLI bevorzuge | es ist nicht nötig, jedoch mag ich es zu nutzen.
parser = argparse.ArgumentParser(description="File Integrity Checker")
parser.add_argument("--check", type=str, help="Directory to check for changes")
args = parser.parse_args()

if not args.check:
    print("Usage: python script.py --check /path/to/directory")
    exit(1)

directory_to_check = args.check

# Haupt punkt des codes in der die Hashes verglichen werden.
old_hashes = load_hashes()
current_hashes = {}

for filepath in fetch_all_files(directory_to_check):
    file_hash = hash_file(filepath)
    if file_hash:
        current_hashes[filepath] = file_hash

# Compare
for path, hash_val in current_hashes.items():
    if path not in old_hashes:
        print(f"[+] New File: {path}")
    elif old_hashes[path] != hash_val:
        print(f"[!] Modified: {path}")
    else:
        print(f"[=] Unchanged: {path}")

for path in old_hashes:
    if path not in current_hashes:
        print(f"[-] Deleted: {path}")

# Neu gesetzte hashes werden die neuen, die alten werden entfernt.
save_hashes(current_hashes)