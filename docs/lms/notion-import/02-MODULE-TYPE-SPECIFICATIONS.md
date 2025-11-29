# Module Type Specifications

**Purpose:** Define all interaction types that modules can use in the FRAMES Learning Module Builder system.

---

## Overview

The FRAMES LMS supports **5 primary module types**, each designed for different learning objectives. Modules can mix types or use pure implementations.

---

## Type A: Text Modules (✅ Implemented)

### Purpose
- Orientation content
- Policies and procedures
- Conceptual foundations
- Safety information

### Interaction Level
**Low** - Linear reading with navigation

### Current Implementation
- Static text content
- Previous/Next buttons
- Progress tracking
- Mobile-responsive

### Example Modules
- Lab Safety 101
- Team Communication Norms
- Project Overview

### Database Fields
```
section_type: 'text'
content: Text (markdown-compatible)
```

---

## Type B: Sandbox Modules (🚧 Planned)

### Purpose
- Real tool practice
- Code editing
- Configuration practice
- Parameter adjustment

### Interaction Level
**High** - Full tool fidelity, realistic workflows

### Features Required
- Code editor (Monaco/CodeMirror)
- File browser
- Run/compile functionality
- Real error messages
- Output display
- Save/restore state

### Example Modules
- "Your First Python Script"
- "Configure a Build File"
- "Debug a Simple Error"
- "Mission Parameter Simulator"

### Database Fields
```
section_type: 'sandbox'
content: Initial code/config (JSON)
sandbox_config: {
  language: 'python' | 'javascript' | 'yaml',
  files: [{name, content}],
  runnable: true/false,
  expected_output: string
}
```

### Integration Needs
- Monaco Editor (VS Code engine)
- Web-based Python interpreter (Pyodide/Skulpt)
- Custom file system abstraction

---

## Type C: Game Modules (🚧 Planned)

### Purpose
- Speed and accuracy
- Pattern recognition
- Automaticity
- Fluency building

### Interaction Level
**Medium-High** - Repeatable, timed, scored

### Features Required
- Timer
- Scoring system
- Leaderboards (optional)
- Increasing difficulty
- Visual feedback
- Replay functionality

### Example Modules
- "Velocity Matching Puzzle"
- "System Telemetry Speed Sort"
- "Wiring Pattern Match"
- "Symbol Recognition Drill"

### Database Fields
```
section_type: 'game'
content: Game instructions
game_config: {
  game_type: 'matching' | 'sorting' | 'reaction',
  difficulty_levels: [1, 2, 3, 4, 5],
  time_limit: 60,
  target_accuracy: 0.85,
  challenges: [{...}]
}
```

### Integration Needs
- Phaser.js or PixiJS game engine
- Touch-optimized controls
- Score persistence
- Analytics hooks

---

## Type D: Interactive Modules (🚧 Planned)

### Purpose
- Exploration
- Spatial understanding
- Discovery learning
- Navigation practice

### Interaction Level
**Medium** - Click, drag, explore, manipulate

### Features Required
- Clickable hotspots
- Drag-and-drop objects
- 3D navigation (optional)
- Tooltips/popovers
- State tracking
- Multi-step tasks

### Example Modules
- "Virtual Lab Tour"
- "Subsystem Explorer"
- "Block Diagram Builder"
- "Equipment Assembly"

### Database Fields
```
section_type: 'interactive'
content: Instructions
interactive_config: {
  environment_type: '2d' | '3d',
  assets: [{id, url, type}],
  hotspots: [{x, y, z, action, tooltip}],
  tasks: [{id, description, completion_criteria}]
}
```

### Integration Needs
- Three.js or Babylon.js (3D)
- React DnD (drag-drop)
- Custom interaction handlers
- Asset loading system

---

## Type E: Guided Struggle Modules (🚧 Planned)

### Purpose
- Problem-solving
- Critical thinking
- AI-assisted learning
- Debugging practice

