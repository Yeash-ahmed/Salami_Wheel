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

# ── Handle save from JS ──────────────────────────────────────
params = st.query_params
if "save_name" in params and "save_amount" in params:
    n = params["save_name"].strip()
    a = params["save_amount"].strip()
    existing = get_spun_names()
    if n.lower() not in existing:
        save_name(n, a)
    st.query_params.clear()
    st.rerun()

spun_names     = get_spun_names()
spun_json      = json.dumps(spun_names)

# ── Global CSS: just kill Streamlit chrome ───────────────────
st.markdown("""
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp {
    background: #0d0120 !important;
    overflow-x: hidden;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"]      { display: none !important; }
header[data-testid="stHeader"]        { display: none !important; }
footer                                { display: none !important; }
#MainMenu                             { display: none !important; }
.stDeployButton                       { display: none !important; }
iframe { border: none !important; display: block; }
</style>
""", unsafe_allow_html=True)

# ── Build the full page as one self-contained HTML ───────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800;900&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
<style>
/* ── Reset ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    font-family: 'Nunito', sans-serif;
    background: radial-gradient(ellipse at top, #2d0a5e 0%, #1a0333 55%, #0d0120 100%);
    min-height: 100vh;
    color: #fff;
    overflow-x: hidden;
}}

/* ── Layout wrapper ── */
.app {{
    max-width: 520px;
    margin: 0 auto;
    padding: 16px 14px 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
}}

/* ── Header ── */
.header {{
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, rgba(255,107,53,0.18), rgba(255,215,0,0.09));
    border: 2px solid rgba(255,215,0,0.3);
    border-radius: 22px;
    padding: 14px 12px 12px;
}}
.header h1 {{
    font-family: 'Baloo 2', cursive;
    font-size: clamp(1.6rem, 7vw, 2.4rem);
    color: #ffd700;
    text-shadow: 0 0 24px rgba(255,215,0,0.65);
    letter-spacing: 1px;
    line-height: 1.1;
}}
.header p {{
    color: rgba(255,255,255,0.8);
    font-size: clamp(0.82rem, 3.5vw, 1rem);
    margin-top: 4px;
}}

/* ── Name card ── */
.name-card {{
    width: 100%;
    background: rgba(255,255,255,0.06);
    border: 2px solid rgba(255,215,0,0.35);
    border-radius: 20px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}}
