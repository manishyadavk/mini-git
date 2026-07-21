import hashlib


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def hash_file(path, chunk_size=65536):
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
