# Agentic Boilerplate

A full-stack application with FastAPI backend and React frontend.

## Project Structure

```
agentic-boilerplate/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application file with test routes
│   └── __init__.py      # Package initialization
├── frontend/            # React frontend
│   ├── src/            # Source files
│   │   ├── App.jsx     # Main App component
│   │   ├── App.css     # App styles
│   │   ├── main.jsx    # Entry point
│   │   └── index.css   # Global styles
│   ├── index.html      # HTML template
│   ├── package.json    # Node dependencies
│   └── vite.config.js  # Vite configuration
├── Pipfile             # Python dependencies
├── start.sh            # Script to launch both servers
└── env.example         # Environment variables template
```

## Prerequisites

- Python 3.x
- Node.js (v16 or higher)
- pipenv (`pip install pipenv`)

## Getting Started

### Option 1: Quick Start (Recommended)

Run both servers with a single command:

```bash
./start.sh
```

This will:
- Install Python dependencies (first run only)
- Install npm dependencies (first run only)
- Start the FastAPI backend on http://localhost:8000
- Start the React frontend on http://localhost:3000

Press `Ctrl+C` to stop both servers.

### Option 2: Manual Start

#### Backend

```bash
# Install dependencies
pipenv install

# Run the server
cd backend
pipenv run python main.py
```

Backend will be available at http://localhost:8000

API Routes:
- `GET /` - Root endpoint
- `GET /api/test` - Test endpoint

#### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Run the dev server
npm run dev
```

Frontend will be available at http://localhost:3000

## Environment Variables

Copy `env.example` to `.env` and configure as needed:

```bash
cp env.example .env
```

Available variables:
- `BACKEND_PORT` - Backend server port (default: 8000)
- `FRONTEND_PORT` - Frontend server port (default: 3000)
- `API_BASE_URL` - Backend API URL (default: http://localhost:8000)
- `NODE_ENV` - Environment mode (development/production)

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Backend
The FastAPI backend includes:
- CORS middleware configured for the React frontend
- Example test route at `/api/test`
- Environment variable support via python-dotenv

### Frontend
The React frontend uses:
- Vite for fast development and building
- Proxy configuration for API calls
- Modern React with hooks

## Building for Production

### Backend
```bash
cd backend
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
npm run preview
```

## License

MIT

