# TWIN FORGE

## AI-Enabled Real-Time Digital Twin for Aero Piston Engine Health Monitoring

Twin Forge is an AI-enabled digital twin system designed for real-time monitoring, fault prediction, Remaining Useful Life (RUL) estimation, and mission reliability assessment of aero piston engines used in MALE UAVs.

The system combines physics-based engine simulation with machine learning and AI-driven health assessment to provide an interactive view of engine condition and potential failures.

---

## 🚀 Key Features

- Real-time aero piston engine telemetry simulation
- Digital twin state monitoring
- Engine Health Index calculation
- AI-based anomaly detection
- Fault classification and fault probability estimation
- Remaining Useful Life (RUL) prediction
- Mission reliability assessment
- Engine degradation tracking
- Multiple fault simulation scenarios
- Interactive Streamlit monitoring dashboard
- FastAPI backend for simulation and AI services

---

## 🧠 System Capabilities

The digital twin continuously evaluates simulated engine parameters including:

- RPM
- Torque
- Power
- Throttle
- Engine Load
- Oil Temperature
- Cylinder Head Temperature
- Exhaust Gas Temperature (EGT)
- Oil Pressure
- Fuel Flow
- Vibration
- Engine Hours

These parameters are processed to estimate:

**Health → Anomaly → Fault → Degradation → RUL → Mission Reliability**

---

## ⚙️ Fault Scenarios

The dashboard supports demonstration scenarios such as:

1. Normal Operation
2. Overheating
3. Low Oil Pressure
4. High Vibration
5. Combustion Anomaly

Each scenario modifies engine conditions and allows the system to demonstrate how the digital twin responds to abnormal operating conditions.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Engine Simulator  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Digital Twin      │
                    │   Engine State      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ Anomaly     │  │ Fault       │  │ Degradation │
       │ Detection   │  │ Detection   │  │ & RUL       │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Mission Reliability │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └─────────────────────┘
```
