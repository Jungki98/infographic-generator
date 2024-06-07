import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)  
    hash_object = hashlib.sha256()
    hash_object.update(salt + password.encode('utf-8'))
    return salt, hash_object.hexdigest()

def check_password(password, salt, stored_hash):
    hash_object = hashlib.sha256()
    hash_object.update(salt + password.encode('utf-8'))
    return hash_object.hexdigest() == stored_hash