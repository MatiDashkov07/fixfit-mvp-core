"use client";

import { useState, useCallback } from "react";
import { CameraView } from "@/components/CameraView";
import { FeedbackDisplay } from "@/components/FeedbackDisplay";
import { ControlPanel } from "@/components/ControlPanel";
import { analyzeFrame } from "@/lib/api";
import type { AnalysisResponse } from "@/types/analysis";

export default function Home() {
  const [isActive, setIsActive] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFrameCapture = useCallback(async (frameData: string) => {
    if (!isActive) return;

    try {
      const result = await analyzeFrame(frameData, Date.now());
      setAnalysisResult(result);
      setError(null);
    } catch (err) {
      console.error("Frame analysis error:", err);
      setError(err instanceof Error ? err.message : "Analysis failed");
    }
  }, [isActive]);

  const handleStart = useCallback(() => {
    setIsActive(true);
    setError(null);
  }, []);

  const handleStop = useCallback(() => {
    setIsActive(false);
  }, []);

  const handleReset = useCallback(() => {
    setAnalysisResult(null);
    setError(null);
  }, []);

  return (
    <main className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-primary mb-2">FixFit</h1>
          <p className="text-text-secondary">AI-Powered Squat Form Analyzer</p>
        </header>

        {/* Main Content */}
        <div className="flex flex-col items-center gap-6">
          {/* Camera + Feedback Display */}
          <div className="relative">
            <CameraView
              isActive={isActive}
              onFrameCapture={handleFrameCapture}
            />
            {analysisResult && (
              <FeedbackDisplay
                feedback={analysisResult.feedback}
                isFormValid={analysisResult.is_form_valid}
                repCount={analysisResult.rep_count}
                correctionCue={analysisResult.correction_cue}
              />
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-error/20 border border-error rounded-lg px-4 py-2 text-error">
              {error}
            </div>
          )}

          {/* Control Panel */}
          <ControlPanel
            isActive={isActive}
            onStart={handleStart}
            onStop={handleStop}
            onReset={handleReset}
          />

          {/* Debug Info (Phase 0 only) */}
          {analysisResult && (
            <div className="w-full max-w-lg bg-surface rounded-lg p-4 text-sm font-mono">
              <h3 className="text-text-secondary mb-2">Debug Response:</h3>
              <pre className="text-text-primary overflow-x-auto">
                {JSON.stringify(analysisResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

