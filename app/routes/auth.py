from datetime import datetime
from fastapi import APIRouter
from starlette.responses import Response

from models.auth_model import LoginReps, LoginReq

router = APIRouter(prefix="/auth")

@router.get("/login",
    response_model=LoginReps,
    responses={
        # 500: {"model": "ERROR MODEL", "description": "ERROR DESCRIPTION"},
        500: {"description": "ERROR DESCRIPTION"},
    },
)
async def login(req: LoginReq):
    """
    login api
    get user info and log user in
    return 404 if user info is not in DB
    """
    # check if user is valid
    isUserValid = checkValidUser(req.id, req.pw)

    if isUserValid:
        return Response(f"Login success")

    else:
        return Response(f"Login fail")

def checkValidUser(id:str, pw:str):
    return True
