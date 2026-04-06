from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.auth.user import auth_router
from app.db.base import Base
from app.db.session import engine, get_db
from app.Routes.dashboard_routes import router as dashboard_router
from app.Routes.roles_route import router as roles_router
from app.Routes.transactions_routes import router as transactions_router
from app.Routes.users_route import router as users_router
from app.Services.user_service import seed_roles

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db = next(get_db())
    seed_roles(db)
    yield
    # Shutdown


app = FastAPI(title="Finance Dashboard Backend", lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
