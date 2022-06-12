from fastapi import FastAPI
from .auth import login

def main():
    app = FastAPI()
    app.include_router(login)
    return app