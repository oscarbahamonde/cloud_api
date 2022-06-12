from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Dict, Optional, Union  
from faunadb.objects import Ref, _Expr as Expr, Query, FaunaTime as Ts

class Prototype(BaseModel):
    ref:Optional[Ref] = None
    ts:Optional[Ts] = None
    data:Dict = {}
    class Config:
        schema_extra = {
            'example': {
                'ref': Ref('classes/prototype'),
                'ts': Ts(2020, 1, 1),
                'data': {
                    'name': 'prototype',
                    'description': 'prototype description',
                    'url': HttpUrl('https://example.com'),
                    'email': EmailStr('papo@chanchitofeliz.com')
                }
            }
        }
    
class User(Prototype):
    data = {
        'uid': str,
        'displayName': str,
        'email': EmailStr,
        'photoURL': Optional[HttpUrl],
        'providerId': str,
        'UserAgent': Optional[str],
        'hosts': List[str],
        'token':{
            'accessToken': Optional[str],
            'expiresIn': Optional[int],
            'refreshToken': Optional[str],
            'idToken': Optional[str],
        },
        'OTP':{
            'secret': Optional[str],
            'code': Optional[str],
            'expiresIn': Optional[int],
        },
        'QRcode': {
            'url': Optional[HttpUrl],
            'payload': Optional[str],
            'expiration': Optional[Ts],
        }
    }
    