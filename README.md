# Recipe App

# ⚠️➔  🚧 Under Construction 🚧
This project is currently under development and some features may not be fully functional yet. Please check back later for updates.

## Overview
The Recipe App allows users to create, modify, and search for recipes by ingredient. It automatically calculates the difficulty of each recipe and provides user authentication for login and logout. The app also includes a Django Admin dashboard for managing database entries and displays statistics and visualizations based on trends and data analysis.

## Features
- User authentication: login, logout, and registration
- Create and modify recipes with ingredients, cooking time, and automatic difficulty rating
- Search for recipes by ingredient
- Display detailed information on each recipe
- Add recipes to an SQLite database (PostgreSQL for production)
- Django Admin dashboard for database management
- Error handling and user-friendly error messages
- Statistics and visualizations based on recipe data

## Technical Requirements
- Python 3.6+
- Django 3.x
- SQLite for development
- PostgreSQL for production
- Proper documentation and automated tests
- `requirements.txt` for module dependencies
- Readme file with setup instructions

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- PostgreSQL (for production)

### Installation
1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/recipe-app.git
    cd recipe-app
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup SQLite database (development)**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. **Run the development server**
    ```bash
    python manage.py runserver
    ```

6. **Access the application**
    Open your browser and go to `http://127.0.0.1:8000/`

### PostgreSQL Setup (Production)
1. **Install PostgreSQL**
    Follow the instructions on the [PostgreSQL website](https://www.postgresql.org/download/).

2. **Configure PostgreSQL database**
    - Create a database and user for your project.
    - Update the `DATABASES` setting in `settings.py` to use PostgreSQL:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    ```

3. **Migrate the database**
    ```bash
    python manage.py migrate
    ```

### Running Tests
Run automated tests to ensure everything is working correctly:
```bash
python manage.py test
