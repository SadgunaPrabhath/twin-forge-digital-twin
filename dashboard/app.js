const API_BASE = "http://127.0.0.1:8000";

// ============================================================
// DOM HELPERS
// ============================================================

function setText(id, value) {
  const element = document.getElementById(id);

  if (element) {
    element.textContent = value;
  }
}

function number(value, fallback = 0) {
  const n = Number(value);

  return Number.isFinite(n) ? n : fallback;
}

// ============================================================
// CLOCK
// ============================================================

function updateClock() {
  const now = new Date();

  setText(
    "timestamp",
    now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }),
  );
}

setInterval(updateClock, 1000);

updateClock();

// ============================================================
// HEALTH RING
// ============================================================

function updateHealthRing(health) {
  health = Math.max(0, Math.min(100, number(health, 100)));

  setText("healthValue", health.toFixed(1));

  const circle = document.getElementById("healthCircle");

  if (!circle) return;

  const circumference = 408.4;

  const offset = circumference - (health / 100) * circumference;

  circle.style.strokeDashoffset = offset;
}

// ============================================================
// HEALTH STATUS
// ============================================================

function updateHealthStatus(health, faultType) {
  const status = document.getElementById("systemStatus");

  const description = document.getElementById("conditionDescription");

  if (!status || !description) return;

  if (faultType && faultType !== "NORMAL") {
    status.textContent = "ATTENTION";

    status.className = "condition-value";

    status.style.color = "var(--yellow)";

    description.textContent = `${faultType.replaceAll("_", " ")} condition detected.`;

    return;
  }

  if (health >= 80) {
    status.textContent = "HEALTHY";

    status.className = "condition-value healthy";

    status.style.color = "";

    description.textContent = "Engine operating within expected limits.";
  } else if (health >= 60) {
    status.textContent = "DEGRADED";

    status.className = "condition-value";

    status.style.color = "var(--yellow)";

    description.textContent = "Engine condition requires increased monitoring.";
  } else {
    status.textContent = "CRITICAL";

    status.className = "condition-value";

    status.style.color = "var(--red)";

    description.textContent = "Immediate engineering attention recommended.";
  }
}

// ============================================================
// FAULT
// ============================================================

function updateFault(fault) {
  if (!fault) return;

  const type = fault.fault_type || "NORMAL";

  const confidence = number(fault.confidence, type === "NORMAL" ? 0.99 : 0);

  setText("faultType", type.replaceAll("_", " "));

  setText("faultConfidence", `${(confidence * 100).toFixed(1)}%`);

  setText(
    "faultExplanation",
    fault.explanation || "No known fault condition detected.",
  );

  const indicator = document.getElementById("faultIndicator");

  if (type === "NORMAL") {
    indicator.textContent = "✓";

    indicator.style.color = "var(--green)";

    indicator.style.background = "rgba(34,197,94,0.1)";

    indicator.style.borderColor = "rgba(34,197,94,0.3)";
  } else {
    indicator.textContent = "⚠";

    indicator.style.color = "var(--yellow)";

    indicator.style.background = "rgba(245,158,11,0.1)";

    indicator.style.borderColor = "rgba(245,158,11,0.3)";
  }
}

// ============================================================
// TELEMETRY
// ============================================================

function updateTelemetry(state) {
  if (!state) return;

  setText("telemetryRPM", number(state.rpm).toFixed(0));

  setText("engineRPM", number(state.rpm).toFixed(0));

  setText("telemetryTorque", number(state.torque).toFixed(1));

  setText("oilTemp", number(state.oil_temperature).toFixed(1));

  setText("cylinderTemp", number(state.cylinder_head_temperature).toFixed(1));

  setText("egt", number(state.egt).toFixed(1));

  setText("oilPressure", number(state.oil_pressure).toFixed(2));

  setText("fuelFlow", number(state.fuel_flow).toFixed(1));

  setText("vibration", number(state.vibration).toFixed(2));

  setText("engineHours", `${number(state.engine_hours).toFixed(1)} h`);

  setText("engineLoad", `${number(state.load).toFixed(1)}%`);

  const phase = state.mission_phase || "CRUISE";

  setText("missionPhase", phase);

  setText("sidebarMission", phase);
}

