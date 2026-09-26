from digital_twin.twin_state import EngineState


class HealthIndexCalculator:
    """
    Calculates an explainable engine health index from 0 to 100.
    """

    def calculate(self, state: EngineState) -> float:
        """
        Calculate health based on normalized deviations
        from simplified operating limits.
        """

        penalties = []

        # Oil temperature
        if state.oil_temperature > 100:
            penalties.append(min(20.0, (state.oil_temperature - 100) * 0.5))

        # Cylinder head temperature
        if state.cylinder_head_temperature > 180:
            penalties.append(min(20.0, (state.cylinder_head_temperature - 180) * 0.4))

        # EGT
        if state.egt > 700:
            penalties.append(min(20.0, (state.egt - 700) * 0.2))

        # Oil pressure
        if 0 < state.oil_pressure < 3.0:
            penalties.append(min(20.0, (3.0 - state.oil_pressure) * 5.0))

        # Vibration
        if state.vibration > 1.0:
            penalties.append(min(20.0, (state.vibration - 1.0) * 10.0))

        total_penalty = sum(penalties)

        health = max(0.0, min(100.0, 100.0 - total_penalty))

        state.health_index = health

        return health
