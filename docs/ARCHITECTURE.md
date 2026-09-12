# System Architecture

## Overview

DoSJE SmartInspect AI is built using a modern, scalable architecture with clear separation of concerns.

## Components

### Backend (FastAPI)
- RESTful API
- Database ORM (SQLAlchemy)
- Authentication (JWT)
- Role-based access control
- AI/ML services

### Frontend (React + Vite)
- Responsive dashboard
- Real-time data visualization
- Interactive maps
- Authentication UI

### Mobile (Flutter)
- Cross-platform inspector app
- GPS integration
- Camera for evidence
- Offline capability

### Database (PostgreSQL)
- Relational data model
- Migrations via Alembic
- Audit logging

## Data Flow

```
Inspector Mobile App
        ↓
  FastAPI Backend
        ↓
  PostgreSQL Database
        ↓
  Officer Dashboard
```
