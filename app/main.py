from operator import imod
from fastapi import Depends, FastAPI, status, HTTPException, Request, APIRouter as global_router
from app.api.routes.routes import router as global_router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api.routes import users_routes
from app.api.routes import visitor_routes
import starlette.responses as _responses
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.session import engine, Base
from app import models, database


database.session.Base.metadata.create_all(bind=engine)

app= FastAPI()
origin= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )



app.include_router(global_router, prefix= "/cardportal")

@app.get('/')
async def root():
    return _responses.RedirectResponse("/docs")

