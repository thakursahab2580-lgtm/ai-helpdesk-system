# ===============================
# UniSupport AI Helpdesk System
# ===============================

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import threading
import queue
import time
import uuid
from urllib.parse import urlparse, parse_qs

DB="tickets.db"

JOB_QUEUE=queue.PriorityQueue()

STATUS={}
REQUESTS=0
TOTAL_TIME=0

WORKER_STATUS="IDLE"

PRIORITY_STATS={"HIGH":0,"MEDIUM":0,"LOW":0}

QUEUE_HISTORY=[]

ADMIN_ID="admin"
ADMIN_PASS="admin123"


# ===============================
# AI CLASSIFIER
# ===============================

def classify(text):

    t=text.lower()

    if "login" in t or "password" in t or "portal" in t:
        return "IT",0.92

    if "fee" in t or "payment" in t:
        return "Fees",0.89

    if "exam" in t or "deferral" in t:
        return "Exams",0.91

    if "timetable" in t:
        return "Timetable",0.87

    return "General",0.75


def priority(text):

    t=text.lower()

    if "exam" in t or "deadline" in t:
        return "HIGH"

    if "login" in t or "password" in t:
        return "MEDIUM"

    return "LOW"


def pvalue(p):

    if p=="HIGH":return 0
    if p=="MEDIUM":return 1
    return 2


# ===============================
# DATABASE
# ===============================

def init_db():

    con=sqlite3.connect(DB)
    cur=con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
    ticket_id TEXT,
    student TEXT,
    description TEXT,
    category TEXT,
    priority TEXT,
    confidence REAL,
    created REAL,
    resolved REAL
    )
    """)

    con.commit()
    con.close()


# ===============================
# WORKER
# ===============================

def worker():

    global WORKER_STATUS

    while True:

        prio,t,job=JOB_QUEUE.get()

        tid=job["id"]

        WORKER_STATUS="PROCESSING"

        STATUS[tid]="PROCESSING"

        time.sleep(1)

        con=sqlite3.connect(DB)
        cur=con.cursor()

        cur.execute(
        "UPDATE tickets SET resolved=? WHERE ticket_id=?",
        (time.time(),tid))

        con.commit()
        con.close()

        STATUS[tid]="RESOLVED"

        WORKER_STATUS="IDLE"

        JOB_QUEUE.task_done()


# ===============================
# SERVER
# ===============================

class Server(BaseHTTPRequestHandler):


    def send(self,code,data):

        body=json.dumps(data).encode()

        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()

        self.wfile.write(body)


    # ===========================
    # CREATE TICKET
    # ===========================

    def do_POST(self):

        global REQUESTS,TOTAL_TIME

        if self.path!="/submit":
            return self.send(404,{"error":"not found"})

        start=time.time()

        length=int(self.headers.get("Content-Length",0))
        data=json.loads(self.rfile.read(length))

        student=data["student_id"]
        desc=data["description"]

        cat,conf=classify(desc)

        pr=priority(desc)

        PRIORITY_STATS[pr]+=1

        tid=str(uuid.uuid4())

        con=sqlite3.connect(DB)
        cur=con.cursor()

        cur.execute(
        "INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?)",
        (tid,student,desc,cat,pr,conf,time.time(),None)
        )

        con.commit()
        con.close()

        STATUS[tid]="QUEUED"

        JOB_QUEUE.put((pvalue(pr),time.time(),{"id":tid}))

        QUEUE_HISTORY.append(JOB_QUEUE.qsize())

        if len(QUEUE_HISTORY)>20:
            QUEUE_HISTORY.pop(0)

        rt=time.time()-start

        REQUESTS+=1
        TOTAL_TIME+=rt

        return self.send(200,{
        "ticket_id":tid,
        "category":cat,
        "priority":pr,
        "confidence":conf,
        "status":"QUEUED"
        })


    # ===========================
    # GET ROUTES
    # ===========================

    def do_GET(self):

        url=urlparse(self.path)

        if url.path=="/metrics":

            avg=0
            if REQUESTS:avg=TOTAL_TIME/REQUESTS

            con=sqlite3.connect(DB)
            cur=con.cursor()

            cur.execute(
            "SELECT ticket_id,description,category,priority,confidence FROM tickets ORDER BY created DESC LIMIT 10"
            )

            rows=cur.fetchall()

            con.close()

            return self.send(200,{
            "req":REQUESTS,
            "avg":round(avg,4),
            "queue":JOB_QUEUE.qsize(),
            "worker":WORKER_STATUS,
            "queue_hist":QUEUE_HISTORY,
            "priority":PRIORITY_STATS,
            "tickets":rows
            })


        if url.path=="/portal":
            return self.html(PORTAL)

        if url.path=="/admin":
            return self.html(ADMIN_LOGIN)

        if url.path=="/dashboard":
            return self.html(DASHBOARD)

        return self.send(404,{"error":"not found"})


    def html(self,html):

        b=html.encode()

        self.send_response(200)
        self.send_header("Content-Type","text/html")
        self.send_header("Content-Length",str(len(b)))
        self.end_headers()

        self.wfile.write(b)


    def log_message(self, format, *args):
        return


# ===============================
# CLIENT PORTAL UI
# ===============================

PORTAL="""
<!DOCTYPE html>
<html>
<head>