.name-card label {{
    font-family: 'Baloo 2', cursive;
    font-size: 1rem;
    color: #ffd700;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
.name-row {{
    display: flex;
    gap: 8px;
    align-items: stretch;
}}
.name-input {{
    flex: 1;
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(255,215,0,0.5);
    border-radius: 50px;
    color: #fff;
    font-family: 'Nunito', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    padding: 12px 18px;
    outline: none;
    transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
    -webkit-appearance: none;
}}
.name-input::placeholder {{ color: rgba(255,255,255,0.4); font-weight: 600; }}
.name-input:focus {{
    border-color: #ffd700;
    background: rgba(255,255,255,0.15);
    box-shadow: 0 0 18px rgba(255,215,0,0.35);
}}
.confirm-btn {{
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    color: #1a0333;
    border: none;
    border-radius: 50px;
    font-family: 'Baloo 2', cursive;
    font-size: 0.95rem;
    font-weight: 900;
    padding: 12px 20px;
    cursor: pointer;
    white-space: nowrap;
    box-shadow: 0 4px 16px rgba(255,140,0,0.45);
    transition: transform 0.15s, box-shadow 0.15s;
    -webkit-tap-highlight-color: transparent;
}}
.confirm-btn:active {{ transform: scale(0.95); }}

/* Status chips */
.status-chip {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 800;
}}
.chip-ok  {{
    background: rgba(46,204,113,0.15);
    border: 1.5px solid rgba(46,204,113,0.5);
    color: #6dffad;
}}
.chip-err {{
    background: rgba(255,80,80,0.15);
    border: 1.5px solid rgba(255,80,80,0.5);
    color: #ff9090;
}}
.chip-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}}
.chip-ok  .chip-dot {{ background: #2ecc71; box-shadow: 0 0 6px #2ecc71; }}
.chip-err .chip-dot {{ background: #ff5050; box-shadow: 0 0 6px #ff5050; }}

/* ── Wheel area ── */
.wheel-area {{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    position: relative;
}}

.wheel-wrap {{
    position: relative;
    width: min(480px, 94vw);
    height: min(480px, 94vw);
}}

/* Rotating rainbow ring */
.wheel-wrap::before {{
    content: '';
    position: absolute;
    inset: -8px;
    border-radius: 50%;
    background: conic-gradient(#ffd700, #ff6b35, #2ecc71, #3498db, #9b59b6, #ffd700);
    animation: ringRot 6s linear infinite;
    opacity: 0.75;
    z-index: 0;
}}
.wheel-wrap::after {{
    content: '';
    position: absolute;
    inset: -3px;
    border-radius: 50%;
    background: #1a0333;
    z-index: 0;
}}
@keyframes ringRot {{ to {{ transform: rotate(360deg); }} }}

canvas {{
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    display: block;
    filter: drop-shadow(0 0 20px rgba(255,215,0,0.5)) drop-shadow(0 0 40px rgba(255,107,53,0.3));
}}

/* Pointer */
.pointer {{
    position: absolute;
    right: -22px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    display: flex;
    align-items: center;
}}
.ptr-arrow {{
    width: 0; height: 0;
    border-top: 22px solid transparent;
    border-bottom: 22px solid transparent;
    border-right: 44px solid #ffd700;
    filter: drop-shadow(0 0 10px rgba(255,215,0,0.9));
}}
.ptr-ball {{
    width: 16px; height: 16px;
    background: radial-gradient(circle, #fff 25%, #ffd700 80%);
    border-radius: 50%;
    margin-left: -5px;
    box-shadow: 0 0 10px #ffd700;
    z-index: 2;
}}

/* ── SPIN button ── */
.spin-btn {{
    margin-top: 16px;
    width: min(440px, 90vw);
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ffd700 100%);
    color: #1a0333;
    border: none;
    border-radius: 60px;
    font-family: 'Baloo 2', cursive;
    font-size: clamp(1.1rem, 5vw, 1.4rem);
    font-weight: 900;
    padding: 15px 0;
    cursor: pointer;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow: 0 6px 28px rgba(255,107,53,0.55);
    transition: transform 0.15s, box-shadow 0.15s;
    -webkit-tap-highlight-color: transparent;
    position: relative;
    overflow: hidden;
}}
.spin-btn::after {{
    content:'';
    position:absolute; top:0; left:-60%;
    width:40%; height:100%;
    background: rgba(255,255,255,0.22);
    transform: skewX(-20deg);
    transition: left 0.4s;
}}
.spin-btn:not(:disabled):hover::after {{ left:120%; }}
.spin-btn:not(:disabled):active {{ transform: scale(0.97); }}
.spin-btn:disabled {{
    background: linear-gradient(135deg, #444, #666);
    color: #999;
    box-shadow: none;
    cursor: not-allowed;
}}

/* ── Result overlay (inside iframe) ── */
.overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.87);
    z-index: 200;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}
.overlay.show {{ display: flex; }}

.result-card {{
    background: linear-gradient(160deg, #1a0533, #2d1155);
    border: 3px solid #ffd700;
    border-radius: 28px;
    padding: clamp(1.4rem, 5vw, 2rem) clamp(1.2rem, 5vw, 2rem);
    text-align: center;
    width: 100%;
    max-width: 360px;
    box-shadow: 0 0 70px rgba(255,215,0,0.4);
    animation: cardPop 0.45s cubic-bezier(0.34,1.56,0.64,1);
}}
@keyframes cardPop {{
    from {{ transform: scale(0.4) rotate(-5deg); opacity:0; }}
    to   {{ transform: scale(1)   rotate(0deg);  opacity:1; }}
}}
.rc-emoji  {{ font-size: clamp(2.5rem,8vw,3.5rem); line-height:1; margin-bottom:6px; }}
.rc-name   {{
    font-family: 'Baloo 2', cursive;
    color: #ffd700;
    font-size: clamp(1.3rem, 5.5vw, 1.7rem);
    font-weight: 900;
    word-break: break-word;
}}
.rc-label  {{ color: rgba(255,255,255,0.5); font-size: 0.88rem; margin: 6px 0 2px; }}
.rc-amount {{
    font-family: 'Baloo 2', cursive;
    color: #fff;
    font-size: clamp(2.4rem, 10vw, 3.4rem);
    font-weight: 900;
    line-height: 1;
    text-shadow: 0 0 28px rgba(255,215,0,0.7);
}}
.rc-taka   {{ color: #ffd700; font-size: 0.5em; vertical-align: super; }}
.rc-eid    {{ color: rgba(255,255,255,0.6); font-size:0.9rem; margin-top:6px; }}
.rc-close  {{
    margin-top: 16px;
    background: linear-gradient(135deg, #ff6b35, #ffd700);
    color: #1a0333;
    border: none;
    border-radius: 50px;
    padding: 12px 36px;
    font-family: 'Baloo 2', cursive;
    font-size: 1.05rem;
    font-weight: 900;
    cursor: pointer;
    box-shadow: 0 4px 18px rgba(255,107,53,0.5);
    -webkit-tap-highlight-color: transparent;
}}
.rc-close:active {{ transform: scale(0.95); }}

/* ── Confetti ── */
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

<div class="app">

  <!-- Header -->
  <div class="header">
     <h1>🌙 ইয়াস ভাই এর সালামি হুইল 🎉</h1>
    <p>Pick your Eid Salami!! 🤩 &nbsp;—&nbsp; Each person spins once!</p>
  </div>

  <!-- Name card -->
  <div class="name-card" id="nameCard">
    <label>✍️ Enter your name</label>
    <div class="name-row">
      <input class="name-input" id="nameInput" type="text"
             placeholder="Your name here…"
             autocomplete="off" autocorrect="off" spellcheck="false"
             maxlength="40"
             onkeydown="if(event.key==='Enter') confirmName()">
      <button class="confirm-btn" onclick="confirmName()">✔ OK</button>
    </div>
    <div id="statusChip" style="display:none"></div>
  </div>

  <!-- Wheel -->
  <div class="wheel-area">
    <div class="wheel-wrap">
      <canvas id="wc"></canvas>
      <div class="pointer">
        <div class="ptr-arrow"></div>
        <div class="ptr-ball"></div>
      </div>
    </div>
    <button class="spin-btn" id="spinBtn" onclick="startSpin()" disabled>🎰 &nbsp;SPIN!</button>
  </div>

</div><!-- /app -->

<!-- Result overlay -->
<div class="confetti-layer" id="confettiLayer"></div>
<div class="overlay" id="overlay">
  <div class="result-card">
    <div class="rc-emoji">🎊</div>
    <div class="rc-name"  id="rcName"></div>
    <div class="rc-label">gets</div>
    <div class="rc-amount"><span id="rcAmt"></span><span class="rc-taka"> Taka</span></div>
    <div class="rc-eid">Eid Salami! 💚</div>
    <button class="rc-close" onclick="closeResult()">Awesome! 🎉</button>
  </div>
</div>

<script>
/* ═══════════════════════════════════════════════════════
   DATA
═══════════════════════════════════════════════════════ */
const SPUN_NAMES   = {spun_json};

const SEGMENTS = [
  "1","9.75","7.50","9.50","4.75",
  "5","2.50","7","1.50","1.25",
  "5.25","6.75","4.25","6","2.25",
  "7.75","8.25","2","1.25","4",
  "9.25","5.50","10","3","3.50",
  "9","6.50","5.75","3.25","3.75",
  "8","2.75","8.75","1.75","4.50",
  "6.25","8.50","500"
];
const FORBIDDEN = SEGMENTS.length - 1;
const FORBIDDEN_SET = new Set([
  FORBIDDEN,
  (FORBIDDEN - 1 + SEGMENTS.length) % SEGMENTS.length,
  (FORBIDDEN + 1) % SEGMENTS.length
]);

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

/* ═══════════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════════ */
let confirmedName = "";
let alreadySpun   = false;
let spinning      = false;

/* ═══════════════════════════════════════════════════════
   CANVAS
═══════════════════════════════════════════════════════ */
const canvas = document.getElementById('wc');
const ctx    = canvas.getContext('2d');
const SZ     = 560;
canvas.width = canvas.height = SZ;
const CX = CY = SZ / 2;
const R  = SZ / 2 - 6;
const arc = (2 * Math.PI) / SEGMENTS.length;
let   wheelAngle = 0;

function draw(a) {{
    ctx.clearRect(0, 0, SZ, SZ);

    // dark border ring
    ctx.beginPath(); ctx.arc(CX, CY, R+5, 0, 2*Math.PI);
    ctx.fillStyle = '#150028'; ctx.fill();

    for (let i = 0; i < SEGMENTS.length; i++) {{
        const s = a + i * arc, e = s + arc;
        ctx.beginPath(); ctx.moveTo(CX,CY); ctx.arc(CX,CY,R,s,e); ctx.closePath();
        ctx.fillStyle = PALETTE[i % PALETTE.length]; ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 2; ctx.stroke();

        ctx.save();
        ctx.translate(CX, CY); ctx.rotate(s + arc/2);
        ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
        ctx.shadowColor = 'rgba(0,0,0,0.95)'; ctx.shadowBlur = 5;
        if (SEGMENTS[i] === "500") {{
            ctx.fillStyle = '#ffe066';
            ctx.font = "900 14px 'Nunito',sans-serif";
            ctx.fillText('500 Taka 💛', R - 10, 0);
        }} else {{
            ctx.fillStyle = '#fff';
            ctx.font = "800 13px 'Nunito',sans-serif";
            ctx.fillText(SEGMENTS[i] + ' Taka', R - 10, 0);
        }}
        ctx.restore();
    }}

    // bevel
    const bv = ctx.createRadialGradient(CX,CY,R-20,CX,CY,R+2);
    bv.addColorStop(0,'transparent');
    bv.addColorStop(0.7,'rgba(255,255,255,0.07)');
    bv.addColorStop(1,'rgba(255,255,255,0.2)');
    ctx.beginPath(); ctx.arc(CX,CY,R,0,2*Math.PI);
    ctx.strokeStyle = bv; ctx.lineWidth = 18; ctx.stroke();

    // gold ring
    ctx.beginPath(); ctx.arc(CX,CY,R,0,2*Math.PI);
    ctx.strokeStyle = 'rgba(255,215,0,0.55)'; ctx.lineWidth = 3; ctx.stroke();

    // hub
    const hub = ctx.createRadialGradient(CX,CY,0,CX,CY,50);
    hub.addColorStop(0,'#fff9c4'); hub.addColorStop(0.4,'#ffd700'); hub.addColorStop(1,'#e65c00');
    ctx.beginPath(); ctx.arc(CX,CY,50,0,2*Math.PI);
    ctx.fillStyle = hub; ctx.fill();
    ctx.strokeStyle = 'white'; ctx.lineWidth = 4; ctx.stroke();

    ctx.font = '36px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.shadowBlur = 0; ctx.fillText('🎡', CX, CY);
}}
draw(wheelAngle);

/* ═══════════════════════════════════════════════════════
   NAME CONFIRM
═══════════════════════════════════════════════════════ */
function confirmName() {{
    const raw = document.getElementById('nameInput').value.trim();
    if (!raw) {{ shakeInput(); return; }}

    confirmedName = raw;
    alreadySpun   = SPUN_NAMES.includes(raw.toLowerCase());

    const chip = document.getElementById('statusChip');
    chip.style.display = 'flex';
    chip.style.alignItems = 'center';
    chip.style.gap = '8px';

    if (alreadySpun) {{
        chip.className = 'status-chip chip-err';
        chip.innerHTML = '<div class="chip-dot"></div>❌ ' + raw + ' has already spun! One chance only.';
        document.getElementById('spinBtn').disabled = true;
    }} else {{
        chip.className = 'status-chip chip-ok';
        chip.innerHTML = '<div class="chip-dot"></div>✅ Welcome, <b>' + raw + '</b>! Press SPIN!';
        document.getElementById('spinBtn').disabled = false;
        document.getElementById('nameInput').blur();
    }}
}}

function shakeInput() {{
    const inp = document.getElementById('nameInput');
    inp.style.animation = 'none';
    inp.style.borderColor = '#ff5050';
    setTimeout(() => {{ inp.style.borderColor = ''; }}, 800);
}}

/* ═══════════════════════════════════════════════════════
   SPIN
═══════════════════════════════════════════════════════ */
function easeOut(t) {{ return 1 - Math.pow(1-t, 4); }}

function getSegmentAtPointer(a) {{
    const norm = ((-a) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI);
    return Math.floor(norm / arc) % SEGMENTS.length;
}}

function startSpin() {{
    if (spinning || !confirmedName || alreadySpun) return;

    spinning = true;
    document.getElementById('spinBtn').disabled = true;
    document.getElementById('nameInput').disabled = true;
    document.querySelector('.confirm-btn').disabled = true;

    // pick winner — never 500 or its neighbours
    let winner;
    do {{ winner = Math.floor(Math.random() * SEGMENTS.length); }}
    while (FORBIDDEN_SET.has(winner));

    const targetAngle    = -(winner * arc + arc / 2);
    const extraRotations = 10 + Math.random() * 5;
    const delta          = ((targetAngle - wheelAngle) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI);
    const totalAngle     = extraRotations * 2 * Math.PI + delta;

    const duration  = 5500 + Math.random() * 1500;
    const startA    = wheelAngle;
    const startTime = performance.now();

    function frame(now) {{
        const p = Math.min((now - startTime) / duration, 1);
        wheelAngle = startA + totalAngle * easeOut(p);
        draw(wheelAngle);
        if (p < 1) {{
            requestAnimationFrame(frame);
        }} else {{
            let actual = getSegmentAtPointer(wheelAngle);
            if (FORBIDDEN_SET.has(actual)) {{
                actual = winner;
                wheelAngle = targetAngle;
                draw(wheelAngle);
            }}
            spinning = false;
            showResult(actual);
        }}
    }}
    requestAnimationFrame(frame);
}}

/* ═══════════════════════════════════════════════════════
   RESULT
═══════════════════════════════════════════════════════ */
function showResult(idx) {{
    const amt = SEGMENTS[idx];
    document.getElementById('rcName').textContent = confirmedName + '!';
    document.getElementById('rcAmt').textContent  = amt;
    document.getElementById('overlay').classList.add('show');
    launchConfetti();

    // Save to Streamlit backend via URL
    const url = new URL(window.parent.location.href);
    url.searchParams.set('save_name',   confirmedName);
    url.searchParams.set('save_amount', amt);
    window.parent.history.replaceState(null, '', url.toString());
    setTimeout(() => {{ window.parent.location.href = url.toString(); }}, 3000);
}}

function closeResult() {{
    document.getElementById('overlay').classList.remove('show');
    document.getElementById('confettiLayer').innerHTML = '';
    // Reset UI for next person — clear the name field fully
    document.getElementById('nameInput').value    = '';
    document.getElementById('nameInput').disabled = false;
    document.querySelector('.confirm-btn').disabled = false;
    document.getElementById('statusChip').style.display = 'none';
    document.getElementById('spinBtn').disabled   = true;
    confirmedName = '';
    alreadySpun   = false;
    // Add this person to local spun list so UI reflects immediately
    SPUN_NAMES.push(confirmedName.toLowerCase());
}}

/* ═══════════════════════════════════════════════════════
   CONFETTI
═══════════════════════════════════════════════════════ */
function launchConfetti() {{
    const layer = document.getElementById('confettiLayer');
    layer.innerHTML = '';
    const cols  = ['#ffd700','#ff6b35','#2ecc71','#3498db','#e74c3c','#9b59b6','#1abc9c'];
    const style = document.createElement('style');
    style.textContent = `@keyframes cf {{ to {{ transform:translateY(110vh) rotate(900deg); opacity:0; }} }}`;
    document.head.appendChild(style);
    for (let i = 0; i < 130; i++) {{
        const d = document.createElement('div');
        const s = 6 + Math.random() * 10;
        d.style.cssText = `position:absolute;width:${{s}}px;height:${{s}}px;
            background:${{cols[i%cols.length]}};
            left:${{Math.random()*100}}%;top:-20px;
            border-radius:${{Math.random()>.5?'50%':'3px'}};
            animation:cf ${{2.5+Math.random()*3}}s linear ${{Math.random()*.7}}s forwards;`;
        layer.appendChild(d);
    }}
}}

</script>
</body>
</html>"""

components.html(html, height=880, scrolling=False)
