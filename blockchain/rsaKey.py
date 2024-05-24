import json

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class Encrypt:
    @staticmethod
    def generate_and_save_rsa_key_pair(private_key_file, public_key_file, key_size=2048):
        # generate rsa keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )

        # save private key into private key file
        with open(private_key_file, 'wb') as f:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            f.write(private_key_bytes)

        # save public key into public key file
        public_key = private_key.public_key()
        with open(public_key_file, 'wb') as f:
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            f.write(public_key_bytes)

    @staticmethod
    def load_rsa_private_key(private_key_file):
        # load private key from the file
        with open(private_key_file, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        return private_key

    @staticmethod
    def load_rsa_public_key(public_key_file):
        # load public key from the file
        with open(public_key_file, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        return public_key

    @staticmethod
    def encryption(message):

        mess_str=str(message)
        # convert JSON message into bytes[]
        message_bytes = mess_str.encode('utf-8')

        # Encrypt the message with the public key
        encrypted_message = Encrypt.load_rsa_public_key('public_key.pem').encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_message

    @staticmethod
    def decryption(encrypted_message):
        #decrypt the message with the private key
        decrypted_message_bytes = Encrypt.load_rsa_private_key('private_key.pem').decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # convert bytes[] into string
        decrypted_message = decrypted_message_bytes.decode('utf-8')

        return decrypted_message
