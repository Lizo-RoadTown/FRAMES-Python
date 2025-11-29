# FRAMES LMS - Module Creation Workflow

**Version:** 1.0
**Last Updated:** November 26, 2025
**Status:** Active - Phase 1 Implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [The 7-Step Workflow](#the-7-step-workflow)
4. [Module Types Reference](#module-types-reference)
5. [Quality Checklist](#quality-checklist)
6. [Notion Integration](#notion-integration)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This workflow guides instructors and developers through creating effective training modules for the FRAMES Student Onboarding LMS. The system supports **5 module types** with varying levels of interactivity and complexity.

### Current System Status
- **Database:** 6 LMS tables operational (Neon PostgreSQL)
- **Frontend:** React viewer with Vision UI Dashboard
- **Backend:** Flask REST API at http://localhost:5001
- **Supported Types:** Text (Phase 0), Interactive/Sandbox/Game/Buddy (Phase 1+)

### Who Should Use This Workflow?
- **Team Leads:** Creating onboarding content for incoming students
- **Faculty:** Designing domain-specific training modules
- **Developers:** Implementing new module types
- **Content Designers:** Building interactive learning experiences

---

## Prerequisites

### System Requirements
- [x] Neon PostgreSQL database access
- [x] Flask backend running (port 5001)
- [x] React frontend running (port 3000)
- [x] Python environment with SQLAlchemy
- [x] Node.js 18+ with React development tools

### Knowledge Requirements
- Basic understanding of LMS module structure
- Familiarity with Markdown (for text modules)
- Python (for database operations)
- React (for interactive modules)
- Access to Notion workspace (optional, for documentation)

### Access Requirements
- Database credentials for Neon PostgreSQL
- GitHub repository access (for version control)
- Notion workspace access (for collaborative planning)
- Anthropic API key (for AI Buddy modules only)

---

## The 7-Step Workflow

### STEP 1: CONCEPT & PLANNING

**Goal:** Define what you're building and why

#### 1.1 Define Learning Objective
Answer these questions:
- What should students **know** after completing this module?
- What should students **be able to do**?
- How does this fit into the larger onboarding journey?

**Example:**
> "After completing 'Lab Safety 101', students will be able to identify 5 key safety protocols and locate emergency equipment in the lab."

#### 1.2 Choose Module Type

| Type | Best For | Implementation Phase |
|------|----------|---------------------|
| **Text** | Reading comprehension, policies, background info | Phase 0 ✅ |
| **Interactive** | Spatial learning, exploration, discovery | Phase 2 🎯 |
| **Sandbox** | Coding practice, debugging, hands-on skills | Phase 3 💻 |
| **Game** | Speed drills, memorization, pattern recognition | Phase 4 🎮 |
| **Buddy** | Guided struggle, problem-solving, critical thinking | Phase 5 🤖 |

**Decision Criteria:**
- **Passive consumption?** → Text
- **Spatial/visual learning?** → Interactive
- **Coding practice?** → Sandbox
- **Speed/accuracy drills?** → Game
- **Complex problem-solving?** → Buddy

#### 1.3 Estimate Completion Time
- Text modules: 5-15 minutes
- Interactive modules: 10-20 minutes
- Sandbox modules: 15-30 minutes
- Game modules: 5-10 minutes
- Buddy modules: 20-40 minutes

#### 1.4 Identify Prerequisites
- What modules must be completed first?
- What prior knowledge is assumed?
- Are there any technical prerequisites (e.g., Python installed)?

#### 1.5 Document in Notion
Create a Notion page with:
- Module title and objective
- Target audience (incoming/established/outgoing students)
- Module type and estimated time
- Prerequisites list
- Draft outline of sections

**Action Items:**
- [ ] Complete learning objective statement
- [ ] Choose module type from table above
- [ ] Estimate completion time
- [ ] List prerequisites
- [ ] Create Notion planning page

---

### STEP 2: DESIGN & CONTENT

**Goal:** Create the instructional content and assets

#### 2.1 Write Instructional Content

**For Text Modules:**
- Break content into 3-7 logical sections
- Use clear headings and subheadings
- Include examples and visuals
- Keep paragraphs short (2-4 sentences)
- Use bullet points for lists
- Add summaries at the end

**For Interactive Modules:**
- Write brief instructions (1-2 sentences)
- Design clickable areas (hotspots)
- Create tooltips/popup text
- Define completion tasks
- Script feedback messages

**For Sandbox Modules:**
- Write problem description
- Create starter code template
- Define expected output
- Write hint progression (3-5 hints)
- Add validation logic

**For Game Modules:**
- Define game mechanics
- Write challenge prompts
- Create difficulty levels
- Design scoring algorithm
- Add win/lose conditions

**For Buddy Modules:**
- Write scenario description
- Define struggle points
- Create buddy personality
- Script conversation triggers
- Add safety guardrails

#### 2.2 Create Assets

**Required Assets by Type:**

| Module Type | Assets Needed |
|-------------|---------------|
| Text | Images, diagrams, embedded videos |
| Interactive | Clickable map/diagram, icons, tooltips |
| Sandbox | Code templates, test cases, solution code |
| Game | Sprites, sounds, background images |
| Buddy | Context documents, example conversations |

**Asset Guidelines:**
- Images: PNG/JPG, max 2MB, mobile-optimized
- Videos: MP4, max 50MB, hosted externally (YouTube/Vimeo)
- Audio: MP3, max 5MB
- Code: Plain text, syntax-highlighted
- Diagrams: SVG preferred (scalable)

#### 2.3 Design Interaction Flow

Create a flowchart showing:
1. Module start
2. Section progression
3. Decision points (if adaptive)
4. Success/failure paths
5. Module completion

**Tools:** Draw.io, Miro, Figma, or pen & paper

#### 2.4 Define Success Criteria

**Completion Criteria:**
- What must students do to complete each section?
- What constitutes "passing" the module?
- Are retries allowed?

**Examples:**
- Text: Read all sections, reach end
- Interactive: Click 5 hotspots, complete task
- Sandbox: Code passes all test cases
- Game: Score above threshold
- Buddy: Demonstrate understanding in conversation

#### 2.5 Map Analytics Events

Plan what to track:

| Event Type | When to Trigger | Data to Capture |
|------------|----------------|-----------------|
| `module_start` | Module opened | timestamp, student_id |
| `section_view` | Section loaded | section_number, timestamp |
| `interaction` | Hotspot clicked, code run, etc. | interaction_type, details |
| `struggle_signal` | Long pause, retry, hint used | signal_type, intensity |
| `section_complete` | Section finished | time_spent, scroll_depth |
| `module_complete` | Module finished | total_time, completion_percent |

**Action Items:**
- [ ] Write all instructional text
- [ ] Create/gather all required assets
- [ ] Draw interaction flow diagram
- [ ] Define completion criteria
- [ ] Map analytics events

---

### STEP 3: DATABASE ENTRY

**Goal:** Add module to database with proper structure

#### 3.1 Create Module Record

**Using Python Script:**

```python
from shared.database.db_models import Module, db
from datetime import datetime

# Create new module
new_module = Module(
    module_id="lab-safety-101",  # Unique ID (kebab-case)
    title="Lab Safety 101",
    description="Essential safety protocols for entering the lab",
    category="Safety",  # Safety, Technical, Team, Project
    estimated_minutes=10,
    created_by_id="faculty-liz-osborn",  # Faculty ID
    university_id="cpp",  # University ID
    status="draft",  # draft, published, archived
    prerequisites=[],  # List of prerequisite module_ids
    related_modules=["equipment-tour"],
    tags=["safety", "onboarding", "required"],
    target_audience="incoming_students",
    notion_page_id=None,  # Optional: Notion page ID
    content_source="database"  # database, notion, or hybrid
)

db.session.add(new_module)
db.session.commit()

print(f"Module created with ID: {new_module.id}")
```

#### 3.2 Create Module Sections

**For each section in your module:**

```python
from shared.database.db_models import ModuleSection

# Section 1: Introduction
section_1 = ModuleSection(
    module_id=new_module.id,  # Foreign key to module
    section_number=1,
    section_type="text",  # text, interactive, sandbox, game, buddy
    title="Welcome to Lab Safety",
    content="""
# Welcome to Lab Safety 101

This module will teach you the essential safety protocols...

## Learning Objectives
- Identify emergency equipment locations
- Understand PPE requirements
- Know evacuation procedures
    """,
    media_url=None,  # Optional: URL to image/video
    duration_seconds=120  # Estimated reading time
)

db.session.add(section_1)

# Section 2: Interactive
section_2 = ModuleSection(
    module_id=new_module.id,
    section_number=2,
    section_type="interactive",
    title="Locate Safety Equipment",
    content=json.dumps({
        "instruction": "Click on 5 safety equipment locations",
        "hotspots": [
            {"id": "fire-extinguisher", "x": 100, "y": 200, "label": "Fire Extinguisher"},
            {"id": "eye-wash", "x": 300, "y": 150, "label": "Eye Wash Station"},
            # ... more hotspots
        ],
        "completion_criteria": {"hotspots_clicked": 5}
    }),
    media_url="/assets/lab-floor-plan.png"
)

db.session.add(section_2)
db.session.commit()
```

#### 3.3 Set Module Type Configuration

**For modules with special configs:**

```python
# Update module with type-specific settings
new_module.module_type = "interactive"
new_module.interaction_level = "medium"  # low, medium, high
new_module.required_components = ["react-dnd", "framer-motion"]

db.session.commit()
```

#### 3.4 Verify Database Entry

```python
# Retrieve and verify
module = Module.query.filter_by(module_id="lab-safety-101").first()
print(module.to_dict())

# Check sections
sections = ModuleSection.query.filter_by(module_id=module.id).order_by(ModuleSection.section_number).all()
for section in sections:
    print(f"Section {section.section_number}: {section.title}")
```

**Action Items:**
- [ ] Create module record in database
- [ ] Add all sections with content
- [ ] Set module type and configuration
- [ ] Verify data with query

---

### STEP 4: COMPONENT DEVELOPMENT (If New Module Type)

**Goal:** Build the React viewer component

**Skip this step if using an existing module type (e.g., text)**

#### 4.1 Create Viewer Component

**File Structure:**
```
apps/onboarding-lms/frontend-react/src/
  └── components/
      └── viewers/
          ├── TextViewer.js       ✅ Already exists
          ├── InteractiveViewer.js  🚧 Phase 2
          ├── SandboxViewer.js      🚧 Phase 3
          ├── GameViewer.js         🚧 Phase 4
          └── BuddyViewer.js        🚧 Phase 5
```

**Example: InteractiveViewer.js**

```javascript
import React, { useState } from 'react';
import { Box, Image, Tooltip, VStack, Text } from '@chakra-ui/react';

function InteractiveViewer({ section, onProgress }) {
  const config = JSON.parse(section.content);
  const [clickedHotspots, setClickedHotspots] = useState(new Set());

  const handleHotspotClick = (hotspotId) => {
    const newClicked = new Set(clickedHotspots);
    newClicked.add(hotspotId);
    setClickedHotspots(newClicked);

    // Track analytics
    trackEvent('hotspot_click', { hotspot_id: hotspotId });

    // Check completion
    if (newClicked.size >= config.completion_criteria.hotspots_clicked) {
      onProgress(100); // Mark section complete
    }
  };

  return (
    <VStack spacing={4}>
      <Text fontSize="lg">{config.instruction}</Text>
      <Box position="relative">
        <Image src={section.media_url} alt="Interactive diagram" />
        {config.hotspots.map(hotspot => (
          <Tooltip key={hotspot.id} label={hotspot.label}>
            <Box
              position="absolute"
              left={hotspot.x}
              top={hotspot.y}
              width="40px"
              height="40px"
              borderRadius="50%"
              bg={clickedHotspots.has(hotspot.id) ? 'green.400' : 'blue.400'}
              cursor="pointer"
              onClick={() => handleHotspotClick(hotspot.id)}
              _hover={{ transform: 'scale(1.1)' }}
            />
          </Tooltip>
        ))}
      </Box>
    </VStack>
  );
}

export default InteractiveViewer;
```

#### 4.2 Update Module Renderer

**File: ModuleRenderer.js**

```javascript
import TextViewer from './viewers/TextViewer';
import InteractiveViewer from './viewers/InteractiveViewer';
import SandboxViewer from './viewers/SandboxViewer';
// ... other imports

const VIEWER_REGISTRY = {
  text: TextViewer,
  interactive: InteractiveViewer,
  sandbox: SandboxViewer,
  game: GameViewer,
  buddy: BuddyViewer,
};

function ModuleRenderer({ section, onProgress }) {
  const ViewerComponent = VIEWER_REGISTRY[section.section_type];

  if (!ViewerComponent) {
    return <div>Unknown section type: {section.section_type}</div>;
  }

  return <ViewerComponent section={section} onProgress={onProgress} />;
}

export default ModuleRenderer;
```

#### 4.3 Implement Progress Tracking

**Connect to backend:**

```javascript
const updateProgress = async (moduleId, studentId, progressData) => {
  const response = await fetch(`/api/modules/${moduleId}/progress`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      student_id: studentId,
      progress_percent: progressData.percent,
      current_section: progressData.section,
      status: progressData.status  // in_progress, completed
    })
  });
  return response.json();
};
```

#### 4.4 Add Analytics Integration

```javascript
const trackEvent = async (eventType, eventData) => {
  await fetch('/api/analytics/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      module_id: moduleId,
      student_id: studentId,
      event_type: eventType,
      timestamp: new Date().toISOString(),
      meta: eventData
    })
  });
};
```

#### 4.5 Mobile Optimization

**Responsive Design Checklist:**
- [ ] Touch targets minimum 44px × 44px
- [ ] Test on tablet (iPad/Android 10-13")
- [ ] Works in portrait and landscape
- [ ] No horizontal scrolling
- [ ] Large, readable fonts (16px minimum)
- [ ] Adequate spacing between interactive elements

**Action Items:**
- [ ] Create viewer component file
- [ ] Implement interaction logic
- [ ] Connect to progress API
- [ ] Add analytics tracking
- [ ] Mobile-optimize UI

---

### STEP 5: TESTING

**Goal:** Verify module works correctly on all devices

#### 5.1 Desktop Testing

**Test Cases:**
- [ ] Module loads without errors
- [ ] All sections display correctly
- [ ] Navigation works (next/previous)
- [ ] Progress bar updates
- [ ] Completion triggers correctly
- [ ] Analytics events fire

**Tools:** Chrome DevTools, React Developer Tools

#### 5.2 Tablet Testing

**Physical Devices:**
- iPad (10.2" or larger)
- Android tablet (10-13")

**Test Scenarios:**
- [ ] Landscape mode
- [ ] Portrait mode
- [ ] Touch interactions work
- [ ] No UI overflow
- [ ] Readable text size
- [ ] Buttons are tappable

#### 5.3 Cross-Browser Testing

**Browsers to Test:**
- Chrome (primary)
- Safari (iOS compatibility)
- Firefox (fallback)
- Edge (Windows compatibility)

#### 5.4 Analytics Verification

**Check database:**

```python
from shared.database.db_models import ModuleAnalyticsEvent

# Verify events were logged
events = ModuleAnalyticsEvent.query.filter_by(
    module_id=module.id,
    student_id="test-student-001"
).all()

for event in events:
    print(f"{event.event_type} at {event.timestamp}")
```

#### 5.5 Student Pilot Test

**If possible, test with 2-3 real students:**
- Observe without intervention
- Note where they struggle
- Ask for feedback afterward
- Record completion time

**Pilot Test Checklist:**
- [ ] Students understand instructions
- [ ] Interactions are intuitive
- [ ] Completion time matches estimate
- [ ] No technical issues
- [ ] Students feel they learned something

**Action Items:**
- [ ] Complete desktop testing
- [ ] Test on tablet devices
- [ ] Verify cross-browser compatibility
- [ ] Check analytics collection
- [ ] Run pilot test with students

---

### STEP 6: DEPLOYMENT

**Goal:** Make module available to students

#### 6.1 Publish Module

**Update module status:**

```python
module = Module.query.filter_by(module_id="lab-safety-101").first()
module.status = "published"
module.published_at = datetime.utcnow()
db.session.commit()
```

#### 6.2 Assign to Students

**Bulk assignment:**

```python
from shared.database.db_models import ModuleAssignment, StudentModel

# Get all incoming students
incoming_students = StudentModel.query.filter_by(status="incoming").all()

# Assign module to each
for student in incoming_students:
    assignment = ModuleAssignment(
        module_id=module.id,
        student_id=student.id,
        required=True,
        assigned_by_id="faculty-liz-osborn",
        due_date=datetime(2025, 12, 15)  # Optional deadline
    )
    db.session.add(assignment)

db.session.commit()
```

#### 6.3 Monitor Completion Rates

**Dashboard query:**

```python
# Get completion statistics
total_assigned = ModuleAssignment.query.filter_by(module_id=module.id).count()
total_completed = ModuleProgress.query.filter_by(
    module_id=module.id,
    status="completed"
).count()

completion_rate = (total_completed / total_assigned) * 100
print(f"Completion rate: {completion_rate:.1f}%")
```

#### 6.4 Gather Feedback

**Enable feedback collection:**

```python
from shared.database.db_models import ModuleFeedback

# Students can submit feedback
feedback = ModuleFeedback(
    module_id=module.id,
    student_id=student.id,
    rating=5,
    difficulty="just_right",
    clarity=5,
    usefulness=5,
    feedback_text="Very helpful for understanding lab safety!",
    suggestions="Maybe add a video tour?"
)

db.session.add(feedback)
db.session.commit()
```

**Action Items:**
- [ ] Set module status to published
- [ ] Assign to target students
- [ ] Monitor completion rates
- [ ] Enable feedback collection

---

### STEP 7: ITERATION

**Goal:** Improve module based on data and feedback

#### 7.1 Review Analytics

**Key Metrics to Check:**

| Metric | Good Range | Red Flag |
|--------|-----------|----------|
| Completion rate | >80% | <60% |
| Average time | Within 20% of estimate | 2x estimate |
| Drop-off rate | <10% | >25% |
| Hint usage | 2-4 per student | >6 or 0 |
| Retry rate | 20-40% (for challenges) | >60% |

**Query Analytics:**

```python
from sqlalchemy import func

# Average time spent
avg_time = db.session.query(
    func.avg(ModuleProgress.total_time_seconds)
).filter_by(module_id=module.id, status="completed").scalar()

print(f"Average completion time: {avg_time / 60:.1f} minutes")

# Drop-off points
dropoffs = ModuleProgress.query.filter_by(
    module_id=module.id,
    status="in_progress"
).all()

for progress in dropoffs:
    print(f"Student {progress.student_id} stopped at section {progress.current_section}")
```

#### 7.2 Adjust Difficulty

**If completion rate is low:**
- Add more hints
- Simplify instructions
- Break into smaller sections
- Add scaffolding

**If completion rate is very high (>95%):**
- May be too easy
- Consider adding optional challenges
- Reduce hints

#### 7.3 Update Content

**Based on feedback:**
- Fix confusing instructions
- Add requested examples
- Replace unclear images
- Update outdated information

**Version Control:**

```python
# Increment revision number
module.revision += 1
module.updated_at = datetime.utcnow()
db.session.commit()
```

#### 7.4 A/B Testing (Advanced)

**Test variations:**
- Different instruction wording
- Alternative interaction patterns
- Various difficulty levels

**Track which version performs better:**

```python
# Add to module meta field
module.meta = {
    "ab_test": {
        "variant": "A",  # or "B"
        "start_date": "2025-11-26",
        "metric": "completion_rate"
    }
}
db.session.commit()
```

**Action Items:**
- [ ] Review analytics dashboard
- [ ] Identify areas for improvement
- [ ] Update content based on feedback
- [ ] Increment revision number
- [ ] Monitor impact of changes

---

## Module Types Reference

### Type 1: Text Module
**Phase:** 0 (Complete)
**Complexity:** Low
**Best For:** Reading comprehension, policies, background information

**Components:**
- Markdown-formatted text
- Embedded images
- Optional videos
- Progress tracking

**Example Modules:**
- Lab Safety 101
- Code of Conduct
- Project Overview

### Type 2: Interactive Module
**Phase:** 2 (In Progress)
**Complexity:** Medium
**Best For:** Spatial learning, exploration, discovery

**Components:**
- Clickable hotspots
- Tooltips and popups
- Task completion tracking
- Feedback messages

**Example Modules:**
- Virtual Lab Tour
- Subsystem Explorer
- Equipment Assembly

### Type 3: Sandbox Module
**Phase:** 3 (Planned)
**Complexity:** High
**Best For:** Coding practice, debugging, hands-on skills

**Components:**
- Monaco code editor
- Code execution (Pyodide or backend)
- Test case validation
- Hint system
- Error handling

**Example Modules:**
- Hello World in Python
- Fix the Bug
- Complete the Function

### Type 4: Game Module
**Phase:** 4 (Planned)
**Complexity:** High
**Best For:** Speed drills, memorization, pattern recognition

**Components:**
- Game engine (Phaser/PixiJS)
- Timer system
- Scoring logic
- Leaderboard
- Replay functionality

**Example Modules:**
- Subsystem Matching
- Fast Parameter Sort
- Error Code Memory

### Type 5: AI Buddy Module
**Phase:** 5 (Planned)
**Complexity:** Very High
**Best For:** Guided struggle, problem-solving, critical thinking

**Components:**
- Anthropic Claude API
- Chat interface
- Context management
- Struggle detection
- Personality modes

**Example Modules:**
- Debug Your First Error
- Choose the Right Tool
- Diagnose System Behavior

---

## Quality Checklist

Use this checklist before publishing any module:

### Content Quality
- [ ] Learning objectives are clear and measurable
- [ ] Instructions are concise and unambiguous
- [ ] Examples are relevant and helpful
- [ ] Text is free of typos and grammatical errors
- [ ] Technical accuracy verified by subject matter expert

### Technical Quality
- [ ] Module loads in <2 seconds
- [ ] All interactions work as expected
- [ ] No console errors or warnings
- [ ] Progress tracking functions correctly
- [ ] Analytics events fire properly

### Mobile Compatibility
- [ ] Works on tablet (10-13" screen)
- [ ] Touch targets are adequately sized
- [ ] No horizontal scrolling
- [ ] Text is readable without zooming
- [ ] Layout adapts to portrait/landscape

### Accessibility
- [ ] Color contrast meets WCAG AA standards
- [ ] Interactive elements are keyboard accessible
- [ ] Alt text provided for images
- [ ] Screen reader compatible (basic)

### Student Experience
- [ ] Completion time matches estimate
- [ ] Difficulty is appropriate for target audience
- [ ] Feedback is clear and constructive
- [ ] Module fits into learning pathway

---

## Notion Integration

### Setting Up Notion Pages

**Option 1: Database Content Source**
- Store content in PostgreSQL only
- Use Notion for planning/documentation
- Set `content_source = 'database'`

**Option 2: Notion Content Source**
- Store content in Notion pages
- Fetch via Notion API at runtime
- Set `content_source = 'notion'`
- Store `notion_page_id` in module record

**Option 3: Hybrid**
- Metadata in PostgreSQL
- Rich content in Notion
- Best of both worlds
- Set `content_source = 'hybrid'`

### Notion Page Template

```markdown
# Module: [Title]

## Overview
- **Type:** [text/interactive/sandbox/game/buddy]
- **Estimated Time:** [X minutes]
- **Target Audience:** [incoming/established/outgoing]
- **Prerequisites:** [List module IDs]

## Learning Objectives
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Sections
### Section 1: [Title]
- Type: [section type]
- Content: [Draft or link]
- Assets: [List images, videos, etc.]

### Section 2: [Title]
...

## Analytics Events
- [event_type]: [when triggered]

## Testing Notes
- Tested on: [devices/browsers]
- Pilot feedback: [summary]

## Iteration Log
- **v1.0** (2025-11-26): Initial release
- **v1.1** (2025-12-01): Updated instructions based on feedback
```

### Syncing Notion to Database

**Using MCP HTTP Extension:**

```python
import requests

def sync_notion_to_db(notion_page_id, module_id):
    # Fetch Notion page content
    notion_content = fetch_notion_page(notion_page_id)

    # Update module in database
    module = Module.query.filter_by(module_id=module_id).first()
    module.notion_page_id = notion_page_id
    module.updated_at = datetime.utcnow()

    # Parse Notion blocks and update sections
    # (Implementation depends on Notion API structure)

    db.session.commit()
```

---

## Troubleshooting

### Common Issues

#### Module doesn't load
**Symptoms:** Blank screen, loading spinner forever
**Causes:**
- Database connection issue
- Invalid module_id
- CORS not configured

**Solutions:**
1. Check browser console for errors
2. Verify module exists: `Module.query.filter_by(module_id="...").first()`
3. Check Flask CORS configuration
4. Restart Flask backend

#### Progress not saving
**Symptoms:** Progress resets when page reloads
**Causes:**
- API endpoint not called
- Database write failed
- Student ID mismatch

**Solutions:**
1. Check network tab in DevTools
2. Verify API response is 200 OK
3. Query database: `ModuleProgress.query.filter_by(student_id="...").all()`
4. Check student ID consistency

#### Analytics not recording
**Symptoms:** No events in `module_analytics_events` table
**Causes:**
- Event tracking function not called
- API endpoint error
- JSON serialization issue

**Solutions:**
1. Add `console.log()` to verify events fire
2. Check API response in network tab
3. Validate event data structure
4. Check database constraints

#### Mobile UI broken
**Symptoms:** Layout issues on tablet
**Causes:**
- Fixed widths instead of responsive
- Touch targets too small
- CSS viewport not set

**Solutions:**
1. Use Chakra UI responsive props
2. Set `<meta name="viewport" content="width=device-width, initial-scale=1">`
3. Increase button sizes to 44px minimum
4. Test with Chrome DevTools mobile emulator

---

## Next Steps

Now that you understand the workflow, you can:

1. **Start with Text Modules** (Phase 0 - Ready Now)
   - Easiest to create
   - Build content library
   - Test analytics pipeline

2. **Plan Interactive Modules** (Phase 2 - Next Priority)
   - Design lab tour or subsystem explorer
   - Gather visual assets
   - Prototype interaction patterns

3. **Prepare for Sandbox** (Phase 3)
   - Research Monaco Editor integration
   - Plan coding challenges
   - Test Pyodide (client-side Python)

4. **Document in Notion**
   - Create module planning workspace
   - Track module creation pipeline
   - Collaborate with team leads

---

## Resources

### Documentation
- [Database Schema](03-DATABASE-SCHEMA.md)
- [Development Roadmap](04-DEVELOPMENT-ROADMAP.md)
- [Module Type Specifications](02-MODULE-TYPE-SPECIFICATIONS.md)

### External Tools
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - Code editor
- [Chakra UI](https://chakra-ui.com/) - React component library
- [Pyodide](https://pyodide.org/) - Python in browser
- [Notion API](https://developers.notion.com/) - Content integration

### Support
- **GitHub Issues:** [Report bugs](https://github.com/Lizo-RoadTown/Frames-App/issues)
- **Team Lead:** eosborn@cpp.edu
- **Documentation:** [docs/lms/](.)

---

**Version History:**
- v1.0 (2025-11-26): Initial workflow documentation
