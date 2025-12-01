# FRAMES Repository Documentation

This page is the in-repo landing spot for the FRAMES platform. Use it to quickly jump to code, documentation, and setup guides without leaving the repository.

## Platform Overview

FRAMES (Framework for Resilience Assessment in Modular Engineering Systems) is a multi-application platform for eight universities collaborating on space missions. The platform currently includes:

1. **Student Onboarding LMS** – AI-assisted learning management system for training new students.
2. **Research Analytics Dashboard** – Faculty and researcher tooling for team dynamics and knowledge transfer analysis.
3. **AI Prediction Core (Planned)** – Machine learning engine for mission success prediction and risk assessment.

All applications share a single Neon-hosted PostgreSQL database that stores university, team, student, module, and interface data.

## Navigation Map

### Top-level references
- **Root overview:** [`README.md`](../README.md) for the high-level platform description.
- **Documentation index:** [`docs/README.md`](README.md) for application-specific and shared guides.
- **Repository layout:** [`MONOREPO_STRUCTURE.md`](../MONOREPO_STRUCTURE.md) to understand where code and docs live.
- **Quick start:** [`SETUP_COMPLETE.md`](../SETUP_COMPLETE.md) plus [`GETTING_STARTED.md`](../GETTING_STARTED.md) for environment setup.

### Applications
- **Onboarding LMS** – docs in [`docs/onboarding-lms/`](onboarding-lms/) and code in [`apps/onboarding-lms/`](../apps/onboarding-lms/).
- **Research Analytics** – docs in [`docs/research-analytics/`](research-analytics/) and code in [`apps/research-analytics/`](../apps/research-analytics/).
- **AI Prediction Core (planned)** – docs in [`docs/ai-prediction-core/`](ai-prediction-core/) and placeholder code in [`apps/ai-core/`](../apps/ai-core/).

### Shared resources
- **Database setup:** [`docs/shared/NEON_DATABASE_SETUP.md`](shared/NEON_DATABASE_SETUP.md).
- **Project roadmap:** [`docs/shared/PROJECT_ROADMAP.md`](shared/PROJECT_ROADMAP.md).
- **Contributing guide:** [`docs/shared/CONTRIBUTING.md`](shared/CONTRIBUTING.md).
- **Schemas & contracts:** [`schemas/`](../schemas/) for database and API schema assets.

## Getting Started Locally

1. Install prerequisites: Python 3.11+, Node.js 18+, and a Neon account.
2. Create an environment file: `cp .env.example .env`, then add your Neon PostgreSQL connection string.
3. Back-end: from the repo root run `python backend/app.py` to start the Flask API at `http://localhost:5000`.
4. Front-ends: see app-specific instructions in [`apps/onboarding-lms/`](../apps/onboarding-lms/) and [`apps/research-analytics/`](../apps/research-analytics/); most use `npm install` then `npm start`.
5. For additional setup details or troubleshooting, reference [`SETUP_COMPLETE.md`](../SETUP_COMPLETE.md) and [`docs/README.md`](README.md).

## Contributing

- Use feature branches for changes and link back to the relevant application docs above.
- Keep documentation in the same directory tree as the feature you are updating (e.g., Onboarding LMS docs stay under `docs/onboarding-lms/`).
- Update shared artifacts (schemas, environment templates) when changes affect multiple applications.

For a complete documentation index, see [`docs/README.md`](README.md).
