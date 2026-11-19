# NSUT Campus Review

A beginner-friendly full-stack CP project using:
- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Database: SQLite

## 1. Install Python

Install Python 3 from https://www.python.org/downloads/ and select **Add Python to PATH** during installation.

Open this project folder in VS Code. Open Terminal > New Terminal.

## 2. Create a virtual environment (recommended)

Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in that terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 3. Install Flask

```powershell
py -m pip install -r requirements.txt
```

## 4. Run the website

```powershell
py app.py
```

You should see a local address similar to:

`http://127.0.0.1:5000`

Ctrl+click the address in the terminal, or paste it into your browser.

The first run automatically creates `campus_review.db` and adds the starter menu/equipment records. Reviews are stored in this SQLite database and remain after you stop and restart the server.

## 5. Understand how the parts connect

1. A student opens a page such as `/outlet/safal`.
2. The HTML template creates the page structure.
3. CSS styles the page and JavaScript makes it interactive.
4. JavaScript calls Flask API routes such as `/api/items/safal`.
5. Flask reads item data from SQLite and sends it to JavaScript as JSON.
6. When a student submits a review, JavaScript sends the rating and comment to `/api/reviews`.
7. Flask validates the data and inserts it into the `reviews` table.

## 6. Important files

- `app.py` — Flask server, API routes, database creation and starter data.
- `templates/index.html` — homepage.
- `templates/outlet.html` — reusable outlet/menu/review page.
- `static/style.css` — all visual styling and responsive layouts.
- `static/main.js` — search, filters, star selection, reviews and scroll effects.
- `campus_review.db` — created automatically when the app runs.

## 7. Update menu items

Open `app.py` and find the `MENU` dictionary. Each row follows this format:

```python
("Item name", "Category", 50, "Optional note")
```

Change the name, category, price or note. To add a new item, add another row under the correct outlet.

The database uses `INSERT OR IGNORE` so existing items are not duplicated. If you want to completely rebuild the starter database while developing, stop Flask, delete `campus_review.db`, then run `py app.py` again. This also deletes any reviews stored in that database, so keep a backup if needed.

## 8. Add the real gym equipment

The gym currently contains clearly marked placeholder entries. After checking the gym, replace the `gym_items` list in `init_db()` with the actual equipment names and categories. If the database already exists, delete it before restarting to load the revised starter list (this also deletes test reviews).

