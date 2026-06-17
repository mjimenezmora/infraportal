id="enc1"
from cryptography.fernet import Fernet
# 1. Pegamos la llave fija como un string de bytes (anteponiendo la 'b')
KEY = b'8LFsLhT9xeD-pxvpw2q5rRkKoRX4l4u82p8fEKZHedc='
# Inicializamos el objeto Fernet con la llave persistente
fernet = Fernet(KEY)

def encriptar_password(password):
    if not password:
        return ""
    return fernet.encrypt(password.encode()).decode()

def desencriptar_password(password_encriptado):
    if not password_encriptado:
        return ""
    return fernet.decrypt(password_encriptado.encode()).decode()
