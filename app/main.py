import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers.image_router import router as image_router
from app.routers.auth_router import router as auth_router

load_dotenv()

app = FastAPI(title="Shopify Developer Challenge")
app.include_router(image_router)
app.include_router(auth_router)


@app.get("/", tags=["Index"])
async def root():
    return {"Status": "OK"}
