# SETUP INSTRUCTIONS

## Prerequisites
- Python 3.12+
- Virtual environment (venv)
- Redis (optional, for memory persistence)

## Installation

1. Clone/Navigate to project:


2. Create and activate virtual environment:


3. Install dependencies:


4. Set environment variables:


## Running the Application

### Start Backend API:


### Start Frontend:


## Verify Installation

Test endpoints:


## Configuration

### AI Service
Edit  to customize:
- Location insights (NZ suburbs)
- Tone vocabulary banks
- Lead scoring weights

### Environment Variables
-  - For AI features (optional with fallbacks)
-  - For persistent memory (optional)

## Testing

Run tests:


## NEMO Protocol (Hourly Checks)


View logs:


## Current Status
- Backend: http://3.25.170.226:8000 (RUNNING)
- Frontend: http://3.25.170.226:3000 (RUNNING)
- All 5 agents operational
- Tests: 4/4 PASSING
