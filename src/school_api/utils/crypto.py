from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

def encrypt_password(password, public_key):
    """使用RSA加密密码"""
    modulus = public_key['modulus']
    exponent = public_key['exponent']
    
    n = int.from_bytes(base64.b64decode(modulus), 'big')
    e = int.from_bytes(base64.b64decode(exponent), 'big')
    
    rsa_key = RSA.construct((n, e))
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypted = cipher.encrypt(password.encode())
    
    return base64.b64encode(encrypted).decode()