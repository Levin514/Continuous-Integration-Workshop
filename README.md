# Continuous Integration
# Gym Membership Management System

Backend API for managing gym membership plans, features, and cost calculations with FastAPI.

## Features

- **Membership Plans**: Basic ($50), Premium ($100), Family ($150)
- **Additional Features**: Personal Training, Group Classes, Exclusive Facilities
- **Smart Pricing**: Group discounts, premium surcharges, and amount-based discounts
- **Input Validation**: Descriptive error messages for all invalid inputs
- **CI/CD**: Automated linting (Pylint) and testing (Pytest) via GitHub Actions

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

API docs available at: `http://localhost:8000/docs`

## Run Tests

```bash
pytest tests/ -v
```

With JUnit XML report:
```bash
pytest tests/ --junitxml=test-results.xml -v
```

## Run Linter

```bash
pylint src/ tests/ main.py --fail-under=8.0
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/plans` | List all plans |
| GET | `/plans/{name}` | Get plan details |
| GET | `/features` | List all features |
| GET | `/features/{name}` | Get feature details |
| POST | `/calculate` | Calculate total cost |
| POST | `/preview` | Preview cost summary |

## Business Rules

1. **Total** = base_cost + features_cost
2. **Group discount** → 10% off for 2+ members on same plan
3. **Premium surcharge** → 15% if any premium feature selected
4. **Amount discount** → $20 off if total > $200, $50 off if total > $400
5. **Order**: base + features → group discount → premium surcharge → amount discount
