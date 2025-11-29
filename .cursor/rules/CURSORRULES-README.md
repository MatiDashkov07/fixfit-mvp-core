# FixFit Cursor Rules - Phased Development Strategy

## 📋 Overview

This project uses a **phased `.cursorrules` approach** to prevent premature optimization and ensure smooth 24-hour hackathon execution.

Instead of overwhelming Claude Opus 4.5 with all implementation details from the start, we provide context-appropriate rules for each development phase.

---

## 🎯 The Problem We're Solving

**Traditional Approach (Single Monolithic `.cursorrules`):**
```
❌ Developer: "Create the project structure"
❌ AI: *Tries to implement MediaPipe logic before Docker exists*
❌ Developer: "Just the folders first!"
❌ AI: *Confused because rules say "always implement full logic"*
❌ Result: Wasted time, broken code, frustration
```

**Phased Approach:**
```
✅ Developer: "Create the project structure"
✅ AI: *Reads Phase 0 rules: scaffold only, dummy data OK*
✅ AI: *Creates file structure with interface definitions*
✅ Developer: "Great! Now implement MediaPipe"
✅ AI: *Switches to Phase 1 rules, writes full implementation*
✅ Result: Clean progression, working code, fast iteration
```

---

## 📁 File Structure

```
.cursorrules                    # Active rules (changes per phase)
.cursorrules-phase0             # Backup of Phase 0 rules
.cursorrules-phase1-full.md     # Comprehensive rules for implementation
CURSORRULES-README.md           # This file
```

---

## 🚀 Phase Progression

### **Phase 0: System Setup & Tracer Bullet** (Hours 0-4)
**File:** `.cursorrules` (current)

**Objectives:**
- ✅ Docker containers start without errors
- ✅ Backend returns dummy JSON via FastAPI
- ✅ Frontend calls backend successfully
- ✅ No CORS errors
- ✅ Hot reload works for both services

**AI Behavior:**
- Creates file scaffolds with `pass` statements
- Defines interfaces (TypeScript, Pydantic)
- Implements dummy endpoints that return hardcoded data
- **DOES NOT** implement MediaPipe or complex math yet

**Example Output:**
```python
# backend/app/core/geometry.py
def calculate_knee_angle(hip: np.ndarray, knee: np.ndarray, ankle: np.ndarray) -> float:
    """Calculate knee angle using Law of Cosines."""
    pass  # TODO: Implement in Phase 1
```

**Completion Checklist:**
```bash
# Run these commands to verify Phase 0 complete:
docker-compose up                                    # ✅ No errors
curl http://localhost:8000/health                    # ✅ Returns 200 OK
curl -X POST http://localhost:8000/api/v1/analyze-frame \
  -H "Content-Type: application/json" \
  -d '{"frame_data":"dummy","timestamp":123}'        # ✅ Returns dummy JSON
open http://localhost:3000                           # ✅ Frontend loads
# Click "Analyze" button in browser                  # ✅ Console shows backend response
```

**When to Advance:**
✅ All checklist items pass → Move to Phase 1

---

### **Phase 1: Feature Implementation** (Hours 4-16)
**File:** Copy `.cursorrules-phase1-full.md` → `.cursorrules`

**Objectives:**
- ✅ MediaPipe pose detection working
- ✅ Knee angle calculations accurate
- ✅ FSM state transitions correct
- ✅ Error detection triggers properly
- ✅ Frontend displays real-time feedback

**AI Behavior:**
- Replaces all `pass` statements with full implementations
- Writes complex mathematical logic (Law of Cosines, vector math)
- Implements MediaPipe integration with proper error handling
- Adds performance optimizations (NumPy vectorization)

**Example Output:**
```python
# backend/app/core/geometry.py
def calculate_knee_angle(hip: np.ndarray, knee: np.ndarray, ankle: np.ndarray) -> float:
    """
    Calculate knee flexion angle using Law of Cosines.
    
    Hip-Knee-Ankle forms a triangle where:
    - 180° = standing (full extension)
    - 90° = parallel squat (minimum depth)
    - <90° = deep squat (optimal)
    """
    vector_thigh = knee - hip
    vector_shin = ankle - knee
    
    cos_angle = np.dot(vector_thigh, vector_shin) / (
        np.linalg.norm(vector_thigh) * np.linalg.norm(vector_shin)
    )
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    
    angle_radians = np.arccos(cos_angle)
    return np.degrees(angle_radians)
```

**Update Instructions:**
```bash
# Replace .cursorrules with Phase 1 version
cp .cursorrules .cursorrules-phase0-backup
cp .cursorrules-phase1-full.md .cursorrules

# Or manually edit .cursorrules and change:
CURRENT PHASE: FEATURE IMPLEMENTATION (Phase 1)
- Priority: Implement business logic (MediaPipe, FSM, Geometry)
- Allowed: Full implementations, complex algorithms
- Replace all `pass` statements with working code
```

---

### **Phase 2: Polish & Performance** (Hours 16-24)
**File:** Update header in existing `.cursorrules`

**Objectives:**
- ✅ Latency under 150ms end-to-end
- ✅ Audio feedback synchronized
- ✅ Mobile responsive
- ✅ Error handling comprehensive
- ✅ Production deployment ready

**AI Behavior:**
- Optimizes existing code (reduce latency, minimize bundle size)
- Adds polish features (animations, sounds, loading states)
- Implements error boundaries and graceful degradation
- Prepares production Docker configuration

