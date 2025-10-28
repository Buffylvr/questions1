# random_questions.py
from flask import Flask, jsonify, render_template_string, request
import random
import json
import os

app = Flask(__name__, static_folder="static")

QUESTIONS_FILE = "questions.json"

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        default = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "What color do you get when you mix blue and yellow?", "answer": "Green"},
            {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare"},
            {"question": "What planet is known as the Red Planet?", "answer": "Mars"}
        ]
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)
        return default
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(questions):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2)

QUESTIONS = load_questions()

# --- Base layout template (same sidebar as before) ---
BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="/static/style.css" />
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h2>Quiz App</h2>
      <nav>
        <a href="/" class="{{ 'active' if active == 'home' else '' }}">🏠 Home</a>
        <a href="/questions" class="{{ 'active' if active == 'questions' else '' }}">🧠 Quiz</a>
      </nav>
    </aside>

    <main class="content">
      {{ content|safe }}
    </main>
  </div>
</body>
</html>
"""

# --- Page loader helper ---
def load_page(name: str) -> str:
    path = os.path.join("pages", f"{name}.html")
    if not os.path.exists(path):
        return f"<h1>Missing page</h1><p>{path} not found.</p>"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# --- Routes ---
@app.route("/")
def home():
    content = load_page("home")
    return render_template_string(BASE_TEMPLATE, title="Home", content=content, active="home")

@app.route("/questions")
def questions_page():
    content = load_page("questions")
    return render_template_string(BASE_TEMPLATE, title="Quiz", content=content, active="questions")

@app.route("/question", methods=["POST"])
def question():
    q = random.choice(QUESTIONS)
    return jsonify(q)

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.get_json(silent=True) or {}
    q = (data.get("question") or "").strip()
    a = (data.get("answer") or "").strip()
    if not q or not a:
        return jsonify({"ok": False, "error": "Question and answer required"}), 400
    for existing in QUESTIONS:
        if existing["question"].lower() == q.lower():
            return jsonify({"ok": False, "error": "Duplicate question"}), 400
    QUESTIONS.append({"question": q, "answer": a})
    save_questions(QUESTIONS)
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("✅ Running at http://127.0.0.1:5000")
    app.run(debug=True)
