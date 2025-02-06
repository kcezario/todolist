# TodoList Project

## Overview

TodoList is a Django-based project providing a **REST API for task management**. It includes **role-based access control**, **authentication**, and **advanced filtering** to support different user levels (Admin, Manager, and Regular Users). This API is designed for real-world applications requiring structured task handling with **user-specific access levels**.

## Features

- **User Authentication:** Token-based authentication with Django REST Framework.
- **Role-Based Access Control (RBAC):**
  - **Admin:** Full control over all tasks and users.
  - **Manager:** Can view all tasks but modify only their own.
  - **User:** Can only manage their own tasks.
- **Task Management:** Create, read, update, and delete tasks.
- **Filtering & Pagination:** Filter tasks by `status` and `due_date`.
- **API Documentation:** Auto-generated Swagger UI with drf-spectacular.

## Technologies Used

- **Python** (3.x)
- **Django** (5.1.6)
- **Django REST Framework** (DRF)
- **Django Filters** (for advanced filtering)
- **drf-spectacular** (for API documentation)
- **python-decouple** (for environment variable management)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/todolist.git
    cd todolist
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the project root and add the following:
    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

5. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## API Documentation

- **Swagger UI**: Available at `/api/docs/` when the server is running.
- **API Schema**: `/api/schema/` provides OpenAPI specification for integrations.

## Running Tests

To ensure everything is working correctly, run:
```bash
python manage.py test
```

## License

This project is licensed under the MIT License.

