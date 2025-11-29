"""
Request models for FixFit API
"""
from pydantic import BaseModel, Field


class FrameRequest(BaseModel):
    """Request payload for frame analysis endpoint."""
    
    frame_data: str = Field(
        ...,
        description="Base64 encoded JPEG image data",
        min_length=1,
    )
    timestamp: float = Field(
        ...,
        description="Unix timestamp when frame was captured",
        gt=0,
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "frame_data": "/9j/4AAQSkZJRgABAQAAAQABAAD...",
                "timestamp": 1700000000.123,
            }
        }
    }

