from dataclasses import dataclass


@dataclass
class RULResult:
    remaining_hours: float
    confidence: float


class RULPredictor:
    """
    Baseline explainable Remaining Useful Life predictor.

    This prototype estimates RUL from current health and
    observed degradation rate.
    """

    def __init__(
        self,
        maximum_life_hours: float = 2000.0,
        minimum_health: float = 20.0,
    ) -> None:
        self.maximum_life_hours = maximum_life_hours
        self.minimum_health = minimum_health

    def predict(
        self,
        health_history: list[float],
        current_engine_hours: float,
    ) -> RULResult:

        if not health_history:
            return RULResult(
                remaining_hours=self.maximum_life_hours,
                confidence=0.20,
            )

        current_health = max(0.0, min(100.0, health_history[-1]))

        # Engine is already at the minimum health threshold.
        if current_health <= self.minimum_health:
            return RULResult(
                remaining_hours=0.0,
                confidence=0.90,
            )

        # Estimate degradation rate from the available history.
        if len(health_history) >= 2:
            health_drop = health_history[0] - health_history[-1]
            periods = len(health_history) - 1

            degradation_per_period = health_drop / periods

            if degradation_per_period > 0:
                remaining_health = current_health - self.minimum_health

                estimated_periods = remaining_health / degradation_per_period

                remaining_hours = max(
                    0.0,
                    min(
                        self.maximum_life_hours - current_engine_hours,
                        estimated_periods,
                    ),
                )

                confidence = min(
                    0.90,
                    0.50 + (0.05 * len(health_history)),
                )

                return RULResult(
                    remaining_hours=remaining_hours,
                    confidence=confidence,
                )

        # No measurable degradation yet.
        remaining_hours = max(
            0.0,
            self.maximum_life_hours - current_engine_hours,
        )

        return RULResult(
            remaining_hours=remaining_hours,
            confidence=0.40,
        )
