TASKS.md
FixFit MVP - 24-Hour Sprint Plan
Strategy: Tracer Bullet → Core Logic → Polish
Methodology: Prove connectivity first, add intelligence second

SPRINT 1 (HOURS 0-4): THE TRACER BULLET
Objective: Prove end-to-end connectivity with ZERO business logic
Success Criteria:

Frontend captures webcam frame
Frontend sends Base64 to backend
Backend returns dummy JSON
Frontend displays response in console
NO MediaPipe, NO geometry, NO FSM


Task 1.1: Docker Setup + Backend Scaffold
Owner: DevOps/Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: None
Checklist:

 Create backend/Dockerfile with Python 3.10 + libgl1-mesa-glx installation
 Create backend/requirements.txt with FastAPI + Uvicorn only (NO MediaPipe yet)
 Create backend/app/main.py with:

FastAPI app initialization
CORS middleware configured for http://localhost:3000
/health endpoint returning {"status": "ok"}


 Create docker-compose.yml with backend service only
 Test: docker-compose up backend → curl localhost:8000/health returns 200 OK

Deliverable: Backend container starts in <10 seconds, health check passes
Risk: Docker + MediaPipe compatibility (mitigated by testing libgl1-mesa-glx early)

Task 1.2: Frontend Scaffold + Camera Access
Owner: Frontend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: None (can run in parallel with Task 1.1)
Checklist:

 Run npx create-next-app@latest frontend --typescript --tailwind --app
 Install Shadcn CLI: npx shadcn-ui@latest init
 Create frontend/Dockerfile with Node 20 Alpine
 Update docker-compose.yml to include frontend service
 Create components/CameraView.tsx:

Request navigator.mediaDevices.getUserMedia({ video: true })
Display video feed in <video> element
Handle permission denied error with user-friendly message


 Create app/page.tsx that renders <CameraView />
 Test: docker-compose up frontend → http://localhost:3000 shows webcam feed

Deliverable: Browser displays live webcam feed, no errors in console
Risk: Camera permissions on HTTPS (mitigated by localhost exception in browsers)

Task 1.3: THE TRACER BULLET - Frame Echo Endpoint
Owner: Full Stack
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Tasks 1.1 AND 1.2 complete
Backend Checklist:

 Create backend/app/api/routes.py:

POST /api/v1/analyze-frame endpoint
Accept FrameRequest (frame_data, timestamp)
Return dummy JSON: {"message": "Frame received at {timestamp}", "dummy": true}
NO image processing, NO MediaPipe


 Create backend/app/models/request.py with basic FrameRequest model
 Register route in main.py

Frontend Checklist:

 Create lib/api.ts:

analyzeFrame(frameData: string, timestamp: number) function
Fetch POST to http://localhost:8000/api/v1/analyze-frame


 Update components/CameraView.tsx:

Add "Capture Frame" button
On click: Convert video frame to canvas → toDataURL('image/jpeg', 0.8) → Base64
Call analyzeFrame() with Base64 data
console.log() the response


 Test: Click button → console shows: {message: "Frame received at...", dummy: true}

Deliverable: Full loop working: Camera → Capture → POST → Echo → Console
Success Metric: This proves the ENTIRE data pipeline works. Everything after this is "just" adding logic.

Task 1.4: Docker Compose Integration Test
Owner: DevOps
Priority: P1
Time Estimate: 30 minutes
Dependencies: Task 1.3 complete
Checklist:

 Verify both containers start with single command: docker-compose up --build
 Verify hot reload works:

Change backend response text → see update without rebuild
Change frontend text → see update without rebuild


 Add volume mounts to docker-compose.yml for hot reload
 Create .env.example with all required variables
 Write README.md with 5-minute quickstart instructions

Deliverable: New developer can run docker-compose up and see working app in 5 minutes

