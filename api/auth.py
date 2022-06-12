from pydantic import BaseModel
from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from api.config import process

login = APIRouter()
auth = Cognito(
    region=process.env.aws_region_name, 
    userPoolId=process.env.aws_user_pool_id,
    client_id=process.env.aws_app_client_id,
)

@login.get('/token')
def RedirectCode(code:str):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': process.env.aws_app_client_id,
        'client_secret': process.env.aws_app_client_secret,
        'code': code,
        'redirect_uri': 'https://api.chanchito.net/login/token'



@login.get("/login", dependencies=[Depends(auth)])
def secure():
    # access token is valid
    return "Hello"


class AccessUser(BaseModel):
    sub: str


@login.get("/access/")
def secure_access(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    # access token is valid and getting user info from access token
    return f"Hello", {current_user.sub}


get_current_user = CognitoCurrentUser(
    region=process.env.aws_region_name,
    userPoolId=process.env.aws_user_pool_id,
    client_id=process.env.aws_app_client_id,
)


@login.get("/user/")
def secure_user(current_user: CognitoClaims = Depends(get_current_user)):
    # ID token is valid and getting user info from ID token
    return f"Hello, {current_user.username}"