import uvicorn

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.conf import settings

from app.routers import item

app = FastAPI(title="FastAPI App Template")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["x-total-count"]
)

app.include_router(item.router)


# app.include_router(bookie.router)
# app.include_router(bet.router)
# app.include_router(selections.router)


@app.get("/healthcheck")
async def health_check():
    """
    Healthcheck. Returns status HTTP 200
    """
    return {"status": status.HTTP_200_OK}


if __name__ == "__main__" and settings.ENVIRONMENT == "local":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
