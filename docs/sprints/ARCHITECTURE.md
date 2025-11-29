ARCHITECTURE.md
FixFit MVP - System Architecture
Version: 1.0
Status: Ready for Implementation
Timeline: 24 hours

EXECUTIVE SUMMARY
FixFit is a real-time AI squat form analyzer that provides instant biomechanical feedback through computer vision. The system processes webcam frames at 20-30 FPS with sub-150ms latency, detecting form errors (knee valgus, insufficient depth) and counting valid repetitions. Built as a containerized monorepo with Python/FastAPI backend and Next.js frontend, the MVP focuses exclusively on squat analysis with zero external dependencies.

1. SYSTEM OVERVIEW
1.1 Architecture Pattern
┌─────────────────┐         ┌─────────────────┐
│   FRONTEND      │         │    BACKEND      │
│   (Next.js)     │         │   (FastAPI)     │
│                 │         │                 │
│  CameraView     │  HTTP   │  MediaPipe      │
│      ↓          │  POST   │  Pose Detector  │
│  Base64 Encode  │────────→│       ↓         │
│      ↓          │         │  Geometry       │
│  API Client     │         │  Calculations   │
│      ↓          │         │       ↓         │
│  SkeletonOverlay│←────────│  FSM Logic      │
│  FeedbackDisplay│  JSON   │       ↓         │
│                 │         │  JSON Response  │
└─────────────────┘         └─────────────────┘
1.2 Data Flow

Capture: Frontend captures webcam frame (640x480 JPEG at 80% quality)
Encode: Convert to Base64 string in browser
Request: POST to /api/v1/analyze-frame with timestamp
Detect: MediaPipe extracts 33 body landmarks (CPU inference)
Calculate: Compute joint angles using 3D geometry
Analyze: FSM determines state + error detection logic evaluates form
Respond: Return JSON with state, feedback, angles, rep count
Render: Frontend displays skeleton overlay (green/red) + text feedback

Latency Budget:

Frame encoding (browser): 10-15ms
Network (localhost): 1-2ms
MediaPipe inference: 40-60ms
Geometry calculations: 3-5ms
FSM + error detection: 2-3ms
JSON serialization: 5-10ms
Total: 80-95ms (well under 150ms target)


2. MONOREPO STRUCTURE
fixfit/
├── .gitignore
├── .env.example
├── docker-compose.yml              # Orchestrates both services
├── README.md                       # 5-minute quickstart
│
├── ARCHITECTURE.md                 # This file
├── API_CONTRACT.md                 # JSON schemas
├── TASKS.md                        # Sprint plan
│
├── backend/
│   ├── Dockerfile                  # Python 3.10 + MediaPipe
│   ├── .dockerignore
│   ├── requirements.txt            # Pinned dependencies
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app + CORS config
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # POST /analyze-frame endpoint
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── squat_fsm.py        # State machine (STANDING → DESCENDING → etc.)
│   │   │   ├── geometry.py         # angle_between_points(), valgus_ratio()
│   │   │   └── error_detection.py  # check_knee_valgus(), check_depth()
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── request.py          # Pydantic: FrameRequest
│   │   │   └── response.py         # Pydantic: AnalysisResponse, Feedback enum
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── mediapipe_wrapper.py # MediaPipe singleton + landmark extraction
│   │       └── image_processing.py  # base64_to_image(), resize_frame()
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_geometry.py        # Unit tests for angle calculations
│       └── test_fsm.py             # State transition tests
│
└── frontend/
    ├── Dockerfile                  # Node 20 Alpine
    ├── .dockerignore
    ├── package.json
    ├── tsconfig.json               # Strict TypeScript
    ├── tailwind.config.ts
    ├── next.config.js              # API proxy to backend
    │
    ├── app/
    │   ├── layout.tsx              # Root layout
    │   ├── page.tsx                # Main squat analysis page
    │   └── globals.css             # Tailwind imports
    │
    ├── components/
    │   ├── ui/                     # Shadcn components (button, card, alert)
    │   ├── CameraView.tsx          # Webcam access + frame capture
    │   ├── SkeletonOverlay.tsx     # Canvas rendering of landmarks
    │   ├── FeedbackDisplay.tsx     # Text feedback + rep counter
    │   └── ControlPanel.tsx        # Start/stop/reset buttons
    │
    ├── lib/
    │   ├── api.ts                  # analyzeFrame() function
    │   └── utils.ts                # cn() helper for Tailwind
    │
    └── types/
        └── analysis.ts             # TypeScript interfaces matching API contract

