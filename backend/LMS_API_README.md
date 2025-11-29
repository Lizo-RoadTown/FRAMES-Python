# LMS API Documentation

## Overview

Flask REST API for the Learning Management System (LMS) module management and student progress tracking.

**Base URL:** `http://localhost:5000/api/lms`

---

## Endpoints

### 1. Get All Modules

**GET** `/api/lms/modules`

Returns a list of all available learning modules.

**Query Parameters:**
- `category` (optional): Filter by category
- `university_id` (optional): Filter by university
- `status` (optional): Filter by status ("draft", "published", "archived") - default: "published"
- `target_audience` (optional): Filter by target audience

**Response:**
```json
{
  "success": true,
  "count": 2,
  "modules": [
    {
      "id": 1,
      "module_id": "intro-to-research",
      "title": "Introduction to Research",
      "description": "Learn the basics of research methodology",
      "category": "fundamentals",
      "estimated_minutes": 45,
      "status": "published",
      "tags": ["research", "methodology"],
      "notion_page_id": "abc123..."
    }
  ]
}
```

---

### 2. Get Module Details

**GET** `/api/lms/modules/<module_id>`

Returns full details for a specific module, including sections.

**Query Parameters:**
- `include_sections` (optional): Include sections array - default: "true"

**Response:**
```json
{
  "success": true,
  "module": {
    "id": 1,
    "title": "Introduction to Research",
    "sections": [
      {
        "id": 1,
        "section_number": 1,
        "section_type": "text",
        "title": "What is Research?",
        "content": "Research is...",
        "duration_seconds": 300
      }
    ]
  }
}
```

---

### 3. Get Student Progress

**GET** `/api/lms/modules/<module_id>/progress?student_id=<student_id>`

Returns progress for a specific student on a module.

**Response:**
```json
{
  "success": true,
  "progress": {
    "module_id": 1,
    "student_id": "student123",
    "status": "in_progress",
    "progress_percent": 75,
    "current_section": 3,
    "started_at": "2025-11-26T10:00:00",
    "total_time_seconds": 1800,
    "completed_sections": [1, 2]
  }
}
```

---

### 4. Track Progress

**POST** `/api/lms/modules/<module_id>/progress`

Records student progress through a module.

**Request Body:**
```json
{
  "student_id": "student123",
  "section_number": 2,
  "progress_percent": 75,
  "status": "in_progress",
  "time_spent_seconds": 120
}
```

**Response:**
```json
{
  "success": true,
  "message": "Progress recorded",
  "progress": {
    "module_id": 1,
    "student_id": "student123",
    "progress_percent": 75,
    "status": "in_progress"
  }
}
```

---

### 5. Get Module Analytics

**GET** `/api/lms/modules/<module_id>/analytics`

Returns usage analytics for a module.

**Response:**
```json
{
  "success": true,
  "analytics": {
    "module_id": 1,
    "module_title": "Introduction to Research",
    "total_students": 50,
    "completed_count": 35,
    "completion_rate": 70.0,
    "avg_time_spent_minutes": 42.5,
    "status_breakdown": {
      "not_started": 5,
      "in_progress": 10,
      "completed": 35
    },
    "section_analytics": [
      {
        "section_number": 1,
        "title": "What is Research?",
        "completion_rate": 90.0,
        "completed_count": 45
      }
    ]
  }
}
```

---

### 6. Get Module Feedback

**GET** `/api/lms/modules/<module_id>/feedback`

Returns all feedback for a module with aggregate statistics.

**Response:**
```json
{
  "success": true,
  "count": 25,
  "aggregate": {
    "avg_rating": 4.2,
    "avg_clarity": 4.5,
    "avg_usefulness": 4.3,
    "difficulty_breakdown": {
      "too_easy": 2,
      "just_right": 20,
      "too_hard": 3
    }
  },
  "feedback": [
    {
      "id": 1,
      "student_id": "student123",
      "rating": 5,
      "difficulty": "just_right",
      "clarity": 5,
      "usefulness": 4,
      "feedback_text": "Very helpful module!",
      "submitted_at": "2025-11-26T15:30:00"
    }
  ]
}
```

---

### 7. Submit Feedback

**POST** `/api/lms/modules/<module_id>/feedback`

Submits student feedback for a module.

**Request Body:**
```json
{
  "student_id": "student123",
  "rating": 4,
  "difficulty": "just_right",
  "clarity": 5,
  "usefulness": 4,
  "feedback_text": "Very helpful module!",
  "suggestions": "Could use more examples"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback submitted successfully",
  "feedback": {
    "id": 1,
    "module_id": 1,
    "student_id": "student123",
    "rating": 4
  }
}
```

---

### 8. Get Module Assignments

**GET** `/api/lms/modules/<module_id>/assignments`

Returns all assignments for a module.

**Response:**
```json
{
  "success": true,
  "count": 3,
  "assignments": [
    {
      "id": 1,
      "module_id": 1,
      "student_id": "student123",
      "due_date": "2025-12-31T23:59:59",
      "required": true,
      "assigned_at": "2025-11-26T10:00:00"
    }
  ]
}
```

---

### 9. Create Assignments

**POST** `/api/lms/modules/<module_id>/assignments`

Assigns a module to multiple students.

**Request Body:**
```json
{
  "student_ids": ["student1", "student2", "student3"],
  "due_date": "2025-12-31T23:59:59",
  "required": true,
  "assigned_by_id": "faculty123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Created 3 assignments",
  "assignments": [...]
}
```

---

### 10. Get Student Modules

**GET** `/api/lms/students/<student_id>/modules`

Returns all modules assigned to a student with their progress.

**Query Parameters:**
- `status` (optional): Filter by module status

**Response:**
```json
{
  "success": true,
  "count": 5,
  "modules": [
    {
      "id": 1,
      "title": "Introduction to Research",
      "assignment": {
        "due_date": "2025-12-31T23:59:59",
        "required": true,
        "assigned_at": "2025-11-26T10:00:00"
      },
      "progress": {
        "status": "in_progress",
        "progress_percent": 75
      }
    }
  ]
}
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created (for POST requests)
- `400` - Bad Request (missing required fields)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## Integration with Frontend

The React frontend should call these endpoints to:

1. **Load module catalog** - `GET /api/lms/modules`
2. **Display module content** - `GET /api/lms/modules/<id>`
3. **Track student progress** - `POST /api/lms/modules/<id>/progress`
4. **Show analytics dashboard** - `GET /api/lms/modules/<id>/analytics`

---

## Testing

Run the test suite:

```bash
cd backend
pytest test_lms_endpoints.py -v
```

Test with curl:

```bash
# Get all modules
curl http://localhost:5000/api/lms/modules

# Get specific module
curl http://localhost:5000/api/lms/modules/1

# Track progress
curl -X POST http://localhost:5000/api/lms/modules/1/progress \
  -H "Content-Type: application/json" \
  -d '{"student_id":"student123","progress_percent":50,"status":"in_progress"}'
```

---

## Database Models Used

- **Module** - Main module metadata
- **ModuleSection** - Content sections within modules
- **ModuleProgress** - Student progress tracking
- **ModuleAssignment** - Module assignments to students
- **ModuleAnalyticsEvent** - Detailed analytics events
- **ModuleFeedback** - Student feedback

See `shared/database/db_models.py` for full schema definitions.
