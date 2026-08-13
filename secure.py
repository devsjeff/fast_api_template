import argon2
hasher = argon2.PasswordHasher()

def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password( hashed_password: str ,password: str) -> bool:
    try:
        return hasher.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False