import logging

# from app.services.auth_manager import AuthManager
from fastapi import FastAPI
from api.routers import contacts, auth, upcoming_birthdays
from core.config import settings
from database.models import Base
from database.db import engine

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

# auth_service = AuthManager()

app.include_router(contacts.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(upcoming_birthdays.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
