# Global Cool-Light E.A LTD — System Design Document (SDD)

**Version:** 1.0
**Date:** 03 September 2025
**Prepared by:** Project Engineering
**Audience:** Founders, Operations, Sales, Engineering, QA, DevOps

---

## 1. Purpose & Scope

This System Design Document (SDD) describes the end‑to‑end architecture, data model, interfaces, deployment, security, performance, and operational plan for Global Cool‑Light E.A LTD’s portfolio + business management website. It translates the approved proposal into a buildable, testable, and maintainable system using **Django 5+ (monolith)** and a **DigitalOcean** deployment.

**In scope:** Public website (5 pages), booking, inquiries & quotations, basic analytics, admin CMS, notifications, dashboards.
**Out of scope (Phase 1):** Online payments, advanced CRM, multilingual, native mobile apps.

---

## 2. Goals & Non‑Goals

### 2.1 Goals

* Professional online presence for refrigeration, AC, and mechanical ventilation services.
* Lead capture via bookings & inquiries; structured quotation workflow.
* Lightweight analytics dashboard for traffic and lead performance.
* Secure, mobile‑first, SEO‑optimized delivery.

### 2.2 Non‑Goals

* Marketing automation & advanced sales pipelines.
* Complex third‑party integrations beyond email, GA4, and Maps.
* Offline‑first mobile experiences.

---

## 3. Users & Personas

* **Prospective Customer (B2B/B2C):** Discovers services, submits booking/inquiry, views portfolio, calls/WhatsApp.
* **Sales/Operations Staff (Admin):** Manages services, bookings, inquiries, quotations, content, and reports.
* **Management (Admin):** Reviews dashboards, exports reports, configures settings.
* **Site Visitor (Anonymous):** Reads content, contacts via forms.

---

## 4. High‑Level Requirements

### 4.1 Functional

1. Public pages: Home, About, Services & Products (+ service detail), Portfolio (projects/case studies), Contact.
2. Booking: date/time selection, customer details, email confirmation, admin calendar & status updates.
3. Inquiries & Quotations: structured inquiry intake, quote creation, PDF export & email, status tracking.
4. Admin CMS: manage content, media, testimonials, team, services, projects.
5. Analytics: traffic (GA4), leads (bookings/inquiries), conversion metrics.

### 4.2 Non‑Functional

* **Availability:** 99.9% monthly uptime target.
* **Performance:** TTFB < 500ms (cached), LCP < 2.5s on 4G; Page load < 3s.
* **Security:** HTTPS, OWASP ASVS L1 controls, role‑based access, daily backups.
* **Scalability:** Single Droplet + Redis cache; horizontal scale path defined.
* **Accessibility:** WCAG 2.1 AA for public pages.
* **SEO:** Technical and on‑page standards; schema markup.

---

## 5. System Context

```
[Visitor Browser]
   | HTTPS
   v
[NGINX] -- static/media --> [DO Block Storage/CDN*]
   | uwsgi/gunicorn
   v
[Django 5 Monolith]
   | ORM
   v
[PostgreSQL]
   | cache/queues
   v
[Redis]

External Services: SMTP (email), GA4 (analytics), Google Maps, (Optional) reCAPTCHA.
*CDN is optional; can be added later.
```

---

## 6. Architecture Overview

### 6.1 Monolith Modules (Django apps)

