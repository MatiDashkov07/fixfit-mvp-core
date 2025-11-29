/**
 * TypeScript types matching backend API contract.
 * These types ensure type safety for all API responses.
 */

export enum SquatState {
  STANDING = "STANDING",
  DESCENDING = "DESCENDING",
  BOTTOM = "BOTTOM",
  ASCENDING = "ASCENDING",
}

export enum Feedback {
  PERFECT = "PERFECT",
  KNEE_VALGUS = "KNEE_VALGUS",
  DEPTH_FAIL = "DEPTH_FAIL",
}

export interface JointAngles {
  left_knee: number;
  right_knee: number;
  average: number;
}

export interface ErrorDetails {
  knee_valgus_ratio: number;
  depth_threshold_reached: boolean;
}

export interface ProcessingInfo {
  timestamp: number;
  processing_time_ms: number;
}

export interface AnalysisResponse {
  current_state: SquatState;
  is_form_valid: boolean;
  correction_cue: string | null;
  rep_count: number;
  feedback: Feedback;
  joint_angles: JointAngles;
  error_details: ErrorDetails;
  processing: ProcessingInfo;
}

export interface FrameRequest {
  frame_data: string;
  timestamp: number;
}

