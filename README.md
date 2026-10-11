# Expense Tracker

A small web app to record and review personal expenses. Built with Python (Flask), SQLite, HTML and CSS.

## Features

- Add expenses with a title, amount, category and date
- Delete expenses
- Filter by category and by month
- Running total and a per-category spending breakdown
- Input validation on the server (positive amounts, known categories)
- Parameterized SQL queries throughout (no SQL injection)
- Responsive layout that works on phones

## Tech stack

| Layer    | Choice            |
|----------|-------------------|
| Backend  | Python 3, Flask   |
| Database | SQLite (stdlib)   |
| Frontend | Jinja2, HTML, CSS |

## Getting started

```bash
git clone <your-repo-url>
cd expense-tracker
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. The database file `expenses.db` is created automatically on first run.

## Project structure

```
expense-tracker/
├── app.py              # routes, database helpers
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    └── index.html
```

## Ideas for extending it

- Edit existing expenses
- Export to CSV
- Monthly budgets with alerts
- User accounts (Flask-Login)
- Charts with Chart.js
- Unit tests with pytest

## License

MIT
