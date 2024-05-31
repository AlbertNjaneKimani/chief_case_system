# Case Management System

This is a Django-based Case Management System designed to manage cases, appointments, and users efficiently. The system includes functionalities such as user registration, profile management, case creation, appointment scheduling, and email notifications.

## Features

- **User Registration and Login**: Allows users to register, login, and logout.
- **Profile Management**: Users can create and edit their profiles.
- **Case Management**: Users can create, view, approve, reject, and resolve cases.
- **Appointment Scheduling**: Users can book appointments related to cases.
- **Email Notifications**: Sends email notifications to users upon appointment creation.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/case-management-system.git
    cd case-management-system
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the database**:
    - Update `DATABASES` settings in `settings.py` to match your database configuration.

5. **Run migrations**:
    ```sh
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

8. **Access the application**:
    - Open your web browser and navigate to `http://127.0.0.1:8000`

## Configuration

### Email Settings

To enable email notifications, configure the email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_specific_password'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'
