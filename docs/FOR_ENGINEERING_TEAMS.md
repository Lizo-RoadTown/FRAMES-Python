# Engineering Teams & Program Leads README

## Overview
This system transforms your team's real engineering workflows into structured onboarding and continuity tools. By integrating with platforms like Notion, GitHub, Jira, and Confluence, it converts your daily engineering activity into standardized, educationally sound modules with minimal effort.

You can use **any component independently**—the integration layer, the module generator, the LMS, or the analytics.

---

## What This System Provides

- Automated onboarding module creation  
- Structured workflow extraction  
- Standardized documentation-to-training pipeline  
- Capture of tacit and legacy knowledge  
- Reduced need for repeated re-teaching  
- Stronger subsystem continuity across semesters  
- Stable foundations for long-term missions  

---

## Engineering Integration Workflow

Engineering teams continue using their normal tools.

The system:

1. Connects to your documentation or task systems via official APIs  
2. Pulls structured documents, tasks, and workflows  
3. Normalizes content through a React-based editor  
4. Converts finalized workflows into OATutor-structured modules  
5. Sends modules to the Student LMS for onboarding  

No extra formatting or manual reorganization needed.

---

## Architecture (Engineering Layer)

```
        ┌─────────────────────────────┐
        │     Engineering Tools       │
        │ Notion • GitHub • Jira etc. │
        └───────────────┬────────────┘
                        │ Integration Layer
        ┌───────────────▼──────────────┐
        │   Cleaned Task & Workflow    │
        │     Extracted Dataset        │
        └───────────────┬──────────────┘
                        │ Module Generator
             ┌──────────▼───────────┐
             │   OATutor-Structured │
             │        Modules       │
             └──────────┬───────────┘
                        │ Delivery
              ┌─────────▼─────────┐
              │   Student LMS     │
              └────────────────────┘
```

---

## Example Workflow (CLI)

```bash
frames-integrate --source=notion --workspace=Avionics
frames-generate --format=oatutor --output=modules/avionics_intro.json
```

These commands:

- Connect to Notion  
- Pull subsystem documentation  
- Normalize workflows  
- Generate a clean OATutor module automatically  

---

## Who This Helps

- CubeSat Teams  
- Robotics Teams  
- Rocketry Clubs  
- R&D Labs  
- Multidisciplinary Engineering Projects  
- Industry Onboarding Programs  
- Capstone and Senior Design Courses  

---

## Outcomes for Engineering Teams

- Faster onboarding  
- Less lost knowledge  
- Clear, reusable workflows  
- Predictable semester transitions  
- Reduced documentation drift  
- Modules that stay aligned with actual team work  

---

## Coming Soon
- Subsystem template libraries  
- Test-stand data integrations  
- Hands-on lab activity generator  
