from pydantic.main import BaseModel


class LoginReq(BaseModel):
    id: str
    pw: str

class LoginReps(BaseModel):
    uid: int