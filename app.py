import streamlit as st
import streamlit.components.v1 as components
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="🎡 Salami Wheel - Eid Special",
    page_icon="🎡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

NAMES_FILE = "spun_names.txt"

def load_spun_names():
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_name(name, amount):
    with open(NAMES_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{name} | {amount} | {timestamp}\n")

def get_spun_names_only():
    names = []
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.strip():
                    parts = line.strip().split("|")
                    if parts:
                        names.append(parts[0].strip().lower())
    return names

if "spin_result" not in st.session_state:
    st.session_state.spin_result = None

spun_names = get_spun_names_only()
spun_names_json = json.dumps(spun_names)

params = st.query_params
if "result_name" in params and "result_amount" in params:
    name = params["result_name"]
    amount = params["result_amount"]
    if name.lower() not in spun_names:
        save_name(name, amount)
        st.session_state.spin_result = f"{name} got {amount} Taka!"
    st.query_params.clear()
    st.rerun()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800;900&family=Nunito:wght@600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: radial-gradient(ellipse at top, #2d0a5e 0%, #1a0333 50%, #0d0120 100%) !important;
    font-family: 'Nunito', sans-serif !important;
    min-height: 100vh;
}

.main .block-container {
    padding: 1.5rem 1rem !important;
    max-width: 700px !important;
    margin: 0 auto !important;
}

section[data-testid="stSidebar"] { display: none !important; }

h1, h2, h3 { font-family: 'Baloo 2', cursive !important; }

/* Header */
.site-header {
    text-align: center;
    margin-bottom: 1.2rem;
    padding: 1.2rem 1rem;
    background: linear-gradient(135deg, rgba(255,107,53,0.15), rgba(255,215,0,0.08));
    border: 2px solid rgba(255,215,0,0.25);
    border-radius: 24px;
    backdrop-filter: blur(10px);
}
.site-header h1 {
    font-size: clamp(1.8rem, 6vw, 2.8rem) !important;
    color: #ffd700 !important;
    text-shadow: 0 0 30px rgba(255,215,0,0.6), 0 2px 8px rgba(0,0,0,0.5);
    margin: 0 !important;
    letter-spacing: 2px;
}
.site-header p {
    color: rgba(255,255,255,0.85) !important;
    font-size: clamp(0.9rem, 3vw, 1.1rem) !important;
    margin: 0.4rem 0 0 !important;
}

/* Name input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 2.5px solid rgba(255,215,0,0.4) !important;
    border-radius: 60px !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.5rem !important;
    text-align: center !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ffd700 !important;
    box-shadow: 0 0 20px rgba(255,215,0,0.3) !important;
    background: rgba(255,255,255,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.45) !important; }
.stTextInput label { display: none !important; }

/* Banners */
.already-spun {
    background: linear-gradient(135deg, rgba(255,50,50,0.2), rgba(200,0,0,0.15));
    border: 2px solid rgba(255,80,80,0.6);
    border-radius: 16px;
    padding: 0.9rem 1.2rem;
    text-align: center;
    color: #ff9090;
    font-weight: 800;
    font-size: 1rem;
    margin: 0.5rem 0;
}
.result-banner {
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    border-radius: 20px;
    padding: 1rem 1.5rem;
    text-align: center;
    margin: 0.7rem 0;
    box-shadow: 0 6px 30px rgba(255,215,0,0.5);
    animation: bannerPop 0.5s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes bannerPop {
    from { transform: scale(0.8); opacity: 0; }
    to   { transform: scale(1);   opacity: 1; }
}
.result-banner h2 {
    color: #1a0333 !important;
    margin: 0 !important;
    font-size: clamp(1rem, 4vw, 1.4rem) !important;
}

/* History & admin */
.history-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1rem;
}
.history-title {
    color: #ffd700;
    font-family: 'Baloo 2', cursive;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}
.history-item {
    color: rgba(255,255,255,0.75);
    font-size: 0.85rem;
    padding: 0.35rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.stExpander {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
}
.stExpander summary { color: rgba(255,255,255,0.8) !important; }

hr { border-color: rgba(255,255,255,0.1) !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="site-header">
    <h1>🎡 Salami Wheel 🎉</h1>
    <p>Pick your Eid Salami!! &nbsp;🤩&nbsp; Each person spins once!</p>
</div>
""", unsafe_allow_html=True)

name_input = st.text_input("name", placeholder="✍️  Enter your name to spin…",
                            key="name_field", label_visibility="collapsed")

already_spun = name_input.strip().lower() in spun_names if name_input.strip() else False

if already_spun:
    st.markdown(f'<div class="already-spun">❌ &nbsp;<b>{name_input.strip()}</b>&nbsp; has already spun! Each person gets one chance only. 🚫</div>',
                unsafe_allow_html=True)

if st.session_state.spin_result:
    st.markdown(f'<div class="result-banner"><h2>🎊 {st.session_state.spin_result} 🎊</h2></div>',
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# WHEEL HTML  –  canvas 560 px, text 13-14 px bold, thick borders, glow ring
# ─────────────────────────────────────────────────────────────────────────────
wheel_html = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&family=Nunito:wght@700;800&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{
    background: transparent;
    overflow: hidden;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.scene {{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 0 16px;
}}

/* Outer decorative ring around the whole wheel assembly */
.wheel-wrap {{
    position: relative;
    width: min(560px, 96vw);
    height: min(560px, 96vw);
}}

/* Golden outer ring */
.wheel-wrap::before {{
    content: '';
    position: absolute;
    inset: -8px;
    border-radius: 50%;
    background: conic-gradient(#ffd700, #ff6b35, #ffd700, #2ecc71, #ffd700, #3498db, #ffd700);
    z-index: 0;
    animation: ringRotate 8s linear infinite;
    opacity: 0.7;
}}
@keyframes ringRotate {{ to {{ transform: rotate(360deg); }} }}

.wheel-wrap::after {{
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    background: radial-gradient(ellipse, #1a0333 60%, transparent 100%);
    z-index: 0;
}}

canvas {{
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    display: block;
    filter: drop-shadow(0 0 24px rgba(255,215,0,0.55)) drop-shadow(0 0 48px rgba(255,107,53,0.35));
}}

/* Pointer – bigger & more visible */
.pointer {{
    position: absolute;
    right: -26px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 0;
}}
.pointer-arrow {{
    width: 0; height: 0;
    border-top: 26px solid transparent;
    border-bottom: 26px solid transparent;
    border-right: 50px solid #ffd700;
    filter: drop-shadow(0 0 12px rgba(255,215,0,0.9)) drop-shadow(0 0 4px #000);
}}
.pointer-knob {{
    width: 20px; height: 20px;
    background: radial-gradient(circle, #fff 30%, #ffd700 100%);
    border-radius: 50%;
    box-shadow: 0 0 12px #ffd700, 0 0 4px #000;
    margin-left: -6px;
    z-index: 2;
}}

/* Spin button */
.spin-btn {{
    margin: 18px auto 0;
    display: block;
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ffd700 100%);
    color: #1a0333;
    border: none;
    border-radius: 60px;
    font-family: 'Baloo 2', cursive;
    font-size: clamp(1.1rem, 4vw, 1.45rem);
    font-weight: 900;
    padding: 14px 0;
    cursor: pointer;
    letter-spacing: 2px;
    width: min(440px, 88vw);
    box-shadow: 0 6px 30px rgba(255,107,53,0.55), 0 2px 0 rgba(0,0,0,0.3) inset;
    transition: transform 0.15s, box-shadow 0.15s;
    text-transform: uppercase;
    position: relative;
    overflow: hidden;
}}
.spin-btn::after {{
    content: '';
    position: absolute;
    top: 0; left: -60%;
    width: 40%; height: 100%;
    background: rgba(255,255,255,0.25);
    transform: skewX(-20deg);
    transition: left 0.4s;
}}
.spin-btn:hover:not(:disabled)::after {{ left: 120%; }}
.spin-btn:hover:not(:disabled) {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 40px rgba(255,107,53,0.75);
}}
.spin-btn:active:not(:disabled) {{ transform: scale(0.97); }}
.spin-btn:disabled {{
    background: linear-gradient(135deg, #555, #777);
    color: #aaa;
    cursor: not-allowed;
    box-shadow: none;
}}

/* Result overlay */
.overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.88);
    z-index: 200;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.25s ease;
}}
.overlay.show {{ display: flex; }}
@keyframes fadeIn {{ from {{ opacity:0 }} to {{ opacity:1 }} }}

.result-card {{
    background: linear-gradient(160deg, #1a0533 0%, #2d1155 100%);
    border: 3px solid #ffd700;
    border-radius: 28px;
    padding: 2.2rem 2.4rem;
    text-align: center;
    max-width: 340px;
    width: 90vw;
    box-shadow: 0 0 80px rgba(255,215,0,0.45), 0 0 160px rgba(255,107,53,0.25);
    animation: cardPop 0.45s cubic-bezier(0.34,1.56,0.64,1);
}}
@keyframes cardPop {{
    from {{ transform: scale(0.4) rotate(-6deg); opacity:0; }}
    to   {{ transform: scale(1)   rotate(0deg);  opacity:1; }}
}}
.rc-emoji  {{ font-size: 3.5rem; line-height: 1; margin-bottom: 0.4rem; }}
.rc-name   {{ color: #ffd700; font-family:'Baloo 2',cursive; font-size: 1.6rem; font-weight:900; }}
.rc-label  {{ color: rgba(255,255,255,0.55); font-size: 0.9rem; margin: 0.3rem 0; }}
.rc-amount {{
    color: #fff;
    font-family: 'Baloo 2', cursive;
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.1;
    text-shadow: 0 0 30px rgba(255,215,0,0.8);
}}
.rc-taka {{ color: #ffd700; font-size: 1.4rem; vertical-align: super; }}
.rc-close {{
    margin-top: 1.4rem;
    background: linear-gradient(135deg, #ff6b35, #ffd700);
    color: #1a0333;
    border: none;
    border-radius: 50px;
    padding: 11px 36px;
    font-family: 'Baloo 2', cursive;
    font-size: 1.05rem;
    font-weight: 900;
    cursor: pointer;
    letter-spacing: 1px;
    box-shadow: 0 4px 20px rgba(255,107,53,0.5);
}}

.confetti-layer {{
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 199;
    overflow: hidden;
}}
</style>
</head>
<body>
<div class="scene">
  <div class="wheel-wrap">
    <canvas id="wc"></canvas>
    <div class="pointer">
      <div class="pointer-arrow"></div>
      <div class="pointer-knob"></div>
    </div>
  </div>
  <button class="spin-btn" id="spinBtn" onclick="startSpin()">🎰 &nbsp;SPIN!</button>
</div>

<div class="confetti-layer" id="confettiLayer"></div>

<div class="overlay" id="overlay">
  <div class="result-card">
    <div class="rc-emoji">🎊</div>
    <div class="rc-name" id="rcName"></div>
    <div class="rc-label">gets</div>
    <div class="rc-amount"><span class="rc-taka"></span><span id="rcAmount"></span> <span style="font-size:1.4rem;color:#ffd700">Taka</span></div>
    <div class="rc-label" style="margin-top:.4rem">Eid Salami! 💚</div>
    <button class="rc-close" onclick="closeResult()">Awesome! 🎉</button>
  </div>
</div>

<script>
/* ── data ─────────────────────────────────────────────────── */
const spunNames   = {spun_names_json};
const currentName = `{name_input.strip().replace('`','').replace(chr(10),'').replace(chr(13),'')}`.trim();
const alreadySpun = spunNames.includes(currentName.toLowerCase());

const segments = [
  "1","9.75","7.50","9.50","4.75",
  "5","2.50","7","1.50","1.25",
  "5.25","6.75","4.25","6","2.25",
  "7.75","8.25","2","1.25","4",
  "9.25","5.50","10","3","3.50",
  "9","6.50","5.75","3.25","3.75",
  "8","2.75","8.75","1.75","4.50",
  "6.25","8.50","500"
];

const FORBIDDEN = segments.length - 1;   // 500-Taka index never lands

const PALETTE = [
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#e74c3c","#2ecc71","#3498db","#f39c12",
  "#9b59b6","#1abc9c","#e67e22"
];

/* ── canvas setup ─────────────────────────────────────────── */
const canvas = document.getElementById('wc');
const ctx    = canvas.getContext('2d');
const SIZE   = 560;
canvas.width  = SIZE;
canvas.height = SIZE;

const CX  = SIZE / 2;
const CY  = SIZE / 2;
const R   = SIZE / 2 - 6;
const arc = (2 * Math.PI) / segments.length;

let angle = 0, spinning = false;

/* ── draw ─────────────────────────────────────────────────── */
function draw(a) {{
    ctx.clearRect(0, 0, SIZE, SIZE);

    /* outer dark border */
    ctx.beginPath();
    ctx.arc(CX, CY, R + 5, 0, 2*Math.PI);
    ctx.fillStyle = '#1a0333';
    ctx.fill();

    for (let i = 0; i < segments.length; i++) {{
        const s = a + i * arc;
        const e = s + arc;

        /* segment */
        ctx.beginPath();
        ctx.moveTo(CX, CY);
        ctx.arc(CX, CY, R, s, e);
        ctx.closePath();
        ctx.fillStyle = PALETTE[i % PALETTE.length];
        ctx.fill();

        /* white divider line */
        ctx.beginPath();
        ctx.moveTo(CX, CY);
        ctx.arc(CX, CY, R, s, e);
        ctx.closePath();
        ctx.strokeStyle = 'rgba(255,255,255,0.45)';
        ctx.lineWidth = 2;
        ctx.stroke();

        /* text */
        ctx.save();
        ctx.translate(CX, CY);
        ctx.rotate(s + arc / 2);
        ctx.textAlign  = 'right';
        ctx.textBaseline = 'middle';
        ctx.shadowColor = 'rgba(0,0,0,0.9)';
        ctx.shadowBlur  = 5;

        const is500 = segments[i] === "500";
        if (is500) {{
            ctx.fillStyle = '#ffe066';
            ctx.font = `900 15px 'Nunito',sans-serif`;
            ctx.fillText('500 Taka 💛', R - 12, 0);
        }} else {{
            ctx.fillStyle = '#ffffff';
            ctx.font = `800 14px 'Nunito',sans-serif`;
            ctx.fillText(segments[i] + ' Taka', R - 12, 0);
        }}
        ctx.restore();
    }}

    /* shiny bevel ring */
    const bevel = ctx.createRadialGradient(CX, CY, R-18, CX, CY, R+2);
    bevel.addColorStop(0,'transparent');
    bevel.addColorStop(0.6,'rgba(255,255,255,0.08)');
    bevel.addColorStop(1,'rgba(255,255,255,0.22)');
    ctx.beginPath();
    ctx.arc(CX, CY, R, 0, 2*Math.PI);
    ctx.strokeStyle = bevel;
    ctx.lineWidth = 18;
    ctx.stroke();

    /* gold border line */
    ctx.beginPath();
    ctx.arc(CX, CY, R, 0, 2*Math.PI);
    ctx.strokeStyle = 'rgba(255,215,0,0.6)';
    ctx.lineWidth = 3;
    ctx.stroke();

    /* center hub */
    const hub = ctx.createRadialGradient(CX, CY, 0, CX, CY, 52);
    hub.addColorStop(0,'#fff9c4');
    hub.addColorStop(0.4,'#ffd700');
    hub.addColorStop(1,'#e65c00');
    ctx.beginPath();
    ctx.arc(CX, CY, 52, 0, 2*Math.PI);
    ctx.fillStyle = hub;
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 4;
    ctx.stroke();

    /* center emoji */
    ctx.font = '38px serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.shadowBlur = 0;
    ctx.fillText('🎡', CX, CY);
}}

draw(angle);

/* ── spin logic ───────────────────────────────────────────── */
function easeOut(t) {{ return 1 - Math.pow(1 - t, 4); }}

// Pointer is at 3-o-clock = canvas angle 0.
// Segment i occupies wheel-space angles [i*arc, (i+1)*arc].
// When wheel has rotated by `a`, segment i sits at canvas angle (a + i*arc).
// Segment under pointer: (-a mod 2PI) / arc  => floor gives index.
function getSegmentAtPointer(a) {{
    const norm = ((-a) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    return Math.floor(norm / arc) % segments.length;
}}

function startSpin() {{
    if (spinning) return;
    if (!currentName) {{ alert('Please enter your name first! ✍️'); return; }}
    if (alreadySpun)  {{ alert('You already spun! One chance per person. 🚫'); return; }}

    spinning = true;
    document.getElementById('spinBtn').disabled = true;

    // ── Pick winner — NEVER 500 Taka ──────────────────────────────────────
    // Also exclude the segments immediately adjacent to FORBIDDEN (neighbours)
    // so the pointer can never "slip" into 500 from a nearby segment.
    const forbidden_neighbours = new Set([
        FORBIDDEN,
        (FORBIDDEN - 1 + segments.length) % segments.length,
        (FORBIDDEN + 1) % segments.length
    ]);
    let winner;
    do {{
        winner = Math.floor(Math.random() * segments.length);
    }} while (forbidden_neighbours.has(winner));

    // ── Target angle: land dead-centre of winner segment ──────────────────
    // Centre of segment `winner` in wheel-space = winner*arc + arc/2
    // For canvas-angle 0: finalAngle = -(winner*arc + arc/2)
    const targetAngle    = -(winner * arc + arc / 2);
    const extraRotations = 10 + Math.random() * 5;
    const delta          = ((targetAngle - angle) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    const totalAngle     = extraRotations * 2 * Math.PI + delta;

    const duration  = 5500 + Math.random() * 1500;
    const startA    = angle;
    const startTime = performance.now();

    function frame(now) {{
        const p = Math.min((now - startTime) / duration, 1);
        angle = startA + totalAngle * easeOut(p);
        draw(angle);
        if (p < 1) {{
            requestAnimationFrame(frame);
        }} else {{
            // Ground-truth: read which segment is actually under pointer
            let actualWinner = getSegmentAtPointer(angle);

            // IRON-CLAD: if 500 somehow ended up under pointer, override it
            if (forbidden_neighbours.has(actualWinner)) {{
                actualWinner = winner;          // use the pre-planned safe winner
                angle = targetAngle;            // snap wheel visually to correct pos
                draw(angle);
            }}

            spinning = false;
            showResult(actualWinner);
        }}
    }}
    requestAnimationFrame(frame);
}}

/* ── result popup ─────────────────────────────────────────── */
function showResult(idx) {{
    const amt = segments[idx];
    document.getElementById('rcName').textContent   = currentName + '!';
    document.getElementById('rcAmount').textContent = amt;
    document.getElementById('overlay').classList.add('show');
    confetti();

    const url = new URL(window.parent.location.href);
    url.searchParams.set('result_name',   currentName);
    url.searchParams.set('result_amount', amt);
    window.parent.history.replaceState(null, '', url.toString());
    setTimeout(() => {{ window.parent.location.href = url.toString(); }}, 2800);
}}

function closeResult() {{
    document.getElementById('overlay').classList.remove('show');
    document.getElementById('confettiLayer').innerHTML = '';
}}

/* ── confetti ─────────────────────────────────────────────── */
function confetti() {{
    const layer  = document.getElementById('confettiLayer');
    layer.innerHTML = '';
    const cols   = ['#ffd700','#ff6b35','#2ecc71','#3498db','#e74c3c','#9b59b6','#1abc9c'];
    const style  = document.createElement('style');
    style.textContent = `@keyframes cf {{ to {{ transform: translateY(105vh) rotate(900deg); opacity:0; }} }}`;
    document.head.appendChild(style);
    for (let i = 0; i < 120; i++) {{
        const d = document.createElement('div');
        const s = 7 + Math.random() * 9;
        d.style.cssText = `
            position:absolute; width:${{s}}px; height:${{s}}px;
            background:${{cols[i%cols.length]}};
            left:${{Math.random()*100}}%;
            top:-20px;
            border-radius:${{Math.random()>.5?'50%':'3px'}};
            animation: cf ${{2.5+Math.random()*3}}s linear ${{Math.random()*.6}}s forwards;
        `;
        layer.appendChild(d);
    }}
}}

/* disable button if no name / already spun */
if (!currentName || alreadySpun) {{
    document.getElementById('spinBtn').disabled = true;
}}
</script>
</body>
</html>"""

components.html(wheel_html, height=680, scrolling=False)

