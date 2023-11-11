from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import padding


def aes_encrypt(key: str, plaintext: str):
    # Convert key to bytes and pad if necessary
    key = key.ljust(32, '\0')[:32].encode('utf-8')

    # Convert plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    # Create AES encryptor
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Use PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext_bytes) + padder.finalize()

    # Encrypt data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return base64-encoded ciphertext
    return b64encode(ciphertext).decode('utf-8')


def aes_decrypt(key: str, ciphertext: str):
    # Convert key to Unicode string
    key = key.ljust(32, '\0').encode('utf-8')[:32]

    # Convert ciphertext to bytes
    ciphertext_bytes = b64decode(ciphertext)

    # Create AES decryptor
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt data
    decrypted_data = decryptor.update(ciphertext_bytes) + decryptor.finalize()

    # Use PKCS7 unpadding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    return plaintext.decode('utf-8')



# 示例
# key = 'mysecretkey'
# plaintext = 'Hello, World!'
#
# encrypted_text = aes_encrypt(key, plaintext)
# print(f'Encrypted Text: {encrypted_text}')
#
# decrypted_text = aes_decrypt(key, encrypted_text)
# print(f'Decrypted Text: {decrypted_text}')
