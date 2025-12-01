# AyurBase - Hospital Management System

AyurBase is a comprehensive Hospital Management System built with a modern tech stack. It facilitates the management of doctors, patients, appointments, and departments, featuring role-based access control, background jobs for notifications, and interactive dashboards.

## 🏗️ Project Structure

The project is divided into two main parts:

*   **`backend/`**: A Flask-based REST API.
    *   **`app/`**: Contains the application logic.
        *   `models.py`: Database models (SQLAlchemy).
        *   `resources.py`: API resources (Flask-RESTful).
        *   `tasks.py`: Celery tasks for background jobs (Reminders, Reports, Exports).
    *   **`celery_worker.py`**: Entry point for the Celery worker.
    *   **`run.py`**: Entry point for the Flask application.

*   **`frontend/`**: A Vue.js 3 application (using Vite).
    *   **`src/`**: Source code.
        *   `pages/`: Application views (Admin, Doctor, Patient dashboards).
        *   `components/`: Reusable UI components.
        *   `store/`: State management (Pinia).
        *   `services/`: API client configuration.

## 🚀 How to Run

### Prerequisites
*   **Python 3.8+**
*   **Node.js 16+**
*   **Redis** (Must be installed and running)

### Option 1: VSCode Tasks (Recommended)
This project comes with configured VSCode tasks to run everything with one click.

1.  Open the project in VSCode.
2.  Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).
3.  Type **"Tasks: Run Task"** and select it.
4.  Choose **"Start App"**.
    *   This will automatically start **Redis**, **Celery Worker**, **Backend**, and **Frontend** in parallel terminals.

### Option 2: Manual Setup

If you prefer running commands manually, open 4 separate terminals:

**1. Start Redis**
```bash
redis-server
```

**2. Start Backend**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

**3. Start Celery Worker (for Background Jobs)**
```bash
cd backend
source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info --beat
```

**4. Start Frontend**
```bash
cd frontend
npm install  # Only first time
npm run dev
```

## 🔑 Default Login Credentials

*   **Admin**: `admin@hms.com` / `admin`
*   **Doctor**: `doctor@hms.com` / `doctor` (or create new via Admin)
*   **Patient**: Register a new account via the UI.

## ✨ Key Features

*   **Role-Based Access**: Distinct dashboards for Admins, Doctors, and Patients.
*   **Appointments**: Booking, cancellation, and completion workflows.
*   **Medical Records**: Doctors can prescribe treatments; Patients can view history.
*   **Reports & Analytics**: Admin dashboard with charts; Monthly reports sent via Google Chat.
*   **Notifications**: Google Chat integration for reminders and status updates.
*   **Data Export**: Patients can export their treatment history as CSV.
