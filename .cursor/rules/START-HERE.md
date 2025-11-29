# FixFit Cursor Rules - Complete Package Summary

## 📦 What You've Received

This package contains a **phased development strategy** for building FixFit in 24 hours using Claude Opus 4.5 in Cursor.

---

## 📁 Files Included

### 1. `.cursorrules` (Phase 0 - Active)
**Purpose:** Infrastructure and tracer bullet setup
**Use When:** Starting fresh, setting up Docker, creating file structure
**Key Features:**
- Allows `pass` statements and scaffolding
- Focuses on connectivity over implementation
- Includes Docker MediaPipe dependency fixes
- Provides emergency escape hatches

**Status:** ✅ **Use this first**

---

### 2. `CURSORRULES-README.md` (Comprehensive Guide)
**Purpose:** Complete explanation of phased approach
**Sections:**
- Why phased rules solve hackathon problems
- Detailed phase descriptions (0, 1, 2)
- How to switch between phases
- Common mistakes and troubleshooting
- Best practices and examples

**Read:** Before starting development

---

### 3. `PHASE-TRANSITION-GUIDE.md` (Quick Reference)
**Purpose:** Fast lookup for phase transitions
**Contents:**
- Checklists for each phase completion
- One-line transition commands
- Emergency rollback procedures
- Phase comparison table

**Keep Open:** During hackathon for quick checks

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Set Up Files
```bash
# In your FixFit project root:
cp .cursorrules .cursorrules
cp CURSORRULES-README.md .
cp PHASE-TRANSITION-GUIDE.md .
```

### Step 2: Verify Phase 0 Active
```bash
head -5 .cursorrules
# Should show: CURRENT PHASE: SYSTEM SETUP & TRACER BULLET (Phase 0)
```

### Step 3: Start Building
Open Cursor and use prompts like:
```
"Create the FixFit project structure"
"Set up Docker for FastAPI with MediaPipe"
"Create the Next.js frontend scaffold"
```

Claude will follow Phase 0 rules and create infrastructure with dummy implementations.

---

## 🎯 The Phased Strategy at a Glance

```
┌─────────────────────────────────────────────────┐
│ PHASE 0: INFRASTRUCTURE (Hours 0-4)            │
│ ✓ Docker containers start                      │
│ ✓ Dummy endpoints return JSON                  │
│ ✓ Frontend calls backend successfully          │
│ ✓ No implementations, just connectivity        │
└─────────────────────────────────────────────────┘
              ↓ Update .cursorrules header
┌─────────────────────────────────────────────────┐
│ PHASE 1: IMPLEMENTATION (Hours 4-16)           │
│ ✓ MediaPipe pose detection working             │
│ ✓ Knee angle calculations accurate             │
│ ✓ FSM state machine complete                   │
│ ✓ Error detection triggers properly            │
└─────────────────────────────────────────────────┘
              ↓ Update .cursorrules header
┌─────────────────────────────────────────────────┐
│ PHASE 2: POLISH (Hours 16-24)                  │
│ ✓ Latency under 150ms                          │
│ ✓ Audio feedback synchronized                  │
│ ✓ Mobile responsive                            │
│ ✓ Production deployment ready                  │
└─────────────────────────────────────────────────┘
```

---

## 🔑 Key Differences from Traditional Approach

### ❌ Traditional (Monolithic Rules)
```
Problem: AI tries to implement everything at once
Result: MediaPipe code written before Docker exists
Outcome: Broken, needs debugging, wastes hours
```

### ✅ Phased Approach
```
Phase 0: AI scaffolds structure, returns dummy data
Result: Infrastructure works in 2 hours
Phase 1: AI fills in business logic with full implementations
Result: Features work in 12 hours
Phase 2: AI optimizes and polishes
Result: Production-ready in 24 hours
```

---

## 📖 Usage Patterns

### Pattern 1: Fresh Start
```bash
# Day 1, Hour 0
1. Copy .cursorrules (Phase 0)
2. Prompt: "Create FixFit project structure"
3. Verify: docker-compose up works
4. Prompt: "Create dummy /analyze-frame endpoint"
5. Verify: curl returns JSON
6. Advance to Phase 1
```

### Pattern 2: Mid-Development Join
```bash
# Joining existing project
1. Check current state: docker-compose up
2. If working → Use Phase 1 rules
3. If broken → Use Phase 0 rules, rebuild
```

