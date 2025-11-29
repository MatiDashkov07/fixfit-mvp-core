# FixFit API Contract
## Version: 1.0

---

## Base URL
- **Development:** `http://localhost:8000`
- **Production:** TBD

---

## Endpoints

### 1. Health Check

**`GET /health`**

Health check endpoint for container orchestration.

**Response (200 OK):**
```json
{
  "status": "ok",
  "service": "fixfit-backend"
}
```

---

### 2. Analyze Frame

**`POST /api/v1/analyze-frame`**

Analyze a single video frame for squat form.

#### Request Body
```json
{
  "frame_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...",
  "timestamp": 1700000000.123
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `frame_data` | string | Yes | Base64 encoded JPEG image (with or without data URL prefix) |
| `timestamp` | float | Yes | Unix timestamp when frame was captured |

#### Response (200 OK)
```json
{
  "current_state": "STANDING",
  "is_form_valid": true,
  "correction_cue": null,
  "rep_count": 0,
  "feedback": "PERFECT",
  "joint_angles": {
    "left_knee": 180.0,
    "right_knee": 180.0,
    "average": 180.0
  },
  "error_details": {
    "knee_valgus_ratio": 1.0,
    "depth_threshold_reached": false
  },
  "processing": {
    "timestamp": 1700000000.150,
    "processing_time_ms": 45.5
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `current_state` | enum | FSM state: `STANDING`, `DESCENDING`, `BOTTOM`, `ASCENDING` |
| `is_form_valid` | boolean | Whether current form passes all checks |
| `correction_cue` | string\|null | Human-readable correction ("WIDEN KNEES", "GO DEEPER") or null |
| `rep_count` | integer | Total valid repetitions completed |
| `feedback` | enum | Form category: `PERFECT`, `KNEE_VALGUS`, `DEPTH_FAIL` |
| `joint_angles.left_knee` | float | Left knee angle in degrees (0-180) |
| `joint_angles.right_knee` | float | Right knee angle in degrees (0-180) |
| `joint_angles.average` | float | Average knee angle in degrees |
| `error_details.knee_valgus_ratio` | float | Knee distance / ankle distance (< 0.85 = valgus) |
| `error_details.depth_threshold_reached` | boolean | Whether squat reached parallel depth |
| `processing.timestamp` | float | Server timestamp when processing completed |
| `processing.processing_time_ms` | float | Total processing time in milliseconds |

#### Error Responses

**400 Bad Request** - Invalid input
```json
{
  "detail": "Missing frame_data"
}
```

**422 Unprocessable Entity** - No person detected
```json
{
  "error": "NO_LANDMARKS_DETECTED",
  "message": "No person detected in frame. Please stand in front of the camera."
}
```

**500 Internal Server Error** - Unexpected error
```json
{
  "detail": "Internal server error"
}
```

---

### 3. Reset Session

**`POST /api/v1/reset`**

Reset the current squat session (FSM state and rep counter).

**Response (200 OK):**
```json
{
  "status": "reset",
  "rep_count": 0
}
```

---

## Enums

### SquatState
```typescript
enum SquatState {
  STANDING = "STANDING",    // Upright position, knees extended
  DESCENDING = "DESCENDING", // Moving down, knee angle decreasing
  BOTTOM = "BOTTOM",        // Lowest position, knee angle < 90°
  ASCENDING = "ASCENDING"   // Moving up, knee angle increasing
}
```

### Feedback
```typescript
enum Feedback {
  PERFECT = "PERFECT",      // No form errors detected
  KNEE_VALGUS = "KNEE_VALGUS", // Knees caving inward
  DEPTH_FAIL = "DEPTH_FAIL"    // Did not reach parallel depth
}
```

---

## FSM State Transitions

```
STANDING ──(knee < 170°)──> DESCENDING
    ↑                           │
    │                           │
(knee > 170°)              (knee < 90°)
    │                           │
    │                           ↓
ASCENDING <──(knee > 100°)── BOTTOM
```

**Transition Thresholds:**
- `STANDING → DESCENDING`: avg_knee_angle < 170°
- `DESCENDING → BOTTOM`: avg_knee_angle < 90°
- `BOTTOM → ASCENDING`: avg_knee_angle > 100°
- `ASCENDING → STANDING`: avg_knee_angle > 170° (increments rep_count if valid)

---

## Error Detection Thresholds

| Check | Threshold | Condition |
|-------|-----------|-----------|
| Knee Valgus | `valgus_ratio < 0.85` | Knees collapsing inward |
| Depth | `!depth_threshold_reached` on ascent | Did not reach 90° knee angle |

---

## Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| End-to-end latency | < 150ms | ~80-95ms |
| Processing time | < 100ms | ~45-60ms |
| Frame rate | 20-30 FPS | Adaptive |
| Encoding time | < 15ms | ~10-15ms |
