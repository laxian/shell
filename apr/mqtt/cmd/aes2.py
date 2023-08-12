import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import subprocess


SALTED = b"paramstr"


def aes_encrypt(input: str, passphrase: str) -> str:
    input_bytes = input.encode("utf-8")
    passphrase_bytes = passphrase.encode("utf-8")
    encrypted_bytes = _encrypt(input_bytes, passphrase_bytes)
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def encrypt_bytes(input: bytes, passphrase: bytes) -> bytes:
    encrypted_bytes = _encrypt(input, passphrase)
    return base64.b64encode(encrypted_bytes)


def aes_decrypt(encrypted: str, passphrase: str) -> str:
    encrypted_bytes = base64.b64decode(encrypted)
    passphrase_bytes = passphrase.encode("utf-8")
    decrypted_bytes = _decrypt(encrypted_bytes, passphrase_bytes)
    return decrypted_bytes.decode("utf-8")


def decrypt_bytes(encrypted: bytes, passphrase: bytes) -> bytes:
    encrypted_bytes = base64.b64decode(encrypted)
    decrypted_bytes = _decrypt(encrypted_bytes, passphrase)
    return decrypted_bytes


def _encrypt(input: bytes, passphrase: bytes) -> bytes:
    salt = get_random_bytes(8)
    key, iv = derive_key_and_iv(passphrase, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    encrypted = cipher.encrypt(pad(input, AES.block_size))
    return SALTED + salt + encrypted


def _decrypt(data: bytes, passphrase: bytes) -> bytes:
    salt = data[8:16]
    if data[:8] != SALTED:
        raise ValueError("Invalid encrypted data")

    key, iv = derive_key_and_iv(passphrase, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(data[16:]), AES.block_size)


def derive_key_and_iv(passphrase: bytes, salt: bytes) -> tuple:
    digest = hashlib.md5()
    digest.update(passphrase + salt)
    dx = b""
    di = b""
    for i in range(3):
        di = digest.digest()
        digest.update(di + passphrase + salt)
        dx += di

    return dx[:32], dx[32:48]


def aes_decrypt_java(encrypted: str, passphrase: str) -> str:
    print(f"-> java -cp ./bin src.Aes '{encrypted}' '{passphrase}' decrypt")
    # 调用命令行并执行一个简单的命令
    result = subprocess.run(
        ["java", "-cp", "./bin", "src.Aes", encrypted, passphrase, "decrypt"],
        capture_output=True,
        text=True,
        shell=False,
    )
    return result.stdout


def aes_encrypt_java(plaintext: str, passphrase: str) -> str:
    print(f"-> java -cp ./bin src.Aes '{plaintext}' '{passphrase}' encrypt")
    # 调用命令行并执行一个简单的命令
    result = subprocess.run(
        ["java", "-cp", "./bin", "src.Aes", plaintext, passphrase, "encrypt"],
        capture_output=True,
        text=True,
        shell=False,
    )
    return result.stdout.strip()


def concat(a: bytes, b: bytes) -> bytes:
    return a + b


if __name__ == "__main__":
    key = "c12307371ee1490e"
    enc = '{"command":"settings get secure robot_id","downloadKey":""}'
    ans = "cGFyYW1zdHJQxp6MRY+J3N+LtlCwfOjI5wgrrc9jZ0gAK1xNwnNuLQD+YhXQl8wV/9Se08XTbpf+dzFSuGWKRudtSv2EGK5163WUXxfLDqc="
    enc = aes_encrypt_java(enc, key).strip()
    print(enc)
    dec = aes_decrypt_java(enc, key)
    print(dec)