3. TECHNOLOGY STACK
3.1 Backend
ComponentVersionRationalePython3.10MediaPipe compatibility requirementFastAPI0.104.1Async/await for I/O, auto OpenAPI docsMediaPipe0.10.8Stable CPU pose detection, no GPU neededOpenCV4.8.1.78 (headless)Image processing without GUI dependenciesNumPy1.26.2Vectorized geometry calculationsPydantic2.5.0Request/response validation with typesUvicorn0.24.0ASGI server with hot reload support
Key Decisions:

CPU-only MediaPipe: GPU adds Docker complexity (CUDA layers, driver compatibility) for minimal speed gain (<20ms). CPU inference achieves 40-60ms, well within budget.
opencv-python-headless: Removes X11/GUI dependencies, reducing image size by 200MB.
No database: Session state (rep count, FSM) maintained in memory. Acceptable for MVP, enables horizontal scaling.

3.2 Frontend
ComponentVersionRationaleNext.js14.0.4App Router for modern React patternsReact18.2.0Industry standard, stableTypeScript5.3.3Type safety for API contract enforcementTailwind CSS3.4.0Rapid styling, mobile-first utilitiesShadcn/UILatestConsistent component library, accessibleLucide React0.294.0Icon system
Key Decisions:

No WebSocket: HTTP polling at 30 FPS (33ms interval) adds negligible latency vs WebSocket complexity. Stateless backend simplifies deployment.
Canvas for skeleton: HTML5 Canvas provides 60 FPS rendering, sufficient for 30 FPS input stream.
No state management library: React hooks (useState, useEffect) sufficient for single-page app.

3.3 Infrastructure
ComponentPurposeDockerConsistent dev/prod environmentsDocker ComposeLocal orchestration, hot reloadDebian 12 Bookworm SlimBase image for backend (Python official image)Node 20 AlpineMinimal frontend base image

4. DOCKER STRATEGY
4.1 Backend Dockerfile (Critical Notes)
dockerfileFROM python:3.10-slim-bookworm AS base

# CRITICAL: MediaPipe requires OpenGL libraries even for CPU inference
# Without these, you'll get: ImportError: libGL.so.1: cannot open shared object file
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \      # ← THIS LINE IS ESSENTIAL
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Verify MediaPipe loads (fail fast if broken)
RUN python -c "import mediapipe as mp; print('MediaPipe OK')"

COPY ./app /app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
Why libgl1-mesa-glx?
MediaPipe's C++ implementation links against OpenGL even when running CPU-only inference. Debian Slim excludes these libraries by default to reduce image size. Without explicit installation, MediaPipe will fail to import.
4.2 Frontend Dockerfile
dockerfileFROM node:20-alpine AS base

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
4.3 Docker Compose Configuration
yamlversion: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app:ro  # Hot reload
    environment:
      - CORS_ORIGINS=http://localhost:3000
      - LOG_LEVEL=INFO
      - MEDIAPIPE_MODEL_COMPLEXITY=1  # 0=Lite, 1=Full, 2=Heavy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app:ro
      - /app/node_modules
      - /app/.next
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
Development Workflow:
bash# Start both services
docker-compose up --build

# Access frontend
open http://localhost:3000

# Access backend docs
open http://localhost:8000/docs

# Code changes auto-reload both services

5. PERFORMANCE OPTIMIZATION STRATEGIES
5.1 Frame Processing Pipeline
Optimization 1: Frame Resizing
python# Resize to 640x480 before MediaPipe inference
# Reduces processing time from 80ms → 45ms
# Minimal accuracy loss (<2% for landmarks)
image = cv2.resize(image, (640, 480))
Optimization 2: JPEG Compression
typescript// Frontend: Compress before Base64 encoding
canvas.toBlob((blob) => {
  // JPEG at 80% quality: 50KB vs 200KB PNG
  // Reduces network time by 75%
}, 'image/jpeg', 0.8);
Optimization 3: NumPy Vectorization
python# Calculate angles for both legs simultaneously
# Single NumPy operation vs loop: 5ms → 1ms
left_angle, right_angle = calculate_angles_vectorized(landmarks)
5.2 Network Optimization
Strategy: Adaptive polling rate
typescript// 30 FPS (33ms) when form is good
// 15 FPS (66ms) when errors detected (reduce load)
const interval = isFormValid ? 33 : 66;
Strategy: Request cancellation
typescript// Cancel in-flight requests if new frame ready
// Prevents queue buildup on slow networks
abortController.abort();

