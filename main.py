from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import reports, dashboard

app = FastAPI(title="CleanCity-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows frontend index.html to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
