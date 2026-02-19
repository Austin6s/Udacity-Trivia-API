# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Reference

### Endpoints

#### `GET /categories`

Fetches all available trivia categories.

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

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
