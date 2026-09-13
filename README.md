# 🚨 DoSJE SmartInspect AI

### Smart Real-Time Monitoring & Inspection Platform

> **Smart India Hackathon 2026 – SIH26095**
> **Problem Statement:** Smart Real-Time Monitoring & Inspection Mobile App
> **Ministry:** Ministry of Social Justice and Empowerment

A centralized AI-assisted monitoring and inspection platform designed to improve transparency, accountability, and real-time monitoring of projects, institutes, and NGOs operating under DoSJE schemes.

---

## 🏆 Problem Statement

Projects, institutes, and NGOs operating under government schemes require effective monitoring, surprise inspections, evidence collection, and compliance tracking.

Traditional inspection processes involve:
- Delayed reporting
- Manual verification
- Limited real-time visibility
- Difficulties in identifying anomalies

## 💡 Proposed Solution

**DoSJE SmartInspect AI** connects government officers, inspectors, and project representatives through a centralized digital platform with:

- ✅ Real-time project monitoring
- ✅ Random/risk-based inspection assignment
- ✅ GPS-verified inspections
- ✅ Evidence collection with metadata
- ✅ Attendance tracking
- ✅ AI-powered anomaly detection
- ✅ Risk scoring engine
- ✅ Compliance monitoring
- ✅ Automated PDF reports
- ✅ CCTV integration (demo)
- ✅ Alert system
- ✅ Role-based access control

---

## ✨ Key Features

### 1. 📊 Officer Dashboard
- Project overview and status
- Real-time risk indicators
- Inspection analytics
- Alert management
- Compliance tracking
- Geographic visualization
- Trend analysis charts

### 2. 🎲 Intelligent Inspection Assignment
- **Random Assignment:** Unbiased inspector selection
- **Risk-Based Assignment:** Prioritize high-risk projects
- **Geographic Consideration:** Inspector proximity
- **Workload Distribution:** Balance inspector workload
- **Transparent Explanation:** Why each inspection was assigned

### 3. 📱 Inspector Mobile Application
- Secure login
- Assigned inspection list
- GPS check-in/verification
- Attendance recording
- Photo/evidence capture
- Offline capability
- Automatic sync

### 4. 🤖 AI/ML Analysis
- **Anomaly Detection:** Isolation Forest algorithm
- **Risk Scoring:** Multi-factor risk engine
- **Pattern Recognition:** Identify unusual activities
- **Automated Insights:** Human review recommended
- **Non-accusatory:** "Anomaly Detected – Human Review Required"

### 5. 📋 Compliance & Reports
- Checklist management
- Status tracking
- Evidence linking
- Automated PDF generation
- Officer review workflow
- Audit trail

### 6. 🎥 CCTV & Video Integration
- Camera management
- Demo/simulated streams (clearly labeled)
- Stream preview
- Status monitoring

---

## 📋 Tech Stack

### Backend
- **Framework:** FastAPI 0.104.1
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 15+
- **Auth:** JWT with Passlib/Bcrypt
- **AI/ML:** Scikit-learn, Pandas, NumPy
- **Reports:** ReportLab
- **Testing:** Pytest

### Frontend
- **Framework:** React 18.2
- **Build Tool:** Vite 5.0
- **Language:** TypeScript 5.2
- **Styling:** Tailwind CSS 3.4
- **Charts:** Recharts
- **Maps:** React Leaflet
- **HTTP:** Axios

### Mobile
- **Framework:** Flutter 3.0+
- **Language:** Dart
- **Location:** Geolocator
- **Camera:** Image Picker
- **State:** Provider
- **Storage:** Shared Preferences

### Infrastructure
- **Containerization:** Docker
- **Orchestration:** Docker Compose

---

## 📁 Project Structure

```
dosje-smart-inspect-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── projects.py
│   │   │   │   ├── inspections.py
│   │   │   │   ├── assignments.py
│   │   │   │   ├── ai.py
│   │   │   │   ├── alerts.py
│   │   │   │   ├── attendance.py
│   │   │   │   ├── evidence.py
│   │   │   │   ├── compliance.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── cctv.py
│   │   │   │   └── dashboard.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── inspection.py
│   │   │   ├── attendance.py
│   │   │   ├── evidence.py
│   │   │   ├── alert.py
│   │   │   ├── compliance.py
│   │   │   ├── risk_score.py
│   │   │   ├── anomaly.py
│   │   │   ├── cctv_camera.py
│   │   │   └── audit_log.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   └── inspection.py
│   │   ├── services/
│   │   │   ├── project.py
│   │   │   ├── inspection.py
│   │   │   ├── assignment.py
│   │   │   └── report.py
│   │   ├── ai/
│   │   │   ├── anomaly.py
│   │   │   └── risk_engine.py
│   │   ├── main.py
│   │   └── seed.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── alembic/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── .env.example
│   ├── Dockerfile
│   └── nginx.conf
│
├── mobile/
│   └── flutter_app/
│       ├── lib/
│       │   ├── screens/
│       │   ├── widgets/
│       │   ├── services/
│       │   └── main.dart
│       └── pubspec.yaml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   └── API.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (Backend)
- **Node.js 18+** (Frontend)
- **npm 9+** (Frontend package manager)
- **PostgreSQL 15+** (Database)
- **Docker & Docker Compose** (Optional, for containerized setup)
- **Flutter 3.0+** (Mobile, optional)

### Option 1: Local Development Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/srivarshinikema/dosje-smart-inspect-ai.git
cd dosje-smart-inspect-ai
```

#### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and configure database URL
# Default: DATABASE_URL=postgresql://user:password@localhost:5432/dosje_db
```

#### Step 3: Database Setup

```bash
# Make sure PostgreSQL is running
# Create database
psql -U postgres -c "CREATE DATABASE dosje_db;"

# Create database user (optional, if not exists)
psql -U postgres -c "CREATE USER dosje_user WITH PASSWORD 'dosje_password';"
psql -U postgres -c "ALTER ROLE dosje_user CREATEDB;"

# Run seed script to populate demo data
python -m app.seed
```

#### Step 4: Start Backend

```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

#### Step 5: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env if needed
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

### Option 2: Docker Setup (Recommended)

```bash
# From project root
cd dosje-smart-inspect-ai

# Update .env.example with database credentials
cp .env.example .env

# Build and start containers
docker compose up --build

# Run seed script (in another terminal)
docker compose exec backend python -m app.seed
```

Services will be available at:
- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:80
- **PostgreSQL:** localhost:5432

---

## 📖 API Documentation

Once backend is running, access the interactive API documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Available API Routes

```
POST   /api/auth/login              - User login
POST   /api/auth/register           - User registration
GET    /api/users/me                - Current user profile

GET    /api/projects/               - List projects
POST   /api/projects/               - Create project
GET    /api/projects/{id}           - Get project
PUT    /api/projects/{id}           - Update project
DELETE /api/projects/{id}           - Delete project
GET    /api/projects/search/{term}  - Search projects
GET    /api/projects/high-risk/list - High-risk projects

GET    /api/inspections/            - List inspections
POST   /api/inspections/            - Create inspection
GET    /api/inspections/{id}        - Get inspection
PUT    /api/inspections/{id}        - Update inspection
GET    /api/inspections/pending/list - Pending inspections

POST   /api/assignments/random      - Random assignment
POST   /api/assignments/risk-based  - Risk-based assignment

POST   /api/ai/analyze/{id}         - Analyze project (AI)
GET    /api/ai/risk/{id}            - Get risk score
GET    /api/ai/anomalies/{id}       - Get anomalies

GET    /api/alerts/                 - List alerts
GET    /api/alerts/{id}             - Get alert
POST   /api/alerts/{id}/acknowledge - Mark as read

POST   /api/attendance/             - Record attendance
GET    /api/attendance/inspection/{id} - Inspection attendance
GET    /api/attendance/project/{id} - Project attendance

POST   /api/evidence/               - Upload evidence
GET    /api/evidence/inspection/{id} - Inspection evidence
GET    /api/evidence/project/{id}   - Project evidence

POST   /api/compliance/             - Create compliance record
GET    /api/compliance/project/{id} - Project compliance
PUT    /api/compliance/{id}         - Update compliance

GET    /api/reports/{id}/data       - Report JSON
GET    /api/reports/{id}/pdf        - Report PDF

GET    /api/cctv/                   - List cameras
POST   /api/cctv/                   - Create camera
GET    /api/cctv/project/{id}       - Project cameras

GET    /api/dashboard/summary       - Dashboard summary
GET    /api/dashboard/project-overview - Project overview
GET    /api/dashboard/inspection-trends - Inspection trends
GET    /api/dashboard/risk-distribution - Risk distribution
```

---

## 👥 Demo Login Credentials

⚠️ **IMPORTANT:** These credentials are for development and demo purposes only. They are synthetic and not connected to any real government systems.

| Role | Email | Password | Access Level |
|------|-------|----------|---------------|
| **Admin** | `admin@demo.com` | `admin123` | Full system access, user management |
| **Government Officer** | `officer@demo.com` | `officer123` | Dashboard, assignment, reports, compliance |
| **Inspector 1** | `inspector1@demo.com` | `inspector123` | Inspections, attendance, evidence upload |
| **Inspector 2** | `inspector2@demo.com` | `inspector123` | Inspections, attendance, evidence upload |
| **Project Rep** | `representative@demo.com` | `project123` | Read-only project access |

### How to Login

1. Visit frontend: http://localhost:5173
2. Use credentials from table above
3. Select user role if prompted
4. Access role-specific dashboard

---

## 🌱 Database Seeding

The seed script populates the database with realistic synthetic demo data:

```bash
# From backend directory (with .venv activated)
python -m app.seed
```

### What Gets Seeded

✅ **5 Demo Users** with different roles
✅ **10 Demo Projects** across different locations
✅ **30 Demo Inspections** with various statuses
✅ **Attendance Records** for each inspection
✅ **Alerts** (high-risk, anomalies, compliance issues)
✅ **Risk Scores** for each project
✅ **Anomaly Detection Results** from AI analysis
✅ **CCTV Cameras** (simulated, clearly marked as demo)
✅ **Compliance Records** with various statuses

