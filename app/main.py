from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth
from app.routers import candidates
from app.routers import auth, candidates, interviews
from app.routers import feedback
from app.routers import reports
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Interview Scheduling & Candidate Tracking System"
)

app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(interviews.router)
app.include_router(feedback.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Interview Scheduling & Candidate Tracking System API"}