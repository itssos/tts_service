
from app.api.v1.routers.tts_router import router as tts_router
from app.core.consts import db
from app.domain.models import RivaTask, Voice

from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    db.connect(reuse_if_open=True)
    db.create_tables([RivaTask, Voice])
    yield
    # Cleanup
    if not db.is_closed():
        db.close()

app = FastAPI(title="Text To Speech with Riva", lifespan=lifespan)
app.include_router(tts_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=9090, reload=True, log_level="debug")