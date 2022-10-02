from pydantic.main import BaseModel
from typing import List


class SingleFavorite(BaseModel):
    favorite_id: int
    station_id: int

class GetFavoritesResp(BaseModel):
    favorite_list: List[SingleFavorite]

class PostFavoriteReq(BaseModel):
    uid: int
    station_id: int
