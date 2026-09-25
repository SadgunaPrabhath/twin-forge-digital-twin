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
from ml.rul_pipeline import RULPipeline


class DigitalTwinEngine:
    """
    Orchestrates the complete digital twin pipeline.

    Components:
    - Digital Twin state management
    - State estimation
    - Health index calculation
    - Anomaly detection
    - Fault classification
    - Degradation tracking
    - Baseline RUL prediction
    - ML-based RUL prediction
    - Mission reliability estimation
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

        # Existing baseline RUL predictor.
        # Kept for compatibility with the existing engine/tests.
        self.rul_predictor = RULPredictor()

        # New ML RUL pipeline.
        self.rul_pipeline = RULPipeline(
            training_samples=1000,
            seed=42,
        )

        self.rul_pipeline.train()

        self.reliability_calculator = MissionReliabilityCalculator()

        self.mission_duration_hours = mission_duration_hours

    def process(
        self,
        sensor_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process one sensor observation through
        the complete Digital Twin pipeline.
        """

        # -------------------------------------------------
        # 1. Update Digital Twin
        # -------------------------------------------------

        state = self.twin.update(sensor_data)

        # -------------------------------------------------
        # 2. Estimate derived engine state
        # -------------------------------------------------

        state = self.state_estimator.estimate(state)

        # -------------------------------------------------
        # 3. Calculate health
        # -------------------------------------------------

        health = self.health_calculator.calculate(state)

        # -------------------------------------------------
        # 4. Detect anomalies
        # -------------------------------------------------

        anomaly = self.anomaly_detector.detect(state)

        # -------------------------------------------------
        # 5. Classify fault
        # -------------------------------------------------

        fault = self.fault_classifier.classify(state)

        # -------------------------------------------------
        # 6. Track degradation
        # -------------------------------------------------

        degradation = self.degradation_tracker.update(health)

        # -------------------------------------------------
        # 7A. Existing baseline RUL prediction
        # -------------------------------------------------

        rul = self.rul_predictor.predict(
            health_history=self.degradation_tracker.history,
            current_engine_hours=state.engine_hours,
        )

        # -------------------------------------------------
        # 7B. New ML RUL prediction
        # -------------------------------------------------

        ml_rul = self.rul_pipeline.predict_telemetry(state)

        # -------------------------------------------------
        # 8. Calculate mission reliability
        # -------------------------------------------------

        reliability = self.reliability_calculator.calculate(
            health_index=health,
            fault_probability=anomaly.score,
            rul_hours=rul.remaining_hours,
            mission_duration_hours=self.mission_duration_hours,
        )

        # -------------------------------------------------
        # 9. Store important outputs in Digital Twin state
        # -------------------------------------------------

        state.degradation_level = degradation

        state.fault_probability = anomaly.score

        state.fault_type = fault.fault_type

        # Keep the existing baseline RUL in EngineState
        # for compatibility.
        state.rul_hours = rul.remaining_hours

        state.mission_reliability = reliability.reliability

        # -------------------------------------------------
        # 10. Return complete assessment
        # -------------------------------------------------

        return {
            "state": state,
            "health_index": health,
            "anomaly": anomaly,
            "fault": fault,
            "degradation": degradation,
            # Existing RUL object.
            "rul": rul,
            # New ML RUL prediction.
            "ml_rul": ml_rul,
            "mission_reliability": reliability,
        }
