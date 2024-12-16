import os
import uuid
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20


class SecureTemporaryFile:
    def __init__(self, filesdir):
        """
        Initialize ChaCha20 encryption with a randomly generated key and nonce.
        """
        self.fd = None
        self.key = os.urandom(32)  # ChaCha20 requires a 256-bit (32-byte) key
        self.key_id = str(uuid.uuid4())  # UUID as a string for the file name
        self.nonce = os.urandom(16)  # 128-bit nonce
        self.cipher = Cipher(ChaCha20(self.key, self.nonce), mode=None)
        self.filepath = os.path.join(filesdir, self.key_id)
        self.size = 0
        self.enc = self.cipher.encryptor()
        self.dec = None

    def open(self, mode):
        """
        Open the file for read or write operations.
        """
        if mode == 'w':
            self.fd = os.open(self.filepath, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            self.dec = None  # Reset decryption object on write mode
        else:
            self.fd = os.open(self.filepath, os.O_RDONLY)
            self.dec = self.cipher.decryptor()
        return self

    def write(self, data):
        """
        Write encrypted data to the file.
        """
        if isinstance(data, str):
            data = data.encode()

        encrypted_data = self.enc.update(data)
        os.write(self.fd, encrypted_data)
        self.size += len(data)

    def read(self, c=None):
        """
        Read and decrypt data from the file.
        """
        if c is None:
            data = os.read(self.fd)
        else:
            data = os.read(self.fd, c)

        if data:
            return self.dec.update(data)
        return self.dec.finalize()

    def close(self):
        """
        Close the file descriptor.
        """
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        """
        Ensure proper cleanup by closing and deleting the file.
        """
        self.close()
        try:
            os.remove(self.filepath)
        except FileNotFoundError:
            pass
