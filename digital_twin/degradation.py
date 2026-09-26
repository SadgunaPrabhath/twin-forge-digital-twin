from dataclasses import dataclass, field
from typing import List


@dataclass
class DegradationTracker:
    """
    Tracks engine degradation over time.
    """

    history: List[float] = field(default_factory=list)

    def update(self, health_index: float) -> float:
        """
        Store the current health value and return degradation level.
        """

        health_index = max(0.0, min(100.0, health_index))

        self.history.append(health_index)

        degradation = 100.0 - health_index

        return degradation

    @property
    def current_degradation(self) -> float:
        """
        Return the latest degradation value.
        """

        if not self.history:
            return 0.0

        return 100.0 - self.history[-1]

    @property
    def average_health(self) -> float:
        """
        Return average historical health.
        """

        if not self.history:
            return 100.0

        return sum(self.history) / len(self.history)
