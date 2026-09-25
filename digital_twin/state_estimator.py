from digital_twin.twin_state import EngineState


class StateEstimator:
    """
    Estimates derived engine operating states from sensor measurements.
    """

    def estimate(self, state: EngineState) -> EngineState:
        """
        Calculate derived engine parameters and update the state.
        """

        # Estimate mechanical power from torque and RPM.
        # Power(kW) = Torque(Nm) * RPM / 9550
        state.power_kw = (state.torque * state.rpm) / 9550

        # Estimate engine load using RPM.
        # This is a simplified prototype relationship.
        if state.rpm > 0:
            state.load = min(100.0, max(0.0, (state.torque / 100.0) * 100.0))
        else:
            state.load = 0.0

        return state
