from pydantic import BaseModel


class ServerModel(BaseModel):
    password: str | None = None
    port: int | None = None
    timeout: str | None = None
    bandwidth: int | None = None
    users: int | None = None
    welcomeText: str | None = None
    registerName: str | None = None