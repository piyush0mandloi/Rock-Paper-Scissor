# Rock Paper Scissors — Flask Project Notes

## What This Project Does
A browser-based Rock Paper Scissors game built with Flask.
Tracks wins, losses, and draws across rounds using sessions.
Has a reset button to wipe the scoreboard.

---

## Files
```
project/
├── a.py               # Flask backend
├── templates/
│   └── index.html     # Jinja2 template
└── static/
    └── style.css      # Styling
```

---

## Key Concepts Used

### 1. Flask Session
`session` is a dictionary-like object that persists data across requests for a single user. It stores data in a **signed cookie** on the browser.

```python
from flask import session

app.secret_key = "your_secret_key"  # mandatory — signs the cookie
```

**Why secret_key?** Flask uses it to cryptographically sign the session cookie so users can't tamper with it.

**Read from session:**
```python
user_score = session.get("user_score", 0)
#                                      ↑ default value if key doesn't exist yet
```

**Write to session:**
```python
session["user_score"] = user_score
```

**Clear session:**
```python
session.clear()  # wipes all keys
```

---

### 2. Session Flow in This Project

Every POST request (user plays a round) follows this pattern:

```
POST arrives
  → READ  current scores from session
  → FIGURE OUT who won
  → UPDATE local score variable
  → WRITE  updated scores back to session
  → RENDER template with new scores
```

Why read then write? Because session doesn't auto-update — you must explicitly save changes back.

---

### 3. Why Not Global Variables for Score?

```python
# ❌ Wrong approach
user_score = 0  # global variable

# ✅ Correct approach
session["user_score"] = 0
```

Global variables are **shared across all users**. If two people play simultaneously, their scores would interfere with each other. Session gives each user their own private storage.

---

### 4. Routes

**`/` — home route**
- GET request → just renders the page with current scores from session
- POST request → processes the round, updates session, renders result

```python
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # game logic here
    return render_template("index.html", ...)
```

**`/reset` — reset route**
- Only GET (user clicks a link — no form submission)
- Clears session, redirects back to home
- Never renders anything itself

```python
@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    return redirect(url_for("home"))
```

---

### 5. redirect vs render_template

| Function | What it does |
|---|---|
| `render_template("index.html")` | Renders an HTML file and returns it |
| `redirect(url_for("home"))` | Sends the browser to a different route |

Reset uses `redirect` not `render_template` because:
- It has no variables to pass to a template
- It should hand control back to `home` which handles all rendering
- Avoids re-triggering reset on browser refresh (Post/Redirect/Get pattern)

---

### 6. url_for
Generates a URL for a given route function by name.

```python
url_for("home")   # returns "/"
url_for("reset")  # returns "/reset"
```

Safer than hardcoding `/` or `/reset` — if you rename the path, `url_for` still works.

---

### 7. Passing Session Data to Template

Since scores only exist inside the POST block, use `session.get()` in `render_template` so GET requests (first page load) also get the scores safely:

```python
return render_template(
    "index.html",
    user_score=session.get("user_score", 0),
    comp_score=session.get("comp_score", 0),
    draw_score=session.get("draw_score", 0),
)
```

---

### 8. Reset Button in HTML

Used `<a>` tag instead of `<button>` because reset is just visiting a URL — a GET request, like clicking any link. No form submission involved.

```html
<a href="{{ url_for('reset') }}" class="reset-btn">Reset Scores</a>
```

---

## Imports Used

```python
from flask import Flask, render_template, request, session, redirect, url_for
```

| Import | Used For |
|---|---|
| `Flask` | Creating the app instance |
| `render_template` | Rendering HTML files from `/templates` |
| `request` | Reading form data (`request.form`) and method (`request.method`) |
| `session` | Storing scores across requests |
| `redirect` | Sending user to a different route |
| `url_for` | Generating URLs by route function name |

---

## Common Mistakes to Remember

| Mistake | Fix |
|---|---|
| Forgetting `app.secret_key` | Session won't work at all without it |
| Using `session['key']` to read | Use `session.get('key', default)` to avoid KeyError |
| Updating local variable but not saving back | Always do `session["key"] = updated_value` |
| Using `render_template(url_for("home"))` | `render_template` takes a filename, `redirect` takes a URL |
| Global variables for score | Use session — globals are shared across all users |