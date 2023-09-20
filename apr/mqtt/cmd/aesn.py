import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

SALTED = b"paramstr"


def _encrypt(data, passphrase):
    salt = os.urandom(8)
    key, iv = derive_key_and_iv(passphrase, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return SALTED + salt + encrypted_data


def _decrypt(data, passphrase):
    salt = data[8:16]
    if data[:8] != SALTED:
        raise ValueError("Invalid crypted data")
    key, iv = derive_key_and_iv(passphrase, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(data[16:]), AES.block_size)
    return decrypted_data


def derive_key_and_iv(passphrase, salt):
    md5 = lambda x: hashlib.md5(x).digest()
    pass_salt = passphrase + salt
    dx = di = b""
    for i in range(3):
        di = md5(di + pass_salt)
        dx += di
    return dx[:32], dx[32:48]


def encrypt(input_text, passphrase):
    return base64.b64encode(
        _encrypt(input_text.encode("utf-8"), passphrase.encode("utf-8"))
    )


def decrypt(crypted, passphrase):
    return _decrypt(base64.b64decode(crypted), passphrase.encode("utf-8"))


def encrypt_bytes(input_bytes, passphrase):
    return base64.b64encode(_encrypt(input_bytes, passphrase.encode("utf-8")))


def decrypt_bytes(crypted_bytes, passphrase):
    return _decrypt(base64.b64decode(crypted_bytes), passphrase.encode("utf-8"))


def encrypt_str(input_text, passphrase):
    return encrypt(input_text, passphrase).decode("utf-8")


def decrypt_str(crypted, passphrase):
    return decrypt(crypted.encode("utf-8"), passphrase).decode("utf-8")


def main():
    passphrase = "mysecretkey"
    input_text = "Hello, this is a test!"

    encrypted_text = encrypt(input_text, passphrase)
    print(f"Encrypted text: {encrypted_text}")

    decrypted_text = decrypt(encrypted_text, passphrase)
    print(f"Decrypted text: {decrypted_text.decode('utf-8')}")

    encrypted_text = encrypt_str(input_text, passphrase)
    print(f"Encrypted text: {encrypted_text}")

    decrypted_text = decrypt_str(encrypted_text, passphrase)
    print(f"Decrypted text: {decrypted_text}")


if __name__ == "__main__":
    main()
