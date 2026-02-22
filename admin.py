import streamlit as st
import json
import sqlite3

st.title("Admin Panel")

with open("questions/sql_questions.json") as f:
    data=json.load(f)

q = st.text_area("New Question")
if st.button("Add"):
    data.append({"id":str(len(data)+1),"question":q})
    json.dump(data, open("questions/sql_questions.json","w"), indent=2)

difficulty = st.selectbox("Difficulty",["easy","medium","hard"])
tags = st.text_input("tags comma")

if st.button("Add"):
    data.append({"id":str(len(data)+1),"question":q})
    json.dump(data, open("questions/sql_questions.json","w"), indent=2)

    con = sqlite3.connect("practice.db")
    cur = con.cursor()
    cur.execute("INSERT INTO question_meta VALUES(?,?,?)",(str(len(data)),difficulty,tags))
    con.commit()