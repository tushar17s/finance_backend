# Finance Tracker API (Django + JWT)

## Overview

This project is a backend API for managing financial records such as income and expenses.
It is built using Django and Django REST Framework, with JWT-based authentication and role-based access control.

The system supports three types of users:

* Admin
* Analyst
* Viewer

Each role has different permissions for accessing and modifying data.

---

## Tech Stack

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
* Can view all records and individual records
* Can access dashboard , trends and also access recent transactions at dashboard

### Analyst

* Can view records
* Can access dashboard ,trends and also access recent transactions at dashboard
* Cannot modify data

### Viewer

* Can only access dashboard APIs but not access recent transactions at dashboard
* Cannot access records directly

---

## Key Features

* JWT-based authentication (secure API access)
* Role-based access control
* Financial data tracking (income & expense)
* Aggregated dashboard (total income, expense, balance)
* Trend analysis (monthly/weekly)
* Input validation for data integrity

---

## API Explanation

### Authentication

* `POST /api/token/`
  Used to log in and receive access and refresh tokens

* `POST /api/token/refresh/`
  Used to generate a new access token using the refresh token

---

### Register User

* `POST /register/`
  Creates a new user with a specific role (Admin, Analyst, Viewer)

---

### Financial Records

* `GET /records/`
  Returns list of financial records (based on user role)

* `POST /records/`
  Allows Admin to create a new financial record

* `GET /records/<id>/`
  Fetch a single record

* `PUT /records/<id>/`
  Update a record (Admin only)

* `DELETE /records/<id>/`
  Delete a record (Admin only)

---

### Dashboard

* `GET /dashboard/`
  Returns:

  * Total income
  * Total expense
  * Net balance
  * Category-wise summary
  * Recent transactions

---

### Trends

* `GET /trends/?type=monthly` → Monthly data
* `GET /trends/?type=weekly` → Weekly data

---

## Assumptions

* As per assignment requirements, only a limited number of users exist
* Financial records are primarily created by the Admin user
* Data is not isolated per user to keep the implementation simple and aligned with the assignment scope

---

## Tradeoffs Considered

* The system does not isolate financial data per user using `created_by` filtering
  This decision was made based on the assumption that only a single Admin creates records

* A simple role-based permission system is implemented using conditional checks instead of Django’s built-in permission classes
  This keeps the logic easy to understand for the assignment

* SQLite is used instead of PostgreSQL to simplify setup

* Token refresh handling is not automated on the frontend side since the focus is backend

---

## How to Run the Project

1. Clone the repository
2. Create virtual environment
3. Install dependencies


pip install -r requirements.txt


4. Apply migrations


python manage.py makemigrations
python manage.py migrate


5. Run server


python manage.py runserver


---

## Example Flow

1. Register a user
2. Login to get JWT token
3. Use token in headers:


Authorization: Bearer <access_token>


4. Access APIs based on role

---

## Conclusion

This project demonstrates how authentication and role-based access can be implemented using Django REST Framework.
It also helped in understanding API design, JWT authentication, and role-based control in a practical way.

---
