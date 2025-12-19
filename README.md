# Library Management

Simple library management backend built with Django REST Framework.

---

## Tech Stack
- Python  
- Django  
- Django REST Framework (DRF)  
- Simple JWT  

---

## Features
- JWT Authentication  
- Librarian and Customer roles  
- Add, delete, and browse books  
- Checkout and book reports  

---

#Project Structure

library-management/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── library_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── migrations/
│       └── __init__.py
│
├── books/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
│
├── transactions/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│       └── __init__.py
│
└── venv/


## How to Run

# 1. Clone the repository
git clone https://github.com/your-username/library-management.git
cd library-management

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run the server
python manage.py runserver
