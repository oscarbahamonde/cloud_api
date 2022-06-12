from config import process

from faunadb import query as q
from faunadb.client import FaunaClient
from faunadb.objects import Ref, Query, _Expr, FaunaTime
from faunadb.errors import (
    FaunaError,
    BadRequest,
    NotFound,
    Unauthorized
)
from pydantic import BaseModel, Field, BaseConfig
from pydantic.error_wrappers import ValidationError, _ErrorDictRequired
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union
from fastapi import APIRouter, Request, Response
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

client = FaunaClient(secret=process.env.fauna_secret)




class DocRef(BaseModel):

    class Config(BaseConfig):
        arbitrary_types_allowed = True

    ref: Ref
    ts: FaunaTime
    data: Dict


class FaunaORM(ABC):

    @abstractmethod
    def createOne(self, instance: BaseModel) -> DocRef:
        pass
    
    @abstractmethod
    def createMany(self, instances: List[BaseModel]) -> List[DocRef]:
        pass
    
    @abstractmethod
    def getOne(self, ref: Ref) -> DocRef:
        pass
    
    @abstractmethod
    def getMany(self, refs: List[Ref]) -> List[DocRef]:
        pass
    
    @abstractmethod
    def updateOne(self, ref: Ref, instance: BaseModel) -> DocRef:
        pass
    
    @abstractmethod
    def updateMany(self, refs: List[Ref], instance: BaseModel) -> List[DocRef]:
        pass
    
    @abstractmethod
    def deleteOne(self, ref: Ref) -> DocRef:
        pass
    
    @abstractmethod
    def deleteMany(self, refs: List[Ref]) -> List[DocRef]:
        pass
    
    @abstractmethod
    def bigQuery(self, query: Query) -> List[DocRef]:
        pass

    @abstractmethod
    def queryOne(self, query: Query) -> DocRef:
        pass
    
    @abstractmethod
    def queryCount(self, query: Query) -> int:
        pass
    
    @abstractmethod
    def collectionExists(self, collection: str) -> bool:
        pass
    
    @abstractmethod
    def createCollection(self, collection: str) -> Ref:
        pass
    
    @abstractmethod
    def createIndex(self, collection: str, index: str, terms:Optional[List[str]]=None) -> Ref:
        pass
    
    @abstractmethod
    def queryByIndex(self, collection: str, index: str, terms:Optional[List[str]]=None) -> List[DocRef]:
        pass
    
    
class FaunaTxn(FaunaORM):
    
    def __init__(self, client: FaunaClient):
        self.client = client

    def createOne(self, instance: BaseModel) -> DocRef:
        return self.client.query(q.create(instance))

    def createMany(self, instances: List[BaseModel]) -> List[DocRef]:
        return self.client.query(q.create(instances))

    def getOne(self, ref: Ref) -> DocRef:
        return self.client.query(q.get(ref))

    def getMany(self, refs: List[Ref]) -> List[DocRef]:
        return self.client.query(q.get(refs))

    def updateOne(self, ref: Ref, instance: BaseModel) -> DocRef:
        return self.client.query(q.update(ref, instance))

    def updateMany(self, refs: List[Ref], instance: BaseModel) -> List[DocRef]:
        return self.client.query(q.update(refs, instance))

    def deleteOne(self, ref: Ref) -> DocRef:
        return self.client.query(q.delete(ref))

    def deleteMany(self, refs: List[Ref]) -> List[DocRef]:
        return self.client.query(q.delete(refs))

    def bigQuery(self, query: Query) -> List[DocRef]:
        return self.client.query(query)

    def queryOne(self, query: Query) -> DocRef:
        return self.client.query(query)

    def queryCount(self, query: Query) -> int:
        return self.client.query(q.count(query))

    def collectionExists(self, collection: str) -> bool:
        return self.client.query(q.collection(collection))

    def createCollection(self, collection: str) -> Ref:
        return self.client.query(q.create_collection(collection))

    def createIndex(self, collection: str, index: str, terms:Optional[List[str]]=None) -> Ref:
        return self.client
    
    def queryByIndex(self, collection: str, index: str, terms:Optional[List[str]]=None) -> List[DocRef]:
        return self.client.query(q.query(q.index(collection, index, terms)))
    
    def commit(self) -> List[DocRef]:
        return self.client.query(q.commit())
    
    def rollback(self) -> List[DocRef]:
        return self.client.query(q.rollback())
    
    def transaction(self) -> List[DocRef]:
        return self.client.query(q.transaction())
    
