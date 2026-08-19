from fastapi import FastAPI
from ROUTES import router

app = FastAPI()
app.include_router(router=router)
