# Global Cool-Light E.A LTD — System Architecture & Structure

**Version:** 1.0
**Date:** 03 September 2025
**Prepared by:** Engineering Team

---

## Contents

1. Overview
2. Architectural Principles
3. System Context Diagram
4. Logical Architecture & Modules
5. Data Model & Key Entities
6. API Design & Contracts
7. Deployment Architecture
8. Infrastructure Components & Setup
9. CI/CD, Branching & Release Flow
10. Runtime Topology & Scaling
11. Security & Compliance
12. Observability, Logging & Alerts
13. Backup, DR & Recovery
14. Repository & Project Structure
15. Developer Onboarding & Runtime Commands
16. Appendix: Sequence Flows

---

## 1. Overview

This document defines the **system architecture** and **project structure** for the Global Cool‑Light platform (Public Website, Admin Portal, Client Portal). The recommended implementation is a **Django 5 monolithic application** with a server‑rendered public site and API endpoints (DRF) powering frontends and portals. Storage uses **PostgreSQL** for production, Redis for cache/queues, and DigitalOcean for compute & object storage.

---

## 2. Architectural Principles

* **Monolith-first**: Single Django codebase to reduce complexity and centralize business logic.
* **Separation of concerns**: Django apps split by domain (auth, leads, cms, services, portfolio, billing, notifications, analytics).
* **API-first**: DRF for all business features so frontends (client portal or future apps) reuse endpoints.
* **Idempotent infra**: IaC and scripted deployments.
* **Secure by default**: Least privilege, secrets manager, CSRF protection, and SAST/DAST gates.

---

## 3. System Context Diagram

```
[User Browsers & Mobile] <-> HTTPS <-> [NGINX Reverse Proxy] <-> Gunicorn -> [Django 5 App]
                                      |                          |
                                      |                          +-> PostgreSQL (managed)
                                      |                          +-> Redis (cache + Celery broker)
                                      |                          +-> DO Spaces (object storage)
                                      |                          +-> External APIs (GA4, Google Maps, SMTP)
                                      v
                             [CDN (optional) / Static Files]
```

---

## 4. Logical Architecture & Modules

Django project split into apps (each app is a logical module):

* **core**: settings, logging, middleware, common utilities, feature flags
* **users**: authentication, user profiles, roles & permissions, sessions
* **cms**: pages, blog, banners, hero, meta/SEO fields
* **services**: service catalog, categories, specs
* **portfolio**: projects, images, case studies
* **leads**: bookings, inquiries, quotations, clients
* **dashboard**: admin KPIs, aggregators
* **notifications**: email templates, queueing, logs
* **media**: media management & thumbnails (Pillow)
* **analytics**: local event pipeline & GA aggregator
* **billing**: invoices & lightweight billing objects (Phase1 placeholder)
* **api**: DRF viewsets, routers, serializers (public & admin namespaces)
* **tasks**: Celery tasks (email send, PDF generation, backups)
* **tests**: shared test utilities, factories

Each app contains models, serializers, views, admin, and tests. Use `services` and `portfolio` as examples of domain apps.

---

## 5. Data Model & Key Entities

(Condensed ER overview; full ERD to be produced as separate artifact)

* **User**(id, email, password\_hash, role, is\_active, metadata)
* **Role**(id, name, permissions)
* **ServiceCategory**(id, name, slug)
* **Service**(id, category\_id, name, slug, specs\_json, base\_price\_min, base\_price\_max)
* **Project**(id, title, summary, body\_html, services\_m2m)
* **MediaAsset**(id, url, alt, width, height, tags)
* **Client**(id, name, contact\_email, phone, address)
* **Booking**(id, service\_id, client\_id, preferred\_date, preferred\_time\_slot, status, admin\_notes)
* **Inquiry**(id, client\_id, service\_id?, message, attachments)
* **Quotation**(id, inquiry\_id, items\_json, subtotal, tax, total, status, pdf\_url)
* **Notification**(id, type, to, status, payload)
* **AuditLog**(id, user\_id, action, target, diff, ip)

Indexes: created\_at on leads, email on users/clients, status composite indexes on bookings/quotations.

---

## 6. API Design & Contracts

API base paths:

* Public: `/api/v1/public/` (read-only lists: services, projects, blog)
* Auth: `/api/v1/auth/` (login, register, profile)
* Leads: `/api/v1/leads/` (bookings, inquiries)
* Admin: `/api/v1/admin/` (protected endpoints)

Example endpoint summaries:

* `POST /api/v1/leads/bookings/` → create booking

  * Request: `{service_slug, name, email, phone, preferred_date, preferred_time_slot}`
  * Response: `201 {booking_id, status, token}`
* `GET /api/v1/public/services/?category=` → list services
* `POST /api/v1/leads/inquiries/` → create inquiry with multipart attachments

Auth & Security:

* Session cookie for browser admin UI (Django auth) + CSRF.
* JWT (SimpleJWT) for client portal + API usage (stateless mobile future).
* Rate limiting: DRF throttle classes on public write endpoints.

OpenAPI: Maintain `specs/openapi.yaml` as canonical contract. Agents must update it when endpoints change.

---

## 7. Deployment Architecture

Environments: `local` (docker-compose), `staging`, `production`.

Production topology (recommended minimal):

* DigitalOcean Droplet (2 vCPU / 4GB) or Managed App Service
* PostgreSQL Managed (DO Managed DB) or separate DB Droplet
* Redis (DO Managed or Droplet)
* Nginx reverse proxy + Gunicorn
* DO Spaces for media & backups
* Let's Encrypt for SSL
* Optional CDN in front of static & media

