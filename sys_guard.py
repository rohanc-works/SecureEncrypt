```python
#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib
import time

try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def monitor_resources():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    print(f"CPU: {cpu}% | RAM: {mem}% | Disk: {disk}%")

def clean_temp():
    temp_dirs = ['/tmp', '/var/tmp']
    count = 0
    now = time.time()
    for d in temp_dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            path = os.path.join(d, f)
            if os.path.isfile(path) and (now - os.path.getmtime(path)) > 86400:
                try:
                    os.remove(path)
                    count += 1
                except OSError:
                    pass
    print(f"Cleaned {count} old temporary files")

def verify_integrity(directory):
    manifest = os.path.join(directory, ".integrity_manifest")
    if not os.path.exists(manifest):
        hashes = {}
        for root, _, files in os.walk(directory):
            for f in files:
                if f == ".integrity_manifest":
                    continue
                path = os.path.join(root, f)
                hashes[path] = get_file_hash(path)
        with open(manifest, "w") as mf:
            for p, h in hashes.items():
                mf.write(f"{h}  {p}\n")
        print("Manifest created")
    else:
        changes = 0
        with open(manifest, "r") as mf:
            for line in mf:
                h, p = line.strip().split("  ", 1)
                if os.path.exists(p):
                    if get_file_hash(p) != h:
                        print(f"Changed: {p}")
                        changes += 1
                else:
                    print(f"Missing: {p}")
                    changes += 1
        if changes == 0:
            print("No changes detected")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sys_guard.py [monitor|clean|verify <dir>]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "monitor":
        monitor_resources()
    elif cmd == "clean":
        clean_temp()
    elif cmd == "verify":
        if len(sys.argv) != 3:
            print("Usage: python sys_guard.py verify <directory>")
            sys.exit(1)
        verify_integrity(sys.argv[2])
    else:
        print("Unknown command")
```
