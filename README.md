\# Movie Rating System

\## Overview

This project is a back-end system for managing movies, directors, genres, and user ratings, developed as part of the Software Engineering course at AUT. It consists of two phases:

\- \*\*Phase 1 (Back-End)\*\*: Implements a RESTful API using FastAPI for CRUD operations on movies, handling relationships (one-to-many, many-to-many), and database interactions with PostgreSQL and SQLAlchemy. The system supports pagination, filtering, and average rating calculation.

\- \*\*Phase 2 (Logging - Optional)\*\*: Adds structured logging for observability, including request/response logging, error handling, and decorator-based function logging for latency and errors. This phase is for extra credit and focuses on concepts like latency, throughput, error rate, saturation, and capacity.

The project is built by a team of two: Reza and Melika, using Git for collaboration with branches and pull requests.

\## Features

\- Manage movies, directors, genres, and ratings.

\- Relationships: Movies belong to one director, have multiple genres (many-to-many), and multiple ratings (one-to-many).

\- APIs for listing movies with pagination and filters (title, year, genre), getting details, creating, updating, deleting movies, and adding ratings.

\- Average rating calculation integrated into movie responses.

\- Structured JSON logging for requests, errors, and function calls (Phase 2).

\- Database seeding from TMDB CSV files.

\- Error handling with custom exceptions (404 Not Found, 422 Validation).

\## Technologies

\- \*\*Language\*\*: Python 3.12+

\- \*\*Framework\*\*: FastAPI

\- \*\*ORM\*\*: SQLAlchemy

\- \*\*Database\*\*: PostgreSQL

\- \*\*Dependency Management\*\*: Poetry

\- \*\*Version Control\*\*: Git and GitHub

\- \*\*Logging\*\*: Python's logging module with python-json-logger for structured JSON (Phase 2)

\- \*\*Other\*\*: Pydantic for schemas/validation, Alembic for migrations, pandas for seeding

\## Setup and Installation

1\. \*\*Clone the Repository\*\*:

\`\`\`

git clone https://github.com/rezahashemics/movie-rating-system.git

cd movie-rating-system

\`\`\`

2\. \*\*Install Dependencies\*\*:

\`\`\`

poetry install

\`\`\`

3\. \*\*Set Up Environment Variables\*\*:

Create \`.env\` file in root:

\`\`\`

DATABASE\_URL=postgresql://postgres:password@localhost:5432/movie\_db

\`\`\`

(Adjust credentials as needed)

4\. \*\*Set Up PostgreSQL Database\*\*:

\- Start PostgreSQL service (e.g., \`sudo service postgresql start\` on Linux).

\- Create database:

\`\`\`

psql -U postgres -c "CREATE DATABASE movie\_db;"

\`\`\`

5\. \*\*Run Migrations\*\*:

\`\`\`

alembic upgrade head

\`\`\`

6\. \*\*Seed the Database\*\*:

\- Download TMDB CSVs if not present (from Kaggle or manually).

\- Run:

\`\`\`

poetry run python scripts/seed.py

poetry run python scripts/seed\_check.py # Verify movies count > 0

\`\`\`

\## Running the App

\- Start the server:

\`\`\`

poetry run uvicorn app.main:app --reload

\`\`\`

\- Access Swagger UI for API docs/testing: http://127.0.0.1:8000/docs

\- Test endpoints with Postman or curl (see API Endpoints below).

\## API Endpoints

All endpoints are under \`/api/v1\`. Responses follow {"status": "success/failure", "data/error": {...}} format.

| Method | Endpoint | Description | Params/Body | Example Response Status |

|--------|----------|-------------|-------------|-------------------------|

| GET | /movies | List movies with pagination/filtering | Query: page (int), page\_size (int), title (str), release\_year (int), genre (str) | 200 OK |

| GET | /movies/{movie\_id} | Get movie details with average rating | Path: movie\_id (int) | 200 OK / 404 Not Found |

| POST | /movies | Create movie | Body: {"title": "str", "director\_id": int, "release\_year": int, "cast": "str", "genres": \[int\]} | 201 Created / 422 Invalid |

| PUT | /movies/{movie\_id} | Update movie (partial) | Path: movie\_id (int), Body: optional fields | 200 OK / 404 / 422 |

| DELETE | /movies/{movie\_id} | Delete movie | Path: movie\_id (int) | 204 No Content / 404 |

| POST | /movies/{movie\_id}/ratings | Add rating | Path: movie\_id (int), Body: {"score": 1-10} | 201 Created / 404 / 422 |

\## Logging (Phase 2)

\- Structured JSON logs for requests (method, path, params, headers), responses (status), and errors.

\- Decorator for service methods to log entry/exit, duration, args, results/errors.

\- Logs output to console (stdout); can be redirected to files or tools like ELK in production.

Example Log:

\`\`\`json

{"asctime": "2025-12-20 19:02:32,899", "name": "movie\_rating", "levelname": "INFO", "message": "Request completed: status\_code=200", "funcName": "dispatch", "route": "/api/v1/movies"}

\`\`\`

\## Testing with Postman

Import the provided Postman collection examples (from earlier messages) for 8 test cases covering CRUD, filtering, and errors. Run after seeding DB.

\## Project Structure

\`\`\`

movie-rating-system/

├── alembic/ # Migrations

├── app/ # Main app code

│ ├── controllers/ # API routes

│ ├── db/ # Database config

│ ├── exceptions/ # Custom errors

│ ├── logging/ # Logging config and decorators

│ ├── middlewares/ # Request logging middleware

│ ├── models/ # SQLAlchemy models

│ ├── repositories/ # Data access layer

│ ├── schemas/ # Pydantic schemas

│ ├── services/ # Business logic

│ └── main.py # FastAPI app entry

├── scripts/ # Seeding scripts, CSVs

├── .env # Env vars

├── alembic.ini # Alembic config

├── poetry.lock # Dependencies lock

├── pyproject.toml # Poetry config

└── README.md # This file

\`\`\`

\## Git Workflow

\- Main branch for stable code.

\- Feature branches: reza/melika for individual work.

\- Pull requests for merging to main.

\## Contributors

\- Reza Hashemi: APIs 1,2,3,6 + average ratings.

\- Melika: APIs 4,5,7,8 + validations.

\- Joint: DB setup, seeding, logging (Phase 2).
