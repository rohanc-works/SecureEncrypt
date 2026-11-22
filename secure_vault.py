#!/usr/bin/env python3
import os
import sys
import subprocess
import getpass

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return kdf.derive(password.encode())

def process_file(file_path: str, password: str, mode: str):
    with open(file_path, "rb") as f:
        data = f.read()

    if mode == "encrypt":
        salt = os.urandom(16)
        key = derive_key(password, salt)
        fernet = Fernet(key)
        token = fernet.encrypt(data)
        output_path = file_path + ".enc"
        with open(output_path, "wb") as f:
            f.write(salt + token)
        os.remove(file_path)

    elif mode == "decrypt":
        if not file_path.endswith(".enc"):
            print("Error: File does not have .enc extension")
            return
        salt = data[:16]
        encrypted_data = data[16:]
        key = derive_key(password, salt)
        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception:
            print("Error: Decryption failed. Wrong password or corrupted file.")
            return
        output_path = file_path[:-4]
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
        os.remove(file_path)

    print(f"Success: {os.path.basename(output_path)}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ["encrypt", "decrypt"]:
        print(f"Usage: {sys.argv[0]} [encrypt|decrypt] <file_path>")
        sys.exit(1)

    action = sys.argv[1]
    target = sys.argv[2]
    
    if not os.path.exists(target):
        print("Error: File not found")
        sys.exit(1)

    pwd = getpass.getpass("Passkey: ")
    process_file(target, pwd, action)