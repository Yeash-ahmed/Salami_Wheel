import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="🎡 Salami Wheel - Eid Special",
    page_icon="🎡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

NAMES_FILE = "spun_names.txt"

def load_all_records():
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_name(name, amount):
    with open(NAMES_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{name} | {amount} | {timestamp}\n")

def get_spun_names():
    names = []
    for record in load_all_records():
        parts = record.split("|")
        if parts:
            names.append(parts[0].strip().lower())
    return names

# Handle save
params = st.query_params
if "save_name" in params and "save_amount" in params:
    n = params["save_name"].strip()
    a = params["save_amount"].strip()
    existing = get_spun_names()
    if n.lower() not in existing:
        save_name(n, a)
    st.query_params.clear()
    st.rerun()

spun_names = get_spun_names()
spun_json = json.dumps(spun_names)

# Clean Streamlit UI
st.markdown("""
<style>
html, body, .stApp {
    background: #0d0120 !important;
}
.main .block-container { padding: 0 !important; }
header, footer, #MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
    background: radial-gradient(#2d0a5e, #0d0120);
    font-family: sans-serif;
    text-align: center;
    color: white;
}}

canvas {{
    width: 90vw;
    max-width: 420px;
    border-radius: 50%;
    will-change: transform;
}}

button {{
    margin-top: 15px;
    padding: 12px 25px;
    font-size: 18px;
    border-radius: 30px;
    border: none;
    background: gold;
    font-weight: bold;
}}

</style>
</head>
<body>

<h2>🎡 Salami Wheel</h2>

<input id="nameInput" placeholder="Enter name" style="padding:10px;border-radius:20px;border:none;width:70%">
<br><br>

<button onclick="confirmName()">Confirm</button>
<br>
<button id="spinBtn" onclick="spin()" disabled>SPIN</button>

<br><br>
<canvas id="wheel"></canvas>

<script>
const SPUN = {spun_json};

const SEG = ["1","2","3","4","5","6","7","8","9","10","500"];
const FORBIDDEN = SEG.length - 1;

let name = "";
let angle = 0;
let spinning = false;

const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");

const SIZE = Math.min(window.innerWidth * 0.9, 420);
canvas.width = canvas.height = SIZE;

const cx = SIZE/2;
const r = SIZE/2 - 5;
const arc = 2*Math.PI / SEG.length;

function draw(a) {{
    ctx.clearRect(0,0,SIZE,SIZE);

    for(let i=0;i<SEG.length;i++) {{
        let s = a + i*arc;
        let e = s + arc;

        ctx.beginPath();
        ctx.moveTo(cx,cx);
        ctx.arc(cx,cx,r,s,e);
        ctx.fillStyle = i%2?"#ff6b35":"#2ecc71";
        ctx.fill();

        ctx.save();
        ctx.translate(cx,cx);
        ctx.rotate(s + arc/2);
        ctx.fillStyle="white";
        ctx.font="bold 14px sans-serif";
        ctx.fillText(SEG[i], r-10, 0);
        ctx.restore();
    }}
}}

draw(angle);

function confirmName() {{
    const n = document.getElementById("nameInput").value.trim();
    if(!n) return;

    if(SPUN.includes(n.toLowerCase())) {{
        alert("Already spun!");
        return;
    }}

    name = n;
    document.getElementById("spinBtn").disabled = false;
}}

function spin() {{
    if(spinning) return;
    spinning = true;

    let winner;
    do {{
        winner = Math.floor(Math.random()*SEG.length);
    }} while(winner === FORBIDDEN);

    let target = -(winner*arc + arc/2);
    let start = angle;
    let total = 8*Math.PI + target;

    let duration = 3500;
    let startTime = performance.now();

    function animate(t) {{
        let p = Math.min((t-startTime)/duration,1);
        let eased = 1 - Math.pow(1-p,4);

        angle = start + total*eased;
        draw(angle);

        if(p<1) requestAnimationFrame(animate);
        else {{
            spinning = false;
            showResult(winner);
        }}
    }}

    requestAnimationFrame(animate);
}}

function showResult(i) {{
    alert(name + " got " + SEG[i] + " Taka");

    const url = new URL(window.parent.location.href);
    url.searchParams.set("save_name", name);
    url.searchParams.set("save_amount", SEG[i]);
    window.parent.location.href = url.toString();
}}
</script>

</body>
</html>
"""

components.html(html, height=700)
