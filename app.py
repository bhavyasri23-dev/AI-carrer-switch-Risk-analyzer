from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for sessions

# -------------------------------
# Sample skills database for careers
# -------------------------------
skills_db = {
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Data Visualization"],
    "Machine Learning Engineer": ["Python", "ML Algorithms", "TensorFlow", "Cloud"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Backend Development"],
    "Data Analyst": ["Excel", "SQL", "Data Visualization", "Python"],
    "Product Manager": ["Communication", "Project Management", "Data Analysis"],
    "UX/UI Designer": ["Design Thinking", "Figma", "Prototyping"],
    "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "Python"],
    "Cloud Engineer": ["AWS", "Azure", "DevOps", "Linux"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "Cloud"],
    "Business Analyst": ["Excel", "SQL", "Communication", "Reporting"],
    "AI Researcher": ["Python", "Deep Learning", "Research Papers"],
    "Blockchain Developer": ["Solidity", "Smart Contracts", "Ethereum"],
    "Digital Marketing Specialist": ["SEO", "Content Marketing", "Analytics"],
    "Software Tester": ["Automation Testing", "Manual Testing", "Selenium"],
    "Database Administrator": ["SQL", "Database Design", "Backup & Recovery"]
}

# -------------------------------
# Simple in-memory user storage
# -------------------------------
users = {}  # {username: password}

# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    username = session.get("username")
    return render_template("home.html", username=username)

# -------------------------------
# Form Page
# -------------------------------
@app.route("/form")
def form():
    username = session.get("username")
    return render_template("form.html", careers=list(skills_db.keys()), username=username)

# -------------------------------
# Predict Page
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    skill = int(request.form.get("skill"))
    hours = int(request.form.get("hours"))
    experience = int(request.form.get("experience"))
    difficulty = int(request.form.get("difficulty"))

    # Support single career selection
    selected_careers = [request.form.get("career")] if "career" in request.form else ["Data Scientist"]

    results = []
    for career in selected_careers:
        base_risk = max(1, difficulty - skill)
        probability = min(95, base_risk * 20)
        readiness = min(100, skill * 20 + hours * 2 + experience * 1.5)

        required_skills = skills_db.get(career, [])
        missing_skills = [s for s in required_skills if skill < 3]  # demo logic
        recommendations = [f"Learn {s}" for s in missing_skills]

        results.append({
            "career": career,
            "risk": "Low" if probability < 40 else "Medium" if probability < 70 else "High",
            "probability": probability,
            "readiness": readiness,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "risk_factors": ["Skill gap", "Low experience"]  # placeholder
        })

    notifications = [f"Reminder: Check your progress for {c['career']}" for c in results]
    username = session.get("username")
    return render_template("results.html", results=results, notifications=notifications, username=username)

# -------------------------------
# Register Page
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username already exists", "error")
        else:
            users[username] = password
            session["username"] = username
            flash("Account created successfully!", "success")
            return redirect(url_for("home"))
    return render_template("register.html")

# -------------------------------
# Login Page
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials", "error")
    return render_template("login.html")

# -------------------------------
# Logout
# -------------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

# -------------------------------
# Dashboard
# -------------------------------
@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    return render_template("dashboard.html", username=username)

# -------------------------------
# Run the App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