* **core/**: settings, logging, middleware, users, roles, permissions, audit.
* **cms/**: pages, media assets, team, testimonials, SEO fields, WYSIWYG.
* **services/**: service categories, service items, specs, pricing ranges.
* **portfolio/**: projects, case studies, images, tags, results/metrics.
* **leads/**: bookings, inquiries, quotations, clients, communications log.
* **dashboard/**: KPIs, reports, exports (CSV), simple charts.
* **notifications/**: email templates, dispatch, status.
* **api/**: DRF endpoints for AJAX and future integrations.

### 6.2 Rendering Strategy

* Public pages via server‑rendered Django templates (HTMX‑friendly).
* Admin via Django Admin + select custom views (Tailwind/Bootstrap 5).
* Progressive enhancement with vanilla JS/HTMX; jQuery only where necessary.

### 6.3 Data Flow Key Paths

1. **Booking:** Public form → validate (CSRF, rate‑limit, captcha) → save Booking → email confirmations → Admin calendar/list → status updates → (optional) convert to Quote.
2. **Inquiry → Quote:** Public inquiry → triage → create Quote → generate PDF → email to client → track status (Sent, Viewed\*, Accepted, Rejected). (\*Viewed tracked via signed pixel link.)
3. **Analytics:** GA4 page & event tags → Admin dashboard reads from local DB (leads) + GA4 sampled KPIs entered manually or via notes (Phase 1).

---

## 7. Detailed Design

### 7.1 Data Model (entities)

* **User**(id, name, email, phone?, password\_hash, role, is\_active, last\_login, created\_at)
* **Role**(id, name \[Admin, Staff, Viewer], permissions)
* **Client**(id, org\_name?, contact\_name, email, phone, address?, notes)
* **ServiceCategory**(id, name, slug, description, icon?)
* **Service**(id, category\_id, name, slug, summary, specs\_json, base\_price\_min?, base\_price\_max?, duration\_estimate?, is\_active, seo\_fields)
* **Booking**(id, service\_id, client\_id?, name, email, phone, preferred\_date, preferred\_time\_slot, message, status \[New, Confirmed, Rescheduled, Completed, Canceled], admin\_notes, source \[Web, Phone], created\_at)
* **Inquiry**(id, service\_id?, client\_id?, name, email, phone, subject, message, status \[New, In Review, Closed], priority, created\_at)
* **Quotation**(id, inquiry\_id?, client\_id, quote\_no, items\_json, subtotal, tax, total, terms, valid\_until, status \[Draft, Sent, Accepted, Rejected, Expired], pdf\_url, sent\_at, decided\_at)
* **Project**(id, title, slug, summary, body\_html, services\_many\_to\_many, location, start\_date?, end\_date?, images\_many, results/metrics json, featured, seo\_fields)
* **Testimonial**(id, author\_name, org, quote, rating?, related\_project?, is\_published)
* **TeamMember**(id, name, role\_title, bio, certifications, photo)
* **MediaAsset**(id, file, alt\_text, caption, mime\_type, width, height, tags)
* **ContactMessage**(id, name, email, phone, subject, message, created\_at)
* **Notification**(id, type, to\_email, subject, body, template\_key, status, error\_msg?, sent\_at)
* **AuditLog**(id, user\_id?, action, model, object\_id, changes\_json, ip, created\_at)
* **Setting**(key, value\_json) — site configs, email, business hours, emergency contact.

> **Indexes:** email, phone on clients/leads; created\_at on leads; composite (service\_id, status) for bookings.

### 7.2 ERD (text)

```
User (1)───(n) AuditLog
Role (1)───(n) User
Client (1)──(n) Booking
Client (1)──(n) Inquiry
Client (1)──(n) Quotation
ServiceCategory (1)──(n) Service
Service (1)──(n) Booking
Service (1)──(n) Inquiry
Inquiry (1)──(0..1) Quotation
Project (m)──(m) Service (through ProjectService)
Project (1)──(n) MediaAsset (through ProjectImage)
Testimonial (0..n)──(0..1) Project
```

### 7.3 Key Workflows (sequence)

**A) Booking Submission**

1. Visitor opens service detail and clicks *Book Service*.
2. Form validates (required fields, time slot). reCAPTCHA optional.
3. Booking saved → Confirmation screen.
4. Emails: customer (ack), admin (new booking).
5. Admin reviews in calendar/list view → sets status.

**B) Inquiry → Quote**

1. Visitor submits inquiry.
2. Staff triage; if qualified, create Client and Quote.
3. Add line items (service/task, qty, unit price) → totals.
4. Generate PDF, email with acceptance link.
5. Client accepts/rejects → status updates; audit logged.

**C) Portfolio Publishing**

1. Staff creates Project with images and metrics.
2. Save as draft → preview → publish.

### 7.4 API (DRF) — Internal/External Ready

Base path: `/api/v1` (session or token auth for staff)

* **Public (rate‑limited)**

  * `POST /leads/bookings/` — create booking
  * `POST /leads/inquiries/` — create inquiry
  * `POST /leads/quote-accept/{quote_no}/` — signed token accept/reject
* **Admin**

  * `GET /leads/bookings/?status=` — list/filter
  * `PATCH /leads/bookings/{id}/` — update status/notes
  * `GET /leads/inquiries/` `POST /leads/quotes/` `GET /leads/quotes/{id}/pdf`
  * `GET/POST /cms/services/` `GET/POST /portfolio/projects/`
  * `GET /dashboard/metrics/` (leads counts, conversion, recent)

> All POST endpoints protected by CSRF for browser; JWT/Token for programmatic use. Apply `django-ratelimit` to public endpoints.

### 7.5 Templates & Components

* **UI Library:** Bootstrap 5 + utility classes; icons (Bootstrap Icons).
* **Shared components:** header, footer, breadcrumb, card, gallery, testimonial slider, lead forms, map block, callouts, CTA.

### 7.6 Email Templates

* Booking Acknowledgement, Booking Notification (Admin)
* Inquiry Acknowledgement, New Inquiry (Admin)
* Quote Sent, Quote Accepted, Quote Rejected

---

## 8. Security Design

* **Transport:** Enforce HTTPS (Let’s Encrypt), HSTS, secure cookies, TLS1.2+.
* **Auth:** Django auth; strong password policy; optional 2FA (Phase 2). Admin login IP throttling.
* **Authorization:** Role‑based permissions (Admin, Staff, Viewer). Object‑level checks on leads/quotes.
* **Input Protection:** CSRF, XSS escaping, ORM for SQLi prevention; server‑side validation.
* **Headers:** CSP (script-src 'self' GA domain), X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
* **Rate limiting:** `django-ratelimit` on public POSTs and login.
* **Secrets:** `.env` via DO secrets; never in VCS.
* **Backups:** Daily DB + media; 7‑day retention; monthly snapshot.
* **Audit:** Create/update/delete tracked in AuditLog with user & IP.

---

## 9. Performance & Scalability

* **Caching:** Redis for per‑view and low‑cardinality pages; Django cache middleware for anon traffic.
* **Static & Media:** NGINX `gzip`/`brotli`; image thumbnails; lazy‑loading; WebP.
* **DB:** Proper indexes; N+1 avoided (select\_related, prefetch\_related).
* **Concurrency:** Gunicorn with 3–4 workers (tuned to Droplet size).
* **CDN:** Optional DO CDN for media if traffic grows.
* **SLOs:** LCP < 2.5s, CLS < 0.1, TTFB < 500ms cached.

---

## 10. SEO & Accessibility

* Semantic HTML, ARIA where needed, keyboard navigation.
* Meta titles/descriptions per page; Open Graph/Twitter cards.
* Schema.org markup: Organization, Service, Product (if used), FAQ, BreadcrumbList.
* XML sitemap + robots.txt; canonical URLs; clean slugs.
* Internationalization hooks prepared (Phase 2 enablement).

---

## 11. Analytics & Event Model

* **GA4** page views + events: `lead_submit` (booking/inquiry), `quote_accept`, `quote_reject`, `cta_click`, `phone_click`.
* Consent banner for cookies; anonymize IP.
* Admin dashboard pulls lead metrics from DB; GA4 summarized manually in Phase 1 notes field.

---

## 12. Admin UX & Permissions

* **Admin**: Full access to all modules and settings.
* **Staff**: Manage leads, quotes, projects, testimonials; view dashboards.
* **Viewer**: Read‑only for dashboards and content preview.
* Custom list filters: date ranges, status, service.
* Calendar view for bookings; CSV export for leads/quotes/projects.

---

## 13. Deployment Architecture

### 13.1 Environments

* **Local Dev:** Docker (`web`, `db`, `redis`, `nginx`).
* **Staging:** DO Droplet; staging domain with HTTP auth; separate DB.
* **Production:** DO Droplet (2 vCPU/4GB+), PostgreSQL managed or on Droplet, Redis, NGINX, certbot.

### 13.2 CI/CD (GitHub Actions)

* Lint & test on PR; build Docker image; push to GHCR/DOCR.
* Staging auto‑deploy on `develop`; production manual approval on `main`.
* Run migrations, collectstatic, warm cache, health check.

### 13.3 Runtime Topology

```
[Internet]
  -> [NGINX reverse proxy]
       -> [Gunicorn: Django app]
            -> [PostgreSQL]
            -> [Redis]
       -> [/static, /media]
```

### 13.4 Configuration Matrix

* `DJANGO_SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
* DB: `DATABASE_URL`
* Cache: `REDIS_URL`
* Email: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `FROM_EMAIL`
* GA4: measurement ID
* Security: `CSP_*`, `SECURE_*` flags

---

## 14. Logging, Monitoring & Alerts

* **App logs:** JSON to stdout; rotated by systemd; error & access logs in NGINX.
* **Error tracking:** Sentry (optional) or Django email admins.
* **Uptime:** Health endpoint `/healthz`; use UptimeRobot/DO monitor.
* **Metrics:** Basic server metrics via DO; disk, CPU, memory alerts.

---

## 15. Testing Strategy

* **Unit tests:** models, forms, services, utils.
* **Integration tests:** booking/inquiry flows, quote generation, email send.
* **E2E (smoke):** Cypress or Playwright for critical paths.
* **Performance tests:** `locust` for booking/inquiry endpoints.
* **Security tests:** dependency scan, headers, auth, CSRF, rate‑limit checks.
* **Accessibility audits:** axe + Lighthouse.

**Acceptance Criteria (samples):**

* Submitting a booking creates a record, sends two emails, and shows success page.
* Quote PDF renders within 2s and totals are accurate within 0.01 KSh.
* LCP < 2.5s on 4G (home, services, portfolio list) for 75th percentile.

---

## 16. Backup & DR

* **DB backups:** nightly pg\_dump to DO Spaces (encrypted), retain 7 days; weekly full snapshot retained 4 weeks.
* **Media backups:** nightly rsync to Spaces; object versioning enabled if using CDN/Spaces.
* **Restore drills:** quarterly test restore to staging; document RTO 2h, RPO 24h.

---

## 17. Content Model & Editorial Workflow

* Page templates: Home, About, Services List, Service Detail, Portfolio List, Project Detail, Contact.
* Reusable blocks: hero, feature grid, testimonial slider, CTA, FAQ, contact block, map block.
* Workflow: Draft → Review → Publish. Versioning via database history (simple) or `django-simple-history`.

---

## 18. Risks & Mitigations

* **Spam submissions:** Add reCAPTCHA + rate limiting.
* **High media weight:** Enforce upload limits; background image compression.
* **Single VM failure:** Backups + snapshots; plan for DO managed Postgres in Phase 2.
* **SEO regressions:** Pre‑launch checklist, Lighthouse gating in CI.
* **Quote dispute:** Signed acceptance links + immutable PDF copies.

---

## 19. Roadmap (Future Phases)

* **Phase 2:** Payments (M-Pesa, cards), advanced CRM (pipelines, reminders), GA4 API sync, DO Spaces CDN, 2FA.
* **Phase 3:** Customer Portal (view quotes, invoices, bookings), multilingual, field‑service technician app.

---

## 20. Deliverables (Engineering)

* Dockerized Django app, infra as code (basic DO scripts), CI/CD pipelines.
* Admin customizations, dashboards, email templates, PDF generator.
* Comprehensive README, ops runbook, and training guide.

---

## 21. Checklists

### 21.1 Pre‑Launch

* [ ] All critical paths tested (booking, inquiry, quote PDF, email).
* [ ] SEO: titles, meta, schema, sitemap, robots, canonical.
* [ ] Security: HTTPS, HSTS, CSP, CSRF, rate limits, admin URL hardened.
* [ ] Performance: Lighthouse ≥ 90 desktop, ≥ 85 mobile; images optimized.
* [ ] Backups configured & trial restore validated.

### 21.2 Post‑Launch (Day 1–30)

* [ ] Monitor errors & uptime.
* [ ] Content polish & portfolio import.
* [ ] SEO indexing verified (GSC), submit sitemaps.
* [ ] Collect baseline metrics; tune cache/DB indexes.

---

## 22. Appendix

* **Quotation PDF:** We will use WeasyPrint or xhtml2pdf with a branded template.
* **WYSIWYG:** `django-ckeditor` for rich fields; sanitize HTML.
* **Mapping:** Google Maps embed on Contact page; API key stored in secrets.
* **Budget note:** Original proposal table totals appear off by a factor of 10. Engineering delivery is unaffected, but Finance should align figures before contract signature.

---

**End of Document**
