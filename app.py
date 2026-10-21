import streamlit as st
import pickle
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

  /* ── Global reset ── */
  html, body, [class*="css"] {
      font-family: 'Outfit', sans-serif;
  }

  /* ── Animated gradient background ── */
  .stApp {
      background: linear-gradient(135deg, #0f0c29 0%, #1a1a4e 40%, #24243e 70%, #0f0c29 100%);
      background-attachment: fixed;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero banner ── */
  .hero {
      text-align: center;
      padding: 2.5rem 1rem 1.5rem;
  }
  .hero-badge {
      display: inline-block;
      background: linear-gradient(90deg, #f7971e, #ffd200);
      color: #0f0c29;
      font-weight: 700;
      font-size: 0.78rem;
      letter-spacing: 2px;
      text-transform: uppercase;
      padding: 4px 16px;
      border-radius: 100px;
      margin-bottom: 0.9rem;
  }
  .hero h1 {
      font-size: 3rem;
      font-weight: 800;
      background: linear-gradient(90deg, #f7971e 0%, #ffd200 50%, #fff 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 0 0 0.4rem;
      line-height: 1.1;
  }
  .hero p {
      color: rgba(255,255,255,0.55);
      font-size: 1rem;
      margin: 0;
  }

  /* ── Glass card ── */
  .glass-card {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 20px;
      padding: 1.8rem 2rem;
      margin-bottom: 1.2rem;
      backdrop-filter: blur(12px);
  }
  .card-title {
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 2.5px;
      text-transform: uppercase;
      color: #ffd200;
      margin-bottom: 1rem;
  }

  /* ── Selectbox & number input overrides ── */
  div[data-baseweb="select"] > div,
  div[data-baseweb="input"] input {
      background: rgba(255,255,255,0.07) !important;
      border: 1px solid rgba(255,255,255,0.15) !important;
      border-radius: 12px !important;
      color: #fff !important;
      font-family: 'Outfit', sans-serif !important;
  }
  div[data-baseweb="select"] svg { color: #ffd200 !important; }
  .stSelectbox label, .stNumberInput label {
      color: rgba(255,255,255,0.65) !important;
      font-size: 0.82rem !important;
      font-weight: 600 !important;
      letter-spacing: 0.5px !important;
  }

  /* ── Predict button ── */
  .stButton > button {
      width: 100%;
      background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
      color: #0f0c29;
      font-weight: 800;
      font-size: 1.05rem;
      letter-spacing: 1px;
      border: none;
      border-radius: 14px;
      padding: 0.85rem 2rem;
      cursor: pointer;
      transition: transform 0.18s ease, box-shadow 0.18s ease;
      box-shadow: 0 4px 24px rgba(247,151,30,0.35);
      font-family: 'Outfit', sans-serif;
  }
  .stButton > button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 32px rgba(247,151,30,0.55);
  }
  .stButton > button:active { transform: translateY(0); }

  /* ── Divider ── */
  .custom-divider {
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
      margin: 0.5rem 0 1.4rem;
  }

  /* ── Result cards ── */
  .result-wrapper {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
  }
  .result-card {
      flex: 1;
      border-radius: 18px;
      padding: 1.4rem 1.2rem 1.2rem;
      text-align: center;
      position: relative;
      overflow: hidden;
  }
  .result-card.win {
      background: linear-gradient(135deg, rgba(34,197,94,0.25), rgba(16,185,129,0.12));
      border: 1px solid rgba(34,197,94,0.4);
  }
  .result-card.loss {
      background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.1));
      border: 1px solid rgba(239,68,68,0.35);
  }
  .result-card .team-name {
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      opacity: 0.75;
      margin-bottom: 0.4rem;
  }
  .result-card.win .team-name { color: #4ade80; }
  .result-card.loss .team-name { color: #f87171; }
  .result-card .pct {
      font-size: 3.2rem;
      font-weight: 800;
      line-height: 1;
      margin-bottom: 0.3rem;
  }
  .result-card.win .pct { color: #4ade80; }
  .result-card.loss .pct { color: #f87171; }
  .result-card .label {
      font-size: 0.75rem;
      opacity: 0.55;
      font-weight: 500;
  }

  /* ── Progress bar wrapper ── */
  .bar-wrapper {
      margin-top: 1.2rem;
      background: rgba(255,255,255,0.08);
      border-radius: 100px;
      height: 10px;
      overflow: hidden;
  }
  .bar-fill {
      height: 100%;
      border-radius: 100px;
      background: linear-gradient(90deg, #f7971e, #ffd200);
      transition: width 0.6s cubic-bezier(.4,0,.2,1);
  }

  /* ── Footer ── */
  .footer {
      text-align: center;
      padding: 2rem 0 1rem;
      color: rgba(255,255,255,0.25);
      font-size: 0.78rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
teams = sorted([
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
])

cities = sorted([
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
])

pipe = pickle.load(open('pipe.pkl', 'rb'))

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🏏 Powered by Machine Learning</div>
  <h1>IPL Win Predictor</h1>
  <p>Real-time win probability based on live match data</p>
</div>
""", unsafe_allow_html=True)

# ── Card 1 — Teams ────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card"><div class="card-title">⚔️ &nbsp;Select Teams</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("🏏 Batting Team", teams, key="batting")
with col2:
    bowling_team = st.selectbox("🎯 Bowling Team", teams, key="bowling")
st.markdown('</div>', unsafe_allow_html=True)

# ── Card 2 — Venue & Target ───────────────────────────────────────────────────
st.markdown('<div class="glass-card"><div class="card-title">📍 &nbsp;Venue & Target</div>', unsafe_allow_html=True)
col3, col4 = st.columns([2, 1])
with col3:
    selected_city = st.selectbox("🏟️ Host City", cities, key="city")
with col4:
    target = st.number_input("🎯 Target", min_value=1, step=1, key="target")
st.markdown('</div>', unsafe_allow_html=True)

# ── Card 3 — Match Situation ──────────────────────────────────────────────────
st.markdown('<div class="glass-card"><div class="card-title">📊 &nbsp;Current Match Situation</div>', unsafe_allow_html=True)
col5, col6, col7 = st.columns(3)
with col5:
    score = st.number_input("🏃 Score", min_value=0, step=1, key="score")
with col6:
    overs = st.number_input("🕐 Overs", min_value=0.1, max_value=19.9, step=0.1, format="%.1f", key="overs")
with col7:
    wickets = st.number_input("🚨 Wickets", min_value=0, max_value=9, step=1, key="wickets")
st.markdown('</div>', unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
predict_btn = st.button("⚡  Predict Win Probability")

# ── Result ────────────────────────────────────────────────────────────────────
if predict_btn:
    if batting_team == bowling_team:
        st.warning("⚠️ Batting and bowling teams cannot be the same!")
    elif overs == 0:
        st.warning("⚠️ Overs completed cannot be 0!")
    else:
        runs_left   = target - score
        balls_left  = 120 - (overs * 6)
        wkts_left   = 10 - wickets
        crr         = score / overs
        rrr         = (runs_left * 6) / balls_left if balls_left > 0 else 999

        input_df = pd.DataFrame({
            'batting_team':  [batting_team],
            'bowling_team':  [bowling_team],
            'city':          [selected_city],
            'runs_left':     [runs_left],
            'balls_left':    [balls_left],
            'wickets':       [wkts_left],
            'total_runs_x':  [target],
            'crr':           [crr],
            'rrr':           [rrr],
        })

        result = pipe.predict_proba(input_df)
        win  = round(result[0][1] * 100)
        loss = round(result[0][0] * 100)

        # ── Result cards ──
        st.markdown(f"""
        <div class="glass-card" style="margin-top:0.5rem;">
          <div class="card-title">🎯 &nbsp;Prediction Result</div>
          <div class="result-wrapper">
            <div class="result-card win">
              <div class="team-name">{batting_team}</div>
              <div class="pct">{win}%</div>
              <div class="label">Win Probability</div>
            </div>
            <div class="result-card loss">
              <div class="team-name">{bowling_team}</div>
              <div class="pct">{loss}%</div>
              <div class="label">Win Probability</div>
            </div>
          </div>
          <div class="bar-wrapper" style="margin-top:1.2rem;">
            <div class="bar-fill" style="width:{win}%;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:0.4rem;">
            <span style="font-size:0.72rem;color:rgba(255,255,255,0.4);">{batting_team}</span>
            <span style="font-size:0.72rem;color:rgba(255,255,255,0.4);">{bowling_team}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Match summary stats ──
        st.markdown(f"""
        <div class="glass-card">
          <div class="card-title">📋 &nbsp;Match Summary</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;text-align:center;">
            <div>
              <div style="font-size:1.6rem;font-weight:800;color:#ffd200;">{int(runs_left)}</div>
              <div style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-top:2px;">Runs Needed</div>
            </div>
            <div>
              <div style="font-size:1.6rem;font-weight:800;color:#ffd200;">{int(balls_left)}</div>
              <div style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-top:2px;">Balls Left</div>
            </div>
            <div>
              <div style="font-size:1.6rem;font-weight:800;color:#ffd200;">{rrr:.2f}</div>
              <div style="font-size:0.72rem;color:rgba(255,255,255,0.45);margin-top:2px;">Required RR</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with ❤️ using Streamlit &nbsp;•&nbsp; IPL Win Predictor &nbsp;•&nbsp; ML Powered
</div>
""", unsafe_allow_html=True)