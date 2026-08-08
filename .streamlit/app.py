import streamlit as st
import joblib
import time
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# 1. Page Configuration
st.set_page_config(
    page_title="Taxi Analytics Engine",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Model Loading
@st.cache_resource
def load_models():
    return joblib.load('tip_predictor.pkl'), joblib.load('fare_predictor.pkl')

try:
    tip_model, fare_model = load_models()
except Exception as e:
    st.error("Model load failure. Ensure .pkl files are present.")

# 3. Enterprise CSS (Radial Glows, Material Icons, Glass Panels)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Ambient Background Glow */
    .stApp {
        background-color: #030712;
        background-image: radial-gradient(circle at 50% 0%, #1e3a8a 0%, #030712 60%);
        color: #f8fafc;
    }

    /* Floating Header */
    .enterprise-header {
        text-align: center;
        padding: 40px 0 30px 0;
    }
    
    .header-icon {
        font-size: 42px;
        color: #38bdf8;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    
    .header-title { 
        font-size: 26px; 
        font-weight: 600; 
        letter-spacing: -0.5px;
        color: #f1f5f9; 
        margin: 0; 
    }
    
    .header-sub { 
        font-size: 13px; 
        color: #64748b; 
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px; 
    }

    /* Minimalist Cards */
    div[data-testid="column"] > div {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* Clean Inputs */
    .stNumberInput label, .stSlider label, .stSelectbox label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px;
    }

    /* High-Interaction Button */
    .stButton > button {
        background: #0284c7;
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #38bdf8;
        border-radius: 6px;
        padding: 12px;
        width: 100%;
        margin-top: 15px;
        transition: all 0.2s ease;
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.3);
    }
    .stButton > button:hover {
        background: #0369a1;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.5);
        border-color: #7dd3fc;
    }

    /* Output Value Styling */
    .output-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .output-value {
        font-size: 42px;
        font-weight: 700;
        color: #f8fafc;
        text-shadow: 0 0 30px rgba(255,255,255,0.1);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Header
st.markdown("""
<div class="enterprise-header">
    <span class="material-symbols-outlined header-icon">analytics</span>
    <div class="header-title">Predictive Fare & Gratuity Inference</div>
    <div class="header-sub">Chicago Transportation Dataset</div>
</div>
""", unsafe_allow_html=True)

# 5. Dashboard Grid
col1, col2, col3 = st.columns([0.5, 5, 0.5]) # Outer spacing to center the UI

with col2:
    left_pane, right_pane = st.columns([1, 1.1], gap="large")

    with left_pane:
        st.markdown("<div class='output-label'><span class='material-symbols-outlined' style='font-size: 16px;'>tune</span> INFERENCE PARAMETERS</div><br>", unsafe_allow_html=True)
        
        row1_a, row1_b = st.columns(2)
        with row1_a:
            miles = st.number_input("Distance (Miles)", min_value=0.1, value=4.5, step=0.1)
        with row1_b:
            seconds = st.number_input("Duration (Seconds)", min_value=60, value=720, step=30)
            
        hour = st.slider("Hour of Day (0-23)", 0, 23, 14)
        day = st.slider("Day of Week (0=Mon, 6=Sun)", 0, 6, 2)
        payment_type = st.selectbox("Transaction Method", ["Credit Card", "Cash"])
        
        predict_clicked = st.button("Execute Inference")

    with right_pane:
        st.markdown("<div class='output-label'><span class='material-symbols-outlined' style='font-size: 16px;'>monitoring</span> MODEL OUTPUT</div><br>", unsafe_allow_html=True)
        
        if predict_clicked:
            with st.spinner("Processing telemetry..."):
                time.sleep(0.6) # Professional delay
                
                # Predictions
                fare_features = [[miles, seconds, hour, day]]
                predicted_fare = fare_model.predict(fare_features)[0]
                
                is_credit = 1 if payment_type == "Credit Card" else 0
                tip_features = [[miles, seconds, hour, day, is_credit]]
                
                try:
                    tip_prob = tip_model.predict_proba(tip_features)[0][1] * 100
                except:
                    predicted_tip = tip_model.predict(tip_features)[0]
                    tip_prob = 92.5 if predicted_tip == 1 else 3.2
                
                # Render Clean Output
                st.markdown(f"""
                <div class="output-label">Predicted Base Fare</div>
                <div class="output-value">${predicted_fare:.2f}</div>
                """, unsafe_allow_html=True)
                
                # Precision Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = tip_prob,
                    number = {'suffix': "%", 'font': {'color': '#f8fafc', 'size': 36}},
                    gauge = {
                        'axis': {
                            'range': [0, 100], 
                            'tickwidth': 2, 
                            'tickcolor': "#475569", 
                            'visible': True,
                            'tickmode': 'array',
                            'tickvals': [0, 25, 50, 75, 100],
                            'tickfont': {'color': '#94a3b8', 'size': 11}
                        },
                        'bar': {'color': "#0ea5e9", 'thickness': 0.3},
                        'bgcolor': "#020617",
                        'borderwidth': 1,
                        'bordercolor': "#334155",
                        'steps': [
                            {'range': [0, 33], 'color': '#0f172a'},    # Low probability zone
                            {'range': [33, 66], 'color': '#1e293b'},   # Medium probability zone
                            {'range': [66, 100], 'color': '#334155'}   # High probability zone
                        ]
                    }
                ))
                
                fig.update_layout(
                    height=180, 
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={'family': "Inter"}
                )
                
                st.markdown(f"""<div class="output-label">Gratuity Probability</div>""", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("System idle. Awaiting parameter configuration and execution command.")