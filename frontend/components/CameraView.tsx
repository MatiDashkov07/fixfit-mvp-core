"use client";

import { useRef, useEffect, useCallback } from "react";

interface CameraViewProps {
  isActive: boolean;
  onFrameCapture: (frameData: string) => void;
  captureIntervalMs?: number;
}

/**
 * CameraView component for webcam access and frame capture.
 * Captures frames at specified interval when active.
 */
export function CameraView({
  isActive,
  onFrameCapture,
  captureIntervalMs = 100, // 10 FPS for Phase 0, increase to 33ms (30 FPS) later
}: CameraViewProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize camera stream
  const initCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: "user",
        },
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
    } catch (error) {
      console.error("Camera access error:", error);
      // TODO: Show user-friendly permission error in Phase 1
    }
  }, []);

  // Capture single frame as Base64 JPEG
  const captureFrame = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas || video.readyState !== 4) {
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    ctx.drawImage(video, 0, 0);

    // Convert to Base64 JPEG (80% quality for bandwidth optimization)
    const frameData = canvas.toDataURL("image/jpeg", 0.8);

    // Send to parent for API call
    onFrameCapture(frameData);
  }, [onFrameCapture]);

  // Start/stop capture interval based on isActive
  useEffect(() => {
    if (isActive) {
      // Start capturing frames
      intervalRef.current = setInterval(captureFrame, captureIntervalMs);
    } else {
      // Stop capturing
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isActive, captureFrame, captureIntervalMs]);

  // Initialize camera on mount
  useEffect(() => {
    initCamera();

    return () => {
      // Cleanup: stop stream on unmount
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, [initCamera]);

  return (
    <div className="video-container">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="w-full h-full object-cover"
      />
      {/* Hidden canvas for frame capture */}
      <canvas ref={canvasRef} className="hidden" />
      
      {/* Recording indicator */}
      {isActive && (
        <div className="absolute top-4 left-4 flex items-center gap-2 bg-black/50 rounded-full px-3 py-1">
          <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
          <span className="text-white text-sm font-medium">ANALYZING</span>
        </div>
      )}
    </div>
  );
}

