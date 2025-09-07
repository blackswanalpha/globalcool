# AI Agentic Implementation Instruction Set — Global Cool-Light E.A LTD

This document provides actionable, production-ready instructions for building the Global Cool-Light website + admin + client portals using **AI agents** (task-specialized autonomous assistants). It covers agent roles, orchestration, prompt templates, tooling, data contracts, testing, safety, monitoring, and handoff rules. Use this as a runbook for building, QAing, and deploying the system with AI assistance while keeping humans in the loop for approvals and risk control.

---

# 1. High-level strategy & constraints

* **Goal:** Use multiple cooperating AI agents to design, implement, test, and deploy a Django 5 monolith website (public) + Admin portal + Client portal with features defined earlier.
* **Agent model assumptions:** Agents are stateless workers invoked with prompts and limited context windows; orchestration is done by a coordinator (or orchestration agent).
* **Human-in-the-loop:** Required for final approvals on design, security-sensitive decisions, and production deploys.
* **Security & compliance:** Secrets never exposed to agents; configuration stored in secret manager. Agents may create config templates but must call humans to inject secrets.
* **Repeatability:** All agent actions produce artifacts (PRs, issues, docs) stored in repo/issue tracker for audit.
* **Idempotence:** Agents must use idempotent operations (create files, modify code via branches & PRs) and not directly commit to main without approval.

---

# 2. Agent roles & responsibilities (core set)

1. **Orchestrator Agent (Coordinator)**

   * Receives high-level objectives; decomposes tasks; assigns subtasks to other agents; tracks state and deadlines; enforces policies.
2. **Product/PM Agent**

   * Maintains scope, acceptance criteria, and feature backlog; validates that work meets product requirements.
3. **Design Agent (UI/UX)**

   * Generates wireframes, high-fidelity mockups, design system, Figma files (or JSON spec), and animation specs; produces assets and component tokens.
4. **Frontend Agent**

   * Implements templates, CSS (Tailwind/Bootstrap mix), client-side JS, responsive layouts, and Framer Motion/animation hooks; creates React components if required or Django template code.
5. **Backend Agent**

   * Implements Django apps, models, views, forms, DRF endpoints, serializers, auth, business logic, and unit tests.
6. **DevOps Agent**

   * Sets up CI/CD (GitHub Actions), Docker, deployment scripts, Nginx/Gunicorn configuration, DO droplet or managed services templates, backup scripts, monitoring.
7. **Testing/QA Agent**

   * Writes unit, integration, and E2E tests (pytest, Playwright/Cypress), test data, test plans, and automated test runs in CI.
8. **Security Agent**

   * Runs SAST/DAST checks, suggests CSP and headers, ensures OWASP basics, creates threat model and mitigation tasks.
9. **Content Agent (Copywriter/SEO)**

   * Produces SEO-friendly page content, meta tags, sitemaps, and blog seeds.
10. **Support/Operations Agent**

    * Creates runbooks, monitoring dashboards, alerting rules, backup and restore docs.
11. **QA Reviewer Agent** (Optional)

    * Independent verification agent that runs checklists and outputs pass/fail per feature.

> Each agent should output: artifact (file/PR), a short summary, automated tests (where applicable), and an “ask” for a human decision when needed.

---

# 3. Orchestration & workflow (how agents work together)

1. **Input**: Product owner (human) gives Orchestrator a ticket: e.g., “Implement Service Booking flow end-to-end (public + admin)”.
2. **Decompose**: Orchestrator breaks into tasks: DB models, APIs, templates, booking form UX, email notifications, calendar view, tests, infra.
3. **Assign**: Map tasks to Backend, Frontend, Design, DevOps, Testing agents.
4. **Parallel work**: Agents operate on separate branches in repo; each creates commit + PR with tests and docs.
5. **Review loop**:

   * QA Agent runs automated tests.
   * Security Agent runs scans.
   * Product/PM Agent reviews acceptance criteria.
   * Human approves PRs for staging. Orchestrator queues merge.
6. **Staging deploy**: DevOps agent deploys to staging; QA runs E2E; human UAT.
7. **Production release**: On human approval, orchestrator triggers production deploy and notifies Ops for monitoring.
8. **Post-deploy**: Monitoring, alerts, and 30-day support tasks created.

---

# 4. Communication formats & artifacts

