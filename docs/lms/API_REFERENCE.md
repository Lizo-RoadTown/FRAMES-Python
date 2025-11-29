# LMS API Reference
## Ascent Basecamp Learning Management System

**Version:** 1.0  
**Base URL:** `/api/lms`  
**Last Updated:** 2025-11-28

---

## Overview

The LMS API provides endpoints for managing student learning experiences, tracking progress, and enabling competitive features. It supports the Ascent Basecamp learning system with ghost cohorts, subsystem competency tracking, and race mode.

### Key Features
- ✅ Module lifecycle management (start → activity → complete)
- ✅ Real-time progress tracking
- ✅ Subsystem competency progression
- ✅ Leaderboards and rankings
- ✅ Ghost cohort benchmarking
- ✅ Competitive race mode

### Authentication
All endpoints require authentication. Include the student ID in the URL path.

---

## Endpoints

### Module Lifecycle

#### Start Module
Start a learning module session.

**Endpoint:** `POST /students/{student_id}/modules/{module_id}/start`

**Parameters:**
- `student_id` (path): Student identifier
- `module_id` (path): Module identifier (integer)

**Response (201):**
```json
{
  "success": true,
  "log_id": 12345,
  "attempt_number": 1,
  "module_title": "Power Systems Fundamentals",
  "started_at": "2025-11-28T10:30:00.000Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/lms/students/student_001/modules/42/start
```

---

#### Log Activity
Track progress during module (time spent, errors).

**Endpoint:** `POST /students/{student_id}/modules/{module_id}/log_activity`

**Parameters:**
- `student_id` (path): Student identifier
- `module_id` (path): Module identifier

**Request Body:**
```json
{
  "time_spent_seconds": 120,
  "errors_count": 3,
  "attempt_number": 1  // optional
}
```

**Response (200):**
```json
{
  "success": true,
  "log_id": 12345,
  "time_spent_seconds": 120,
  "errors_count": 3,
  "updated_at": "2025-11-28T10:32:00.000Z"
}
```

**Notes:**
- Updates cumulative time and errors
- If `attempt_number` not provided, uses most recent session
- Call `/start` before using this endpoint

---

#### Complete Module
Mark module as completed with final score.

**Endpoint:** `POST /students/{student_id}/modules/{module_id}/complete`

**Request Body:**
```json
{
  "time_spent_seconds": 300,
  "errors_count": 2,
  "mastery_score": 85.5,
  "attempt_number": 1  // optional
}
```

**Response (200):**
```json
{
  "success": true,
  "completed_at": "2025-11-28T10:35:00.000Z",
  "mastery_score": 85.5,
  "subsystem": "power",
  "modules_completed": 5,
  "competency_level": "competency"
}
```

**Competency Levels:**
- `orientation` - Just starting (0-2 modules)
- `competency` - Building skills (3-5 modules)
- `integration` - Connecting concepts (6-10 modules)
- `autonomy` - Expert level (11+ modules)

**Notes:**
- Automatically updates `subsystem_competency` table
- Mastery score range: 0-100

---

### Competitive Features

#### Get Ghost Cohorts
Retrieve benchmark performance data from historical cohorts.

**Endpoint:** `GET /modules/{module_id}/ghost_cohorts`

**Response (200):**
```json
{
  "success": true,
  "count": 3,
  "ghost_cohorts": [
    {
      "cohort_id": 1,
      "cohort_name": "Fall 2024 Stanford",
      "semester": "Fall 2024",
      "university": "Stanford University",
      "subsystem": "power"
    }
  ],
  "time_targets": {
    "fast": 180,
    "medium": 300,
    "slow": 420
  },
  "checkpoints": [
    {"step": 1, "target_time": 60},
    {"step": 2, "target_time": 120},
    {"step": 3, "target_time": 180}
  ],
  "ghost_data": {
    "average_time": 287,
    "average_score": 82.3,
    "completion_rate": 0.89
  }
}
```

**Notes:**
- Returns empty if no ghost data exists
- Used for competitive race mode
- Provides benchmarking targets

---

#### Get Leaderboard
Retrieve rankings and student position.

**Endpoint:** `GET /students/{student_id}/leaderboard`

**Query Parameters:**
- `subsystem` (optional): Filter by subsystem (e.g., "power", "avionics")
- `module_id` (optional): Specific module leaderboard

**Response (200):**
```json
{
  "success": true,
  "top_10": [
    {
      "student_id": "student_042",
      "best_score": 98.5,
      "best_time": 156,
      "attempts": 2,
      "rank": 1
    },
    {
      "student_id": "student_007",
      "best_score": 95.2,
      "best_time": 178,
      "attempts": 1,
      "rank": 2
    }
  ],
  "student_rank": {
    "student_id": "student_001",
    "best_score": 85.5,
    "best_time": 300,
    "attempts": 1,
    "rank": 15
  },
  "filters": {
    "subsystem": "power",
    "module_id": 42
  }
}
```

