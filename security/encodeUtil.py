from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode


class SecurityUtils:
    key = b"shidh,..,@!@#344$5"
    iv = b"sfiojifjoffdwert"
    AES_MODE = algorithms.AES
    CHARSET_NAME = "UTF-8"

    @classmethod
    def encrypt(cls, key, iv, plaintext):
        key = cls.generate_key(key)
        cipher = Cipher(cls.AES_MODE(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padded_data = plaintext.encode(cls.CHARSET_NAME)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return b64encode(ciphertext).decode(cls.CHARSET_NAME)

    @classmethod
    def decrypt(cls, key, iv, cipher_text):
        key = cls.generate_key(key)
        cipher = Cipher(cls.AES_MODE(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        ciphertext = b64decode(cipher_text)
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

        return decrypted_data.decode(cls.CHARSET_NAME)

    @classmethod
    def generate_key(cls, key):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=1000,
            salt=key,
            length=32,
            backend=default_backend()
        )
        key_bytes = kdf.derive(key)
        return key_bytes


# # 示例
# plaintext = 'Hello, World!'
# encrypted_text = SecurityUtils.encrypt(SecurityUtils.key, SecurityUtils.iv, plaintext)
# print(f'Encrypted Text: {encrypted_text}')
#
# decrypted_text = SecurityUtils.decrypt(SecurityUtils.key, SecurityUtils.iv, encrypted_text)
# print(f'Decrypted Text: {decrypted_text}')
