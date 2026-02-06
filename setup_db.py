import sqlite3

con = sqlite3.connect("practice.db")
cur = con.cursor()

# =========================
# EMPLOYEES TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS employees(
 id INTEGER,
 name TEXT,
 salary INTEGER,
 dept_id INTEGER,
 hire_date TEXT
)
""")

cur.executemany(
"INSERT INTO employees VALUES(?,?,?,?,?)",
[
(1,"A",50000,1,"2021-01-10"),
(2,"B",70000,2,"2020-03-15"),
(3,"C",60000,1,"2022-07-19"),
(4,"D",80000,2,"2019-11-01"),
(5,"E",45000,3,"2023-02-10"),
(6,"F",90000,2,"2018-06-25"),
(7,"G",75000,4,"2021-09-05"),
(8,"H",52000,3,"2022-12-12"),
(9,"I",67000,4,"2020-05-30"),
(10,"J",48000,1,"2023-08-01")
]
)

# =========================
# DEPARTMENTS TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS departments(
 id INTEGER,
 dept_name TEXT
)
""")

cur.executemany(
"INSERT INTO departments VALUES(?,?)",
[
(1,"HR"),
(2,"IT"),
(3,"Finance"),
(4,"Sales")
]
)

# =========================
# ORDERS TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
 order_id INTEGER,
 emp_id INTEGER,
 amount INTEGER,
 order_date TEXT
)
""")

cur.executemany(
"INSERT INTO orders VALUES(?,?,?,?)",
[
(1,1,200,"2024-01-01"),
(2,2,500,"2024-01-02"),
(3,1,300,"2024-01-03"),
(4,3,700,"2024-01-05"),
(5,4,1000,"2024-01-07"),
(6,2,400,"2024-01-10"),
(7,5,250,"2024-01-11"),
(8,6,900,"2024-01-12"),
(9,7,650,"2024-01-15"),
(10,1,150,"2024-01-20")
]
)

# =========================
# PROJECTS TABLE (NEW)
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS projects(
 project_id INTEGER,
 project_name TEXT,
 dept_id INTEGER,
 budget INTEGER
)
""")

cur.executemany(
"INSERT INTO projects VALUES(?,?,?,?)",
[
(1,"HR System",1,50000),
(2,"Website",2,120000),
(3,"Accounting Tool",3,80000),
(4,"CRM",4,150000),
(5,"Data Warehouse",2,200000)
]
)

# =========================
# EMP_PROJECT TABLE (MANY TO MANY)
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS emp_project(
 emp_id INTEGER,
 project_id INTEGER
)
""")

cur.executemany(
"INSERT INTO emp_project VALUES(?,?)",
[
(1,1),
(2,2),
(3,1),
(4,2),
(5,3),
(6,5),
(7,4),
(8,3),
(9,4),
(10,1)
]
)

# =========================
# ATTENDANCE TABLE (NEW)
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
 emp_id INTEGER,
 att_date TEXT,
 status TEXT
)
""")

cur.executemany(
"INSERT INTO attendance VALUES(?,?,?)",
[
(1,"2024-01-01","Present"),
(2,"2024-01-01","Absent"),
(3,"2024-01-01","Present"),
(4,"2024-01-01","Present"),
(5,"2024-01-01","WFH"),
(6,"2024-01-01","Present"),
(7,"2024-01-01","Absent"),
(8,"2024-01-01","Present"),
(9,"2024-01-01","Present"),
(10,"2024-01-01","WFH")
]
)


con.commit()
con.close()

print("SQLite DB Ready")
