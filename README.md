# Trivia API

A full-stack trivia game application where users can view, add, delete, and search trivia questions, as well as play a quiz game. Built with a Flask REST API backend and React frontend.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL
- Node.js 16x

### Backend Setup

1. **Set up a virtual environment** from the `/backend` directory:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up the database** with Postgres running:

```bash
createdb trivia
psql trivia < trivia.psql
```

4. **Configure environment variables** by creating a `.env` file in the `/backend` directory:

```
POSTGRES_PWD=your_postgres_password
```

5. **Start the server:**

```bash
flask run --reload
```

The backend runs on http://localhost:5000.

### Frontend Setup

1. **Install dependencies** from the `/frontend` directory:

```bash
cd frontend
npm install
```

2. **Start the development server:**

```bash
npm start
```

The frontend runs on http://localhost:3000.

### Running Tests

Set up a test database and run the test suite:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
cd backend
python test_flaskr.py
```

## API Reference

### Endpoints

#### `GET /categories`

Fetches a dictionary of all available categories.

- **Request Arguments:** None
- **Response Body:**

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

#### `GET /questions?page=<int>`

Fetches a paginated list of questions (10 per page).

- **Request Arguments:**
  - `page` (int, optional) — Page number, defaults to 1.
- **Response Body:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the chemical symbol for water?",
      "answer": "H2O",
      "category": "1",
      "difficulty": 1
    }
  ],
  "total_questions": 19,
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "current_category": null
}
```

- **Errors:** Returns 404 if the requested page has no questions.

---

#### `DELETE /questions/<int:question_id>`

Deletes the question with the given ID.

- **Request Arguments:**
  - `question_id` (int) — ID of the question to delete.
- **Response Body:**

```json
{
  "success": true,
  "deleted": 1
}
```

- **Errors:** Returns 404 if the question does not exist. Returns 422 if the deletion fails.

---

#### `POST /questions` (Create)

Creates a new trivia question.

- **Request Body:**

```json
{
  "question": "What is 2 + 2?",
  "answer": "4",
  "difficulty": 1,
  "category": "1"
}
```

- **Response Body:**

```json
{
  "success": true,
  "created": 24
}
```

- **Errors:** Returns 400 if any required field is missing. Returns 422 if the insertion fails.

---

#### `POST /questions` (Search)

Searches for questions containing the given search term (case-insensitive).

- **Request Body:**

```json
{
  "searchTerm": "water"
}
```

- **Response Body:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the chemical symbol for water?",
      "answer": "H2O",
      "category": "1",
      "difficulty": 1
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

---

#### `GET /categories/<int:category_id>/questions`

Fetches all questions for a specific category.

- **Request Arguments:**
  - `category_id` (int) — ID of the category.
- **Response Body:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the chemical symbol for water?",
      "answer": "H2O",
      "category": "1",
      "difficulty": 1
    }
  ],
  "total_questions": 3,
  "current_category": 1
}
```

- **Errors:** Returns 404 if no questions exist in the given category.

---

#### `POST /quizzes`

Returns a random question for the quiz game, excluding previously asked questions.

- **Request Body:**

```json
{
  "previous_questions": [1, 2],
  "quiz_category": {
    "type": "Science",
    "id": 1
  }
}
```

Use `"id": 0` for all categories.

- **Response Body:**

```json
{
  "success": true,
  "question": {
    "id": 3,
    "question": "What is the chemical symbol for gold?",
    "answer": "Au",
    "category": "1",
    "difficulty": 2
  }
}
```

Returns `"question": null` when all questions have been exhausted.

- **Errors:** Returns 400 if `quiz_category` is missing from the request.

---

### Error Responses

All errors return JSON in the following format:

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

| Code | Message |
|------|---------|
| 400  | bad request |
| 404  | resource not found |
| 422  | unprocessable |
| 500  | internal server error |