**Update Instructions:**
```bash
# Edit .cursorrules header:
CURRENT PHASE: POLISH & OPTIMIZATION (Phase 2)
- Priority: Performance tuning, UI polish, production readiness
- Allowed: Refactoring for speed, adding non-core features
- Focus: <150ms latency, mobile support, deployment prep
```

---

## 🔄 How to Switch Phases

### Method 1: Manual Header Update (Recommended)
```bash
# Open .cursorrules in editor
# Change line 4:
CURRENT PHASE: FEATURE IMPLEMENTATION (Phase 1)

# Save and Cursor will automatically reload rules
```

### Method 2: File Replacement
```bash
# Backup current rules
cp .cursorrules .cursorrules-backup-$(date +%Y%m%d-%H%M%S)

# Copy phase-specific template
cp .cursorrules-phase1-full.md .cursorrules

# Cursor automatically detects file change
```

### Method 3: Git Branch Strategy (Advanced)
```bash
# Create branches for each phase
git checkout -b phase0-infrastructure
git add .cursorrules
git commit -m "Phase 0 rules"

git checkout -b phase1-implementation
# Replace .cursorrules with Phase 1 version
git commit -m "Phase 1 rules"

# Switch between phases
git checkout phase0-infrastructure  # Back to scaffolding mode
git checkout phase1-implementation  # Back to full implementation
```

---

## 📖 Usage Examples

### Starting Fresh (Phase 0)
```
You: "Set up the project structure for FixFit"

Claude (reading Phase 0 rules):
- Creates backend/ and frontend/ directories
- Generates Dockerfile with MediaPipe dependencies
- Creates docker-compose.yml with volume mounts
- Scaffolds main.py with dummy /analyze-frame endpoint
- Creates Next.js app with CameraView component (no implementation)
- Defines TypeScript interfaces for API contract
- All business logic files contain `pass` statements

Result: Infrastructure ready, connectivity proven, FAST ✅
```

### After Phase 0 Complete (Phase 1)
```
You: "Implement the knee angle calculation"

Claude (reading Phase 1 rules):
- Implements full Law of Cosines logic
- Adds NumPy vectorization for performance
- Includes proper type hints and docstrings
- Adds unit tests with known angle values
- NO placeholder comments

Result: Production-ready implementation ✅
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ Mistake 1: Using Phase 1 Rules Too Early
```
Problem: AI tries to implement MediaPipe before Docker exists
Solution: Stay in Phase 0 until infrastructure works
```

### ❌ Mistake 2: Forgetting to Update Phase Header
```
Problem: Still in Phase 0 rules but asking for full implementation
Solution: Update CURRENT PHASE in .cursorrules header
```

### ❌ Mistake 3: Skipping Tracer Bullet Verification
```
Problem: Building features on broken foundation
Solution: Complete Phase 0 checklist before advancing
```

---

## 🎓 Best Practices

1. **Trust the Process**
   - Phase 0 feels "incomplete" by design
   - Resist urge to implement everything immediately
   - Connectivity > Intelligence in early hours

2. **Verify Before Advancing**
   - Run the checklist for each phase
   - Don't advance with broken fundamentals
   - `docker-compose up` should ALWAYS work

3. **Save Phase Checkpoints**
   ```bash
   # Before advancing to next phase
   git tag phase0-complete
   git push origin phase0-complete
   ```

4. **Communicate Phase to AI**
   ```
   You: "We're still in Phase 0, just create the scaffold"
   # AI reads CURRENT PHASE header and complies
   ```

5. **Use Comments for Future Phases**
   ```python
   # Phase 0
   def calculate_angle(...):
       pass  # TODO: Law of Cosines in Phase 1
   
   # Phase 1
   def calculate_angle(...):
       # Implemented with proper math
   ```

---

## 🆘 Troubleshooting

### "AI is implementing logic in Phase 0"
```bash
# Check .cursorrules header
head -10 .cursorrules | grep "CURRENT PHASE"

# Should show: CURRENT PHASE: SYSTEM SETUP & TRACER BULLET (Phase 0)
# If not, update it manually
```

### "AI refuses to implement in Phase 1"
```bash
# Update header
sed -i '' 's/SYSTEM SETUP & TRACER BULLET (Phase 0)/FEATURE IMPLEMENTATION (Phase 1)/' .cursorrules
```

### "Not sure which phase I'm in"
```bash
# Check what's working
docker-compose up  # Works? → At least Phase 0 complete

# Check for implementations
grep -r "pass  # TODO" backend/app/core/
# Many matches? → Still in Phase 0
# No matches? → Phase 1 or later
```

---

## 📚 Additional Resources

- **Original Comprehensive Rules:** `.cursorrules-phase1-full.md`
- **Biomechanics Reference:** See "BIOMECHANICS SPECIFICATION" section in Phase 1 rules
- **Docker Debugging:** See "EMERGENCY ESCAPE HATCHES" in any .cursorrules file
- **API Contract:** Defined consistently across all phases

---

## ✅ Quick Reference Card

| Phase | Hours | Focus | AI Can Use `pass` | Full Implementations |
|-------|-------|-------|-------------------|----------------------|
| 0 | 0-4 | Infrastructure | ✅ Yes | ❌ No |
| 1 | 4-16 | Features | ❌ No | ✅ Yes |
| 2 | 16-24 | Polish | ❌ No | ✅ Yes + Optimize |

**Success Mantra:**
```
Phase 0: "Does it connect?"
Phase 1: "Does it work correctly?"
Phase 2: "Does it work beautifully?"
```

---

**Now go build FixFit with confidence!** 🚀💪
