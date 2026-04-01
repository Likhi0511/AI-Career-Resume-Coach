from fastapi import FastAPI
from app.routes.chat import router
from app.db.memory import create_table

app = FastAPI(title="Career Coach AI")

create_table()

app.include_router(router)
