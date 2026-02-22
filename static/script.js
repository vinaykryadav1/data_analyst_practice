// ================= GLOBAL =================
let currentQ = "";
let pyCurrentQ = null;
let powerbiCurrentQ = null;

function loadQ(id, question){
  powerbiCurrentQ = id;

  document.getElementById("qtext").innerText = question;
  document.getElementById("answerText").innerText = "";
}

function revealPowerBI(){

  if(!powerbiCurrentQ){
    alert("Select question first");
    return;
  }

  fetch("/solution/powerbi/" + powerbiCurrentQ)
  .then(r => r.json())
  .then(d => {
    const box = document.getElementById("answerText");
    if(box){
      box.innerText = d.answer || "No answer available";
    }
  })
  .catch(()=>{
    alert("Failed to fetch answer");
  });
}
// ================= PAGE LOAD =================
document.addEventListener("DOMContentLoaded", function () {
  initSQLMonaco();
  initPythonMonaco();
  initTables();
  initCSVUpload();
});


// ================= SQL MONACO =================
function initSQLMonaco() {
  const el = document.getElementById("editor");
  if (!el) return;

  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs" }
  });

  require(["vs/editor/editor.main"], function () {
    window.editor = monaco.editor.create(el, {
      value: "SELECT * FROM employees LIMIT 10;",
      language: "sql",
      theme: "vs-dark",
      automaticLayout: true,
      minimap: { enabled: false }
    });
  });
}


// ================= PYTHON MONACO =================
function initPythonMonaco() {
  const el = document.getElementById("pyEditor");
  if (!el) return;

  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs" }
  });

  require(["vs/editor/editor.main"], function () {
    window.pyEditor = monaco.editor.create(el, {
      value: '# Python\nprint("Hello Vinay 🚀")',
      language: "python",
      theme: "vs-dark",
      automaticLayout: true,
      minimap: { enabled: false }
    });
  });
}


// ================= RUN SQL =================
function runSQL() {
  if (!window.editor) return;

  const query = window.editor.getValue();
  const out = document.getElementById("output");
  if (!out) return;

  out.innerHTML = "Running...";

  fetch("/run_sql", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  })
    .then(r => r.json())
    .then(res => {

      if (res.error) {
        out.innerHTML = "<pre>" + res.error + "</pre>";
        return;
      }

      let table = "<table class='result-table'><thead><tr>";
      res.cols.forEach(c => table += "<th>" + c + "</th>");
      table += "</tr></thead><tbody>";

      res.data.forEach(row => {
        table += "<tr>";
        row.forEach(v => {
          table += "<td>" + (v === null ? "NULL" : v) + "</td>";
        });
        table += "</tr>";
      });

      table += "</tbody></table>";
      out.innerHTML = table;
    });
}

// ================= REVEAL SQL =================
function reveal(){
  if(!currentQ){
    alert("Select question first");
    return;
  }

  fetch("/solution/sql/" + currentQ)
    .then(r => r.json())
    .then(d => {
      const box = document.getElementById("answerBox");
      if(!box) return;

      box.innerText = d.answer || "No answer available";
    })
    .catch(()=>{
      alert("Failed to fetch solution");
    });
}

// ================= RUN PYTHON =================
function runPython() {
  if (!window.pyEditor) return;

  const code = window.pyEditor.getValue();
  const out = document.getElementById("pyOutput");
  if (!out) return;

  out.innerText = "Running...";

  fetch("/run_python", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code })
  })
    .then(r => r.json())
    .then(res => {
      out.innerText = (res.output || "") + (res.error || "");
    });
}


// ================= QUESTION SELECT =================
function selectQuestion(el) {
  currentQ = el.getAttribute("data-qid");
  const txt = el.querySelector(".qtext")?.innerText || "";
  const qtext = document.getElementById("qtext");
  if (qtext) qtext.innerText = txt;
}

function selectPyQuestionFromList(el) {
  pyCurrentQ = el.getAttribute("data-qid");
  const txt = el.querySelector(".qtext")?.innerText || "";
  document.getElementById("pyQTitle").innerText = txt;
  document.getElementById("pyAnswer").innerText = "";
  document.getElementById("pyOutput").innerText = "";
}
window.selectPyQuestionFromList = selectPyQuestionFromList;