Task 1.5: Basic TypeScript Types
Owner: Frontend
Priority: P1
Time Estimate: 30 minutes
Dependencies: Task 1.3 complete
Checklist:

 Create types/analysis.ts:

Define SquatState enum (STANDING, DESCENDING, BOTTOM, ASCENDING)
Define Feedback enum (PERFECT, KNEE_VALGUS, DEPTH_FAIL)
Define AnalysisResponse interface matching API contract


 Update lib/api.ts to use typed interfaces
 Enable TypeScript strict mode in tsconfig.json

Deliverable: Zero TypeScript errors, full IDE autocomplete for API responses

SPRINT 1 GATE: Before proceeding to Sprint 2, verify:

✅ Docker containers start reliably
✅ Camera access works in browser
✅ Backend receives frames and responds
✅ Console shows dummy JSON response
✅ Hot reload works for both services

If ANY of these fail, do NOT proceed. Fix the tracer bullet first.

SPRINT 2 (HOURS 4-8): MEDIAPIPE INTEGRATION
Objective: Replace dummy JSON with real MediaPipe landmark detection

Task 2.1: MediaPipe Installation + Test
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Sprint 1 complete
Checklist:

 Add mediapipe==0.10.8 to requirements.txt
 Add opencv-python-headless==4.8.1.78 to requirements.txt
 Add numpy==1.26.2 to requirements.txt
 Rebuild backend container: docker-compose build backend
 Create backend/app/utils/mediapipe_wrapper.py:

Initialize MediaPipe Pose Landmarker (model_complexity=1)
Create extract_landmarks(image: np.ndarray) function
Return 33 landmark coordinates as NumPy array


 Create backend/app/utils/image_processing.py:

base64_to_image(base64_str: str) -> np.ndarray
resize_frame(image: np.ndarray) -> np.ndarray (resize to 640x480)


 Test with static image:

Load test squat image
Call extract_landmarks()
Print first 5 landmarks to console



Deliverable: MediaPipe successfully detects landmarks in test image
Risk: ⚠️ HIGH - Docker + MediaPipe compatibility. If import fails, verify libgl1-mesa-glx installed.
Fallback: If MediaPipe fails after 2 hours, use OpenCV HOG detector (lower accuracy, but works)

Task 2.2: Update /analyze-frame with Landmarks
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: Task 2.1 complete
Checklist:

 Update backend/app/api/routes.py:

Decode Base64 frame using base64_to_image()
Resize frame to 640x480
Call extract_landmarks()
Return landmarks in response (for now, just raw coordinates)


 Update backend/app/models/response.py:

Add landmarks: list[dict] field (temporary, will be replaced with angles)


 Test with Postman: POST frame → response includes 33 landmarks

Deliverable: Backend returns real landmark data from webcam frames

Task 2.3: Frontend Skeleton Overlay Component
Owner: Frontend
Priority: P1 (PARALLEL WORK)
Time Estimate: 1.5 hours
Dependencies: Task 2.2 complete
Checklist:

 Create components/SkeletonOverlay.tsx:

Create <canvas> element overlaying video feed
Accept landmarks prop (array of {x, y} coordinates)
Draw circles at each landmark position
Draw lines connecting joints (e.g., hip → knee → ankle)
Use green color by default


 Update app/page.tsx:

Display <SkeletonOverlay> on top of <CameraView>
Pass landmark data from API response


 Test: User sees skeleton overlay tracking their movement in real-time

Deliverable: Live skeleton visualization at 20-30 FPS

Task 2.4: Error Handling - No Person Detected
Owner: Backend
Priority: P1
Time Estimate: 30 minutes
Dependencies: Task 2.2 complete
Checklist:

 Update extract_landmarks() to check MediaPipe confidence
 If confidence < 0.5, raise ValueError("No person detected")
 Update /analyze-frame endpoint:

Catch ValueError → return 422 Unprocessable Entity
Include error JSON: {error: "NO_LANDMARKS_DETECTED", message: "..."}


 Test: Point camera at wall → receive 422 error

