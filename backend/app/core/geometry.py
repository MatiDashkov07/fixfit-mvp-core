"""
Geometry calculations for squat form analysis.
Uses Law of Cosines for angle calculations.
"""
import numpy as np


def calculate_angle(
    point_a: np.ndarray,
    point_b: np.ndarray,
    point_c: np.ndarray,
) -> float:
    """
    Calculate angle at point_b formed by points a-b-c using Law of Cosines.
    
    Args:
        point_a: First point coordinates [x, y, z]
        point_b: Vertex point coordinates [x, y, z] (angle measured here)
        point_c: Third point coordinates [x, y, z]
    
    Returns:
        Angle in degrees (0-180)
    """
    pass  # TODO: Implement in Phase 1


def calculate_knee_angle(
    hip: np.ndarray,
    knee: np.ndarray,
    ankle: np.ndarray,
) -> float:
    """
    Calculate knee angle using hip-knee-ankle landmarks.
    
    Args:
        hip: Hip landmark [x, y, z]
        knee: Knee landmark [x, y, z]
        ankle: Ankle landmark [x, y, z]
    
    Returns:
        Knee angle in degrees (180 = fully extended, 90 = parallel squat)
    """
    pass  # TODO: Implement in Phase 1


def get_knee_angles(landmarks: np.ndarray) -> tuple[float, float]:
    """
    Extract both knee angles from MediaPipe landmarks.
    
    Args:
        landmarks: Array of 33 MediaPipe pose landmarks
    
    Returns:
        Tuple of (left_knee_angle, right_knee_angle) in degrees
    """
    pass  # TODO: Implement in Phase 1


def euclidean_distance(point_a: np.ndarray, point_b: np.ndarray) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point_a: First point [x, y, z]
        point_b: Second point [x, y, z]
    
    Returns:
        Distance as float
    """
    pass  # TODO: Implement in Phase 1


def calculate_valgus_ratio(landmarks: np.ndarray) -> float:
    """
    Calculate knee valgus ratio (knee distance / ankle distance).
    
    Ratio < 0.85 indicates knee valgus (knees caving inward).
    Ratio ~1.0 indicates proper knee tracking.
    
    Args:
        landmarks: Array of 33 MediaPipe pose landmarks
    
    Returns:
        Valgus ratio as float
    """
    pass  # TODO: Implement in Phase 1

