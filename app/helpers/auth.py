import bcrypt


def get_password_hash(password:str):
    salt = bcrypt.gensalt()
    byte_pwd = password.encode("UTF-8")
    password_hash = bcrypt.hashpw(bcrypt.hashpw(byte_pwd, salt), salt)
    return password_hash, salt