from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

SKILLS_DB = [
    "Python", "Java", "C++",
    "HTML", "CSS", "JavaScript",
    "SQL", "Excel", "Pandas", "NumPy",
    "Cybersecurity", "Network Security", "Ethical Hacking",
    "Penetration Testing", "Kali Linux", "Wireshark",
    "Communication", "Leadership", "Recruitment",
    "HR Management", "Team Management"
]

JOB_ROLES = {
    "Data Analyst": ["Python", "SQL", "Excel"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript"],
    "Backend Developer": ["Python", "Java"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Python"],
    "Cybersecurity Analyst": ["Cybersecurity", "Network Security", "Ethical Hacking"],
    "HR Manager": ["Communication", "Leadership", "Recruitment"]
}

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:2]:
            content = page.extract_text()
            if content:
                text += content
    return text

def extract_skills(text):
    return [skill for skill in SKILLS_DB if skill.lower() in text.lower()]

def calculate_score(skills):
    return min(len(skills) * 15, 100)

def recommend_jobs(skills):
    recommended = []
    for job, req in JOB_ROLES.items():
        if len(set(skills) & set(req)) >= 2:
            recommended.append(job)
    return recommended

def calculate_ats(skills):
    required = ["Python", "SQL", "Excel"]
    match = len(set(skills) & set(required))
    return int((match / len(required)) * 100)

def generate_feedback(skills, score):
    if score >= 80:
        level = "Advanced"
        msg = "Strong profile with high job readiness."
    elif score >= 50:
        level = "Intermediate"
        msg = "Good base, improve projects."
    else:
        level = "Beginner"
        msg = "Build core skills."

    if "Python" not in skills:
        msg += " Learn Python."
    if "SQL" not in skills:
        msg += " Add SQL."
    if "JavaScript" not in skills:
        msg += " Improve frontend skills."

    return level, msg

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']

    text = extract_text(file)
    skills = extract_skills(text)
    score = calculate_score(skills)
    jobs = recommend_jobs(skills)

    ats = calculate_ats(skills)
    level, feedback = generate_feedback(skills, score)

    return render_template(
        'result.html',
        score=score,
        skills=skills,
        jobs=jobs,
        ats=ats,
        level=level,
        feedback=feedback
    )

if __name__ == '__main__':
    app.run(debug=True)