Deliverable: Graceful handling when user out of frame

SPRINT 2 GATE: Before proceeding to Sprint 3, verify:

✅ MediaPipe imports successfully in Docker container
✅ Backend returns 33 landmarks for valid frames
✅ Frontend displays skeleton overlay tracking user
✅ Error handling works when no person detected


SPRINT 3 (HOURS 8-12): GEOMETRY + FSM
Objective: Implement angle calculations and state machine

Task 3.1: Geometry Module - Knee Angle
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Sprint 2 complete
Checklist:

 Create backend/app/core/geometry.py:

Implement calculate_angle(point_a, point_b, point_c) -> float
Use Law of Cosines: cos(θ) = (a² + b² - c²) / (2ab)
Return angle in degrees (0-180)


 Implement get_knee_angles(landmarks) -> tuple[float, float]:

Extract hip[23], knee[25], ankle[27] for left leg
Extract hip[24], knee[26], ankle[28] for right leg
Return (left_angle, right_angle)


 Write unit tests:

Standing pose (180°)
Parallel squat (90°)
Deep squat (60°)



Deliverable: pytest tests/test_geometry.py passes with 100% coverage

Task 3.2: Geometry Module - Knee Valgus Ratio
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: Task 3.1 complete
Checklist:

 Add to backend/app/core/geometry.py:

Implement euclidean_distance(point_a, point_b) -> float
Implement calculate_valgus_ratio(landmarks) -> float:

knee_distance = distance(left_knee, right_knee)
ankle_distance = distance(left_ankle, right_ankle)
return knee_distance / ankle_distance




 Write unit tests:

Good form: ratio = 1.05 (knees aligned)
Valgus: ratio = 0.78 (knees caving in)



Deliverable: Valgus calculation unit tests pass

Task 3.3: State Machine Implementation
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1.5 hours
Dependencies: Task 3.1 complete
Checklist:

 Create backend/app/core/squat_fsm.py:

Define SquatFSM class with state enum (STANDING, DESCENDING, BOTTOM, ASCENDING)
Track current_state, rep_count, depth_threshold_reached flags
Implement process_frame(avg_knee_angle: float) -> SquatState:

STANDING → DESCENDING: avg_knee < 170°
DESCENDING → BOTTOM: avg_knee < 90°, set depth_threshold_reached = True
BOTTOM → ASCENDING: avg_knee > 100°
ASCENDING → STANDING: avg_knee > 170° AND is_valid == True (increment rep_count)


Implement reset() method to clear state


 Write unit tests:

Test full cycle: 180° → 120° → 85° → 120° → 180° (expect 1 rep)
Test incomplete: 180° → 120° → 105° → 180° (expect 0 reps, depth not reached)



Deliverable: pytest tests/test_fsm.py passes

Task 3.4: Update /analyze-frame with Angles + FSM
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Tasks 3.1, 3.2, 3.3 complete
Checklist:

 Update backend/app/api/routes.py:

Calculate knee angles using get_knee_angles()
Calculate average knee angle
Pass average angle to FSM process_frame()
Return current_state, joint_angles, rep_count in response


 Update backend/app/models/response.py:

Replace landmarks field with JointAngles model
Add current_state and rep_count fields


 Remove landmarks from response (no longer needed, frontend uses angles)

Deliverable: API response includes state machine data

SPRINT 3 GATE: Before proceeding to Sprint 4, verify:

✅ Knee angles calculated correctly (test with known poses)
✅ FSM transitions through states correctly
✅ Rep counter increments on valid squats
✅ API returns current_state, joint_angles, rep_count


SPRINT 4 (HOURS 12-16): ERROR DETECTION + FEEDBACK
Objective: Add form error detection and UI feedback

Task 4.1: Error Detection - Depth Check
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: Sprint 3 complete
Checklist:

 Create backend/app/core/error_detection.py:

