from pydantic import BaseModel, Field


class EmailSignUpRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320, description="User email address")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")


class EmailSignInRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320, description="User email address")
    password: str = Field(..., min_length=1, description="User password")


class YandexSignUpRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Yandex OAuth authorization code")


class YandexSignInRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Yandex OAuth authorization code")


class AuthResponse(BaseModel):
    user_id: str = Field(..., description="User ID")
    access_token: str = Field(..., description="Access token for authentication")
