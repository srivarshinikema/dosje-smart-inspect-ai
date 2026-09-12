# Setup Instructions

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Flutter 3.0+ (optional for mobile)
- Docker (optional)

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend
npm install
```

## Environment Variables

Create `.env` files in both backend and frontend directories.

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/dosje_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```
