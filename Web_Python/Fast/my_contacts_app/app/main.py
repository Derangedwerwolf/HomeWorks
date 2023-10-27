import logging
from fastapi import FastAPI
from api.routers import contacts, upcoming_birthdays
from core.config import settings

print(settings.DEBUG)
logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Contacts App",
    version="1.0",
    debug=settings.DEBUG,  # Set debug mode based on config
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

app.include_router(contacts.router, prefix=settings.API_PREFIX)
app.include_router(upcoming_birthdays.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