* **Tasks**: Use JSON task objects `{ id, title, description, acceptance_criteria, owner_agent, dependencies, priority, estimate }`.
* **PR format**: Title, Summary, Files Changed, Tests Added, How to run locally, Screenshots (if UI), Security notes.
* **Issue template**: `bug`, `feature`, `security`, `ops`.
* **Design spec**: Figma JSON export or HTML + annotated screenshots.
* **API spec**: OpenAPI 3.0 YAML file in `specs/api/openapi.yaml`.
* **Database migrations**: Standard Django migrations in repo.
* **Test reports**: JUnit or GitHub Actions test artifacts.

---

# 5. Prompt templates (examples agents must use)

> Agents should use templated prompts, filled with task data. Keep prompts short and include constraints.

## Orchestrator → Backend Agent

```
Task: Implement Booking model + endpoints
Repo: <git_url>
Branch: feature/bookings
Acceptance Criteria:
- Django model Booking with fields: service (FK), client (FK), name, email, phone, preferred_date (date), preferred_time_slot (string), status(enum)
- Admin interface for booking with list filters
- API endpoints: POST /api/v1/bookings/ (create), GET /api/v1/bookings/?status=
- Unit tests covering model validation and API
Constraints: Use Django 5, PostgreSQL production, SQLite dev.
Return: PR URL, test results, instructions to run locally.
```

## Design Agent → Frontend Agent

```
Task: Implement Service Detail page template
Design: Figma file exported as URL: <figma_export_url>
Assets: icons, hero image locations (or placeholders)
Acceptance Criteria:
- Responsive design with hero, specs, gallery, booking CTA
- Booking modal triggers POST to /api/v1/bookings/
- Use Bootstrap 5 classes + Tailwind utility for spacing
Return: PR URL, screenshot of desktop and mobile states, testable URL on staging.
```

## Backend Agent → Testing Agent

```
Task: Provide test data & fixtures for bookings
Constraints: Use Factory Boy & pytest fixtures
Deliverables: fixtures/bookings.json, test factories, summary of sample objects created
```

---

# 6. Repos, branches, CI & conventions

* **Monorepo / single repo** recommended for a monolithic Django app:

  * `backend/` (Django project)
  * `frontend/` (if separate React components or static assets)
  * `specs/` (openapi, ERD)
  * `design/` (Figma export, assets)
  * `ci/` (GitHub Actions)
  * `docs/` (SDD, runbooks)
* **Branching policy**: `main`, `develop`, `feature/<ticket>`, `hotfix/<ticket>`.
* **CI**:

  * PRs trigger lint, unit tests, security scans, and UI snapshot tests.
  * Merge only after green checks and human approval for main branch.
* **PR size**: Prefer small PRs (< 400 lines) to ease review by humans and agents.

---

# 7. Data contracts & API design

* **OpenAPI** file to be canonical source of truth. Agents must not implement endpoints without updating `specs/api/openapi.yaml`.
* **Booking create request**:

```yaml
POST /api/v1/bookings/
requestBody:
  content:
    application/json:
      schema:
        type: object
        properties:
          service_slug: {type: string}
          name: {type: string}
          email: {type: string, format: email}
          phone: {type: string}
          preferred_date: {type: string, format: date}
          preferred_time_slot: {type: string}
```

* **Responses**: 201 with booking id and status; 400 on validation errors.

---

# 8. Testing & quality gates

* **Unit tests** (coverage target 80% for backend business logic).
* **Integration tests** for APIs (pytest + requests).
* **E2E tests** for critical flows (Playwright/Cypress): booking flow, quote acceptance, admin approve.
* **Performance tests**: load test booking endpoint (locust target) and page load times (Lighthouse).
* **Security checks**: Snyk/Dependabot for dependencies; bandit for Python; DAST scanning during staging.
* **Acceptance criteria**: every feature must include at least one automated test; deploy gated by CI passing tests + security pass + human signoff for production.

---

# 9. Human approval & escalation policy

* **Design approvals**: Human must sign-off high-fidelity designs before frontend agent finalizes.
* **Security-critical operations**: Secret rotations, production DB access, and external payment integration require human ops approval.
* **Escalation**: Orchestrator notifies product owner and security officer on any failing security gate or ambiguous acceptance criteria.

---

# 10. Security & secrets handling

* **Agent rule**: Never store secrets in repo or in prompt history. Agents may output a placeholder `{{SMTP_PASSWORD}}` and create a secret placeholder issue for human to add secret to secret manager (e.g., DO secrets, GitHub Actions secrets).
* **Environment files**: Agents can create `.env.example` but not `.env`.
* **Least privilege**: Agents create service accounts with minimal scope for CI and deployments.
* **Audit trail**: Each agent action logged with `agent_id`, `timestamp`, and `artifact_url`.

---

# 11. Monitoring, observability & post-deploy

