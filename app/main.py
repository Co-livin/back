from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import spaces
from app.routers import tasks
from app.routers import events

app = FastAPI(title="coli API", version="0.1.0", root_path="/api", docs_url="/docs")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(spaces.router, prefix="/spaces", tags=["spaces"])
app.include_router(tasks.router, tags=["tasks"])
app.include_router(events.router, tags=["events"])
