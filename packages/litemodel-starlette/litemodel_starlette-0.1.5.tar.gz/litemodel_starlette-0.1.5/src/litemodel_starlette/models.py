import bcrypt
from litemodel.async_core import Model


class AdminUser(Model):
    username: str
    password: str
    role: str

    def password_match(self, non_hashed_password: str | bytes) -> bool:
        return bcrypt.checkpw(self.password.encode(), AdminUser.hash_password(non_hashed_password))

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def identity(self) -> int:
        return self.id

    @staticmethod
    def hash_password(non_hashed_password: str | bytes) -> bytes:
        if isinstance(non_hashed_password, str):
            non_hashed_password = non_hashed_password.encode()
        salt = bcrypt.gensalt()
        # Hashing the password
        return bcrypt.hashpw(non_hashed_password, salt)