Containerization: Docker images for app; use GitHub Actions to build and push to DO Container Registry.

---

## 8. Infrastructure Components & Setup

* **Compute:** DO Droplet (or Kubernetes for scale)
* **DB:** DO Managed PostgreSQL (multi-AZ recommended)
* **Cache / Broker:** Redis (for caching and Celery broker)
* **Object Storage:** DO Spaces (S3 API) for media & backups
* **CI/CD:** GitHub Actions → build, test, push image, deploy using SSH or DO App Platform
* **Secrets:** GitHub Secrets / DO Secrets
* **Monitoring:** Sentry for errors, UptimeRobot for health checks, DO Monitoring + Grafana (optional)

---

## 9. CI/CD, Branching & Release Flow

* Branching: `main` (production), `develop` (staging), `feature/xxx`, `hotfix/xxx`.
* PR checks: flake8/isort, black, mypy (optional), pytest unit tests, frontend build tests.
* Merge policy: require 1 human approval for `develop` and 2 for `main` (including security review).
* Deployment: `develop` -> auto deploy to staging on merge; `main` -> manual deploy to production after approvals.

GitHub Actions pipelines:

* `ci.yml`: lint, test (backend), test (frontend), build docker image, push image to registry.
* `deploy-staging.yml`: on merge to develop -> deploy to staging via SSH/script.
* `deploy-prod.yml`: manual dispatch -> deploy to production.

---

## 10. Runtime Topology & Scaling

* **Vertical scale:** increase Droplet size (CPU/RAM) for initial demand.
* **Horizontal scale (future):** separate web & worker nodes, load balancer, multiple gunicorn instances.
* **Caching:** Redis for per-view and low-cardinality content.
* **Static & Media CDN:** Offload to CDN for scale.

---

## 11. Security & Compliance

* **Network:** enforce HTTPS, HSTS, secure cookies.
* **App:** CSRF, XSS prevention, input validation via serializers.
* **Auth:** strong password policy, optional 2FA for admin, session expiry.
* **Secrets:** store in secrets manager, never in repo.
* **Logging & Audit:** log critical events and admin actions.
* **Vulnerability Management:** Dependabot, Snyk, scheduled scanning.
* **GDPR/Privacy:** cookie consent, data retention policy, right to delete.

---

## 12. Observability, Logging & Alerts

* **Logging:** Structured JSON logs to stdout; collect via DO logs or centralized logging.
* **Errors:** Sentry integration for exceptions and performance traces.
* **Metrics:** basic app metrics (request counts, latencies), Redis, DB health exposed on `/metrics` for Prometheus (optional).
* **Alerts:** error rate, high latency, disk full, backup failure notifications to Slack/email.

---

## 13. Backup, DR & Recovery

* **Database backups:** automated daily pg\_dump to DO Spaces, retention 14 days.
* **Media backups:** daily rsync to Spaces snapshot, incremental backups weekly.
* **Snapshot:** weekly Droplet snapshot.
* **RTO/RPO:** RTO target 2 hours, RPO 24 hours.
* **Restore drills:** quarterly test restore into staging; document steps in `docs/ops/restore.md`.

---

## 14. Repository & Project Structure

```
global-coollight/
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/  # django settings split by env
│   ├── apps/
│   │   ├── core/
│   │   ├── users/
│   │   ├── cms/
│   │   ├── services/
│   │   ├── portfolio/
│   │   ├── leads/
│   │   ├── notifications/
│   │   └── api/
│   ├── specs/openapi.yaml
│   └── tests/
├── frontend/ (if using Next.js)
│   ├── package.json
│   ├── src/
│   └── public/
├── infra/
│   ├── docker-compose.yml
│   ├── ansible/ or terraform/  # optional
│   └── scripts/
├── docs/
│   ├── sdd.md
│   └── ops/
└── .github/workflows/
```

---

## 15. Developer Onboarding & Runtime Commands

**Local dev (docker-compose):**

```bash
# start dev containers
cp .env.example .env
docker-compose up --build
# run migrations
docker-compose exec web python manage.py migrate
# create superuser
docker-compose exec web python manage.py createsuperuser
```

**Run tests:**

```bash
docker-compose exec web pytest -q
```

**Build & Deploy (CI):** GitHub Actions runs build and deployment scripts.

---

## 16. Appendix: Sequence Flows

### Booking Flow (simplified)

```
1. User POST /api/v1/leads/bookings/ (submit booking form)
2. Django validates and creates Booking record (status=New)
3. Booking saved -> Celery task enqueued to send confirmation email
4. Notification record created (status=queued)
5. Worker sends email via SMTP provider; Notification updated to sent
6. Admin dashboard picks up new booking via metrics endpoint
```

### Quote Acceptance Flow


```
1. Admin generates Quotation -> PDF created via WeasyPrint (task)
2. System emails quote with tokenized accept/reject URL
3. Client clicks accept -> GET /quotes/accept/?token=xxx -> backend validates token -> set Quotation.status=Accepted
4. Trigger downstream actions (create Invoice, notify sales)
```

---

## Final Notes & Next Steps

1. Produce a full ERD diagram (tools: draw\.io / dbdiagram) and attach to `docs/erdiagram.png`.
2. Create `specs/openapi.yaml` covering all endpoints described.
3. Implement `docker-compose` local environment and CI GitHub Actions templates.
4. Run a security review and automated scans early in the dev cycle.

If you'd like, I can now:

* Generate the **OpenAPI spec** for all major endpoints, or
* Produce a **detailed ERD** (visual) and table-by-table DTOs for all models.
  Which should I do next?