**Notes:**
- Returns top 10 + requesting student's position
- Rankings ordered by score (desc), then time (asc)
- Overall leaderboard averages all modules if no `module_id`

---

#### Get Subsystem Competency
Retrieve student's competency levels across subsystems.

**Endpoint:** `GET /students/{student_id}/subsystem_competency`

**Response (200):**
```json
{
  "success": true,
  "student_id": "student_001",
  "competencies": [
    {
      "subsystem": "power",
      "competency_level": "competency",
      "modules_completed": 5,
      "last_activity": "2025-11-28T10:35:00.000Z",
      "recommended_modules": [
        {
          "id": 43,
          "title": "Battery Management Systems",
          "estimated_minutes": 45
        },
        {
          "id": 44,
          "title": "Solar Panel Sizing",
          "estimated_minutes": 30
        }
      ]
    },
    {
      "subsystem": "avionics",
      "competency_level": "orientation",
      "modules_completed": 2,
      "last_activity": "2025-11-27T14:20:00.000Z",
      "recommended_modules": [...]
    }
  ]
}
```

**Notes:**
- Shows progression through subsystems
- Recommends next uncompleted modules
- Sorted by modules_completed (desc)

---

### Race Mode

#### Start Race
Begin competitive race against ghost cohorts.

**Endpoint:** `POST /students/{student_id}/race/start`

**Request Body:**
```json
{
  "module_id": 42
}
```

**Response (201):**
```json
{
  "success": true,
  "race_id": 5,
  "session_id": 12346,
  "attempt_number": 1,
  "started_at": "2025-11-28T11:00:00.000Z",
  "ghost_data": {
    "average_time": 287,
    "best_time": 156
  },
  "time_targets": {
    "legendary": 180,
    "excellent": 240,
    "good": 300
  },
  "checkpoints": [
    {"step": 1, "target_time": 60},
    {"step": 2, "target_time": 120},
    {"step": 3, "target_time": 180}
  ]
}
```

**Notes:**
- Returns 404 if module has no race configuration
- Creates learner_performance session automatically
- Use checkpoints for real-time feedback

---

#### Complete Race
Finish race and get results.

**Endpoint:** `POST /students/{student_id}/race/complete`

**Request Body:**
```json
{
  "module_id": 42,
  "time_seconds": 180,
  "errors_count": 1,
  "mastery_score": 92.0
}
```

**Response (200):**
```json
{
  "success": true,
  "completed_at": "2025-11-28T11:03:00.000Z",
  "time_seconds": 180,
  "errors_count": 1,
  "mastery_score": 92.0,
  "rank": 3,
  "total_completions": 47,
  "percentile": 6.4,
  "celebration": "legendary",
  "ghost_comparison": {
    "average_time": 287,
    "your_time": 180,
    "improvement": "37% faster"
  },
  "time_targets": {
    "legendary": 180,
    "excellent": 240,
    "good": 300
  }
}
```

**Celebration Levels:**
- `legendary` - Top 10%
- `excellent` - Top 25%
- `good` - Top 50%
- `complete` - Completed

**Notes:**
- Updates leaderboard automatically
- Compares to ghost cohort benchmarks
- Returns celebration level for UI feedback

---

## Error Responses

### 404 Not Found
```json
{
  "success": false,
  "error": "Module not found"
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": "module_id required"
}
```

### 404 No Active Session
```json
{
  "success": false,
  "error": "No active session found. Call /start first"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Database connection failed"
}
```

---

## Database Schema

### learner_performance
Tracks all student module activity.

| Column | Type | Description |
|--------|------|-------------|
| log_id | INT | Primary key |
| student_id | VARCHAR(255) | Student identifier |
| module_id | INT | Module reference |
| attempt_number | INT | Attempt counter (1, 2, 3...) |
| time_spent_seconds | INT | Cumulative time |
| errors_count | INT | Cumulative errors |
| mastery_score | DECIMAL(5,2) | Final score (0-100) |
| completed | BOOLEAN | Completion status |
| timestamp | TIMESTAMP | Last update time |

### subsystem_competency
Tracks competency progression.

| Column | Type | Description |
|--------|------|-------------|
| competency_id | INT | Primary key |
| student_id | VARCHAR(255) | Student identifier |
| subsystem | VARCHAR(255) | Subsystem name |
| competency_level | VARCHAR(50) | Level (orientation/competency/integration/autonomy) |
| modules_completed | INT | Count of completed modules |
| last_activity | TIMESTAMP | Last module completion |
| created_at | TIMESTAMP | First module in subsystem |
| updated_at | TIMESTAMP | Last update |

