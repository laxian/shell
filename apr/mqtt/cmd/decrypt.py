from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


def decrypt(private_key, en_str):
    en_bytes = base64.b64decode(en_str)

    # 初始化解密器
    cipher = PKCS1_OAEP.new(private_key)

    decrypted_bytes = bytearray()
    chunk_size = 128
    while en_bytes:
        chunk, en_bytes = en_bytes[:chunk_size], en_bytes[chunk_size:]
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_bytes.extend(decrypted_chunk)

    decrypted_string = decrypted_bytes.decode("utf-8")
    return decrypted_string


# 调用示例
private_key_path = "./private/private.pem"  # 替换为实际的私钥文件路径
en_str = "e/gcV6kCRcN0g2mLcKeMpq4S+TDZVDq+ECMtcHuv2acm5GjVKP+Y0Dv/fNx53jKDKDVTD/0O9fOWe+yjZJNjwOw9/Jdk/QTcKput5gzX2FZB0/63lHo2+wsxpttz3c/6b7jCzJC9FexEyL2QE7v9gsQbzcpIQnMjHaADNLDZJ7Q="  # 将字符串替换为实际的Base64编码的加密字符串

with open(private_key_path, "rb") as f:
    private_key = RSA.import_key(f.read())

decrypted_text = decrypt(private_key, en_str)
print("Decrypted text:", decrypted_text)