**Note:** All data is SYNTHETIC and for DEMO purposes only. No real personal information or actual government data is included.

---

## 🔐 Security Notes

### ⚠️ Demo Mode Only

- **Demo credentials** are hardcoded in this repository for testing purposes
- **SECRET_KEY** in `.env.example` is not secure and must be changed in production
- **CORS is open** (`allow_origins=["*"]`) for development only
- **JWT tokens** have short expiry for demo purposes
- **Password hashing** uses Bcrypt (secure, production-ready)

### Production Deployment

Before deploying to production:

1. ✅ Change `SECRET_KEY` in `.env` to a strong random value
2. ✅ Remove demo users and credentials
3. ✅ Configure restrictive CORS origins
4. ✅ Use HTTPS/TLS certificates
5. ✅ Enable rate limiting
6. ✅ Configure proper logging and monitoring
7. ✅ Use environment-specific `.env` files
8. ✅ Never commit secrets to version control
9. ✅ Implement proper authentication (Okta, Azure AD, etc.)
10. ✅ Enable database encryption at rest

---

## 🔧 Environment Variables

### Backend Configuration

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://dosje_user:dosje_password@localhost:5432/dosje_db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### Frontend Configuration

Create `frontend/.env`:

```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=DoSJE SmartInspect AI
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

### Frontend Tests

```bash
cd frontend

# Run tests (when configured)
npm test
```

---

## 🐛 Troubleshooting

### Backend Issues

**Error: "Database connection refused"**
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env`
- Check database credentials

```bash
psql -U postgres -c "SELECT version();"
```

**Error: "ModuleNotFoundError: No module named 'app'"**
- Ensure you're in `backend/` directory
- Verify virtual environment is activated
- Run `pip install -r requirements.txt`

**Error: "Port 8000 already in use"**
```bash
# Use different port
uvicorn app.main:app --port 8001

# Or kill process using port 8000
# Linux/Mac: lsof -ti :8000 | xargs kill -9
# Windows: netstat -ano | findstr :8000
```

### Frontend Issues

**Error: "npm ERR! 404 Not Found"**
- Clear npm cache
- Delete `node_modules/` and reinstall

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Error: "CORS error in console"**
- Backend CORS must be configured
- Check `ALLOWED_ORIGINS` in backend `.env`
- Ensure frontend URL matches CORS configuration

**Port 5173 in use**
```bash
npm run dev -- --port 5174
```

### Database Issues

**Error: "Database already exists"**
- Drop existing database: `psql -U postgres -c "DROP DATABASE dosje_db;"`
- Or use a different database name in `.env`

**Seed script fails**
- Ensure database exists and is accessible
- Check that virtual environment is activated
- Verify all models are properly imported

---

## 📊 AI/ML Explanation

### Anomaly Detection

**Algorithm:** Isolation Forest
**Inputs:**
- Inspection frequency
- Attendance percentage
- Evidence collection count
- Days since last inspection
- Evidence per inspection ratio

**Output:**
- Anomaly score (0-1)
- Risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Reasons for anomaly
- Recommendation (Human Review Required)

**Important:** AI never makes accusations. Results say "Anomaly Detected – Human Review Required" to ensure officer makes the final determination.

### Risk Scoring

**Factors (Equal 20% weight each):**
1. Attendance Risk
2. Compliance Risk
3. Inspection History Risk
4. Evidence Risk
5. Operational Risk

**Risk Levels:**
- **CRITICAL:** Score ≥ 80 → Immediate investigation
- **HIGH:** Score 60-79 → Urgent review
- **MEDIUM:** Score 40-59 → Standard inspection
- **LOW:** Score < 40 → Routine monitoring

**Transparency:** Each factor is calculated, explained, and can be reviewed by officers.

---

## 📄 License

MIT License - Copyright (c) 2026 Sri Varshini Kema

See [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Development:** Sri Varshini Kema, Bhanu prakesh Ramisetti.

**Testing:** Tharun Sai Kumar Ravilala, Neelima Korakappulla .

**Deploying:** Shaik Aarif, Adapa Hemanth.

**Project:** DoSJE SmartInspect AI - SIH26095

**Ministry:** Ministry of Social Justice and Empowerment

**Challenge:** Smart Real-Time Monitoring & Inspection Mobile App

---

## 📞 Support & Documentation

- **API Docs:** http://localhost:8000/docs
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Setup Guide:** [docs/SETUP.md](docs/SETUP.md)
- **GitHub:** https://github.com/srivarshinikema/dosje-smart-inspect-ai

---

## 📝 Notes

- This is a **prototype for demonstration purposes**
- All data shown is **SYNTHETIC and FOR DEMO ONLY**
- The CCTV streams are **simulated** and clearly marked as demo
- No real government data or systems are accessed
- Perfect for hackathon demonstrations and proof-of-concept validations

---

**Made with ❤️ for Smart India Hackathon 2026**