### ghost_cohorts
Historical performance benchmarks.

| Column | Type | Description |
|--------|------|-------------|
| cohort_id | INT | Primary key |
| cohort_name | VARCHAR(255) | Display name |
| semester | VARCHAR(100) | Academic term |
| university | VARCHAR(255) | Institution |
| subsystem | VARCHAR(255) | Focus area |

### race_metadata
Race configuration per module.

| Column | Type | Description |
|--------|------|-------------|
| race_id | INT | Primary key |
| module_id | INT | Module reference |
| ghost_data | JSONB | Performance stats |
| time_targets | JSONB | Target times |
| checkpoints | JSONB | Step-by-step targets |
| leaderboard_data | JSONB | Rankings |

---

## Usage Examples

### Complete Module Flow
```javascript
// 1. Start module
const startResp = await fetch('/api/lms/students/student_001/modules/42/start', {
  method: 'POST'
});
const { log_id, attempt_number } = await startResp.json();

// 2. Track progress (called periodically)
await fetch('/api/lms/students/student_001/modules/42/log_activity', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    time_spent_seconds: 120,
    errors_count: 2,
    attempt_number
  })
});

// 3. Complete module
const completeResp = await fetch('/api/lms/students/student_001/modules/42/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    time_spent_seconds: 300,
    errors_count: 3,
    mastery_score: 85.5,
    attempt_number
  })
});
const result = await completeResp.json();
console.log(`Competency level: ${result.competency_level}`);
```

### Race Mode Flow
```javascript
// 1. Start race
const raceStart = await fetch('/api/lms/students/student_001/race/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ module_id: 42 })
});
const { session_id, time_targets, checkpoints } = await raceStart.json();

// 2. Display timer and checkpoints
// ... student completes module ...

// 3. Complete race
const raceComplete = await fetch('/api/lms/students/student_001/race/complete', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    module_id: 42,
    time_seconds: 180,
    errors_count: 1,
    mastery_score: 92.0
  })
});
const { rank, percentile, celebration } = await raceComplete.json();

if (celebration === 'legendary') {
  // Show fireworks animation!
}
```

---

## Testing

Run tests with pytest:
```bash
cd backend
pytest test_lms_endpoints.py -v
```

### Test Coverage
- ✅ Module start/activity/complete lifecycle
- ✅ Ghost cohorts retrieval
- ✅ Leaderboard queries
- ✅ Subsystem competency tracking
- ✅ Race mode start/complete
- ✅ Error handling (404, 400, 500)
- ✅ Data validation

---

## Postman Collection

Import this collection for quick API testing:

```json
{
  "info": {
    "name": "Ascent Basecamp LMS API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Start Module",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/students/{{student_id}}/modules/{{module_id}}/start"
      }
    },
    {
      "name": "Log Activity",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/students/{{student_id}}/modules/{{module_id}}/log_activity",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"time_spent_seconds\": 120,\n  \"errors_count\": 2\n}"
        }
      }
    },
    {
      "name": "Complete Module",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/students/{{student_id}}/modules/{{module_id}}/complete",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"time_spent_seconds\": 300,\n  \"errors_count\": 3,\n  \"mastery_score\": 85.5\n}"
        }
      }
    },
    {
      "name": "Get Leaderboard",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/students/{{student_id}}/leaderboard?module_id={{module_id}}"
      }
    }
  ]
}
```

**Environment Variables:**
- `base_url`: `http://localhost:5000/api/lms`
- `student_id`: `student_001`
- `module_id`: `42`

---

## Quick Start Guide

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://..."

# Run migrations
python scripts/create_ascent_basecamp_schema.py
```

### 2. Start API Server
```bash
python backend/app.py
```

### 3. Test Endpoints
```bash
# Start a module
curl -X POST http://localhost:5000/api/lms/students/test/modules/1/start

# Get subsystem competency
curl http://localhost:5000/api/lms/students/test/subsystem_competency
```

### 4. Integrate Frontend
```javascript
// Import API client
import { lmsAPI } from './api/lms';

// Use in components
const { data } = await lmsAPI.startModule(studentId, moduleId);
```

---

## Support

For issues or questions:
- Check the test suite: `backend/test_lms_endpoints.py`
- Review database schema: `scripts/create_ascent_basecamp_schema.py`
- See Agent Team Chat: `AGENT_TEAM_CHAT.md`

**Last Updated:** 2025-11-28 by Agent Beta  
**Database Schema:** Created by Agent Gamma (Session #3)
