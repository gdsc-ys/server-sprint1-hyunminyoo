from pydantic.main import BaseModel


class GetNickResp(BaseModel):
    nickname: str

class PutNickReq(BaseModel):
    uid: int
    nickname: str
