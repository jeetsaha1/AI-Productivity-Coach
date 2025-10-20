from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# ==============================
# Base HTML layout (Bootstrap + Navbar)
# ==============================
BASE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>AI Productivity Coach</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">AI Productivity Coach</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="/tasks">Tasks</a></li>
            <li class="nav-item"><a class="nav-link" href="/timer">Timer</a></li>
            <li class="nav-item"><a class="nav-link" href="/focus">Focus</a></li>
            <li class="nav-item"><a class="nav-link" href="/wellness">Wellness</a></li>
            <li class="nav-item"><a class="nav-link" href="/growth">Growth</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container py-4">
      {{ content }}
    </div>

    <footer class="text-center py-3">
      <small class="text-muted">Demo AI Productivity Coach — running in-memory (not persistent)</small>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

# Function to render page with injected content
def render_page(content_html: str, **context) -> str:
    from jinja2 import Template
    template = Template(BASE_HTML.replace("{{ content }}", content_html))
    return template.render(**context)

# ==============================
# In-memory Task Store
# ==============================
tasks = []

# ==============================
# Routes
# ==============================
@app.route("/")
def home():
    return render_page("<h1>Welcome to AI Productivity Coach</h1><p>Select a section above to begin.</p>")

# ---- TASKS ----
@app.route("/tasks", methods=["GET", "POST"])
def tasks_page():
    global tasks
    if request.method == "POST":
        new_task = request.form.get("task")
        if new_task:
            tasks.append({"text": new_task, "done": False})
    return render_page("""
        <h2>Your Tasks</h2>
        <form method="POST" class="mb-3">
            <input type="text" name="task" class="form-control mb-2" placeholder="Enter a new task">
            <button type="submit" class="btn btn-success">Add Task</button>
        </form>

        <ul class="list-group">
            {% for task in tasks %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span style="text-decoration: {{'line-through' if task['done'] else 'none'}};">
                        {{ task["text"] }}
                    </span>
                    <div>
                        <a href="/tasks/done/{{ loop.index0 }}" class="btn btn-sm btn-primary">Done</a>
                        <a href="/tasks/delete/{{ loop.index0 }}" class="btn btn-sm btn-danger">Delete</a>
                    </div>
                </li>
            {% endfor %}
        </ul>
    """, tasks=tasks)

@app.route("/tasks/done/<int:task_id>")
def mark_done(task_id):
    global tasks
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
    return redirect(url_for("tasks_page"))

@app.route("/tasks/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("tasks_page"))

# ---- TIMER ----
@app.route("/timer")
def timer():
    return render_page("""
        <h2>Productivity Timer</h2>
        <p>Simple Pomodoro-style timer.</p>
        <button class='btn btn-success' onclick="startTimer()">Start 25-min Timer</button>
        <p id='timerDisplay' class='mt-3 fs-4'></p>
        <script>
            function startTimer() {
                let timeLeft = 25 * 60; 
                const display = document.getElementById("timerDisplay");
                const timer = setInterval(function() {
                    let minutes = Math.floor(timeLeft / 60);
                    let seconds = timeLeft % 60;
                    display.textContent = minutes + "m " + (seconds < 10 ? "0" : "") + seconds + "s";
                    timeLeft--;
                    if (timeLeft < 0) {
                        clearInterval(timer);
                        display.textContent = "⏰ Time's up! Take a break.";
                        alert("⏰ Pomodoro session ended!");
                    }
                }, 1000);
            }
        </script>
    """)

# ---- FOCUS ----
@app.route("/focus")
def focus():
    return render_page("""
        <h2>Custom Focus Timer</h2>
        <p>Set your own focus session time:</p>

        <div class="mb-3">
            <label for="minutes" class="form-label">Minutes</label>
            <input type="number" id="minutes" class="form-control" value="25" min="1">
        </div>
        <button class="btn btn-primary" onclick="startFocus()">Start Focus</button>

        <p id="focusDisplay" class="mt-3 fs-4"></p>

        <script>
            function startFocus() {
                let minutesInput = document.getElementById("minutes").value;
                let timeLeft = minutesInput * 60;  
                const display = document.getElementById("focusDisplay");

                const timer = setInterval(function() {
                    let minutes = Math.floor(timeLeft / 60);
                    let seconds = timeLeft % 60;
                    display.textContent = minutes + "m " + (seconds < 10 ? "0" : "") + seconds + "s";
                    timeLeft--;
                    if (timeLeft < 0) {
                        clearInterval(timer);
                        display.textContent = "✅ Focus session complete!";
                        alert("✅ Your focus session has ended!");
                    }
                }, 1000);
            }
        </script>
    """)

# ---- WELLNESS ----
@app.route("/wellness")
def wellness():
    return render_page("<h2>Wellness</h2><p>Meditation, break reminders, and health tips to balance productivity.</p>")

# ---- GROWTH ----
@app.route("/growth")
def growth():
    return render_page("<h2>Personal Growth</h2><p>Learning goals, progress tracking, and motivational insights.</p>")

# ==============================
# Run the app
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