### Pattern 3: Debug Mode
```bash
# Something broke
1. Rollback to Phase 0 rules
2. Verify infrastructure still works
3. Advance phase-by-phase
```

---

## 🎓 Pro Tips for Maximum Speed

### 1. Communicate Phase to AI
```
You: "We're in Phase 0, just create the file structure"
AI: *Creates scaffolds with pass statements*

You: "Now we're in Phase 1, implement MediaPipe"
AI: *Writes full implementation*
```

### 2. Trust the Scaffolds
```python
# Phase 0 output looks "incomplete" - this is correct!
def calculate_knee_angle(...) -> float:
    pass  # TODO: Implement in Phase 1

# Don't ask AI to fill it in yet - verify infrastructure first
```

### 3. Use Checklists Religiously
```bash
# Before advancing phases
cat PHASE-TRANSITION-GUIDE.md
# Run all prerequisite checks
# Only advance when ALL pass ✅
```

### 4. Commit After Each Phase
```bash
git add .
git commit -m "Phase 0 complete: Infrastructure working"
git tag phase0-complete

# Later if something breaks
git reset --hard phase0-complete
```

### 5. Keep README Open
```bash
# In second monitor or split screen
cat CURSORRULES-README.md
# Reference throughout development
```

---

## 🆘 Troubleshooting Quick Reference

### "AI is implementing too early"
```bash
# Check header
grep "CURRENT PHASE" .cursorrules
# Should be Phase 0 initially
```

### "AI refuses to implement"
```bash
# Update phase
sed -i '' 's/Phase 0/Phase 1/' .cursorrules
# Prompt again
```

### "Docker won't start"
```bash
# Check MediaPipe dependencies in Dockerfile
grep "libgl1-mesa-glx" backend/Dockerfile
# Should be present for CPU inference
```

### "CORS errors"
```bash
# Check FastAPI middleware
grep "CORSMiddleware" backend/app/main.py
# Should allow localhost:3000
```

---

## 📊 Expected Timeline

| Hour | Phase | Activity | Deliverable |
|------|-------|----------|-------------|
| 0-2 | 0 | Docker setup | Containers start |
| 2-4 | 0 | Dummy endpoints | Frontend ↔ Backend works |
| 4-8 | 1 | MediaPipe integration | Landmarks detected |
| 8-12 | 1 | FSM + calculations | Angle/valgus working |
| 12-16 | 1 | Error detection | Corrections trigger |
| 16-20 | 2 | Performance tuning | <150ms latency |
| 20-24 | 2 | Polish + deploy | Production ready |

---

## ✅ Success Metrics

### Phase 0 Complete When:
- ✅ `docker-compose up` runs without errors
- ✅ `curl localhost:8000/health` returns 200
- ✅ Frontend button click → backend response in console
- ✅ No import errors or missing dependencies

### Phase 1 Complete When:
- ✅ MediaPipe detects 33 landmarks
- ✅ Knee angle calculation returns correct degrees
- ✅ FSM transitions through all states
- ✅ Error detection shows "GO DEEPER" or "WIDEN KNEES"

### Phase 2 Complete When:
- ✅ End-to-end latency < 150ms
- ✅ Mobile browser shows responsive layout
- ✅ Audio feedback plays correctly
- ✅ Docker image builds for production

---

## 🎯 Final Checklist Before Hackathon

- [ ] `.cursorrules` copied to project root
- [ ] `CURSORRULES-README.md` available for reference
- [ ] `PHASE-TRANSITION-GUIDE.md` printed or on second screen
- [ ] Cursor IDE installed and Claude Opus 4.5 selected
- [ ] Docker Desktop running
- [ ] Git repository initialized
- [ ] Coffee/energy drinks ready ☕

---

## 🚀 You're Ready!

**The phased approach gives you:**
- ✅ Clear progression (don't skip steps)
- ✅ Fast infrastructure (2 hours, not 8)
- ✅ Working tracer bullet (proof of concept)
- ✅ Incremental complexity (avoid overwhelm)
- ✅ Emergency rollback (if something breaks)

**Remember the mantra:**
```
Phase 0: "Does it connect?" 🔗
Phase 1: "Does it work?" ⚙️
Phase 2: "Does it shine?" ✨
```

**Now go build FixFit and win that hackathon!** 🏆🚀💪

---

*Questions? Check CURSORRULES-README.md*
*Quick lookup? Check PHASE-TRANSITION-GUIDE.md*
*Emergency? Check escape hatches in .cursorrules*