6. ERROR HANDLING
6.1 Frontend Error Scenarios
ErrorCauseHandlingCamera permission deniedUser blocks accessShow permission instructions overlayNo person detectedUser out of frameDisplay "Stand in front of camera" messageAPI timeoutBackend overloadedRetry with exponential backoffNetwork errorBackend unreachableShow offline indicator, queue frames
6.2 Backend Error Scenarios
ErrorCauseResponseInvalid Base64Corrupt frame data400 Bad RequestMediaPipe failureLow confidence detection422 Unprocessable EntityInternal errorUnexpected exception500 Internal Server Error (logged)

7. SECURITY & PRIVACY
MVP Security Posture:

✅ No user authentication (reduces complexity)
✅ No frame storage (privacy-first design)
✅ CORS restricted to localhost:3000 (dev) and production domain
✅ No sensitive data logged (only timestamps, angles)
⚠️ No rate limiting (acceptable for local MVP, add for production)
⚠️ No HTTPS in development (required for mobile camera access)

Production Hardening (Post-MVP):

Add Helmet.js security headers
Implement rate limiting (10 req/sec per IP)
Deploy behind HTTPS reverse proxy
Add request size limits (max 5MB frames)


8. TESTING STRATEGY
8.1 Unit Tests (Backend)
Target Coverage: 80%+ for core logic
python# tests/test_geometry.py
def test_knee_angle_standing():
    """Verify 180° angle for fully extended leg"""
    landmarks = create_standing_pose()
    angle = calculate_knee_angle(landmarks)
    assert 175 <= angle <= 185  # Allow 5° tolerance

# tests/test_fsm.py
def test_squat_state_transitions():
    """Verify full squat cycle"""
    fsm = SquatFSM()
    assert fsm.process_frame(180) == "STANDING"
    assert fsm.process_frame(120) == "DESCENDING"
    assert fsm.process_frame(85) == "BOTTOM"
    assert fsm.process_frame(120) == "ASCENDING"
    assert fsm.rep_count == 1
8.2 Integration Tests
Manual Testing Checklist:

 Camera access works in Chrome, Firefox, Safari
 Skeleton overlay renders at 30 FPS without lag
 Rep counter increments only on valid squats
 "GO DEEPER" appears when depth insufficient
 "WIDEN KNEES" appears on knee valgus
 Mobile responsive (portrait mode on iPhone/Android)


9. DEPLOYMENT
9.1 Development
bashdocker-compose up --build

Hot reload enabled
Logs to console
No optimization

9.2 Production (Single Container)
Build Strategy:
dockerfile# Multi-stage build combining frontend + backend
FROM backend-image AS backend
FROM frontend-image AS frontend

# Combine into single image with Nginx reverse proxy
# Backend: :8000/api/v1/*
# Frontend: :3000/* (served statically)
Deployment Targets:

Render.com (Docker support, auto-deploy from GitHub)
Railway.app (Docker support, auto-scaling)
Fly.io (Edge deployment for low latency)

Environment Variables:
bashCORS_ORIGINS=https://fixfit.app
LOG_LEVEL=WARNING
MEDIAPIPE_MODEL_COMPLEXITY=1

10. RISK MITIGATION
Critical Risks
Risk: MediaPipe import fails in Docker
Mitigation: Test MediaPipe in container during Sprint 1 (first hour)
Fallback: Use OpenCV HOG detector (lower accuracy, but works)
Risk: Camera access blocked on iOS
Mitigation: Deploy to Vercel early for HTTPS testing
Fallback: Desktop-only MVP, defer mobile to post-launch
Risk: End-to-end latency exceeds 150ms
Mitigation: Profile every stage, optimize bottleneck first
Fallback: Reduce frame rate to 20 FPS (still usable)

APPENDIX A: GLOSSARY
TermDefinitionFSMFinite State Machine - tracks squat phase (standing, descending, etc.)Landmark2D/3D coordinate of body joint (e.g., knee, hip) detected by MediaPipeValgusInward collapse of knees during squat (injury risk)Tracer BulletMinimal end-to-end proof of concept (connectivity only, no logic)Base64Text encoding of binary image data for JSON transmission

APPENDIX B: REFERENCES

MediaPipe Pose Documentation
FastAPI Documentation
Next.js 14 App Router
Squat Biomechanics Standards (NSCA)


END OF ARCHITECTURE.MD