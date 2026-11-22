# Linux Utilities

Two simple scripts to keep your server safe and clean.

## Secure Vault

Encrypts and decrypts files using a password. It is useful for hiding sensitive data on your disk.

**Usage**
```bash
python3 secure_vault.py encrypt secret.txt
python3 secure_vault.py decrypt secret.txt.enc
```

## System Guard

Monitors your server health, cleans up old temporary files, and checks if your important files have been changed without permission.

**Usage**
```bash
python3 sys_guard.py monitor
python3 sys_guard.py clean
python3 sys_guard.py verify /home/user/documents
```

## Note

Both scripts will install any missing Python libraries automatically when you run them for the first time.