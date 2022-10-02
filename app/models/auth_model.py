from pydantic.main import BaseModel


# class LoginReq(BaseModel):
#     id: str
#     pw: str

class LoginReps(BaseModel):
    uid: int
    sessionID: int

class RegUserReq(BaseModel):
    id:str
    pw:str
    nickname:str

class RegUserReps(BaseModel):
    uid: int