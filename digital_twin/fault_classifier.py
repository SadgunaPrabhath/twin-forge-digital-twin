from dataclasses import dataclass

from digital_twin.twin_state import EngineState


@dataclass
class FaultResult:
    fault_type: str
    confidence: float
    explanation: str


class FaultClassifier:
    """
    Explainable rule-based fault classifier.

    This is the initial prototype.
    A trained ML classifier can replace this layer later.
    """

    def classify(self, state: EngineState) -> FaultResult:

        # Severe overheating
        if state.oil_temperature > 110 and state.cylinder_head_temperature > 200:
            return FaultResult(
                fault_type="OVERHEATING",
                confidence=0.95,
                explanation=(
                    "Oil temperature and cylinder head temperature "
                    "are above expected operating limits."
                ),
            )

        # Low lubrication pressure
        if 0 < state.oil_pressure < 2.5:
            return FaultResult(
                fault_type="LOW_OIL_PRESSURE",
                confidence=0.95,
                explanation=(
                    "Oil pressure is below the minimum expected operating range."
                ),
            )

        # Excessive vibration
        if state.vibration > 1.5:
            return FaultResult(
                fault_type="HIGH_VIBRATION",
                confidence=0.90,
                explanation=(
                    "Engine vibration is significantly above "
                    "the expected operating level."
                ),
            )

        # High exhaust temperature
        if state.egt > 750:
            return FaultResult(
                fault_type="COMBUSTION_ANOMALY",
                confidence=0.85,
                explanation=(
                    "Exhaust gas temperature is above the expected operating limit."
                ),
            )

        return FaultResult(
            fault_type="NORMAL",
            confidence=0.99,
            explanation="No known fault condition detected.",
        )