* **Metrics**: Expose Prometheus or basic metrics endpoint: `requests_total`, `bookings_total`, `error_rate`.
* **Logs**: Structured JSON logs; errors forwarded to Sentry or similar.
* **Alerts**:

  * High error rate (>1% for 5m) → page on-call.
  * Booking endpoint > 500 errors → alert ops + orchestrator.
* **Health checks**: `/healthz` returns DB, cache, and disk status.
* **Agent task**: Support/Operations Agent creates dashboards in Grafana/DO monitoring.

---

# 12. Example task decomposition for a feature (Booking end-to-end)

1. **Orchestrator**: Create task `BOOK-001`.
2. **Design Agent**: Wireframe booking modal + booking confirmation page → output Figma JSON and acceptance criteria.
3. **Backend Agent**: Create `leads` app, Booking model, migrations, serializer, API view, admin config, unit tests.
4. **Frontend Agent**: Create booking modal, call API, validations, loading states, success screen.
5. **Testing Agent**: Create integration tests and Playwright E2E for booking flow.
6. **DevOps Agent**: Ensure staging env has email provider placeholder, run migrations in staging.
7. **Security Agent**: Scan code and ensure rate-limiting, CSRF active, captcha flag added (if needed).
8. **QA Agent**: Run automated tests, run manual UAT checklist, report pass/fail.
9. **Human**: Review UAT and merge to main; approve production deploy.

---

# 13. Evaluation metrics & acceptance

* **Functional**: Feature behaves per acceptance criteria (manual + tests).
* **Quality**: Passing CI tests, test coverage threshold, no high-severity security alerts.
* **Performance**: Page load targets (LCP < 2.5s for key pages) and API p95 < 300ms for normal ops.
* **UX**: Human sign-off after viewing prototypes and running simple usability tests.
* **Reliability**: 30-day observed error rate < 0.5%.

---

# 14. Templates & snippets (for immediate use)

## Task JSON template

```json
{
  "id": "BOOK-001",
  "title": "Implement Booking create API",
  "description": "Create Booking model, migration, serializer, POST endpoint and basic admin listing.",
  "acceptance_criteria": [
    "POST /api/v1/bookings/ returns 201 and creates Booking",
    "Admin list shows new bookings",
    "Unit tests cover validation"
  ],
  "owner_agent": "backend-agent",
  "dependencies": []
}
```

## PR template (markdown)

```
# PR: Implement Booking model & API

## Summary
- Add `leads.Booking` model
- Add API endpoint POST /api/v1/bookings/
- Add admin list and filter
- Add unit tests

## How to run locally
1. pip install -r requirements.txt
2. python manage.py migrate
3. pytest tests/leads

## Screenshots
- [ ] desktop booking modal
- [ ] mobile booking modal

## Security Notes
- Rate limiting applied to endpoint
- CSRF enabled for browser requests

## Tests
- Added tests/leads/test_booking.py
```

---

# 15. Human-readable checkpoints (what to review)

* UI design fidelity vs wireframes: content, spacing, accessibility.
* API contract vs implementation: check OpenAPI.
* Tests: ensure new feature is covered and tests pass in CI.
* Security: run and review SAST/DAST results.
* Infra: ensure backups and health checks configured for staging.

---

# 16. Limitations & known risks

* Agents can produce code that compiles but may require human judgement on edge cases.
* Automated design-to-code mapping is error-prone for complex UI interactions; always have a designer/human review.
* Secrets mishandling risk must be mitigated by strict policy and secret manager integration.
* Regulatory/legal decisions (GDPR nuances, contracts) require legal/human review.

---

# 17. Final checklist to activate agent pipeline

* [ ] Create repo scaffold and `.github/workflows/ci.yml`.
* [ ] Configure secret manager (DO secrets / GitHub secrets).
* [ ] Upload initial SDD, API spec, UX wireframes (artifacts).
* [ ] Start Orchestrator with initial backlog (feature list).
* [ ] Assign agents to owners and provide their executor environment (containers, tokens).
* [ ] Define human approvers for design, security, and production deploys.

---

# 18. Closing notes

This instruction set is designed to let you run a multi-agent pipeline safely and productively. Start by implementing one canonical feature (e.g., Booking) following this flow to validate the pipeline. Capture lessons learned and tighten the orchestration rules before scaling to all 70 UI pages and full platform features.

If you want, I can:

* Generate concrete agent prompts for each of the 70 page tasks (automatically), or
* Produce the initial Orchestrator JSON backlog for the Booking and Portfolio features and create starter branches/PR templates. Which do you want next?
