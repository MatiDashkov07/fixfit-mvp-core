"use client";

import { Feedback } from "@/types/analysis";

interface FeedbackDisplayProps {
  feedback: Feedback;
  isFormValid: boolean;
  repCount: number;
  correctionCue: string | null;
}

/**
 * FeedbackDisplay component for showing real-time form feedback.
 * Overlays on top of camera view.
 */
export function FeedbackDisplay({
  feedback,
  isFormValid,
  repCount,
  correctionCue,
}: FeedbackDisplayProps) {
  const feedbackConfig = {
    [Feedback.PERFECT]: {
      text: "GOOD FORM",
      bgColor: "bg-primary/80",
      textColor: "text-white",
    },
    [Feedback.KNEE_VALGUS]: {
      text: "WIDEN KNEES",
      bgColor: "bg-error/80",
      textColor: "text-white",
    },
    [Feedback.DEPTH_FAIL]: {
      text: "GO DEEPER",
      bgColor: "bg-error/80",
      textColor: "text-white",
    },
  };

  const config = feedbackConfig[feedback] || feedbackConfig[Feedback.PERFECT];

  return (
    <>
      {/* Rep Counter - Top Right */}
      <div className="absolute top-4 right-4 bg-black/60 rounded-xl px-4 py-2">
        <div className="text-center">
          <div className="text-5xl font-bold text-white">{repCount}</div>
          <div className="text-xs text-text-secondary uppercase tracking-wider">
            Reps
          </div>
        </div>
      </div>

      {/* Feedback Badge - Bottom Center */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2">
        <div
          className={`
            ${config.bgColor} 
            ${config.textColor}
            ${!isFormValid ? "feedback-error" : ""}
            rounded-full px-6 py-3 font-bold text-lg
            shadow-lg
          `}
        >
          {correctionCue || config.text}
        </div>
      </div>
    </>
  );
}

