from dataclasses import dataclass


@dataclass
class ReliabilityResult:
    reliability: float
    risk_level: str
    explanation: str


class MissionReliabilityCalculator:
    """
    Calculates a simple explainable mission reliability score.
    """

    def calculate(
        self,
        health_index: float,
        fault_probability: float,
        rul_hours: float,
        mission_duration_hours: float,
    ) -> ReliabilityResult:

        health_index = max(0.0, min(100.0, health_index))
        fault_probability = max(0.0, min(1.0, fault_probability))
        rul_hours = max(0.0, rul_hours)
        mission_duration_hours = max(0.0, mission_duration_hours)

        # Health contribution: 0-1
        health_score = health_index / 100.0

        # Fault contribution: 1 = no fault risk
        fault_score = 1.0 - fault_probability

        # RUL contribution
        if mission_duration_hours == 0:
            rul_score = 1.0
        else:
            rul_score = min(1.0, rul_hours / mission_duration_hours)

        # Weighted reliability score
        reliability = 0.5 * health_score + 0.3 * fault_score + 0.2 * rul_score

        reliability = max(0.0, min(1.0, reliability))

        reliability_percent = reliability * 100.0

        if reliability_percent >= 80:
            risk_level = "LOW"
        elif reliability_percent >= 60:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        explanation = (
            f"Health contribution: {health_score:.2f}, "
            f"fault-risk contribution: {fault_score:.2f}, "
            f"RUL contribution: {rul_score:.2f}."
        )

        return ReliabilityResult(
            reliability=reliability_percent,
            risk_level=risk_level,
            explanation=explanation,
        )
