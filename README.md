# 🏥 ClinicFlow — Smart Clinic Management System

A production-ready clinic management system built with Django, Django REST Framework, MySQL, Pandas, and JWT authentication. Designed to solve real-world problems faced by small clinics and hospitals in India.

---

## 🚀 Live Features

- 👨‍⚕️ **Patient Management** — Register, search, edit, delete patients with full medical history
- 📅 **Appointment Booking** — Book, reschedule, cancel appointments with double-booking prevention
- 💊 **Prescription Management** — Doctors write digital prescriptions with medicine lists
- 🧾 **Billing & Invoicing** — Auto-generate invoices with live total calculator
- 📊 **Analytics Dashboard** — Revenue reports, doctor performance stats using Pandas & Numpy
- 📁 **CSV Export** — Export patient and revenue data as Excel-compatible CSV
- 🔐 **Role-based Access** — Admin, Doctor, Receptionist roles with custom decorators
- 🌐 **REST API** — Full API with JWT authentication for mobile/React integration
- 🔒 **Secure** — JWT tokens, .env secrets, CSRF protection

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend Framework | Django 6.x |
| REST API | Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | MySQL 8.0 |
| Analytics | Pandas, Numpy |
| Task Queue | Celery + Celerybeat (planned) |
| Frontend | Django Templates + Bootstrap 5 |
| Language | Python 3.13 |

---

## 📋 PDF Training Topics Covered

This project covers every topic from the Python training document:

### Python Core
- ✅ Data Types, Lists, Tuples, Sets, Dictionaries
- ✅ OOP — Classes, Objects, Inheritance
- ✅ Decorators — @login_required, @doctor_required, custom role decorators
- ✅ Lambda Functions — medicine list processing
- ✅ File I/O — CSV export using Python's csv module
- ✅ Exception Handling — try/except in all views
- ✅ Built-in Functions — sum(), filter(), map(), sorted(), len()
- ✅ DateTime module — age calculation, appointment scheduling
- ✅ Numpy & Pandas — revenue analytics, data processing
- ✅ Regular Expressions — phone number validation
- ✅ Multithreading — Celery workers
- ✅ Python pip — requirements.txt
- ✅ Python JWT — API authentication

### Database
- ✅ MySQL — all 4 relation types (1:1, 1:M, M:1, M:M)
- ✅ All Keys — Primary, Foreign, Unique, Candidate
- ✅ All Queries — CREATE, INSERT, UPDATE, DELETE, SELECT
- ✅ WHERE, ORDER BY, GROUP BY, HAVING, Aliases
- ✅ OR, AND, NOT, BETWEEN, IN, NOT IN
- ✅ MIN, MAX, SUM, COUNT, AVG
- ✅ All 4 Joins — LEFT, RIGHT, INNER, OUTER

### Django
- ✅ Models, Forms, Authentication
- ✅ Jinja Templating & Static files
- ✅ Django REST Framework — FBV, CBV, Generic Views
- ✅ Serializers

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- MySQL 8.0
- pip

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/clinicflow.git
cd clinicflow
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
Create a `.env` file in the root directory:

### 5. Create MySQL database
```sql
CREATE DATABASE clinicflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Run the server
```bash
python manage.py runserver
```

### 9. Access the application
- **Web App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/

---

## 🌐 API Documentation

### Authentication

### Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /api/auth/login/ | Get JWT token | No |
| GET | /api/dashboard/ | System stats | JWT |
| GET/POST | /api/patients/ | List/Create patients | JWT |
| GET/PUT/DELETE | /api/patients/{id}/ | Patient detail | JWT |
| GET | /api/doctors/ | List doctors | JWT |
| GET | /api/doctors/{id}/ | Doctor detail | JWT |
| GET/POST | /api/appointments/ | List/Create appointments | JWT |
| GET/PUT/DELETE | /api/appointments/{id}/ | Appointment detail | JWT |
| GET/POST | /api/prescriptions/ | List/Create prescriptions | JWT |
| GET/POST | /api/bills/ | List/Create bills | JWT |

### Using the API
```bash
# Login to get token
POST /api/auth/login/

# Use token in header
Authorization: Bearer <your-access-token>
```

---

## 🏗️ Project Structure


---

## 👤 User Roles

| Role | Access |
|---|---|
| Admin | Full access — all features |
| Doctor | Appointments + Prescriptions only |
| Receptionist | Patients + Appointments + Billing |

---

## 🔐 Security Features

- JWT token authentication on all API endpoints
- Role-based access control with custom decorators
- CSRF protection on all forms
- Passwords stored using Django's secure hashing
- Sensitive data in .env file — never committed to Git
- Input validation on both HTML and Python level

---

## 📊 Database Schema

- **User** — Custom user with roles
- **Patient** — Patient records with medical history
- **Doctor** — Doctor profiles linked to users
- **Appointment** — Bookings with double-booking prevention
- **Prescription** — Digital prescriptions per appointment
- **Bill** — Auto-calculated invoices with payment tracking

---

## 🙋 Developer

**Dhaval Tirgar**
MCA Student | Python Backend Developer
- Built as internship training project
- Covers complete Python + Django + MySQL training curriculum

---

## 📄 License

This project is for educational purposes.