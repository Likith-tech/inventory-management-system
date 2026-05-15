# Inventory Management System

Professional Flask mini project for managing products, categories, suppliers, incoming stock, sales, low stock alerts, and reports.

## Tech Stack

- Python Flask
- SQLite
- SQLAlchemy
- Flask Login
- Flask-WTF
- Bootstrap 5
- JavaScript

## How To Run

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Default login:

```text
Username: admin
Password: admin123
```

## File Purpose

- `app.py`: Starts the Flask server.
- `config.py`: Stores app settings, database path, and default admin credentials.
- `app/__init__.py`: Creates the Flask app, initializes extensions, registers blueprints, and creates tables.
- `app/models/`: SQLAlchemy database models.
- `app/forms/`: Flask-WTF form classes and validation.
- `app/routes/`: Flask Blueprint route files for each feature.
- `app/services/`: Business logic such as stock updates and report export.
- `app/utils/`: Small helper functions.
- `app/templates/`: HTML pages.
- `app/static/`: CSS and JavaScript files.

## Development Roadmap

1. Authentication and dashboard.
2. Product, category, and supplier management.
3. Incoming stock and sales entry.
4. Automatic stock quantity update.
5. Low stock alert.
6. Date-filtered reports.
7. CSV and PDF export.
8. Future API layer for React frontend.

## VS Code Setup

1. Open the `Inventory_app` folder in VS Code.
2. Select the Python interpreter from `venv/Scripts/python.exe`.
3. Open a terminal in VS Code.
4. Activate the virtual environment.
5. Run `python app.py`.

## GitHub Workflow

```powershell
git init
git add .
git commit -m "Initial inventory management system"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

Team workflow:

- Create a branch for each feature.
- Pull the latest `main` before starting work.
- Commit small changes with clear messages.
- Open pull requests for review.
- Avoid editing the same file together without coordination.

## Future React + Flask Architecture

Later, this project can be split into:

```text
frontend/  React app
backend/   Flask REST API
```

Flask would provide JSON APIs such as:

- `POST /api/login`
- `GET /api/products`
- `POST /api/products`
- `POST /api/stock-in`
- `POST /api/sales`
- `GET /api/reports`

React would handle the user interface, while Flask would manage authentication, database logic, reports, and exports.
