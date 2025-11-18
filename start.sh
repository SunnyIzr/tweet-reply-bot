#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Agentic Boilerplate...${NC}"

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill 0
    exit
}

trap cleanup SIGINT SIGTERM

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Using defaults...${NC}"
fi

# Start backend
echo -e "${GREEN}Starting FastAPI backend...${NC}"
cd backend
if [ ! -d "../.venv" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    cd ..
    pipenv install
    cd backend
fi
cd ..
pipenv run python backend/main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
echo -e "${GREEN}Starting React frontend...${NC}"
cd frontend

# Install npm dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing npm dependencies...${NC}"
    npm install
fi

npm run dev &
FRONTEND_PID=$!

echo -e "\n${GREEN}Both servers are running!${NC}"
echo -e "${BLUE}Backend:${NC} http://localhost:8000"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