<title>UniSupport AI Helpdesk</title>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(120deg,#2a5298,#6dd5fa);
height:100vh;
display:flex;
align-items:center;
justify-content:center;
margin:0;
}

.box{
background:white;
padding:40px;
width:420px;
border-radius:12px;
box-shadow:0 10px 30px rgba(0,0,0,0.2);
text-align:center;
}

input,textarea{
width:100%;
padding:12px;
margin-top:10px;
border-radius:6px;
border:1px solid #ccc;
}

button{
margin-top:15px;
padding:12px;
width:100%;
background:#2a5298;
color:white;
border:none;
border-radius:6px;
cursor:pointer;
}

.popup{
position:fixed;
top:20px;
right:20px;
background:#2ecc71;
color:white;
padding:12px 20px;
border-radius:6px;
display:none;
}

</style>
</head>

<body>

<div class="box">

<h2>Submit Support Ticket</h2>

<input id="sid" placeholder="Student ID">

<textarea id="desc" placeholder="Describe your issue"></textarea>

<button onclick="send()">Submit</button>

<p id="result"></p>

</div>

<div class="popup" id="pop">✔ Ticket Submitted</div>

<script>

async function send(){

const r=await fetch("/submit",{

method:"POST",

headers:{"Content-Type":"application/json"},

body:JSON.stringify({
student_id:document.getElementById("sid").value,
description:document.getElementById("desc").value
})

})

const d=await r.json()

document.getElementById("result").innerHTML=
"Ticket ID: "+d.ticket_id+
"<br>Category: "+d.category+
"<br>Priority: "+d.priority+
"<br>Confidence: "+d.confidence

document.getElementById("sid").value=""
document.getElementById("desc").value=""

const p=document.getElementById("pop")

p.style.display="block"

setTimeout(()=>p.style.display="none",2000)

}

</script>

</body>
</html>
"""


# ===============================
# ADMIN LOGIN
# ===============================

ADMIN_LOGIN="""
<!DOCTYPE html>
<html>

<head>
<title>Admin Login</title>

<style>

body{
background:#2a5298;
display:flex;
align-items:center;
justify-content:center;
height:100vh;
font-family:Segoe UI;
}

.box{
background:white;
padding:40px;
border-radius:10px;
width:300px;
text-align:center;
}

input{
width:100%;
padding:10px;
margin-top:10px;
}

button{
margin-top:15px;
padding:10px;
width:100%;
background:#2a5298;
color:white;
border:none;
}

</style>

</head>

<body>

<div class="box">

<h2>Admin Login</h2>

<input id="id" placeholder="Admin ID">
<input id="pw" type="password" placeholder="Password">

<button onclick="login()">Login</button>

<p id="msg"></p>

</div>

<script>

function login(){

const id=document.getElementById("id").value
const pw=document.getElementById("pw").value

if(id=="admin" && pw=="admin123"){

window.location="/dashboard"

}else{

document.getElementById("msg").innerText="Invalid login"

}

}

</script>

</body>
</html>
"""


# ===============================
# ADMIN DASHBOARD
# ===============================

DASHBOARD = """
<!DOCTYPE html>
<html>

<head>

<title>UniSupport Admin Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family:Segoe UI;
background:#f1f4f9;
margin:0;
}

.header{
background:#1f3c88;
color:white;
padding:18px;
font-size:22px;
text-align:center;
font-weight:600;
}

