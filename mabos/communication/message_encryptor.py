# mabos/communication/message_encryptor.py
from cryptography.fernet import Fernet

class MessageEncryptor:
    def encrypt(self, message):
        # Encrypt the message using a secure encryption algorithm
        # Generate a key for encryption
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        # Convert message to bytes if it's a string
        if isinstance(message, str):
            message = message.encode('utf-8')

        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message)

        return encrypted_message

    def decrypt(self, encrypted_message):
        # Generate the decryption key
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)

        # Decrypt the encrypted message
        decrypted_message = cipher_suite.decrypt(encrypted_message)

        # Convert the decrypted message back to string if needed
        if isinstance(decrypted_message, bytes):
            decrypted_message = decrypted_message.decode('utf-8')

        return decrypted_message
        pass