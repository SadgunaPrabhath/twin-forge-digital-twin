import time
from datetime import datetime

import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Twin Forge | Digital Twin",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "scenario" not in st.session_state:
    st.session_state.scenario = "normal"

if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# API HELPERS
# ============================================================

def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{API_BASE}{endpoint}",
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:
        st.error(f"API connection error: {exc}")
        return None


def get_state():
    try:
        response = requests.get(
            f"{API_BASE}/api/v1/twin/state",
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except Exception:
        return None


def run_scenario(scenario):
    result = api_post(
        "/api/v1/demo/scenario",
        {"scenario": scenario},
    )

    if result:
        st.session_state.scenario = scenario

        health = float(
            result.get("health_index", 0)
        )

        st.session_state.history.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "health": health,
            }
        )

        if len(st.session_state.history) > 40:
            st.session_state.history.pop(0)

    return result


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #07111f;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .hero {
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #0b1d33,
            #102b45
        );
        border: 1px solid #1d405f;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        color: #8da8c2;
        font-size: 0.95rem;
    }

    .metric-card {
        background: #0d1b2a;
        border: 1px solid #20364d;
        border-radius: 14px;
        padding: 1rem;
        min-height: 115px;
    }

    .metric-label {
        color: #8299ad;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 750;
        margin-top: 0.4rem;
    }

    .metric-unit {
        color: #8299ad;
        font-size: 0.8rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
    }

    .status-normal {
        color: #22c55e;
        font-weight: 800;
    }

    .status-warning {
        color: #f59e0b;
        font-weight: 800;
    }

    .status-critical {
        color: #ef4444;
        font-weight: 800;
    }

    .fault-box {
        padding: 1rem;
        border-radius: 14px;
        background: #111d2b;
        border: 1px solid #263c52;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            ✈️ TWIN FORGE
        </div>
        <div class="hero-subtitle">
            AI-Enabled Real-Time Digital Twin for Aero Piston Engine
            Health Monitoring, Fault Prediction & Mission Reliability
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎛️ Mission Control")

    st.caption("Digital Twin Simulation")

    scenarios = {
        "🟢 Normal Operation": "normal",
        "🔥 Overheating": "overheating",
        "🛢️ Low Oil Pressure": "low_oil_pressure",
        "📳 High Vibration": "high_vibration",
        "⚡ Combustion Anomaly": "combustion_anomaly",
    }

    for label, scenario in scenarios.items():

        if st.button(
            label,
            use_container_width=True,
        ):
            result = run_scenario(scenario)

            if result:
                st.rerun()

    st.divider()

    st.markdown("### 🎬 Demonstration")

    if st.button(
        "▶ Run Current Scenario",
        use_container_width=True,
    ):
        result = run_scenario(
            st.session_state.scenario
        )

        if result:
            st.rerun()

    st.caption(
        "Use the scenario buttons to demonstrate "
        "real-time fault detection."
    )

    st.divider()

    st.markdown("### System")

    st.success("API Connected")

    st.caption(
        f"Scenario: "
        f"`{st.session_state.scenario.upper()}`"
    )


# ============================================================
# GET CURRENT DATA
# ============================================================

data = get_state()

if not data or data.get("state") is None:

    st.warning(
        "No telemetry available yet. "
        "Select a scenario from Mission Control."
    )

    st.stop()


state = data.get("state") or {}
fault = data.get("fault") or {}
anomaly = data.get("anomaly") or {}
rul = data.get("rul") or {}
reliability = data.get("mission_reliability") or {}


# ============================================================
# CORE VALUES
# ============================================================

health = float(
    data.get(
        "health_index",
        state.get("health_index", 0),
    )
)

fault_probability = float(
    data.get(
        "fault_probability",
        0,
    )
)

rul_hours = float(
    data.get(
        "rul_hours",
        rul.get("remaining_hours", 0),
    )
)

reliability_value = float(
    data.get(
        "reliability",
        reliability.get("reliability", 0),
    )
)

fault_type = data.get(
    "fault_type",
    fault.get("fault_type", "NORMAL"),
)

severity = data.get(
    "severity",
    "NORMAL",
)


# ============================================================
# STATUS
# ============================================================

if health >= 80 and fault_type == "NORMAL":
    status = "HEALTHY"
    status_class = "status-normal"

elif health >= 40:
    status = "WARNING"
    status_class = "status-warning"

else:
    status = "CRITICAL"
    status_class = "status-critical"


# ============================================================
# TOP METRICS
# ============================================================

st.markdown(
    '<div class="section-title">ENGINE STATUS</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)


with c1:
    st.metric(
        "Health Index",
        f"{health:.1f}%",
    )


with c2:
    st.metric(
        "RUL",
        f"{rul_hours:.1f} h",
    )


with c3:
    st.metric(
        "Mission Reliability",
        f"{reliability_value:.1f}%",
    )


with c4:
    st.metric(
        "Fault Probability",
        f"{fault_probability * 100:.1f}%",
    )


with c5:
    st.metric(
        "Engine Hours",
        f"{float(state.get('engine_hours', 0)):.1f}",
    )


# ============================================================
# HEALTH + FAULT
# ============================================================

st.markdown(
    '<div class="section-title">AI HEALTH ASSESSMENT</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1, 1])


with left:

    st.markdown("### Health Index")

    st.progress(
        max(0.0, min(1.0, health / 100))
    )

    st.markdown(
        f"""
        <div class="{status_class}">
            {status}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Current mission phase: "
        f"{state.get('mission_phase', 'UNKNOWN')}"
    )


with right:

    st.markdown("### Fault Intelligence")

    st.markdown(
        f"""
        <div class="fault-box">

        <b>Detected Fault:</b>
        {fault_type.replace("_", " ")}

        <br><br>

        <b>Confidence:</b>
        {float(fault.get("confidence", 0)) * 100:.1f}%

        <br><br>

        <b>Severity:</b>
        {severity}

        <br><br>

        <b>Explanation:</b>
        {fault.get(
            "explanation",
            "No fault detected."
        )}

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TELEMETRY
# ============================================================

st.markdown(
    '<div class="section-title">LIVE ENGINE TELEMETRY</div>',
    unsafe_allow_html=True,
)

t1, t2, t3, t4 = st.columns(4)


with t1:
    st.metric(
        "RPM",
        f"{float(state.get('rpm', 0)):.0f}",
    )

    st.metric(
        "Torque",
        f"{float(state.get('torque', 0)):.1f} Nm",
    )


with t2:
    st.metric(
        "Oil Temperature",
        f"{float(state.get('oil_temperature', 0)):.1f} °C",
    )

    st.metric(
        "Oil Pressure",
        f"{float(state.get('oil_pressure', 0)):.2f}",
    )


with t3:
    st.metric(
        "Cylinder Head",
        f"{float(state.get('cylinder_head_temperature', 0)):.1f} °C",
    )

    st.metric(
        "EGT",
        f"{float(state.get('egt', 0)):.1f} °C",
    )


with t4:
    st.metric(
        "Vibration",
        f"{float(state.get('vibration', 0)):.2f}",
    )

    st.metric(
        "Fuel Flow",
        f"{float(state.get('fuel_flow', 0)):.1f}",
    )


# ============================================================
# ANOMALY EXPLANATION
# ============================================================

st.markdown(
    '<div class="section-title">ANOMALY EXPLANATION</div>',
    unsafe_allow_html=True,
)

reasons = anomaly.get("reasons", [])

if reasons:

    for reason in reasons:
        st.warning(f"⚠️ {reason}")

else:

    st.success(
        "✓ No abnormal sensor conditions detected."
    )


# ============================================================
# HEALTH HISTORY
# ============================================================

st.markdown(
    '<div class="section-title">HEALTH TREND</div>',
    unsafe_allow_html=True,
)

if st.session_state.history:

    import pandas as pd

    chart_data = pd.DataFrame(
        st.session_state.history
    )

    chart_data = chart_data.set_index("time")

    st.line_chart(
        chart_data["health"],
        height=280,
    )


# ============================================================
# MISSION RELIABILITY
# ============================================================

st.markdown(
    '<div class="section-title">MISSION RELIABILITY</div>',
    unsafe_allow_html=True,
)

r1, r2, r3 = st.columns(3)


with r1:
    st.metric(
        "Reliability",
        f"{reliability_value:.1f}%",
    )


with r2:
    st.metric(
        "Risk Level",
        reliability.get(
            "risk_level",
            "UNKNOWN",
        ),
    )


with r3:
    st.metric(
        "RUL Confidence",
        f"{float(rul.get('confidence', 0)) * 100:.1f}%",
    )


st.caption(
    reliability.get(
        "explanation",
        "Mission reliability assessment unavailable.",
    )
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Twin Forge • Physics-Informed Drone Digital Twin • "
    "Real-Time Health Monitoring • Predictive Maintenance"
)
