import hashlib
from io import BytesIO

def calculate_checksum_of_file(fileName: str) -> str:
    with open(fileName, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()

def calculate_checksum_of_bytes(bytes: BytesIO) -> str:
    file_hash = hashlib.sha256()
    while chunk := bytes.read(8192):
        file_hash.update(chunk)
    
    bytes.seek(0)

    return file_hash.hexdigest()