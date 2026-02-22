import sqlite3

con = sqlite3.connect("practice.db")
cur = con.cursor()

# =========================
# EMPLOYEES TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS employees(
 emp_id INTEGER,
 emp_name TEXT,
 salary INTEGER,
 manager_id INTEGER,
 dept_name TEXT,
 city TEXT,
 joining_date TEXT
)
""")

cur.executemany(
"INSERT INTO employees VALUES(?,?,?,?,?,?,?)",
[
(1, 'Amit', 54321, 1, 'IT', 'Delhi', '2025-01-07'),
(5, 'Shayam', 76543, 5, 'Sales', 'Delhi', '2025-04-12'),
(7, 'Suraj', 34566, 7, 'Sales', 'Delhi', '2025-04-12'),
(3, 'Aman', 45366, 3, 'Admin', 'Delhi', '2025-07-16'),
(4, 'Mohit', 65433, 5, 'Sales', 'Mumbai', '2025-08-14'),
(6, 'Kishan', 65432, 7, 'Sales', 'Pune', '2025-08-14'),
(2, 'Rohit', 87654, 1, 'IT', 'Mumbai', '2025-09-17'),
(8, 'Chandan', 76542, 1, 'IT', 'Pune', '2025-09-17'),
(9, 'Prakash', 25375, 5, 'Admin', 'Surat', '2025-11-20'),
(10, 'Ram', 57857, 3, 'Admin', 'Surat', '2025-11-20')
]
)

# =========================
# ADDRESSS TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS user_address(
 id INTEGER,
 full_address TEXT
)
""")

cur.executemany(
"INSERT INTO user_address VALUES(?,?)",
[
(1,"123, MG Road, Shivaji Nagar Bengaluru 560001"),
(2,"Plot No. 45, Sector 18 Gurugram 122001"),
(3,"44/1 Bharat Apartment, 560041 Jayanagar Bangalore"),
(4,"Flat No. 202, Apoorva Society Mumbai 400055"),
(5,"12-B, Sri Krishna Vihar Apartments 	530011 	Visakhapatnam")
]
)

# =========================
# ORDERS TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
 order_id INTEGER,
 cust_id INTEGER,
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
# SALES TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS sales(
 sale_id INTEGER,
 cust_id INTEGER,
 product_id INTEGER,
 emp_id INTEGER,
 sale_date TEXT,
 quantity INTEGER,
 amount INTEGER
)
""")

cur.executemany(
"INSERT INTO sales VALUES(?,?,?,?,?,?,?)",
[
(1, 1, 101, 201, '2024-01-10', 1, 50000.00),
(2, 2, 102, 202, '2024-01-15', 1, 30000.00),
(3, 3, 103, 203, '2024-02-05', 2, 4000.00),
(4, 1, 102, 201, '2024-02-20', 1, 28000.00),
(5, 4, 101, 204, '2024-03-01', 1, 52000.00),
(6, 5, 103, 205, '2024-03-18', 3, 6000.00),
(7, 2, 104, 202, '2024-04-10', 1, 2500.00),
(8, 3, 102, 203, '2024-04-12', 1, 31000.00),
(9, 1, 101, 201, '2024-04-15', 1, 50000.00),
(10, 1, 101, 201, '2024-04-15', 1, 50000.00)
]
)

# =========================
# transactions
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions(
 txn_id INTEGER,
 user_id INTEGER,
 txn_amount INTEGER,
 txn_date TEXT
)
""")

cur.executemany(
"INSERT INTO transactions VALUES(?,?,?,?)",
[
(101,1,58909,'2024-01-01 10:00:00'),
(102,2,89351,'2024-01-05 14:30:00'),
(103,1,23546,'2024-01-03 09:15:00'),
(104,2,34757,'2024-01-03 09:15:00'),
(105,3,35264,'2024-01-02 18:45:00'),
(106,5,85665,'2024-01-10 11:00:00'),
(107,4,46364,'2024-02-20 12:00:00'),
(108,3,26346,'2024-02-08 09:00:00'),
(109,4,23637,'2024-02-14 16:08:00'),
(110,1,63654,'2024-03-13 11:11:00')
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
# =========================
# LOGIN
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS logins(
 user_id INTEGER,
 login_date TEXT,
 status TEXT
)
""")

cur.executemany(
"INSERT INTO logins VALUES(?,?,?)",
[
(1,"2024-01-01","Online"),
(2,"2024-01-01","Offline"),
(1,"2024-01-01","Offline"),
(3,"2024-01-01","Online"),
(2,"2024-01-01","Offline"),
(1,"2024-01-01","Online"),
(4,"2024-01-01","Offline"),
(1,"2024-01-01","Online"),
(2,"2024-01-01","Offline"),
(3,"2024-01-01","Online")
]
)

# =========================
# IPL MATCH
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS ipl_match(
 TeamA TEXT,
 TeamB TEXT,
 Winer TEXT
)
""")

cur.executemany(
"INSERT INTO ipl_match VALUES(?,?,?)",
[
('Chennai Super Kings', 'Delhi Capitals', 'Chennai Super Kings'),
('Delhi Capitals', 'Gujarat Titans', 'Delhi Capitals'),
('Chennai Super Kings', 'Kolkata Knight Riders', 'Chennai Super Kings'),
('Lucknow Super Giants', 'Delhi Capitals', 'Lucknow Super Giants'),
('Mumbai Indians', 'Punjab Kings', 'Mumbai Indians'),
('Rajasthan Royals', 'Punjab Kings', 'Punjab Kings'),
('Royal Challengers Bengaluru', 'Sunrisers Hyderabad', 'Royal Challengers Bengaluru'),
('Mumbai Indians', 'Sunrisers Hyderabad', 'Mumbai Indians'),
('Mumbai Indians', 'Chennai Super Kings', 'Chennai Super Kings')
]
)

# =========================
# monthly_sales
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS monthly_sales(
 order_id INTEGER,
 order_date TEXT,
 amount TEXT
)
""")

cur.executemany(
"INSERT INTO monthly_sales VALUES(?,?,?)",
[
(1, '2025-01-05', 10000),
(2, '2025-01-20', 15000),
(3, '2025-02-10', 20000),
(4, '2025-02-18', 12000),
(5, '2025-03-05', 18000),
(6, '2025-03-25', 22000),
(7, '2025-04-15', 13000),
(8, '2025-04-22', 16000),
(9, '2025-05-11', 22000),
(10, '2025-05-17', 12400)
]
)

# =========================
# ADDRESSS TABLE
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS products(
 product_id INTEGER,
 product_name TEXT,
 category TEXT
)
""")

cur.executemany(
"INSERT INTO products VALUES(?,?,?)",
[
(101,'Laptop','Electronics'),
(102,'Mobile','Electronics'),
(103,'Headphones','Accessories'),
(104,'Keyboard','Accessories'),
(105,'Mouse','Accessories')
]
)

# =========================
# USERS
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 email TEXT,
 password TEXT,
 score INTEGER DEFAULT 0
)
""")

# =========================
# SUBMISSIONS
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS submissions(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_email TEXT,
 question_id TEXT,
 section TEXT,
 status TEXT,
 submitted_code TEXT,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# QUESTION META
# =========================
cur.execute("""
CREATE TABLE IF NOT EXISTS question_meta(
 qid TEXT,
 difficulty TEXT,
 tags TEXT
)
""")


con.commit()
con.close()

print("SQLite DB Ready")