Implement check_depth(fsm: SquatFSM, current_state: SquatState) -> bool:

If state == ASCENDING and fsm.depth_threshold_reached == False:

return DEPTH_FAIL


Else:

return PERFECT






 Update FSM to track depth_threshold_reached flag
 Write unit tests:

Test shallow squat: 180° → 120° → 105° → 180° (expect DEPTH_FAIL)
Test deep squat: 180° → 85° → 180° (expect PERFECT)



Deliverable: Depth check correctly identifies insufficient depth

Task 4.2: Error Detection - Knee Valgus Check
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 45 minutes
Dependencies: Task 4.1 complete
Checklist:

 Add to backend/app/core/error_detection.py:

Implement check_knee_valgus(valgus_ratio: float, current_state: SquatState) -> bool:

If current_state in [DESCENDING, BOTTOM, ASCENDING] AND valgus_ratio < 0.85:

return KNEE_VALGUS


Else:

return PERFECT






 Write unit tests:

Test good form: ratio = 1.05 (expect PERFECT)
Test valgus: ratio = 0.78 (expect KNEE_VALGUS)



Deliverable: Valgus check correctly identifies knee collapse

Task 4.3: Integrate Error Detection into /analyze-frame
Owner: Backend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Tasks 4.1, 4.2 complete
Checklist:

 Update backend/app/api/routes.py:

Calculate valgus ratio
Call check_depth() and check_knee_valgus()
Determine feedback enum value (PERFECT, KNEE_VALGUS, or DEPTH_FAIL)
Set is_valid = (feedback == PERFECT)
FSM only increments rep_count if is_valid == True


 Update backend/app/models/response.py:

Add feedback enum field
Add is_valid boolean field


 Test: Perform shallow squat → API returns feedback: "DEPTH_FAIL", is_valid: false

Deliverable: Complete error detection pipeline functional

Task 4.4: Frontend Feedback Display Component
Owner: Frontend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1.5 hours
Dependencies: Task 4.3 complete
Checklist:

 Create components/FeedbackDisplay.tsx:

Accept feedback, is_valid, rep_count props
Display rep counter (large font, top right)
Display feedback text:

PERFECT: "GOOD FORM" (green)
KNEE_VALGUS: "WIDEN KNEES" (red, large)
DEPTH_FAIL: "GO DEEPER" (red, large)




 Update components/SkeletonOverlay.tsx:

Accept is_valid prop
Change skeleton color:

Green when is_valid == true
Red when is_valid == false




 Update app/page.tsx:

Pass API response data to both components
Display feedback and skeleton color reactively



Deliverable: User sees real-time form corrections as they squat

Task 4.5: UI Polish - Control Panel
Owner: Frontend
Priority: P1
Time Estimate: 45 minutes
Dependencies: Task 4.4 complete
Checklist:

 Create components/ControlPanel.tsx:

"Start Session" button (begins frame capture loop)
"Stop Session" button (pauses capture)
"Reset Counter" button (calls backend to reset FSM state)


 Add session state management (useState for isActive)
 Implement frame capture loop:

When active, capture frame every 33ms (30 FPS)
Send to backend via analyzeFrame()
Update UI with response



Deliverable: User can start/stop/reset squat sessions

SPRINT 4 GATE: Before proceeding to Sprint 5, verify:

✅ Depth errors detected and displayed
✅ Knee valgus errors detected and displayed
✅ Rep counter only increments on valid squats
✅ Skeleton color changes green/red based on form
✅ Start/stop controls work


SPRINT 5 (HOURS 16-20): AUDIO + PERFORMANCE
Objective: Add audio feedback and optimize latency

Task 5.1: Audio Feedback System
Owner: Frontend
Priority: P0 (CRITICAL PATH)
Time Estimate: 1 hour
Dependencies: Sprint 4 complete
Checklist:

 Create lib/audio.ts:

