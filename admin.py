import streamlit as st
import json

st.title("Admin Panel")

with open("questions/sql_questions.json") as f:
    data=json.load(f)

q = st.text_area("New Question")
if st.button("Add"):
    data.append({"id":str(len(data)+1),"question":q})
    json.dump(data, open("questions/sql_questions.json","w"), indent=2)
