/**
 * API client for FixFit backend communication.
 */
import type { AnalysisResponse, FrameRequest } from "@/types/analysis";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Send a frame for analysis and receive form feedback.
 *
 * @param frameData - Base64 encoded JPEG image
 * @param timestamp - Unix timestamp when frame was captured
 * @returns Analysis response with form feedback
 */
export async function analyzeFrame(
  frameData: string,
  timestamp: number
): Promise<AnalysisResponse> {
  const request: FrameRequest = {
    frame_data: frameData,
    timestamp,
  };

  const response = await fetch(`${API_BASE_URL}/api/v1/analyze-frame`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Reset the current squat session (FSM state and rep counter).
 */
export async function resetSession(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/reset`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(`Reset failed: ${response.status}`);
  }
}

/**
 * Check backend health status.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