// ================= REVEAL PYTHON =================
function revealPython() {
  if (!pyCurrentQ) return alert("Select question first");

  fetch("/solution/python/" + pyCurrentQ)
    .then(r => r.json())
    .then(d => {
      document.getElementById("pyAnswer").innerText =
        d.answer || "No answer";
    });
}



// ================= DOWNLOAD =================
function downloadOutput() {
  const out = document.getElementById("output");
  if (!out) return;

  const blob = new Blob([out.innerText], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "sql_output.txt";
  a.click();
}

function downloadPyOutput() {
  const out = document.getElementById("pyOutput");
  if (!out) return;

  const blob = new Blob([out.innerText], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "python_output.txt";
  a.click();
}


// ================= CSV UPLOAD =================
function initCSVUpload() {

  // SQL
  const sqlDrop = document.getElementById("dropArea");
  const sqlInput = document.getElementById("csvFile");

  if (sqlDrop && sqlInput) {
    sqlDrop.addEventListener("click", () => sqlInput.click());
    sqlInput.addEventListener("change", () => uploadFile(sqlInput.files[0]));
  }

  // Python
  const pyDrop = document.getElementById("dropAreaPy");
  const pyInput = document.getElementById("csvFilePy");

  if (pyDrop && pyInput) {
    pyDrop.addEventListener("click", () => pyInput.click());
    pyInput.addEventListener("change", () => uploadFile(pyInput.files[0]));
  }
}

function uploadFile(file) {
  if (!file) return;

  const fd = new FormData();
  fd.append("file", file);

  fetch("/upload_csv", { method: "POST", body: fd })
    .then(r => r.json())
    .then(d => {
      alert(d.msg || "Uploaded");
      setTimeout(() => location.reload(), 500);
    })
    .catch(() => alert("Upload failed"));
}


// ================= SQL TABLES =================
function initTables() {
  fetch("/get_tables")
    .then(r => r.json())
    .then(list => {
      const dd = document.getElementById("tablesDropdown");
      if (!dd) return;

      dd.innerHTML = '<option value="">-- Select table --</option>';
      list.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.innerText = t;
        dd.appendChild(opt);
      });

      dd.addEventListener("change", e => {
        if (window.editor)
          window.editor.setValue(`SELECT * FROM ${e.target.value} LIMIT 20;`);
      });
    });
}

function clearPyOutput(){
  const out = document.getElementById("pyOutput");
  if(out) out.innerText = "";
}
function clearPyAnswer(){
  const el = document.getElementById("pyAnswer");
  if(el) el.innerText = "";
}

function clearPowerBIAnswer(){
  const el = document.getElementById("powerbiUserAnswer");
  if(el) el.value = "";
}

// ---------- SQL CLEAN ----------
function clearAnswerBox(){
  const box = document.getElementById("answerBox");
  if(box) box.innerText = "";
}
function copyPyAnswer(){
  const el = document.getElementById("pyAnswer");
  if(!el) return;

  navigator.clipboard.writeText(el.innerText || "");
  alert("Copied");
}

// ---------- SQL COPY ----------
function copyAnswer(){
  const box = document.getElementById("answerBox");
  if(!box) return;

  navigator.clipboard.writeText(box.innerText || "");
  alert("Copied");
}
function toggleOutputExpand(){

  // SQL expand
  const sqlPanel = document.querySelector(".bottom-panel");

  if(sqlPanel){
    sqlPanel.classList.toggle("expanded");
    return;
  }

  // Python expand
  const pyOutput = document.getElementById("pyOutput");

  if(pyOutput){
    pyOutput.classList.toggle("py-expanded");
  }
}
function loadQ(id, question){
  powerbiCurrentQ = id;

  document.getElementById("qtext").innerText = question;
  document.getElementById("answerText").innerText = "";
  document.getElementById("powerbiUserAnswer").value = "";
}

