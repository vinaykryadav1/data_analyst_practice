from flask import Flask, render_template, request, jsonify, session, redirect,send_from_directory
import json, mysql.connector
import subprocess, tempfile
import sqlite3
import os

os.environ["PYTHONUTF8"] = "1"

app = Flask(__name__)
app.secret_key = "7bc51e823c9d42b3bc1fd8a369d591bf4328f037b5f4a7f2597add93885f64da"

# ================= LOAD JSON =================
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

sql_q = load_json("questions/sql_questions.json")
py_q  = load_json("questions/python_questions.json")
pb_q  = load_json("questions/powerbi_questions.json")
in_q  = load_json("questions/interview_questions.json")

sql_answers     = {q["id"]: q["answer"] for q in load_json("questions/sql_answers.json")}
python_answers  = {q["id"]: q["answer"] for q in load_json("questions/python_answers.json")}
powerbi_answers = {q["id"]: q["answer"] for q in load_json("questions/powerbi_answers.json")}
interview_answers = {q["id"]: q["answer"] for q in load_json("questions/interview_answers.json")}

# ================= DB =================
def db():
    return sqlite3.connect("practice.db")

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= PAGES =================
@app.route("/sql")
def sql_page():
    return render_template("sql.html", questions=sql_q)

@app.route("/python")
def python_page():
    return render_template("python.html", questions=py_q)

@app.route("/powerbi")
def powerbi_page():
    return render_template("powerbi.html", questions=pb_q)

@app.route("/interview")
def interview_page():
    return render_template("interview.html", questions=in_q)

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/pyspark-notes")
def pyspark_notes():
    return send_from_directory("static/files", "pyspark_notes.pdf")

# ================= RUN SQL =================
@app.route("/run_sql", methods=["POST"])
def run_sql():
    query = request.json.get("query")

    try:
        con = db()
        cur = con.cursor()

        cur.execute(query)

        # if select query
        if cur.description:
            data = cur.fetchall()
            cols = [i[0] for i in cur.description]
        else:
            con.commit()
            data = []
            cols = []
            
        con.close()

        return jsonify({"cols": cols, "data": data})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get_tables")
def get_tables():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]

    return jsonify(tables)



# ================= RUN PYTHON =================
@app.route("/run_python", methods=["POST"])
def run_python():
    import subprocess, tempfile, os

    data = request.get_json()
    code = data.get("code", "")

    latest_csv = session.get("latest_csv")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as f:

        # inject csv path variable
        if latest_csv:
            csv_path = os.path.join("uploads", latest_csv)
            f.write(f'CSV_FILE = r"{csv_path}"\n')

        f.write(code)
        file_path = f.name

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5,
            env=dict(os.environ, PYTHONIOENCODING="utf-8")
        )

        output = result.stdout
        error = result.stderr

    finally:
        os.remove(file_path)

    return jsonify({"output": output, "error": error})

@app.route("/save_answer", methods=["POST"])
def save_answer():
    data = request.json
    print("Saved:", data)
    return jsonify({"msg":"saved"})
# ================= REVEAL ANSWER =================
@app.route("/solution/<section>/<qid>")
def solution(section, qid):

    if section == "sql":
        ans = sql_answers.get(qid, "")
    elif section == "python":
        ans = python_answers.get(qid, "")
    elif section == "powerbi":
        ans = powerbi_answers.get(qid, "")
    elif section == "interview":
        ans = interview_answers.get(qid, "")
    else:
        ans = ""

    return jsonify({"answer": ans})

# ================= LOGIN =================
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # demo login (no DB yet)
        if email == "admin@gmail.com" and password == "1234":
            session["user"] = email
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")

# ================= save submission =================
@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return jsonify({"error":"login required"})

    data = request.json
    qid = data["qid"]
    code = data["code"]
    section = data["section"]

    con = db()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO submissions(user_email,question_id,section,status,submitted_code)
    VALUES(?,?,?,?,?)
    """,(session["user"], qid, section, "solved", code))

    # score update
    cur.execute("""
    UPDATE users SET score = score + 10
    WHERE email=?
    """,(session["user"],))

    con.commit()
    con.close()

    return jsonify({"msg":"saved"})

# ================= leaderboard =================
@app.route("/leaderboard")
def leaderboard():
    con = db()
    cur = con.cursor()

    cur.execute("SELECT email,score FROM users ORDER BY score DESC LIMIT 20")
    data = cur.fetchall()

    return jsonify(data)

# ================= MODE =================
@app.route("/interview_mode")
def interview_mode():
    import random
    q = random.sample(sql_q, 5)
    return render_template("interview_mode.html", questions=q)

# ================= DATASET UPLOAD =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")

    if not file:
        return jsonify({"msg": "No file uploaded"})
        
    if file.filename == "":
        return jsonify({"msg": "Empty filename"})
    
    filename = file.filename

    # -------- SAVE FOR PYTHON USE ----------
    py_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(py_path)
    print("Saved at:", file_path)
    print("Files in upload folder:", os.listdir(UPLOAD_FOLDER))
    # -------- SAVE FOR SQL USE (existing logic) ----------
    import pandas as pd

    df = pd.read_csv(py_path)

    con = db()
    df.to_sql("uploaded_data", con, if_exists="replace", index=False)
    con.close()

    # store latest csv for python runner
    session["latest_csv"] = filename

    return jsonify({"msg": f"{filename} uploaded"})

# add into app.py below other @app.route definitions
from flask import request

@app.route("/admin")
def admin_page():
    # render admin UI
    return render_template("admin.html")

@app.route("/admin/add", methods=["POST"])
def admin_add():
    # simple JSON-based add (appends to file) - only use for demo
    if "user" not in session or session.get("user") != "admin@gmail.com":
        return jsonify({"error":"admin only"})
    data = request.json
    section = data.get("section")
    question = data.get("question")
    diff = data.get("diff","medium")

    # Determine file path
    path = f"questions/{section}_questions.json"
    try:
        with open(path,"r", encoding="utf-8") as f:
            arr = json.load(f)
    except FileNotFoundError:
        arr = []

    new_id = str(len(arr) + 1)
    arr.append({"id": new_id, "question": question, "difficulty": diff})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(arr, f, indent=2, ensure_ascii=False)

    return jsonify({"msg":"added", "id": new_id})

@app.route("/user")
def user_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("user.html")

@app.route("/user/submissions")
def user_submissions():
    if "user" not in session:
        return jsonify([])
    con = db()
    cur = con.cursor()
    cur.execute("SELECT question_id,section,submitted_code,created_at FROM submissions WHERE user_email=? ORDER BY created_at DESC", (session["user"],))
    rows = cur.fetchall()
    con.close()
    # simple mapping
    results = [{"question_id":r[0],"section":r[1],"code":r[2],"created_at":r[3]} for r in rows]
    return jsonify(results)
# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= START =================
if __name__ == "__main__":
    app.run(debug=True)

