"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import (
    auth,
    users,
    projects,
    inspections,
    assignments,
    ai,
    alerts,
    attendance,
    evidence,
    compliance,
    reports,
    cctv,
    dashboard,
)

app = FastAPI(
    title="DoSJE SmartInspect AI",
    description="Smart Real-Time Monitoring & Inspection Platform - SIH26095",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes and tags
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"],
)
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"],
)
app.include_router(
    projects.router,
    prefix="/api/projects",
    tags=["Projects"],
)
app.include_router(
    inspections.router,
    prefix="/api/inspections",
    tags=["Inspections"],
)
app.include_router(
    assignments.router,
    prefix="/api/assignments",
    tags=["Assignments"],
)
app.include_router(
    ai.router,
    prefix="/api/ai",
    tags=["AI/ML Analysis"],
)
app.include_router(
    alerts.router,
    prefix="/api/alerts",
    tags=["Alerts"],
)
app.include_router(
    attendance.router,
    prefix="/api/attendance",
    tags=["Attendance"],
)
app.include_router(
    evidence.router,
    prefix="/api/evidence",
    tags=["Evidence"],
)
app.include_router(
    compliance.router,
    prefix="/api/compliance",
    tags=["Compliance"],
)
app.include_router(
    reports.router,
    prefix="/api/reports",
    tags=["Reports"],
)
app.include_router(
    cctv.router,
    prefix="/api/cctv",
    tags=["CCTV"],
)
app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "message": "DoSJE SmartInspect AI Backend Running",
        "version": "1.0.0",
        "docs_url": "/docs",
        "problem_statement": "SIH26095 - Smart Real-Time Monitoring & Inspection Mobile App",
        "ministry": "Ministry of Social Justice and Empowerment",
    }


@app.get("/health")
def health_check():
    """Health status endpoint."""
    return {"status": "ok", "service": "DoSJE SmartInspect AI"}