Use Web Audio API to generate tones (no external files needed)
playSuccessTone(): 440 Hz (A note), 200ms duration
playAlertTone(): 220 Hz (A lower octave), 300ms duration


 Update app/page.tsx:

Track previous is_valid state
On transition true → false: play alert tone
On rep increment: play success tone


 Test: Perform squat with error → hear alert tone

Deliverable: Audio feedback synchronized with visual feedback

Task 5.2: Backend Performance Optimization
Owner: Backend
Priority: P1
Time Estimate: 1.5 hours
Dependencies: Sprint 4 complete
Checklist:

 Add time instrumentation to /analyze-frame:

Log processing time for each stage (decode, MediaPipe, geometry, FSM)
Include processing_time_ms in response


 Optimize bottlenecks:

Vectorize angle calculations with NumPy (batch both legs)
Cache MediaPipe model (singleton pattern)
Reduce image quality if needed (640x480 @ 70% JPEG)


 Target: processing_time_ms < 100ms consistently

Deliverable: Backend consistently processes frames in <100ms
Risk: ⚠️ MEDIUM - May require algorithm refactoring if target not met

Task 5.3: Frontend Mobile Responsive Layout
Owner: Frontend
Priority: P1
Time Estimate: 1 hour
Dependencies: Task 5.1 complete
Checklist:

 Test on iPhone Safari and Chrome Android
 Adjust camera aspect ratio for portrait mode (9:16)
 Ensure buttons are thumb-reachable (bottom of screen)
 Test camera permissions flow on mobile
 Verify skeleton overlay scales correctly

Deliverable: App usable on mobile browsers (portrait mode)
Risk: ⚠️ HIGH - iOS requires HTTPS for camera access (deploy early to Vercel for testing)

Task 5.4: Error Handling + Loading States
Owner: Full Stack
Priority: P1
Time Estimate: 1 hour
Dependencies: None (can parallelize)
Backend Checklist:

 Add global exception handler in main.py
 Log errors with stack traces (LOG_LEVEL=ERROR)
 Return user-friendly error messages

Frontend Checklist:

 Add loading spinner during frame analysis
 Handle network timeout (retry with exponential backoff)
 Display error toast for persistent failures
 Handle camera permission denied gracefully

Deliverable: App never crashes, shows helpful error messages

SPRINT 5 GATE: Before proceeding to Sprint 6, verify:

✅ Audio feedback works (success + alert tones)
✅ Backend processing time <100ms
✅ Mobile layout functional
✅ Error handling prevents crashes


SPRINT 6 (HOURS 20-24): TESTING + DEPLOYMENT
Objective: Integration testing, bug fixes, deployment prep

Task 6.1: End-to-End Testing
Owner: All
Priority: P0 (CRITICAL PATH)
Time Estimate: 2 hours
Dependencies: Sprint 5 complete
Test Scenarios:

Happy Path: User performs 5 perfect squats → rep counter shows 5
Depth Error: User performs shallow squat → sees "GO DEEPER", rep not counted
Valgus Error: User's knees cave in → sees "WIDEN KNEES", rep not counted
Recovery: User fixes form after error → next rep counted correctly
Edge Cases: User leaves frame → recovers gracefully, no crash

Bug Triage:

P0 (Blocker): Crashes, incorrect rep counting, MediaPipe failures
P1 (High): Laggy UI, audio glitches, mobile layout issues
P2 (Low): Minor visual polish, color tweaks

Deliverable: Documented bug list with severity ratings, P0 bugs fixed

Task 6.2: Production Dockerfile Optimization
Owner: DevOps
Priority: P1
Time Estimate: 1 hour
Dependencies: Task 6.1 complete
Checklist:

 Remove development tools from backend image (pytest, black, mypy)
 Use multi-stage build to reduce image size
 Optimize Next.js build (standalone output)
 Target: Backend image <400MB, Frontend image <150MB
 Test: Build production images → start containers → verify functionality

