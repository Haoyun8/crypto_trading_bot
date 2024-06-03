from cryptography.fernet import Fernet

class Security:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, message):
        return self.cipher.encrypt(message.encode())

    def decrypt(self, token):
        return self.cipher.decrypt(token).decode()

# Usage example
# security = Security()
# encrypted = security.encrypt("my_api_secret")
# decrypted = security.decrypt(encrypted)
# print(decrypted)
