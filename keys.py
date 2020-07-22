import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding



class AsymetricKey():
    def __init__(self, key):
        self.key = key

    @staticmethod
    def from_pem(key_value, password="a"):
        private_key = serialization.load_pem_private_key(
            key_value.encode(),
            password=password.encode(),
            backend=default_backend()
            )
        return AsymetricKey(private_key)

    @staticmethod
    def from_generate():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        return AsymetricKey(private_key)

    def to_pem(self, password="a"):
        pem = self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
            )
        return pem.decode()

    def public_key(self):
        return self.key.public_key()

    def public_serialise(self):
        pub_bytes = self.key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        return pub_bytes.decode()

    def encrypt(self, data):
        message = data.encode()

        encrypted = self.public_key().encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
        return base64.b64encode(encrypted).decode()

    def decrypt(self, data):
        data = base64.b64decode(data.encode())

        original_message = self.key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
        return original_message.decode()
