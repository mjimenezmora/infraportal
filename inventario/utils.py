id="enc1"
from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
fernet = Fernet(KEY)

def encriptar_password(password):
    return fernet.encrypt(password.encode()).decode()

def desencriptar_password(password_encriptado):
    return fernet.decrypt(password_encriptado.encode()).decode()
