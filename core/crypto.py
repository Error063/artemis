import zlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class CipherAES:
    def __init__(self,AES_KEY,AES_IV, BLOCK_SIZE=128, KEY_SIZE=256):
        self.BLOCK_SIZE = BLOCK_SIZE
        self.KEY_SIZE = KEY_SIZE
        self.AES_KEY = AES_KEY
        self.AES_IV  = AES_IV

    def _pad(self,data):
        block_size = self.BLOCK_SIZE // 8
        padding_length = block_size - len(data) % block_size
        return data + bytes([padding_length]) * padding_length

    def _unpad(self, padded_data):
        pad_char = padded_data[-1]
        if not 1 <= pad_char <= self.BLOCK_SIZE // 8:
            raise ValueError("Invalid padding")
        return padded_data[:-pad_char]

    def encrypt(self, plaintext):
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.AES_KEY), modes.CBC(self.AES_IV), backend=backend)
        encryptor = cipher.encryptor()

        padded_plaintext = self._pad(plaintext)
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.AES_KEY), modes.CBC(self.AES_IV), backend=backend)
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return self._unpad(decrypted_data)