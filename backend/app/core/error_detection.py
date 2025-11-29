"""
Error detection for squat form analysis.
Detects: Knee valgus, insufficient depth.
"""
from app.models.response import Feedback
from app.core.squat_fsm import SquatPhase


# Threshold constants
VALGUS_RATIO_THRESHOLD = 0.85  # Below this indicates knee valgus
DEPTH_ANGLE_THRESHOLD = 90.0  # Must reach this angle for valid depth


def check_knee_valgus(valgus_ratio: float, current_state: SquatPhase) -> Feedback:
    """
    Check for knee valgus (knees caving inward).
    
    Only checks during active squat phases (DESCENDING, BOTTOM, ASCENDING).
    
    Args:
        valgus_ratio: Ratio of knee distance to ankle distance
        current_state: Current FSM state
    
    Returns:
        KNEE_VALGUS if detected, PERFECT otherwise
    """
    pass  # TODO: Implement in Phase 1


def check_depth(depth_reached: bool, current_state: SquatPhase) -> Feedback:
    """
    Check if squat reached sufficient depth.
    
    Only relevant when transitioning from ASCENDING to STANDING.
    
    Args:
        depth_reached: Whether depth threshold was reached this rep
        current_state: Current FSM state
    
    Returns:
        DEPTH_FAIL if insufficient depth on ascent, PERFECT otherwise
    """
    pass  # TODO: Implement in Phase 1


def get_correction_cue(feedback: Feedback) -> str | None:
    """
    Get human-readable correction cue for feedback type.
    
    Args:
        feedback: Feedback enum value
    
    Returns:
        Correction string or None if form is perfect
    """
    cues = {
        Feedback.PERFECT: None,
        Feedback.KNEE_VALGUS: "WIDEN KNEES",
        Feedback.DEPTH_FAIL: "GO DEEPER",
    }
    return cues.get(feedback)

