# MuveFit — AI-Assisted Fitness Trainer

MuveFit is a camera-based movement analysis and body-awareness application that uses AI to help users understand exercise form, movement quality, and consistency.

## Architecture

```
React/Vite Frontend (port 3000)
        ↓
FastAPI Backend (port 8000)
        ↓
Exercise Engine + Form Analysis + Scoring
        ↓
SQLite (dev) / PostgreSQL (production)
```

## Features

- **Real-time pose detection** using MediaPipe
- **5 exercises**: Squat, Plank, Burpee, Squat Hold, Glute Bridge
- **Form analysis** with specific biomechanical rules per exercise
- **Scoring** with explainable component scores
- **Feedback** with prioritized corrective messages
- **Workout reports** with detailed breakdowns
- **History & progress** tracking
- **AI Coach** chatbot for performance questions

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Clone the repository

```bash
git clone <repository-url>
cd MuveFit--AI-Assist-Trainer
```

### 2. Backend setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Copy environment file
cp .env.example .env

# Run development server
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### 3. Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | MuveFit API |
| `APP_VERSION` | Application version | 0.1.0 |
| `ENVIRONMENT` | Environment (development/production) | development |
| `DEBUG` | Enable debug mode | true |
| `PORT` | Server port | 8000 |
| `DATABASE_URL` | Database connection URL | sqlite:///./backend/muvefit.db |
| `DATABASE_ECHO` | Enable SQL logging | false |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed origins | http://localhost:3000,... |
| `JWT_SECRET_KEY` | Secret key for tokens | dev-secret-change-in-production |
| `JWT_EXPIRATION_MINUTES` | Token expiration | 60 |
| `OPENAI_API_KEY` | OpenAI API key (optional) | |

### Frontend (frontend/.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | http://localhost:8000 |

## Production Deployment

### 1. Environment Setup

```bash
# Set production environment
export ENVIRONMENT=production
export DEBUG=false
export DATABASE_URL=postgresql://user:password@localhost:5432/muvefit
export CORS_ALLOWED_ORIGINS=https://yourdomain.com
export JWT_SECRET_KEY=<your-secure-random-key>
```

### 2. Database

For PostgreSQL:

```bash
# Install PostgreSQL driver
pip install psycopg2-binary

# Create database
createdb muvefit

# Set DATABASE_URL
export DATABASE_URL=postgresql://user:password@localhost:5432/muvefit
```

### 3. Build Frontend

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### 4. Run Production Server

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Or with gunicorn:

```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

## API Endpoints

### Health
- `GET /api/health` — Health check
- `GET /api/health/ready` — Readiness check

### Authentication
- `POST /api/auth/register` — Register user
- `POST /api/auth/login` — Login
- `GET /api/auth/me` — Get current user
- `POST /api/auth/logout` — Logout

### Exercises
- `GET /api/exercises/` — List exercises

### Workouts
- `POST /api/workouts/` — Start workout
- `GET /api/workouts/{id}` — Get workout
- `POST /api/workouts/{id}/complete` — Complete workout
- `POST /api/workouts/{id}/exercises` — Add exercise
- `POST /api/workouts/{id}/exercises/{eid}/start` — Start exercise
- `POST /api/workouts/{id}/exercises/{eid}/process` — Process frame
- `POST /api/workouts/{id}/exercises/{eid}/complete` — Complete exercise

### Reports & History
- `GET /api/reports/{id}` — Get report
- `GET /api/history` — Workout history
- `GET /api/progress` — Progress data

### AI Coach
- `POST /api/chatbot/chat` — Chat with AI coach

## Testing

### Backend Tests

```bash
python -m pytest backend/tests/ -v
```

### Frontend Build

```bash
cd frontend
npm run build
```

## Project Structure

```
MuveFit--AI-Assist-Trainer/
├── backend/
│   ├── api/              # FastAPI routers
│   ├── analysis/         # Form analysis engines
│   ├── database/         # Database setup
│   ├── exercises/        # Exercise analyzers
│   ├── feedback/         # Feedback engine
│   ├── models/           # SQLAlchemy models
│   ├── reports/          # Report services
│   ├── schemas/          # Pydantic schemas
│   ├── scoring/          # Scoring engine
│   ├── services/         # Business logic
│   ├── tests/            # Test suite
│   ├── config.py         # Settings
│   └── main.py           # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── api.js        # API client
│   │   ├── hooks.js      # React hooks
│   │   ├── App.jsx       # Main app
│   │   └── ...
│   └── ...
├── docs/                 # Documentation
├── exercises/            # Original exercise scripts
├── models/               # MediaPipe models
├── .env.example          # Environment template
└── README.md             # This file
```

## License

Private — All rights reserved.
