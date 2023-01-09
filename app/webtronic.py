from fastapi import FastAPI
from .core.models import models
from .core.models.database import engine
from .handlers import posts, users, login

app = FastAPI(title="Webtronic API")
app.include_router(users.router)
app.include_router(login.router)
app.include_router(posts.router)

models.Base.metadata.create_all(bind=engine)
