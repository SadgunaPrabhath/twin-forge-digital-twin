from typing import Any, Dict

from digital_twin.anomaly_detector import AnomalyDetector
from digital_twin.degradation import DegradationTracker
from digital_twin.fault_classifier import FaultClassifier
from digital_twin.health_index import HealthIndexCalculator
from digital_twin.mission_reliability import (
    MissionReliabilityCalculator,
)
from digital_twin.rul_predictor import RULPredictor
from digital_twin.state_estimator import StateEstimator
from digital_twin.twin import DigitalTwin


class DigitalTwinEngine:
    """
    Orchestrates the complete digital twin pipeline.
    """

    def __init__(
        self,
        mission_duration_hours: float = 1.0,
    ) -> None:

        self.twin = DigitalTwin()
        self.state_estimator = StateEstimator()
        self.health_calculator = HealthIndexCalculator()
        self.anomaly_detector = AnomalyDetector()
        self.fault_classifier = FaultClassifier()
        self.degradation_tracker = DegradationTracker()

        self.rul_predictor = RULPredictor()
        self.reliability_calculator = MissionReliabilityCalculator()

        self.mission_duration_hours = mission_duration_hours

    def process(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process one sensor observation through the entire pipeline.
        """

        # 1. Update Digital Twin
        state = self.twin.update(sensor_data)

        # 2. Estimate derived engine state
        state = self.state_estimator.estimate(state)

        # 3. Calculate health
        health = self.health_calculator.calculate(state)

        # 4. Detect anomalies
        anomaly = self.anomaly_detector.detect(state)

        # 5. Classify fault
        fault = self.fault_classifier.classify(state)

        # 6. Track degradation
        degradation = self.degradation_tracker.update(health)

        # 7. Predict RUL
        rul = self.rul_predictor.predict(
            health_history=self.degradation_tracker.history,
            current_engine_hours=state.engine_hours,
        )

        # 8. Calculate mission reliability
        reliability = self.reliability_calculator.calculate(
            health_index=health,
            fault_probability=anomaly.score,
            rul_hours=rul.remaining_hours,
            mission_duration_hours=self.mission_duration_hours,
        )

        # Store important outputs in the state
        state.degradation_level = degradation
        state.fault_probability = anomaly.score
        state.fault_type = fault.fault_type
        state.rul_hours = rul.remaining_hours
        state.mission_reliability = reliability.reliability

        return {
            "state": state,
            "health_index": health,
            "anomaly": anomaly,
            "fault": fault,
            "degradation": degradation,
            "rul": rul,
            "mission_reliability": reliability,
        }
