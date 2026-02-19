# Udacity Trivia API

Full-stack trivia game application with a Flask REST API backend and React frontend.

## Project Structure

```
backend/           # Flask REST API
  flaskr/__init__.py  # App factory + all API endpoints
  models.py           # SQLAlchemy models (Question, Category)
  test_flaskr.py      # Unit tests (unittest)
  trivia.psql         # PostgreSQL schema + seed data
  requirements.txt    # Python dependencies
  .env                # Environment variables (POSTGRES_PWD)

frontend/          # React.js frontend
  src/components/     # React components (QuestionView, FormView, QuizView, etc.)
  package.json        # Node.js dependencies
```

## Tech Stack

- **Backend**: Python 3.10+, Flask, SQLAlchemy, PostgreSQL
- **Frontend**: React 16, Node 16x
- **Database**: PostgreSQL on localhost:5432 (`trivia` / `trivia_test`)

## Setup

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
createdb trivia
psql trivia < trivia.psql
flask run --reload    # http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm start             # http://localhost:3000
```

## Testing
```bash
createdb trivia_test
psql trivia_test < backend/trivia.psql
cd backend && python test_flaskr.py
```

## API Endpoints

- `GET /categories` — List all categories
- `GET /questions?page=<int>` — Paginated questions (10/page)
- `DELETE /questions/<id>` — Delete a question
- `POST /questions` — Create question or search (if `searchTerm` in body)
- `GET /categories/<id>/questions` — Questions by category
- `POST /quizzes` — Get next quiz question

## Git

- Remote: `https://github.com/Austin6s/Udacity-Trivia-API.git`
- Main branch: `main`
