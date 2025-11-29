# FixFit Cursor Rules - Quick Phase Transition Guide

## 🚦 Current Phase Status

**Check your phase:**
```bash
head -5 .cursorrules | grep "CURRENT PHASE"
```

---

## Phase 0 → Phase 1 Transition

### ✅ Prerequisites (Complete These First)
```bash
# 1. Docker containers start
docker-compose up
# Should see: backend_1 and frontend_1 running

# 2. Backend health check
curl http://localhost:8000/health
# Should return: {"status": "ok"}

# 3. Dummy endpoint works
curl -X POST http://localhost:8000/api/v1/analyze-frame \
  -H "Content-Type: application/json" \
  -d '{"frame_data":"test","timestamp":123}'
# Should return: JSON with dummy data

# 4. Frontend loads
open http://localhost:3000
# Should see: FixFit interface

# 5. Frontend can call backend
# Open browser console (F12), click analyze button
# Should see: Network request success, no CORS errors
```

### 🔄 How to Transition
**Option A: Edit Header (Fast)**
```bash
# Open .cursorrules in editor, change line 4 to:
CURRENT PHASE: FEATURE IMPLEMENTATION (Phase 1)
- Priority: Implement business logic (MediaPipe, FSM, Geometry)
- Allowed: Full implementations, complex algorithms
- Replace all `pass` statements with working code
```

**Option B: Use Phase 1 Template (Complete)**
```bash
# Backup current
cp .cursorrules .cursorrules-phase0-backup

# If you have the comprehensive template:
cp .cursorrules-phase1-full.md .cursorrules

# Verify
grep "CURRENT PHASE" .cursorrules
```

---

## Phase 1 → Phase 2 Transition

### ✅ Prerequisites
```bash
# 1. MediaPipe detects landmarks
# Backend logs should show: "Detected 33 landmarks with confidence: 0.95"

# 2. Knee angle calculation works
# Test with known pose, verify angle in response

# 3. FSM transitions correctly
# Perform squat, check state changes: STANDING → DESCENDING → BOTTOM → ASCENDING

# 4. Error detection triggers
# Test bad form, verify correction_cue appears

# 5. Frontend displays feedback
# See green/red skeleton, correction text, rep counter
```

### 🔄 How to Transition
```bash
# Edit .cursorrules header:
CURRENT PHASE: POLISH & OPTIMIZATION (Phase 2)
- Priority: Performance tuning, UI polish, production readiness
- Allowed: Refactoring for speed, adding non-core features
- Focus: <150ms latency, mobile support, deployment prep
```

---

## 🆘 Emergency Rollback

**If Phase 1 breaks everything:**
```bash
# Restore Phase 0 rules
cp .cursorrules-phase0-backup .cursorrules

# Rebuild containers
docker-compose down
docker-compose up --build

# Verify infrastructure still works
curl http://localhost:8000/health
```

---

## 📊 Phase Cheat Sheet

| What You Want | Phase Required | AI Behavior |
|---------------|----------------|-------------|
| Create file structure | Phase 0 | Scaffold with `pass` |
| Define API contract | Phase 0 | Create interfaces only |
| Dummy endpoint | Phase 0 | Return hardcoded JSON |
| Implement MediaPipe | Phase 1 | Full implementation |
| FSM logic | Phase 1 | Complete state machine |
| Optimize latency | Phase 2 | Refactor existing code |
| Add animations | Phase 2 | Polish features |

---

## 🎯 One-Line Phase Checks

```bash
# Am I ready for Phase 1?
docker-compose up && curl http://localhost:8000/health && echo "✅ Ready for Phase 1"

# Am I ready for Phase 2?
curl -X POST http://localhost:8000/api/v1/analyze-frame -d '{"frame_data":"..."}'  | grep -q "knee_angle" && echo "✅ Ready for Phase 2"

# Which files still have TODOs?
grep -r "TODO.*Phase" backend/ frontend/
```

---

## 💡 Pro Tips

1. **Don't Skip Phases**
   - Each phase builds on the previous
   - Skipping = debugging hell later

2. **Test After Every Transition**
   ```bash
   docker-compose restart
   # Verify everything still works
   ```

3. **Commit Phase Milestones**
   ```bash
   git tag phase0-complete
   git tag phase1-complete
   ```

4. **Use Phase in Prompts**
   ```
   "We're in Phase 1 now, implement the knee angle calculation"
   # AI sees CURRENT PHASE header and proceeds correctly
   ```

5. **When in Doubt, Check the Header**
   ```bash
   cat .cursorrules | head -10
   ```

---

**Remember:** 
- Phase 0 = Connectivity ✅
- Phase 1 = Functionality ✅
- Phase 2 = Beauty ✅

**Go ship it!** 🚀