// ============================================================
// PREDICTION
// ============================================================

function updatePrediction(result) {
  const rul = result.rul || result.ml_rul || {};

  const reliability = result.mission_reliability || {};

  const degradation = result.degradation;

  const rulHours = number(rul.remaining_hours ?? result.rul_hours, 0);

  const reliabilityValue = number(
    reliability.reliability ?? result.reliability,
    0,
  );

  const degradationValue = number(
    typeof degradation === "object" ? degradation.level : degradation,
    0,
  );

  setText("rulValue", rulHours.toFixed(0));

  setText("reliabilityValue", (reliabilityValue * 100).toFixed(1));

  setText("degradationValue", degradationValue.toFixed(1));
}

// ============================================================
// MAIN API CALL
// ============================================================

async function fetchTwinState() {
  try {
    const response = await fetch(`${API_BASE}/api/v1/twin/state`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    console.log("Twin state:", data);

    processResult(data);
  } catch (error) {
    console.error("Twin state error:", error);
  }
}

// ============================================================
// PROCESS RESULT
// ============================================================

function processResult(result) {
  if (!result) return;

  const state = result.state || result;

  const health = number(result.health_index ?? state.health_index, 100);

  const anomaly = result.anomaly || {};

  const fault = result.fault || {};

  updateHealthRing(health);

  updateHealthStatus(health, fault.fault_type);

  updateTelemetry(state);

  updateFault(fault);

  updatePrediction(result);

  setText(
    "faultProbability",
    (number(anomaly.score, state.fault_probability || 0) * 100).toFixed(1),
  );

  updateChart(health);
}

// ============================================================
// HEALTH CHART
// ============================================================

const healthHistory = [];

function updateChart(health) {
  healthHistory.push(Math.max(0, Math.min(100, health)));

  if (healthHistory.length > 30) {
    healthHistory.shift();
  }

  const width = 800;
  const height = 220;

  const padding = 8;

  if (healthHistory.length < 2) {
    return;
  }

  const points = healthHistory.map((value, index) => {
    const x =
      padding + (index / (healthHistory.length - 1)) * (width - padding * 2);

    const y = height - padding - (value / 100) * (height - padding * 2);

    return [x, y];
  });

  const linePath = points
    .map(([x, y], index) => `${index === 0 ? "M" : "L"} ${x} ${y}`)
    .join(" ");

  const areaPath = `${linePath}
         L ${points[points.length - 1][0]} ${height}
         L ${points[0][0]} ${height}
         Z`;

  const line = document.getElementById("chartLine");

  const area = document.getElementById("chartArea");

  if (line) {
    line.setAttribute("d", linePath);
  }

  if (area) {
    area.setAttribute("d", areaPath);
  }
}

// ============================================================
// DEMO MODE
// ============================================================

let demoRPM = 4200;
let demoOilTemp = 92;
let demoEGT = 680;

function demoTelemetry() {
  demoRPM += (Math.random() - 0.5) * 80;

  demoOilTemp += (Math.random() - 0.5) * 0.8;

  demoEGT += (Math.random() - 0.5) * 5;

  setText("telemetryRPM", demoRPM.toFixed(0));

  setText("engineRPM", demoRPM.toFixed(0));

  setText("oilTemp", demoOilTemp.toFixed(1));

  setText("egt", demoEGT.toFixed(1));
}

// ============================================================
// START
// ============================================================

fetchTwinState();

// Refresh actual Digital Twin state every 2 seconds.

setInterval(fetchTwinState, 2000);

// Small telemetry animation.

setInterval(demoTelemetry, 1000);