.container{
width:92%;
margin:auto;
margin-top:30px;
}

.cards{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:20px;
margin-bottom:25px;
}

.card{
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
text-align:center;
}

.card h3{
margin:0;
font-size:14px;
color:#666;
}

.card p{
margin-top:8px;
font-size:22px;
font-weight:600;
}

.charts{
display:grid;
grid-template-columns:1fr 1fr;
gap:25px;
}

.chart-box{
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

canvas{
height:250px !important;
}

table{
width:100%;
margin-top:30px;
border-collapse:collapse;
background:white;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
border-radius:10px;
overflow:hidden;
}

th{
background:#1f3c88;
color:white;
padding:12px;
font-size:14px;
}

td{
padding:10px;
border-bottom:1px solid #eee;
font-size:13px;
}

tbody{
display:block;
max-height:220px;
overflow-y:auto;
}

thead, tbody tr{
display:table;
width:100%;
table-layout:fixed;
}

.priority-high{
color:red;
font-weight:600;
}

.priority-medium{
color:orange;
font-weight:600;
}

.priority-low{
color:green;
font-weight:600;
}

</style>

</head>

<body>

<div class="header">UniSupport AI Helpdesk Dashboard</div>

<div class="container">

<div class="cards">

<div class="card">
<h3>Total Requests</h3>
<p id="req">0</p>
</div>

<div class="card">
<h3>Queue Size</h3>
<p id="queue">0</p>
</div>

<div class="card">
<h3>Avg Response</h3>
<p id="avg">0</p>
</div>

<div class="card">
<h3>Worker Status</h3>
<p id="worker">IDLE</p>
</div>

</div>


<div class="charts">

<div class="chart-box">
<h3>Queue Activity</h3>
<canvas id="queueChart"></canvas>
</div>

<div class="chart-box">
<h3>Priority Distribution</h3>
<canvas id="priorityChart"></canvas>
</div>

</div>


<table>

<thead>
<tr>
<th>Ticket ID</th>
<th>Description</th>
<th>Category</th>
<th>Priority</th>
<th>Confidence</th>
</tr>
</thead>

<tbody id="tickets"></tbody>

</table>

</div>

<script>

const queueChart = new Chart(
document.getElementById("queueChart"),
{
type:"line",
data:{
labels:[],
datasets:[{
label:"Queue Size",
data:[],
borderColor:"#1f3c88",
fill:false,
tension:0.3
}]
},
options:{responsive:true}
})

const priorityChart = new Chart(
document.getElementById("priorityChart"),
{
type:"doughnut",
data:{
labels:["HIGH","MEDIUM","LOW"],
datasets:[{
data:[0,0,0],
backgroundColor:["#e74c3c","#f39c12","#2ecc71"]
}]
}
})

async function update(){

const r = await fetch("/metrics")
const d = await r.json()

document.getElementById("req").innerText = d.req
document.getElementById("queue").innerText = d.queue
document.getElementById("avg").innerText = d.avg
document.getElementById("worker").innerText = d.worker


queueChart.data.labels = d.queue_hist.map((_,i)=>i)
queueChart.data.datasets[0].data = d.queue_hist
queueChart.update()

priorityChart.data.datasets[0].data=[
d.priority.HIGH,
d.priority.MEDIUM,
d.priority.LOW
]

priorityChart.update()

let rows=""

d.tickets.forEach(t=>{

let pclass="priority-low"

if(t[3]=="HIGH") pclass="priority-high"
if(t[3]=="MEDIUM") pclass="priority-medium"

rows+=`
<tr>
<td>${t[0]}</td>
<td>${t[1]}</td>
<td>${t[2]}</td>
<td class="${pclass}">${t[3]}</td>
<td>${t[4]}</td>
</tr>
`

})

document.getElementById("tickets").innerHTML=rows

}

setInterval(update,1000)
update()

</script>

</body>
</html>
"""


# ===============================
# MAIN
# ===============================

def main():

    init_db()

    t=threading.Thread(target=worker,daemon=True)
    t.start()

    server=HTTPServer(("127.0.0.1",8000),Server)

    print("\\nUniSupport AI Helpdesk Running")
    print("Client Portal: http://127.0.0.1:8000/portal")
    print("Admin Login: http://127.0.0.1:8000/admin")

    server.serve_forever()


if __name__=="__main__":
    main()