Deliverable: Production-optimized Docker images

Task 6.3: Deployment to Render/Railway
Owner: DevOps
Priority: P1
Time Estimate: 1 hour
Dependencies: Task 6.2 complete
Checklist:

 Choose deployment platform (Render.com recommended for Docker support)
 Create render.yaml or railway.json config
 Set environment variables:

CORS_ORIGINS=https://fixfit.app
LOG_LEVEL=WARNING


 Deploy backend container
 Deploy frontend to Vercel/Netlify (for HTTPS + edge caching)
 Update frontend NEXT_PUBLIC_API_URL to production backend URL
 Test: Access public URL → perform squat → verify full functionality

Deliverable: Public URL accessible over HTTPS

Task 6.4: Demo Video + Documentation
Owner: All
Priority: P1
Time Estimate: 1 hour
Dependencies: Task 6.3 complete
Checklist:

 Record 2-minute demo video:

Show good form squat (green overlay, rep counted)
Show depth error (red overlay, "GO DEEPER")
Show valgus error (red overlay, "WIDEN KNEES")
Show recovery (correct form after error)


 Update README.md:

Add demo GIF/video link
Document setup instructions
Add troubleshooting section


 Create DEMO.md with talking points for presentation

Deliverable: Professional demo materials ready for submission

Task 6.5: Final Polish (Time Permitting)
Owner: Frontend
Priority: P2 (NICE TO HAVE)
Time Estimate: 1 hour
Dependencies: Task 6.4 complete
Checklist:

 Add subtle animations (skeleton lines fade in/out)
 Improve loading states (skeleton placeholder)
 Add keyboard shortcuts (Space = start/stop, R = reset)
 Optimize font loading (reduce CLS)
 Add favicon and meta tags for social sharing

Deliverable: Polished, professional-looking interface

RISK MITIGATION CHECKPOINTS
Hour 4 Checkpoint (End of Sprint 1)
Question: Is the tracer bullet working?
If NO: Do NOT proceed. Debug connectivity issues first.
Hour 8 Checkpoint (End of Sprint 2)
Question: Is MediaPipe detecting landmarks?
If NO: Consider fallback to simpler pose detection (OpenCV HOG).
Hour 12 Checkpoint (End of Sprint 3)
Question: Is the FSM counting reps correctly?
If NO: Simplify state machine (remove error detection if needed).
Hour 16 Checkpoint (End of Sprint 4)
Question: Does error detection work?
If NO: Ship with basic rep counting only, defer error detection.
Hour 20 Checkpoint (End of Sprint 5)
Question: Is performance acceptable (<150ms latency)?
If NO: Reduce frame rate to 20 FPS, increase JPEG compression.

CONTINGENCY PLANS
If Behind Schedule (Hour 16+):
Priority 1 (Must Have):

 Camera → Backend → Skeleton overlay working
 Rep counting functional
 One error detection (either depth OR valgus)

Priority 2 (Should Have):

 Both error detections (depth AND valgus)
 Audio feedback
 Mobile support

Priority 3 (Nice to Have):

 Performance optimization
 UI polish
 Production deployment

CUT IF NEEDED:

Audio feedback (visual cues sufficient for MVP)
Mobile support (desktop-only acceptable)
Advanced animations


SUCCESS CRITERIA (FINAL CHECKLIST)
Functional Requirements

 User can perform squat and see skeleton overlay
 Rep counter increments on valid squats
 Depth errors detected and displayed
 Knee valgus errors detected and displayed
 Session controls (start/stop/reset) work

Performance Requirements

 End-to-end latency <150ms (measured)
 Sustained 20-30 FPS frame rate
 Backend processing <100ms per frame

Quality Requirements

 No crashes during normal use
 Error messages user-friendly
 Works on Chrome, Firefox, Safari (desktop)
 Mobile responsive (bonus)


END OF TASKS.MD