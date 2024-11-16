import jwt
from datetime import datetime, timedelta


class JWTTokenFactory:
    """Базовый интерфейс для создания JWT-токенов."""

    def create_token(self, user_id, algorithm, expiration_minutes=60):
        raise NotImplementedError("Метод должен быть реализован в наследуемом классе")


class JWTTokenFactoryHMAC(JWTTokenFactory):
    """Реализация фабрики для HMAC-шифрования токенов."""

    def __init__(self, secret_key="your_secret_key"):
        self.secret_key = secret_key

    def create_token(self, user_id, algorithm="HS256", expiration_minutes=60):
        data = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expiration_minutes),
        }
        return jwt.encode(data, self.secret_key, algorithm=algorithm)
