"""
MediaPipe Pose Landmarker wrapper with singleton pattern.
"""
import numpy as np
from typing import Optional

# MediaPipe landmark indices for squat analysis
LANDMARK_INDICES = {
    "LEFT_HIP": 23,
    "RIGHT_HIP": 24,
    "LEFT_KNEE": 25,
    "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27,
    "RIGHT_ANKLE": 28,
}


class PoseDetector:
    """
    Singleton wrapper for MediaPipe Pose detection.
    
    Uses model_complexity=1 (Full) for balance of speed and accuracy.
    """
    
    _instance: Optional["PoseDetector"] = None
    
    def __new__(cls) -> "PoseDetector":
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize MediaPipe Pose if not already done."""
        if self._initialized:
            return
        
        # TODO: Initialize MediaPipe Pose in Phase 1
        # self.pose = mp.solutions.pose.Pose(
        #     model_complexity=1,
        #     min_detection_confidence=0.5,
        #     min_tracking_confidence=0.5,
        # )
        self._initialized = True
    
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract pose landmarks from image.
        
        Args:
            image: RGB image as numpy array (H, W, 3)
        
        Returns:
            Array of 33 landmarks with (x, y, z, visibility) or None if no pose detected
        """
        pass  # TODO: Implement in Phase 1
    
    def get_landmark_confidence(self, landmarks: np.ndarray) -> float:
        """
        Calculate average visibility/confidence of key landmarks.
        
        Args:
            landmarks: Array of 33 landmarks
        
        Returns:
            Average confidence score (0.0 - 1.0)
        """
        pass  # TODO: Implement in Phase 1


# Global singleton instance
pose_detector = PoseDetector()