// function revealAns(id){
//   fetch("/solution/interview/" + id)
//   .then(r=>r.json())
//   .then(d=>{
//     document.getElementById("ans-"+id).innerText =
//       "Answer: " + (d.answer || "No answer found");
//   })
//   .catch(()=> alert("Error loading answer"));
// }
function resetInterview(){

  // stop timer
  clearInterval(interviewTimer);
  started = false;

  // reset time
  interviewSeconds = 1800;
  document.getElementById("int-timer").innerText = "30:00";

  // start button text reset
  document.getElementById("startBtn").innerText = "Start";

  // disable open + reveal buttons
  document.querySelectorAll(".open-btn").forEach(b=>b.disabled=true);
  document.querySelectorAll(".reveal-btn").forEach(b=>b.disabled=true);

  // clear and close all textareas
  document.querySelectorAll(".ans-input").forEach(t=>{
    t.value = "";
    t.parentElement.style.display = "none";
  });

  // clear revealed answers
  document.querySelectorAll("[id^='ans-']").forEach(p=>{
    p.innerText = "";
  });
}
let interviewSeconds = 1800;
let interviewTimer = null;
let started = false;

// START / STOP
function toggleInterview(){
  const btn = document.getElementById("startBtn");

  if(!started){
    started = true;
    btn.innerText = "Stop";
    startTimer();
    enableButtons();
  }else{
    started = false;
    btn.innerText = "Start";
    stopTimer();
  }
}

// TIMER
function startTimer(){
  interviewTimer = setInterval(()=>{
    interviewSeconds--;

    const mm = Math.floor(interviewSeconds/60).toString().padStart(2,'0');
    const ss = (interviewSeconds%60).toString().padStart(2,'0');

    document.getElementById("int-timer").innerText = mm+":"+ss;

    if(interviewSeconds<=0){
      clearInterval(interviewTimer);
      alert("Time up");
    }
  },1000);
}

function stopTimer(){
  clearInterval(interviewTimer);
  interviewSeconds = 1800;
  document.getElementById("int-timer").innerText = "30:00";
}


// ENABLE OPEN + REVEAL
function enableButtons(){
  document.querySelectorAll(".open-btn").forEach(b=>b.disabled=false);
  document.querySelectorAll(".reveal-btn").forEach(b=>b.disabled=false);
}

// OPEN TEXTAREA
function openQuestion(id){
  document.getElementById("area-"+id).style.display="block";
}

// REVEAL ANSWER
// let interviewAnswers = [];

// fetch("/questions/interview_answers.json")
//   .then(r=>r.json())
//   .then(data=> interviewAnswers = data);

// function revealAns(id){
//   const found = interviewAnswers.find(q => q.id === id);
//   document.getElementById("ans-"+id).innerText =
//     "Answer: " + (found ? found.answer : "No answer found");
// }
function revealAns(id){
  fetch("/solution/interview/" + id)
  .then(r=>r.json())
  .then(d=>{
    document.getElementById("ans-"+id).innerText =
      "Answer: " + (d.answer || "No answer found");
  })
  .catch(()=> alert("Reveal error"));
}

// SUBMIT → TXT DOWNLOAD
function submitInterview(){

  let text = "Interview Answers\n\n";

  document.querySelectorAll(".ans-input").forEach((ta, index)=>{

    const qCard = ta.closest(".panel-card");

    // FULL question text (Q number + question)
    const fullQuestion = qCard.querySelector("div strong").parentElement.innerText.trim();

    const userAnswer = ta.value.trim() || "No answer given";

    text += fullQuestion + "\n";
    text += "Your Answer: " + userAnswer + "\n\n";
  });

  const blob = new Blob([text], {type:"text/plain"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "interview_answers.txt";
  a.click();
}
// ================= DIFFICULTY FILTER =================
document.addEventListener("DOMContentLoaded", function(){

  // SQL filter
  const sqlFilter = document.getElementById("filterDifficulty");
  if(sqlFilter){
    sqlFilter.addEventListener("change", function(){
      const val = this.value;
      document.querySelectorAll("#questionsList .qitem").forEach(item=>{
        const diff = item.getAttribute("data-difficulty");
        item.style.display = (val==="all" || diff===val) ? "block" : "none";
      });
    });
  }

  // Python filter
  const pyFilter = document.getElementById("pyFilterDifficulty");
  if(pyFilter){
    pyFilter.addEventListener("change", function(){
      const val = this.value;
      document.querySelectorAll("#pyList .qitem").forEach(item=>{
        const diff = item.getAttribute("data-difficulty");
        item.style.display = (val==="all" || diff===val) ? "block" : "none";
      });
    });
  }

});