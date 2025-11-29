"use client";

import { Play, Square, RotateCcw } from "lucide-react";

interface ControlPanelProps {
  isActive: boolean;
  onStart: () => void;
  onStop: () => void;
  onReset: () => void;
}

/**
 * ControlPanel component for session control buttons.
 */
export function ControlPanel({
  isActive,
  onStart,
  onStop,
  onReset,
}: ControlPanelProps) {
  return (
    <div className="flex items-center gap-4">
      {/* Start/Stop Button */}
      {!isActive ? (
        <button
          onClick={onStart}
          className="flex items-center gap-2 bg-primary hover:bg-primary-dark 
                     text-white font-semibold px-6 py-3 rounded-xl
                     transition-colors shadow-lg"
        >
          <Play className="w-5 h-5" />
          Start Session
        </button>
      ) : (
        <button
          onClick={onStop}
          className="flex items-center gap-2 bg-error hover:bg-error-dark 
                     text-white font-semibold px-6 py-3 rounded-xl
                     transition-colors shadow-lg"
        >
          <Square className="w-5 h-5" />
          Stop
        </button>
      )}

      {/* Reset Button */}
      <button
        onClick={onReset}
        className="flex items-center gap-2 bg-surface hover:bg-surface/80
                   text-text-primary font-semibold px-6 py-3 rounded-xl
                   border border-text-secondary/20 transition-colors"
      >
        <RotateCcw className="w-5 h-5" />
        Reset
      </button>
    </div>
  );
}

