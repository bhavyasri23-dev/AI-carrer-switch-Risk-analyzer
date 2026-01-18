from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    skill = int(request.form["skill"])
    hours = int(request.form["hours"])
    experience = int(request.form["experience"])
    difficulty = int(request.form["difficulty"])

    prediction = model.predict([[skill, hours, experience, difficulty]])[0]
    proba = model.predict_proba([[skill, hours, experience, difficulty]])

    risk_map = {0: "HIGH", 1: "MEDIUM", 2: "LOW"}
    risk = risk_map[prediction]

    probability = round(max(proba[0]) * 100, 2)
    readiness = max(0, 100 - probability)

    missing_skills = []
    if skill < 3:
        missing_skills.append("Core technical skills")
    if experience < 2:
        missing_skills.append("Industry experience")

    months = len(missing_skills) * 4

    risk_factors = []
    if skill < 3:
        risk_factors.append("Low skill level")
    if hours < 5:
        risk_factors.append("Low weekly learning hours")
    if difficulty > 3:
        risk_factors.append("High career difficulty")

    recommendations = []
    if skill < 3:
        recommendations.append("Improve core skills")
    if hours < 8:
        recommendations.append("Increase learning hours")
    if experience < 3:
        recommendations.append("Work on real-world projects")

    return render_template(
        "results.html",
        risk=risk,
        probability=probability,
        readiness=readiness,
        missing_skills=missing_skills,
        months=months,
        risk_factors=risk_factors,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)
