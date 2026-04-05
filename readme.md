# Finance Tracker API (Django + JWT)

##  Overview

This project is a backend API for managing financial records such as income and expenses.
It is built using Django and Django REST Framework, with JWT-based authentication and role-based access control.

The system supports three types of users:

* Admin
* Analyst
* Viewer

Each role has different permissions for accessing and modifying data.

---

##  Tech Stack

* Python
* Django
* Django REST Framework (DRF)
* SQLite (for development)
* JWT Authentication (SimpleJWT)

---

## Authentication

The project uses JWT (JSON Web Token) for authentication.

* Users log in using `/api/token/`
* Access token is used for API requests
* Refresh token is used to generate a new access token when it expires

---

## User Roles & Permissions

### Admin

* Can create, update, and delete financial records
* Can view all records and also single record
* Can access dashboard and trends

### Analyst

* Can view records
* Can access dashboard and trends
* Cannot modify data

### Viewer

* Can only access dashboard APIs
* Cannot access records directly

---

## API Endpoints

### Authentication

* `POST /api/token/` → Get access & refresh token
* `POST /api/token/refresh/` → Refresh access token

---

###  User

* `POST /register/` → Register a new user

---

###  Financial Records

* `GET /records/` → List records
* `POST /records/` → Create record (Admin only)
* `GET /records/<id>/` → Get single record
* `PUT /records/<id>/` → Update record
* `DELETE /records/<id>/` → Delete record

---

### Dashboard & Insights

* `GET /dashboard/` → Summary, category-wise data, recent transactions
* `GET /trends/` → Monthly or weekly trends

---

## Key Features

* JWT-based authentication (secure API access)
* Role-based access control
* Financial data tracking (income & expense)
* Aggregated dashboard (total income, expense, balance)
* Trend analysis (monthly/weekly)
* Input validation for data integrity

---

##  Assumptions

* As per assignment requirements, only a limited number of users exist.
* Financial records are primarily created by the Admin user.
* Data is not isolated per user to keep the implementation simple and aligned with the assignment scope.

---

##  How to Run the Project

1. Clone the repository
2. Create virtual environment
3. Install dependencies


pip install -r requirements.txt
```

4. Apply migrations


python manage.py makemigrations
python manage.py migrate


5. Run server


python manage.py runserver


##  Example Flow

1. Register a user
2. Login to get JWT token
3. Use token in headers:


Authorization: Bearer <access_token>


4. Access APIs based on role

---

##  Conclusion

This project demonstrates how authentication and role-based access can be implemented in a backend system using Django REST Framework. It also provides practical experience with API design, data handling, and security concepts.

---
