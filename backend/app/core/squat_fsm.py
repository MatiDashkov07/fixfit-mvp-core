"""
Finite State Machine for squat phase tracking.
Tracks: STANDING → DESCENDING → BOTTOM → ASCENDING → STANDING
"""
from enum import Enum
from typing import Optional


class SquatPhase(str, Enum):
    """States in the squat movement cycle."""
    STANDING = "STANDING"
    DESCENDING = "DESCENDING"
    BOTTOM = "BOTTOM"
    ASCENDING = "ASCENDING"


class SquatFSM:
    """
    Finite State Machine for tracking squat phases and counting reps.
    
    Transition thresholds:
    - STANDING → DESCENDING: avg_knee_angle < 170°
    - DESCENDING → BOTTOM: avg_knee_angle < 90°
    - BOTTOM → ASCENDING: avg_knee_angle > 100°
    - ASCENDING → STANDING: avg_knee_angle > 170° (increment rep if valid)
    """
    
    # Angle thresholds in degrees
    STANDING_THRESHOLD = 170.0
    BOTTOM_THRESHOLD = 90.0
    ASCENDING_THRESHOLD = 100.0
    
    def __init__(self) -> None:
        """Initialize FSM in STANDING state with zero reps."""
        self.current_state: SquatPhase = SquatPhase.STANDING
        self.rep_count: int = 0
        self.depth_threshold_reached: bool = False
        self._current_rep_valid: bool = True
    
    def process_frame(self, avg_knee_angle: float, is_form_valid: bool = True) -> SquatPhase:
        """
        Process a single frame and update state machine.
        
        Args:
            avg_knee_angle: Average of left and right knee angles in degrees
            is_form_valid: Whether current form passes error checks
        
        Returns:
            Current state after processing
        """
        pass  # TODO: Implement in Phase 1
    
    def reset(self) -> None:
        """Reset FSM to initial state."""
        self.current_state = SquatPhase.STANDING
        self.rep_count = 0
        self.depth_threshold_reached = False
        self._current_rep_valid = True
    
    def get_state(self) -> dict:
        """
        Get current FSM state as dictionary.
        
        Returns:
            Dict with current_state, rep_count, depth_threshold_reached
        """
        return {
            "current_state": self.current_state.value,
            "rep_count": self.rep_count,
            "depth_threshold_reached": self.depth_threshold_reached,
        }

