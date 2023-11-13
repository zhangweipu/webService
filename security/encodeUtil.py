from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode


class SecurityUtils:
    key = "shidh,..,@!@#344$5"
    iv = "sfiojifjoffdwert"
    AES_MODE = algorithms.AES
    CHARSET_NAME = "UTF-8"

    #  x4XU4mk3b4xQqPkFq60KOg==  x4XU4mk3b4xQqPkFq60KOg==

    @classmethod
    def encrypt(cls, key, iv, plaintext):
        key = cls.generate_key(key)
        cipher = Cipher(cls.AES_MODE(key), modes.CBC(iv.encode('utf-8')), backend=default_backend())
        encryptor = cipher.encryptor()
        # 使用 PKCS7 填充方式
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode(cls.CHARSET_NAME)) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return b64encode(ciphertext).decode(cls.CHARSET_NAME)

    @classmethod
    def decrypt(cls, key, iv, cipher_text):
        key = cls.generate_key(key)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv.encode("utf-8")), backend=default_backend())
        decryptor = cipher.decryptor()

        ciphertext_bytes = b64decode(cipher_text)
        decrypted_bytes = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        return decrypted_bytes.decode('utf-8')
    @classmethod
    def generate_key(cls, key):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            iterations=1000,
            salt=key.encode('utf-8'),
            length=32,
            backend=default_backend()
        )
        key_bytes = kdf.derive(key.encode('utf-8'))
        return key_bytes


#
# # # 示例
# plaintext = 'com.wp.itime'
# encrypted_text = SecurityUtils.encrypt(SecurityUtils.key, SecurityUtils.iv, plaintext)
# print(f'Encrypted Text: {encrypted_text}')
#
# decrypted_text = SecurityUtils.decrypt(SecurityUtils.key, SecurityUtils.iv, "x4XU4mk3b4xQqPkFq60KOg==")
# print(f'Decrypted Text: {decrypted_text}')
# print(type(decrypted_text))
# print(type("com.wp.itime"))
# ssd=decrypted_text.replace('\x04', '')
# print(ssd)
# if ssd == 'com.wp.itime':
#     print("sss")
# else:
#     print("aaaaa")
# for i in ssd:
#     if i!='\t':
#         print(i)