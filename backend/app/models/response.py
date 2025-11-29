"""
Response models for FixFit API
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SquatState(str, Enum):
    """Finite state machine states for squat tracking."""
    STANDING = "STANDING"
    DESCENDING = "DESCENDING"
    BOTTOM = "BOTTOM"
    ASCENDING = "ASCENDING"


class Feedback(str, Enum):
    """Form feedback types."""
    PERFECT = "PERFECT"
    KNEE_VALGUS = "KNEE_VALGUS"
    DEPTH_FAIL = "DEPTH_FAIL"


class JointAngles(BaseModel):
    """Joint angle measurements in degrees."""
    left_knee: float = Field(..., ge=0, le=180, description="Left knee angle in degrees")
    right_knee: float = Field(..., ge=0, le=180, description="Right knee angle in degrees")
    average: float = Field(..., ge=0, le=180, description="Average knee angle in degrees")


class ErrorDetails(BaseModel):
    """Detailed error detection information."""
    knee_valgus_ratio: float = Field(
        ...,
        ge=0,
        description="Ratio of knee distance to ankle distance (< 0.85 indicates valgus)",
    )
    depth_threshold_reached: bool = Field(
        ...,
        description="Whether squat reached parallel depth (avg knee angle < 90°)",
    )


class ProcessingInfo(BaseModel):
    """Processing metadata for performance monitoring."""
    timestamp: float = Field(..., description="Server timestamp when processing completed")
    processing_time_ms: float = Field(..., ge=0, description="Total processing time in milliseconds")


class AnalysisResponse(BaseModel):
    """Complete response payload for frame analysis."""
    
    current_state: SquatState = Field(..., description="Current FSM state")
    is_form_valid: bool = Field(..., description="Whether current form is acceptable")
    correction_cue: Optional[str] = Field(
        None,
        description="Human-readable correction instruction (null if form is valid)",
    )
    rep_count: int = Field(..., ge=0, description="Total valid repetitions completed")
    feedback: Feedback = Field(..., description="Form feedback category")
    joint_angles: JointAngles = Field(..., description="Measured joint angles")
    error_details: ErrorDetails = Field(..., description="Detailed error detection data")
    processing: ProcessingInfo = Field(..., description="Processing metadata")

    model_config = {
        "json_schema_extra": {
            "example": {
                "current_state": "STANDING",
                "is_form_valid": True,
                "correction_cue": None,
                "rep_count": 0,
                "feedback": "PERFECT",
                "joint_angles": {
                    "left_knee": 180.0,
                    "right_knee": 180.0,
                    "average": 180.0,
                },
                "error_details": {
                    "knee_valgus_ratio": 1.0,
                    "depth_threshold_reached": False,
                },
                "processing": {
                    "timestamp": 1700000000.123,
                    "processing_time_ms": 45.5,
                },
            }
        }
    }