### Interaction Level
**Variable** - Combines other types with AI coaching

### Features Required
- AI Cohort Buddy chat interface
- Hints system (progressive disclosure)
- Error analysis
- Contextual help
- Decision trees
- Multiple solution paths

### Example Modules
- "Debug Your First Error"
- "Choose the Right Approach"
- "Diagnose System Behavior"
- "Mission Planning Decision Tree"

### Database Fields
```
section_type: 'guided_struggle'
content: Problem scenario
struggle_config: {
  problem_type: 'debug' | 'decision' | 'analysis',
  initial_state: {...},
  correct_paths: [{steps, explanation}],
  hints: [{trigger_condition, hint_text}],
  buddy_personality: 'curious' | 'methodical' | 'encouraging'
}
```

### Integration Needs
- Anthropic Claude API
- Chat UI component
- Hint trigger system
- Solution validation logic
- Analytics for struggle patterns

---

## Mixed-Type Modules

Modules can combine types in sequences:

**Example: "Welcome to the Lab"**
1. Text - Overview
2. Interactive - Virtual tour
3. Game - Quick knowledge check
4. Guided Struggle - First task with AI buddy

**Database Approach:**
Each section has its own `section_type` and type-specific config.

---

## Interaction Data Tracking

All module types must emit these analytics events:

### Common Events (All Types)
- `section_view` - Section loaded
- `section_complete` - Section finished
- `pause` - User pauses (>30s idle)
- `resume` - User returns
- `complete` - Module finished

### Type-Specific Events

**Sandbox:**
- `code_run` - Code executed
- `error_encountered` - Compilation/runtime error
- `code_change` - Edit made
- `hint_used` - Help requested

**Game:**
- `game_start` - Game begins
- `game_complete` - Game finished
- `score` - Final score
- `retry` - Replay clicked
- `difficulty_change` - Level adjusted

**Interactive:**
- `hotspot_click` - Element clicked
- `object_drag` - Item moved
- `task_complete` - Sub-task finished
- `discovery` - Hidden element found

**Guided Struggle:**
- `buddy_message` - AI responds
- `student_message` - Student asks question
- `hint_requested` - Hint clicked
- `solution_attempted` - Student tries solution
- `give_up` - Skip requested

---

## Adaptive Difficulty Hooks

Each module type can support difficulty adjustment:

### Triggers
- Too many errors → reduce complexity
- Fast completion + high accuracy → increase challenge
- Multiple hints used → add scaffolding
- Long pauses → offer simpler path

### Adjustments

**Sandbox:**
- Pre-populate more code
- Provide more comments
- Reduce complexity of task

**Game:**
- Slow down timer
- Reduce number of items
- Increase target size

**Interactive:**
- Add more tooltips
- Highlight next step
- Reduce distractors

**Guided Struggle:**
- AI buddy becomes more directive
- Hints appear earlier
- Suggest breaking problem into parts

---

## Module Type Selection Guide

**Use Text when:**
- Content is primarily informational
- No practice needed
- Safety/compliance requirements
- Quick reference

**Use Sandbox when:**
- Students need real tool practice
- Errors are valuable learning moments
- Building technical skills
- Preparing for real work

**Use Game when:**
- Speed and automaticity matter
- Pattern recognition is key
- Motivation needs boost
- Repetition aids learning

**Use Interactive when:**
- Spatial/visual understanding required
- Exploration drives learning
- Discovery is motivating
- Navigation is a skill

**Use Guided Struggle when:**
- Problem-solving is the goal
- Multiple solution paths exist
- Debugging/critical thinking matters
- AI coaching adds value

---

## Implementation Priority

**Phase 1:** Text (✅ Done)
**Phase 2:** Interactive (easiest addition)
**Phase 3:** Sandbox (high value for CS students)
**Phase 4:** Game (motivation + fluency)
**Phase 5:** Guided Struggle (most complex, requires AI integration)
