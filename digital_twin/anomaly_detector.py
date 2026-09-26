from dataclasses import dataclass
from typing import List

from digital_twin.twin_state import EngineState


@dataclass
class AnomalyResult:
    is_anomaly: bool
    score: float
    reasons: List[str]


class AnomalyDetector:
    """
    Detects abnormal engine operating conditions using
    transparent sensor thresholds.
    """

    def detect(self, state: EngineState) -> AnomalyResult:
        reasons = []
        score = 0.0

        # Temperature anomaly
        if state.oil_temperature > 110:
            reasons.append("High oil temperature")
            score += 0.20

        # Cylinder head temperature anomaly
        if state.cylinder_head_temperature > 200:
            reasons.append("High cylinder head temperature")
            score += 0.20

        # EGT anomaly
        if state.egt > 750:
            reasons.append("High exhaust gas temperature")
            score += 0.20

        # Oil pressure anomaly
        if 0 < state.oil_pressure < 2.5:
            reasons.append("Low oil pressure")
            score += 0.20

        # Vibration anomaly
        if state.vibration > 1.5:
            reasons.append("High vibration")
            score += 0.20

        score = min(1.0, score)

        return AnomalyResult(
            is_anomaly=score > 0.0,
            score=score,
            reasons=reasons,
        )
