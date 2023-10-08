from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #what the default hashing algorigthm

def hash(password: str):
    return password_context.hash(password)


def verify(plain_password, hased_password):
    return password_context.verify(plain_password, hased_password)