class FQLModel(BaseModel):
    doc_ref:Optional[DocRef] = Field(None, alias='ref')
    ts:Optional[FaunaTime] = Field(None, alias='ts')
    data:Dict = Field(..., alias='data')
    class Config(BaseConfig):
        arbitrary_types_allowed = True
        json_encoders = {
            Ref: lambda ref: ref.to_dict(),
            FaunaTime: lambda time: time.to_dict(),
            Query: lambda query: query.to_dict(),
            _Expr: lambda expr: expr.to_dict(),
        }
        json_decoders = {
            Ref: lambda ref: Ref.from_dict(ref),
            FaunaTime: lambda time: FaunaTime.from_dict(time),
            Query: lambda query: Query.from_dict(query),
            _Expr: lambda expr: _Expr.from_dict(expr),
        }
        
def ormGetOne(contraint:Union(str, Ref, Query, _Expr)) -> DocRef:
    return client.query(q.get(contraint))

def ormGetMany(contraint:Union(str, Ref, Query, _Expr)) -> List[DocRef]:
    return client.query(q.get(contraint))

def ormCreateOne(instance:BaseModel) -> DocRef:
    return client.query(q.create(instance))

def ormCreateMany(instances:List[BaseModel]) -> List[DocRef]:
    return client.query(q.create(instances))

def ormUpdateOne(ref:Ref, instance:BaseModel) -> DocRef:
    return client.query(q.update(ref, instance))

def ormUpdateMany(refs:List[Ref], instance:BaseModel) -> List[DocRef]:
    return client.query(q.update(refs, instance))

def ormDeleteOne(ref:Ref) -> DocRef:
    return client.query(q.delete(ref))

def ormDeleteMany(refs:List[Ref]) -> List[DocRef]:
    return client.query(q.delete(refs))

def ormBigQuery(query:Query) -> List[DocRef]:
    return client.query(query)

def ormQueryOne(query:Query) -> DocRef:
    return client.query(query)

def ormQueryCount(query:Query) -> int:
    return client.query(q.count(query))

def ormCollectionExists(collection:str) -> bool:
    return client.query(q.collection(collection))

def ormCreateCollection(collection:str) -> Ref:
    return client.query(q.create_collection(collection))

def ormCreateIndex(collection:str, index:str, terms:Optional[List[str]]=None) -> Ref:
    return client.query(q.create_index(collection, index, terms))

def ormQueryByIndex(collection:str, index:str, terms:Optional[List[str]]=None) -> List[DocRef]:
    return client.query(q.query(q.index(collection, index, terms)))

def ormCommit() -> List[DocRef]:
    return client.query(q.commit())

def ormRollback() -> List[DocRef]:
    return client.query(q.rollback())

def ormTransaction() -> List[DocRef]:
    return client.query(q.transaction())

FQLRouter = type('FQLRouter', (FQLModel, APIRouter), {
    'getOne': ormGetOne,
    'getMany': ormGetMany,
    'createOne': ormCreateOne,
    'createMany': ormCreateMany,
    'updateOne': ormUpdateOne,
    'updateMany': ormUpdateMany,
    'deleteOne': ormDeleteOne,
    'deleteMany': ormDeleteMany,
    'bigQuery': ormBigQuery,
    'queryOne': ormQueryOne,
    'queryCount': ormQueryCount,
    'collectionExists': ormCollectionExists,
    'createCollection': ormCreateCollection,
    'createIndex': ormCreateIndex,
    'queryByIndex': ormQueryByIndex,
    'commit': ormCommit,
    'rollback': ormRollback,
    'transaction': ormTransaction,
})

