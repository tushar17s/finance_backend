# Role-Based Finance Data Processing Backend

##  Overview
This project is a backend system designed to manage financial records with role-based access control. It supports different user roles (Admin, Analyst, Viewer) and provides secure data handling along with analytical insights through dashboard APIs.

---

##  Features

###  User & Role Management
- User registration with roles (Admin, Analyst, Viewer)
- Role-based access control enforced at API level

###  Financial Records Management
- Create, view, update, delete financial records
- Fields include amount, type, category, date, and notes
- Data filtering and structured storage

### Dashboard APIs
- Total income, expenses, and net balance
- Category-wise aggregation
- Recent transactions

###  Access Control
- Viewer → Dashboard only
- Analyst → Records + Dashboard
- Admin → Full access

###  Validation & Error Handling
- Input validation (amount, type)
- Proper error messages and status codes

---

##  Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (can be replaced with PostgreSQL)

---

##  API Endpoints

### User
- POST `/register/`

### Records
- GET `/records/`
- POST `/records/`
- GET `/records/<id>/`
- PUT `/records/<id>/`
- DELETE `/records/<id>/`

### Dashboard
- GET `/summary/`
- GET `/category-summary/`
- GET `/recent/`

---

## ▶How to Run

```bash
git clone <your-repo-link>
cd project-folder
pip install -r requirements.txt
python manage.py runserver