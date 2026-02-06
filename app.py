from flask import Flask, render_template, request, jsonify, session, redirect
import json, mysql.connector
import subprocess, tempfile
import sqlite3


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

    code = request.json.get("code")

    try:
        # temp file create
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode())
            fname = f.name

        # run python
        result = subprocess.run(
            ["python", fname],
            capture_output=True,
            text=True,
            timeout=5
        )

        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })

    except Exception as e:
        return jsonify({"error": str(e)})

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

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= START =================
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)

