"""
API Routes for FixFit
"""
import time
from fastapi import APIRouter, HTTPException

from app.models.request import FrameRequest
from app.models.response import (
    AnalysisResponse,
    SquatState,
    Feedback,
    JointAngles,
    ErrorDetails,
    ProcessingInfo,
)

router = APIRouter()


@router.post("/analyze-frame", response_model=AnalysisResponse)
async def analyze_frame(request: FrameRequest) -> AnalysisResponse:
    """
    Analyze a single video frame for squat form.
    
    PHASE 0: Returns dummy data to prove end-to-end connectivity.
    TODO: Replace with actual MediaPipe + FSM logic in Phase 1.
    """
    start_time = time.perf_counter()
    
    # Validate input exists (Pydantic handles most validation)
    if not request.frame_data:
        raise HTTPException(status_code=400, detail="Missing frame_data")
    
    # PHASE 0: Return dummy response to test API contract
    processing_time_ms = (time.perf_counter() - start_time) * 1000
    
    return AnalysisResponse(
        current_state=SquatState.STANDING,
        is_form_valid=True,
        correction_cue=None,
        rep_count=0,
        feedback=Feedback.PERFECT,
        joint_angles=JointAngles(
            left_knee=180.0,
            right_knee=180.0,
            average=180.0,
        ),
        error_details=ErrorDetails(
            knee_valgus_ratio=1.0,
            depth_threshold_reached=False,
        ),
        processing=ProcessingInfo(
            timestamp=time.time(),
            processing_time_ms=processing_time_ms,
        ),
    )


@router.post("/reset")
async def reset_session() -> dict:
    """
    Reset the current squat session (FSM state and rep counter).
    
    PHASE 0: Returns dummy acknowledgment.
    TODO: Implement actual FSM reset in Phase 1.
    """
    return {"status": "reset", "rep_count": 0}

