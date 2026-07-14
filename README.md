Interview Scheduling & Candidate Tracking System

Overview

The Interview Scheduling & Candidate Tracking System is a FastAPI-based backend application that helps organizations manage candidates, schedule interviews, collect interviewer feedback, and track recruitment status through secure role-based access.

Features

* JWT Authentication
* Role-Based Authorization
* Candidate Management
* Interview Scheduling
* Feedback Management
* Reports & Search
* Pagination
* SQLite Database
* SQLAlchemy ORM
* Pydantic Validation
* Swagger API Documentation
* Pytest Test Cases



Tech Stack

* Python 3.9+
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* JWT Authentication
* Uvicorn
* Pytest



Project Structure


interview_scheduling_candidate_tracking_system
│
├── app
│   ├── routers
│   │   ├── auth.py
│   │   ├── candidates.py
│   │   ├── interviews.py
│   │   ├── feedback.py
│   │   └── reports.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   ├── utils.py
│   └── main.py
│
├── tests
│
├── requirements.txt
├── README.md
└── .env




Installation

Clone the repository

bash
git clone <repository_url>


Create a virtual environment

bash
python -m venv venv


Activate the virtual environment

Windows

bash
venv\Scripts\activate


Install dependencies

bash
pip install -r requirements.txt




Environment Variables

Create a `.env` file.


DATABASE_URL=sqlite:///./interview.db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30




Run the Application

bash
uvicorn app.main:app --reload


Swagger Documentation


http://127.0.0.1:8000/docs




Authentication APIs

Register


POST /auth/register


Login


POST /auth/login




Candidate APIs


POST /candidates
GET /candidates
GET /candidates/{id}
PUT /candidates/{id}
DELETE /candidates/{id}




Interview APIs


POST /interviews
GET /interviews
GET /interviews/{id}
PUT /interviews/{id}




Feedback APIs


POST /feedback
GET /feedback/{interview_id}




Report APIs


GET /reports/candidates
GET /reports/interviews
GET /reports/selected
GET /reports/rejected




User Roles

Admin

* Manage all users
* Manage candidates
* Manage interviews
* View reports
* View feedback

HR

* Manage candidates
* Schedule interviews
* Update candidate status
* View reports

Interviewer

* View assigned interviews
* Submit interview feedback



Business Rules

* Candidate email must be unique.
* Phone number must be valid.
* One candidate can attend multiple interview rounds.
* Duplicate interview schedules are not allowed.
* Feedback can only be submitted after an interview is marked as Completed.
* Only HR can update the final candidate status.
* Interviewers can view only their assigned interviews.


Testing

Run all test cases.

bash
pytest




Author
Tharun