class FQLCRUDRouter(FQLRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.getOne = ormGetOne
        self.getMany = ormGetMany
        self.createOne = ormCreateOne
        self.createMany = ormCreateMany
        self.updateOne = ormUpdateOne
        self.updateMany = ormUpdateMany
        self.deleteOne = ormDeleteOne
        self.deleteMany = ormDeleteMany
        self.bigQuery = ormBigQuery
        self.queryOne = ormQueryOne
        self.queryCount = ormQueryCount
        self.collectionExists = ormCollectionExists
        self.createCollection = ormCreateCollection
        self.createIndex = ormCreateIndex
        self.queryByIndex = ormQueryByIndex
        self.commit = ormCommit
        self.rollback = ormRollback
        self.transaction = ormTransaction
    
    @classmethod
    async def postOne(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        bbody = await request.body()
        if bbody and not isinstance(bbody, dict):
            raise HTTPException(status_code=400, detail='Invalid body')
        elif bbody:
            bbody = {k:v for k,v in bbody.items() if k in model.__fields__}
        else:
            bbody = {}
        instance = model(**bbody)
        ref = ormCreateOne(instance)
        return JSONResponse(status_code=201, content=ref.to_dict())
    
    @classmethod
    async def postMany(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        bbody = await request.body()
        if bbody and not isinstance(bbody, list):
            raise HTTPException(status_code=400, detail='Invalid body')
        elif bbody:
            bbody = [{k:v for k,v in b.items() if k in model.__fields__} for b in bbody]
        else:
            bbody = []
        instances = [model(**b) for b in bbody]
        refs = ormCreateMany(instances)
        return JSONResponse(status_code=201, content=[r.to_dict() for r in refs])
    
    @classmethod
    async def putOne(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        bbody = await request.body()
        if bbody and not isinstance(bbody, dict):
            raise HTTPException(status_code=400, detail='Invalid body')
        elif bbody:
            bbody = {k:v for k,v in bbody.items() if k in model.__fields__}
        else:
            bbody = {}
        instance = model(**bbody)
        ref = ormUpdateOne(request.path_params['ref'], instance)
        return JSONResponse(status_code=200, content=ref.to_dict())
    
    @classmethod
    async def putMany(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        bbody = await request.body()
        if bbody and not isinstance(bbody, list):
            raise HTTPException(status_code=400, detail='Invalid body')
        elif bbody:
            bbody = [{k:v for k,v in b.items() if k in model.__fields__} for b in bbody]
        else:
            bbody = []
        instances = [model(**b) for b in bbody]
        refs = ormUpdateMany(request.path_params['ref'], instances)
        return JSONResponse(status_code=200, content=[r.to_dict() for r in refs])
    
    @classmethod
    async def deleteOne(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        ormDeleteOne(request.path_params['ref'])
        return JSONResponse(status_code=200, content={})
    
    @classmethod
    async def deleteMany(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        ormDeleteMany(request.path_params['ref'])
        return JSONResponse(status_code=200, content={})
    
    @classmethod
    async def getOne(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        ref = ormGetOne(request.path_params['ref'])
        return JSONResponse(status_code=200, content=ref.to_dict())
    
    @classmethod
    async def getMany(cls, request:Request, model:BaseModel)->JSONResponse:
        qparams = [k for k in request.query_params if k not in model.__fields__]
        if qparams:
            raise HTTPException(status_code=400, detail=f'Invalid query parameters: {qparams}')
        pparams = [k for k in request.path_params if k not in model.__fields__]
        if pparams:
            raise HTTPException(status_code=400, detail=f'Invalid path parameters: {pparams}')
        refs = ormGetMany(request.path_params['ref'])
        return JSONResponse(status_code=200, content=[r.to_dict() for r in refs])
    
    
