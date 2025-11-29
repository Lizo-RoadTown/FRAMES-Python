# FRAMES LMS - Project Overview

**Status:** 🚧 Active Development
**Phase:** Initial Architecture & Prototyping
**Last Updated:** November 26, 2025

---

## Vision

Create an adaptive, interactive learning platform that transforms student onboarding from passive reading to immersive skill-building through:

- **Sandbox environments** (code editors, virtual lab spaces, simulations)
- **Game mechanics** (speed drills, pattern matching, scoring)
- **AI Cohort Buddy** (peer-like conversational AI coach)
- **Multi-modal interaction** (touch, drag, type, manipulate 3D objects)
- **Adaptive difficulty** based on real-time struggle signals
- **Rich analytics** tracking pause patterns, retries, confusion signals

---

## Learning Philosophy

**Productive Struggle** - Not hand-holding, not overwhelm
- Try → Fail → Try Again
- Form mental models through authentic problems
- Build confidence through practice
- Deepen mastery across multiple modalities

**Not a slideshow. An experiential space.**

---

## Target Users

### Primary: Incoming Students
- New to the FRAMES lab environment
- Need orientation before joining team activities
- Using touchscreen tablets/iPads at onboarding stations
- Ages 18-25, diverse technical backgrounds

### Secondary: Team Leads
- Rely on LMS to handle foundational training
- Need analytics to identify struggling students
- Want to reduce time spent on basic orientation

---

## Current Implementation

### What's Built (Phase 0)
✅ **React + Flask Architecture**
- Vision UI Dashboard React frontend (Material-UI)
- Flask REST API backend
- PostgreSQL (Neon) database
- Module library page (card grid)
- Simple text-based module viewer
- Basic progress tracking

✅ **Database Schema**
- `modules` - Module metadata
- `module_sections` - Content sections
- `module_progress` - Student progress
- `module_assignments` - Student-module assignments
- `module_analytics_events` - Interaction tracking
- `module_feedback` - Ratings and comments

✅ **Sample Content**
- "Lab Safety 101" text module (6 sections)

### What's Missing (Phase 1+)
❌ Mobile-optimized UI (sidebar removal)
❌ Module type system (text, sandbox, game, interactive)
❌ Component loader for different interaction types
❌ AI Cohort Buddy integration
❌ Rich analytics dashboard
❌ Adaptive difficulty engine
❌ Module builder interface

---

## Technology Stack

### Current
- **Frontend:** React 18, Material-UI, Vision UI Dashboard theme
- **Backend:** Flask, SQLAlchemy
- **Database:** PostgreSQL (Neon hosted)
- **APIs:** REST (Flask)

### Planned Additions
- **Code Sandboxes:** Monaco Editor (VS Code in browser)
- **3D/Interactive:** Three.js or Babylon.js
- **Game Engine:** Phaser.js or PixiJS
- **Drag-Drop:** React DnD or dnd-kit
- **AI:** Anthropic Claude API (conversational buddy)
- **Analytics:** Custom event tracking + visualization

---

## Key Decisions

### Architecture
- **Monorepo:** All apps in one repo under `apps/`
- **Shared Database:** Single PostgreSQL instance for all applications
- **API-First:** Flask serves JSON, React consumes

### Mobile Strategy
- **Touch-First:** Designed for tablets (10-13" screens)
- **Fullscreen Modules:** Remove sidebar during learning for immersion
- **Landscape Preferred:** But must work in portrait

### Module Types
Modules are classified by interaction mode:
- **Text** - Current implementation (orientation, policies)
- **Sandbox** - Real tool usage (code editors, config panels)
- **Game** - Speed drills, pattern matching, automaticity
- **Interactive** - Clickable environments, 3D navigation
- **Guided Struggle** - AI-moderated problem-solving

---

## Success Metrics

### Student Outcomes
- Completion rate > 85%
- Time to proficiency reduced by 50%
- Team lead intervention requests < 10%
- Student confidence scores > 4/5

### System Performance
- Module load time < 2 seconds
- Analytics latency < 100ms
- Uptime > 99.5%

### Content Quality
- Module engagement (time on task) > 10 min/module
- Retry rate (productive struggle indicator) 20-40%
- Student feedback ratings > 4/5

---

## Project Context

### Related Systems
- **Research Analytics Dashboard** (`apps/research-analytics`) - Faculty/researcher tools
- **AI Prediction Core** (`apps/ai-core`) - ML models for outcomes (planned)

### Shared Infrastructure
- `shared/database/` - Database models and connection utilities
- All three applications share one Neon PostgreSQL database

---

## Next Steps

**Immediate:**
1. Clean up mobile UI (remove sidebar for module viewer)
2. Add module type field to database schema
3. Create component loader system

**Short-term:**
4. Integrate first interactive framework (TBD based on GitHub repos)
5. Build one prototype interactive module (e.g., Virtual Lab Tour)
6. Add AI Buddy API integration

**Medium-term:**
7. Build module builder interface
8. Implement adaptive difficulty engine
9. Create analytics dashboard for team leads

---

## Resources

- **GitHub:** [Lizo-RoadTown/Frames-App](https://github.com/Lizo-RoadTown/Frames-App)
- **Docs:** `docs/lms/` and `docs/shared/`
- **Database:** Neon PostgreSQL (connection string in `.env`)
- **Design Specs:** See `02-MODULE-TYPE-SPECIFICATIONS.md`
