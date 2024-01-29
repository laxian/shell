from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.exceptions import InvalidSignature
import base64

# 生成密钥对
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    return private_key, public_key

# 使用私钥进行加密
def rsa_encrypt(public_key, plaintext):
    encrypted_data = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_data

# 使用私钥进行解密
def rsa_decrypt(private_key, encrypted_data):
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data.decode('utf-8')

def rsa_decrypt_with_file(private_key_path, encrypted_data):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data.decode('utf-8')

# 使用私钥进行签名
def rsa_sign(private_key, data):
    signature = private_key.sign(
        data.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def rsa_sign_sha1(private_key, data):
    signature = private_key.sign(
        data.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA1()  # 使用 SHA-1 哈希算法
    )
    return signature

# 使用公钥进行验证签名
def rsa_verify(public_key, data, signature):
    try:
        public_key.verify(
            signature,
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    
# 使用公钥进行签名验证
def rsa_verify_with_file(public_key_path, data, signature):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    try:
        public_key.verify(
            signature,
            data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


# 从文件读取私钥
def load_private_key_from_file(private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

# 从文件读取公钥
def load_public_key_from_file(public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key



if __name__ == '__main__':
    print("=====")
    # 生成密钥对
    private_key, public_key = generate_rsa_key_pair()

    # 测试数据
    plaintext = "Hello, RSA!"
    encrypted_data = rsa_encrypt(public_key, plaintext)
    decrypted_text = rsa_decrypt(private_key, encrypted_data)

    signature = rsa_sign(private_key, plaintext)
    is_valid_signature = rsa_verify(public_key, plaintext, signature)

    print("Original Text:", plaintext)
    print("Encrypted Data:", encrypted_data)
    print("Decrypted Text:", decrypted_text)
    print("Signature:", signature)
    print("Is Valid Signature:", is_valid_signature)