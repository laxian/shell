from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b"1234567890abcdef"  # 16字节的密钥
iv = b"1234567887654321"  # 16字节的初始向量

# 加密
def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC, key[::-1])
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    return base64.b64encode(ciphertext).decode("utf-8")


# 解密
def aes_decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, key[::-1])
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")


# 用法示例
plaintext = "hello world"
ciphertext = aes_encrypt(plaintext, key)
decrypted = aes_decrypt('cGFyYW1zdHL5K8HYCYYuEGpUZ+xCrkNP0N8lfEt5QzNFLMApqqiMGLfwG1PfdSZwV5Po9TEBD0XxI+fuMrx1oel2Dme0CutrONiNaxtc8KE=', b'c12307371ee1490e')
print(decrypted)  # 输出 'hello world'
