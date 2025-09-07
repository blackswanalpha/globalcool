Great — below are **concrete, ready-to-run agent prompts** for **all 70 page tasks**.
Each page task includes:

* **Task ID & Title**
* **Short Description**
* **Acceptance Criteria** (concise)
* **Assigned Agents** (Design, Frontend, Backend, Testing)
* **Concrete prompt templates** for each agent to copy/paste into your orchestrator or agent runner.
* Branch and repo placeholders are included (`<git_url>`, `feature/<task-id>`); agents should replace them when creating work.

You can feed these prompts to your Orchestrator Agent to dispatch to the relevant agents. I kept each prompt compact so agents can act immediately. If you want these exported as JSON or pushed into your issue tracker automatically, tell me and I’ll format them.

---

# PUBLIC WEBSITE — Tasks P1–P20 (20 pages)

## P1 — Home Page

**Description:** Implement public Home page (hero, services highlights, testimonials, quick contact, CTA).
**Acceptance Criteria:** Desktop & mobile responsive; CTA links to booking; hero accessible; SEO meta present.
**Agents:** Design, Frontend, Backend, Testing

**Design Agent Prompt**

```
Task: Design Home Page (P1)
Branch: feature/p1-home
Deliverable: Figma wireframe + high-fidelity mockup (desktop + mobile), component tokens (colors, typography), hero imagery placeholders.
Constraints: grayscale to color transition allowed; hero CTA prominent; include testimonial slider mock.
Return: Figma URL, exported assets list, acceptance checklist.
```

**Frontend Agent Prompt**

```
Task: Implement Home Page (P1)
Repo: <git_url>
Branch: feature/p1-home
Deliverable: Django template + CSS/partials, responsive layout, hero CTA linking to /booking/, testimonial slider (JS/HTMX), SEO meta tags.
Use: Bootstrap 5 + Tailwind utility classes.
Return: PR URL, screenshots desktop/mobile, local run instructions.
```

**Backend Agent Prompt**

```
Task: Provide Home Page context API (P1)
Repo: <git_url>
Branch: feature/p1-home-api
Deliverable: API endpoints or context providers for: featured services, latest testimonials, quick contact POST handler (/contact/).
Acceptance: contact POST validates, stores ContactMessage, sends admin email (placeholder).
Return: PR URL, migration if any, test outlines.
```

**Testing Agent Prompt**

```
Task: Test Home Page (P1)
Branch: feature/p1-home-tests
Deliverable: Integration tests: GET / (200), contact form POST creates record and sends email (mock), hero CTA navigates to booking.
Return: test files, test run results.
```

---

## P2 — About Us

**Description:** About page with company history, mission, team profiles.
**Acceptance:** Team profiles editable via admin; accessible layout; meta tags.

**Design**

```
Task: Design About Us (P2)
Branch: feature/p2-about-design
Deliverable: mockups with team section, certification badges, timeline. Provide component specs for profile cards.
```

**Frontend**

```
Task: Implement About Us (P2)
Branch: feature/p2-about
Deliverable: Template + responsive CSS; dynamic team section (data from backend); timeline component.
```

**Backend**

```
Task: Team & About CMS (P2)
Branch: feature/p2-about-api
Deliverable: Models TeamMember, AboutPage (rich text), admin CRUD, API endpoints to serve team list and about content.
```

**Testing**

```
Task: Test About Us (P2)
Deliverable: Tests for team listing endpoint, about content render, accessibility checks (a11y).
```

---

## P3 — Company Achievements (Timeline)

**Description:** Milestones & awards timeline page.
**Acceptance:** Timeline items editable from admin; responsive.

**Design**

```
Task: Design Achievements Page (P3)
Deliverable: timeline layout, milestone card component, mobile stacking behavior.
```

**Frontend**

```
Task: Implement Achievements Page (P3)
Deliverable: Template with timeline, lazy-load images, SEO metadata.
```

**Backend**

```
Task: Achievements model & API (P3)
Deliverable: Model Achievement(title, date, description, image), admin CRUD, public API list ordered by date.
```

**Testing**

```
Task: Test Achievements (P3)
Deliverable: API tests and rendering snapshot tests.
```

---

## P4 — Blog Listing

**Description:** Blog index with categories and pagination.
**Acceptance:** Pagination works, category filter works, page SEO.

**Design**

```
Task: Design Blog Listing (P4)
Deliverable: listing card, category sidebar, pagination controls mockups.
```

**Frontend**

```
Task: Implement Blog Listing (P4)
Deliverable: Template + paginated view, category filter, server-side rendering, canonical tags.
```

**Backend**

```
Task: Blog models & endpoints (P4)
Deliverable: Post model (title, slug, excerpt, body, author, tags), list endpoint with pagination.
```

**Testing**

```
Task: Test Blog Listing (P4)
Deliverable: Pagination tests, category filtering tests.
```

---

## P5 — Blog Detail

**Description:** Single blog article page with sharing.
**Acceptance:** Social share metadata (OG), author block, related posts.

**Design**

```
Task: Design Blog Detail (P5)
Deliverable: article layout (hero image, body, author card), related posts UI.
```

**Frontend**

```
Task: Implement Blog Detail (P5)
Deliverable: Template rendering rich content, OG meta tags, structured data (Article schema).
```

**Backend**

```
Task: Blog detail endpoint (P5)
Deliverable: GET /blog/{slug}/ returns full article and related posts. Add read count increment.
```

**Testing**

```
Task: Test Blog Detail (P5)
Deliverable: Response tests, OG meta checks, HTML sanitization tests.
```

---

## P6 — Services Listing

**Description:** Grid of HVAC services with quick CTAs.
**Acceptance:** Each service card links to detail; filters by category.

**Design**

```
Task: Design Services Listing (P6)
Deliverable: card spec, category filters, search field UI.
```

**Frontend**

```
Task: Implement Services Listing (P6)
Deliverable: Template + server-side rendering, filter by category, client-side search.
```

**Backend**

```
Task: Services model & list API (P6)
Deliverable: ServiceCategory + Service models, list endpoint with filter parameters.
```

**Testing**

```
Task: Test Services Listing (P6)
Deliverable: Filter and search tests, list response formatting tests.
```

---

## P7 — Service Detail

**Description:** Detailed service page (specs, booking CTA).
**Acceptance:** Booking CTA triggers booking modal/form; specs section uses JSON schema fields.

**Design**

```
Task: Design Service Detail (P7)
Deliverable: hero + specs layout, technical spec table, CTA placement.
```

**Frontend**

```
Task: Implement Service Detail (P7)
Deliverable: Template with specs table, booking modal wired to /api/v1/bookings/.
```

**Backend**

```
Task: Service detail API (P7)
Deliverable: GET /services/{slug}/ returns service details including specs_json and related projects.
```

**Testing**

```
Task: Test Service Detail (P7)
Deliverable: API tests and UI integration test for booking flow trigger.
```

---

## P8 — Portfolio Listing

**Description:** Gallery of projects with filters (service type, year).
**Acceptance:** Gallery loads progressively; filtering works.

**Design**

```
Task: Design Portfolio Listing (P8)
Deliverable: masonry/grid mock, filter controls, load-more behavior.
```

**Frontend**

```
Task: Implement Portfolio Listing (P8)
Deliverable: Template with filter UI, lazy-load images, accessible lightbox for images.
```

**Backend**

```
Task: Portfolio model & API (P8)
Deliverable: Project model with images, tags, services many-to-many, list endpoint with filters.
```

**Testing**

```
Task: Test Portfolio Listing (P8)
Deliverable: Filter tests, image lazy-load presence.
```

---

## P9 — Portfolio Detail (Project Case Study)

**Description:** Project page with before/after gallery and case study.
**Acceptance:** Image gallery accessible; project metadata present.

**Design**

```
Task: Design Portfolio Detail (P9)
Deliverable: case study layout: summary, problem, solution, results, gallery.
```

**Frontend**

```
Task: Implement Portfolio Detail (P9)
Deliverable: Template, gallery widget (before/after slider), structured data for project.
```

**Backend**

```
Task: Project detail API (P9)
Deliverable: GET /projects/{slug}/ with images and metrics JSON.
```

**Testing**

```
Task: Test Portfolio Detail (P9)
Deliverable: Rendering tests, gallery accessibility checks.
```

---

## P10 — Job Listings / Careers

**Description:** Career openings listing and application form.
**Acceptance:** Application file upload stores in media and notifies admin.

**Design**

```
Task: Design Careers Page (P10)
Deliverable: listing layout + job detail mock + simple application form UI.
```

**Frontend**

```
Task: Implement Careers Page (P10)
Deliverable: listing & detail templates, application form with file upload to media.
```

**Backend**

```
Task: Careers model & application handler (P10)
Deliverable: JobOpening model; Application model with file storage; admin notifications.
```

**Testing**

```
Task: Test Careers (P10)
Deliverable: File upload handling tests, email notification test (mocked).
```

---

## P11 — Contact Us

**Description:** Contact page with form + Google Maps.
**Acceptance:** Form stores ContactMessage; map uses API key placeholder.

**Design**

```
Task: Design Contact Page (P11)
Deliverable: form layout, contact details block, map block placement.
```

**Frontend**

```
Task: Implement Contact Page (P11)
Deliverable: template with form POST to backend, map embed placeholder, phone click-to-call.
```

**Backend**

```
Task: Contact endpoint (P11)
Deliverable: POST /contact/ creates ContactMessage, sends admin notification; rate-limit applied.
```

**Testing**

```
Task: Test Contact Page (P11)
Deliverable: form validation tests, spam/rate-limit tests.
```

---

## P12 — Booking Form Page

**Description:** Full booking page with date/time picker and service selection.
**Acceptance:** Validates availability, persists booking, sends confirmation email (placeholder).

**Design**

```
Task: Design Booking Form Page (P12)
Deliverable: multi-step booking form mock, availability UI, calendar widget spec.
```

**Frontend**

```
Task: Implement Booking Form (P12)
Deliverable: template + JS for date/time selection, form POST to /api/v1/bookings/, show success page.
```

**Backend**

```
Task: Booking API (P12)
Deliverable: POST /api/v1/bookings/ with validation against business hours and max bookings per slot; store booking, enqueue email task.
```

**Testing**

```
Task: Test Booking Flow (P12)
Deliverable: Integration tests for availability checks, booking creation, email enqueue.
```

---

## P13 — Booking Confirmation Page

**Description:** Confirmation page shown after booking success.
**Acceptance:** Shows booking summary and next steps; link to client portal signup.

**Design**

```
Task: Design Booking Confirmation (P13)
Deliverable: confirmation layout, CTA to create client account, calendar add-to link.
```

**Frontend**

```
Task: Implement Booking Confirmation (P13)
Deliverable: template rendering booking reference and add-to-calendar link.
```

**Backend**

```
Task: Confirmation data provider (P13)
Deliverable: endpoint to fetch booking summary by token for confirmation page.
```

**Testing**

```
Task: Test Confirmation Page (P13)
Deliverable: Tokenized fetch tests, rendering check.
```

---

## P14 — Inquiry Form (Multi-step)

**Description:** Multi-step inquiry with file upload and service specification fields.
**Acceptance:** Submissions stored; attachments saved; admin notified.

**Design**

```
Task: Design Inquiry Form (P14)
Deliverable: multi-step form UI, progress indicator, file upload UX.
```

**Frontend**

```
Task: Implement Inquiry Form (P14)
Deliverable: form with stepper, POST to /api/v1/inquiries/, client-side validation and attachment upload.
```

**Backend**

```
Task: Inquiry API (P14)
Deliverable: model Inquiry with attachments, secure file handling, admin notification.
```

**Testing**

```
Task: Test Inquiry Flow (P14)
Deliverable: stepper flow tests, file attachment tests, DB record assertions.
```

---

## P15 — Quotation Request Page

**Description:** Page for client to request a detailed quotation (uploads allowed).
**Acceptance:** Quotation request creates Inquiry and optionally Draft Quotation in admin.

**Design**

```
Task: Design Quotation Request (P15)
Deliverable: form design with fields for scope, budget estimate, attachments.
```

**Frontend**

```
Task: Implement Quotation Request (P15)
Deliverable: template + file upload; POST to create Inquiry & optional auto-draft quote flag.
```

**Backend**

```
Task: Quotation request handler (P15)
Deliverable: Create Inquiry and if flagged create Quotation draft with reference to attachment(s).
```

**Testing**

```
Task: Test Quotation Request (P15)
Deliverable: end-to-end test that verifies Inquiry and optional Quotation creation.
```

---

## P16 — Testimonials Page

**Description:** Aggregated testimonials with filters and video support.
**Acceptance:** CMS-managed testimonials show on page; video placeholders load lazily.

**Design**

```
Task: Design Testimonials Page (P16)
Deliverable: carousel mock, card layout, video support.
```

**Frontend**

```
Task: Implement Testimonials (P16)
Deliverable: template with carousel and filters, lazy-load video embeds.
```

**Backend**

```
Task: Testimonials API (P16)
Deliverable: Model Testimonial, publish/unpublish flag, public list endpoint.
```

**Testing**

```
Task: Test Testimonials (P16)
Deliverable: API tests for published filtering, UI snapshot tests for carousel.
```

---

## P17 — Success Stories (Detailed Case Studies)

**Description:** Long-form case studies with metrics and downloadable PDFs.
**Acceptance:** PDF generation for each case study; print-friendly layout.

**Design**

```
Task: Design Success Story Page (P17)
Deliverable: long-form article layout, metric callouts, PDF download button.
```

**Frontend**

```
Task: Implement Success Story (P17)
Deliverable: template with print styles, link to /projects/{slug}/pdf
```

**Backend**

```
Task: Generate PDF for project (P17)
Deliverable: Endpoint to render project to PDF (WeasyPrint), caching the generated PDF URL.
```

**Testing**

```
Task: Test Success Story (P17)
Deliverable: PDF generation test, content integrity check.
```

---

## P18 — Privacy Policy

**Description:** Static page for privacy policy and cookie consent details.
**Acceptance:** GDPR notices present; cookie consent UX included.

**Design**

```
Task: Design Privacy Policy (P18)
Deliverable: readable layout, headings for sections, cookie consent mock.
```

**Frontend**

```
Task: Implement Privacy Policy (P18)
Deliverable: static template and cookie consent component that toggles GA tracking.
```

**Backend**

```
Task: Cookie consent toggle handling (P18)
Deliverable: Endpoint to store user consent (optional) and return consent status.
```

**Testing**

```
Task: Test Privacy Policy (P18)
Deliverable: consent flow tests, content rendering tests.
```

---

## P19 — Terms of Service

**Description:** Legal terms page.
**Acceptance:** Accessible, printable layout.

**Design**

```
Task: Design Terms of Service (P19)
Deliverable: structured legal page mock with TOC.
```

**Frontend**

```
Task: Implement Terms (P19)
Deliverable: static template with anchor links for TOC.
```

**Backend**

```
Task: No backend changes required (P19)
Deliverable: static content management via CMS for legal text.
```

**Testing**

```
Task: Test Terms (P19)
Deliverable: rendering and print-styles test.
```

---

## P20 — Sitemap / HTML Sitemap

**Description:** Human-readable sitemap page and XML sitemap generation.
**Acceptance:** XML sitemap generated dynamically, HTML sitemap page lists major pages.

**Design**

```
Task: Design Sitemap Page (P20)
Deliverable: HTML sitemap layout with categories and lastmod info.
```

**Frontend**

```
Task: Implement Sitemap (P20)
Deliverable: /sitemap/ HTML page and /sitemap.xml endpoint generation.
```

**Backend**

```
Task: Sitemap generation (P20)
Deliverable: sitemap framework integration to produce dynamic XML sitemap and HTML view.
```

**Testing**

```
Task: Test Sitemap (P20)
Deliverable: check /sitemap.xml validity and HTML sitemap links exist.
```

---

# ADMIN PORTAL — Tasks A1–A30 (30 pages)

*We’ll number Admin tasks A1–A30 corresponding to the 30 admin pages.*

## A1 — Admin Login Page

**Description:** Secure admin login with 2FA placeholder.
**Acceptance:** CSRF protection, rate-limiting, remember-me checkbox.

**Design**

```
Task: Design Admin Login (A1)
Deliverable: login page mock with error states, forgot password flow.
```

**Frontend**

```
Task: Implement Admin Login (A1)
Deliverable: template + auth form, rate-limit hint, redirect after login.
```

**Backend**

```
Task: Admin auth endpoints (A1)
Deliverable: login view, failed login logging, optional 2FA flag in user model.
```

**Testing**

```
Task: Test Admin Login (A1)
Deliverable: auth tests, rate-limit tests, CSRF check.
```

---

## A2 — Admin Dashboard Overview

**Description:** KPI dashboard (bookings, inquiries, recent activity).
**Acceptance:** Widgets load via API; configurable date range.

**Design**

```
Task: Design Admin Dashboard (A2)
Deliverable: widget layout, KPI card specs, activity feed component.
```

**Frontend**

```
Task: Implement Admin Dashboard (A2)
Deliverable: dashboard template, widgets fetch /api/admin/metrics/, chart placeholders.
```

**Backend**

```
Task: Admin metrics API (A2)
Deliverable: endpoint aggregate bookings/inquiries/quotes for date ranges.
```

**Testing**

```
Task: Test Dashboard (A2)
Deliverable: metrics API tests and widget rendering integration tests.
```

---

## A3 — Users Listing (Admin)

**Description:** Manage admin & staff users.
**Acceptance:** CRUD, search, roles filter.

**Design**

```
Task: Design Users Listing (A3)
Deliverable: table layout, pagination, bulk actions UI.
```

**Frontend**

```
Task: Implement Users Listing (A3)
Deliverable: admin template with data table, filters and action buttons.
```

**Backend**

```
Task: Users admin endpoints (A3)
Deliverable: admin user model CRUD, REST endpoints (protected).
```

**Testing**

```
Task: Test Users Listing (A3)
Deliverable: permission tests, CRUD tests.
```

---

## A4 — Add/Edit User

**Description:** Form to create or modify user accounts and assign roles.
**Acceptance:** Validation, role assignment enforced.

**Design**

```
Task: Design Add/Edit User (A4)
Deliverable: form layout with role and permission matrix UI.
```

**Frontend**

```
Task: Implement Add/Edit User (A4)
Deliverable: admin form, validation messages, submit to user API.
```

**Backend**

```
Task: User create/update handlers (A4)
Deliverable: endpoints, password validation rules, email invite flow.
```

**Testing**

```
Task: Test Add/Edit User (A4)
Deliverable: unit tests for role assignment and password rules.
```

---

## A5 — Roles & Permissions Management

**Description:** Manage role definitions and module access.
**Acceptance:** Role creation, permission toggles, role-based UI gating.

**Design**

```
Task: Design Roles & Permissions (A5)
Deliverable: role editor mock, permission matrix visualization.
```

**Frontend**

```
Task: Implement Roles UI (A5)
Deliverable: UI to create/edit roles and toggle permissions; reflect changes immediately.
```

**Backend**

```
Task: Role model & enforcement (A5)
Deliverable: Role model, permission checks middleware, admin endpoints.
```

**Testing**

```
Task: Test Roles (A5)
Deliverable: permission enforcement tests and UI gating tests.
```

---

## A6 — Activity Logs

**Description:** Audit trail of admin actions.
**Acceptance:** Filterable logs, export CSV.

**Design**

```
Task: Design Activity Log (A6)
Deliverable: log table mock, filter controls, export button UI.
```

**Frontend**

```
Task: Implement Activity Log (A6)
Deliverable: admin view with paginated logs and export to CSV.
```

**Backend**

```
Task: Audit log infrastructure (A6)
Deliverable: AuditLog model, API for querying with filters, CSV export endpoint.
```

**Testing**

```
Task: Test Activity Logs (A6)
Deliverable: creation on actions, filter tests, CSV export tests.
```

---

## A7 — Account Security Settings

**Description:** Admin security settings page (2FA, sessions).
**Acceptance:** Session revocation, 2FA status toggle (placeholder).

**Design**

```
Task: Design Account Security (A7)
Deliverable: session list UI and 2FA toggle mock.
```

**Frontend**

```
Task: Implement Account Security (A7)
Deliverable: UI to list sessions, revoke, and toggle 2FA (UI only unless backend supports).
```

**Backend**

```
Task: Sessions & 2FA backend (A7)
Deliverable: session management endpoints, 2FA flag storage; API to revoke sessions.
```

**Testing**

```
Task: Test Account Security (A7)
Deliverable: session revoke tests and 2FA flag tests.
```

---

## A8 — Services Overview (Admin)

**Description:** Admin list of services with CRUD controls.
**Acceptance:** Service create/edit/delete; publish toggle.

**Design**

```
Task: Design Services Admin (A8)
Deliverable: services table mock, inline publish toggle UI.
```

**Frontend**

```
Task: Implement Services Admin (A8)
Deliverable: admin list view, action buttons, bulk operations.
```

**Backend**

```
Task: Services admin endpoints (A8)
Deliverable: admin APIs for service CRUD and publish toggle.
```

**Testing**

```
Task: Test Services Admin (A8)
Deliverable: CRUD tests and publish state tests.
```

---

## A9 — Add/Edit Service (Admin)

**Description:** Create or edit service entries with specs.
**Acceptance:** Specs JSON editor or structured fields; image uploads.

**Design**

```
Task: Design Add/Edit Service (A9)
Deliverable: form layout, specs editor UX, image upload controls.
```

**Frontend**

```
Task: Implement Service Editor (A9)
Deliverable: admin form with WYSIWYG and JSON specs helper, image uploader.
```

**Backend**

```
Task: Service editor backend (A9)
Deliverable: Save service fields, process images, validation for specs_json.
```

**Testing**

```
Task: Test Service Editor (A9)
Deliverable: validation tests for specs and image handling.
```

---

## A10 — Portfolio Management

**Description:** Admin module to manage projects/case studies.
**Acceptance:** Project create/edit, image uploads, feature flag.

**Design**

```
Task: Design Portfolio Admin (A10)
Deliverable: list + editor mock for projects, bulk image uploader.
```

**Frontend**

```
Task: Implement Portfolio Admin (A10)
Deliverable: admin list & editor templates for projects, drag-and-drop images.
```

**Backend**

```
Task: Projects admin backend (A10)
Deliverable: Project model CRUD, image handling, ordering, publish toggles.
```

**Testing**

```
Task: Test Portfolio Admin (A10)
Deliverable: project CRUD tests and media tests.
```

---

## A11 — Project Detail Editing

**Description:** Edit project details including metrics and attachments.
**Acceptance:** Save metrics JSON and regenerate PDF.

**Design**

```
Task: Design Project Editor (A11)
Deliverable: metrics input UI, PDF preview placeholder.
```

**Frontend**

```
Task: Implement Project Editor (A11)
Deliverable: editor with fields for results/metrics and PDF generation trigger.
```

**Backend**

```
Task: Project update & PDF (A11)
Deliverable: save metrics, endpoint to regenerate project PDF.
```

**Testing**

```
Task: Test Project Editor (A11)
Deliverable: metrics persistence tests and PDF regeneration tests.
```

---

## A12 — Testimonials Management

**Description:** Approve/reject/manage testimonials.
**Acceptance:** Toggle publish; attach project relation.

**Design**

```
Task: Design Testimonials Admin (A12)
Deliverable: list with approval actions and preview panel.
```

**Frontend**

```
Task: Implement Testimonials Admin (A12)
Deliverable: admin list and editor for testimonials with publish toggle.
```

**Backend**

```
Task: Testimonials backend (A12)
Deliverable: model with publish flag and relation to project; admin endpoints.
```

**Testing**

```
Task: Test Testimonials Admin (A12)
Deliverable: publish/unpublish tests and relation tests.
```

---

## A13 — Team Management (Admin)

**Description:** Manage team member profiles and certifications.
**Acceptance:** Profile photos, bio, certifications list stored.

**Design**

```
Task: Design Team Admin (A13)
Deliverable: team list and editor mock.
```

**Frontend**

```
Task: Implement Team Admin (A13)
Deliverable: admin CRUD templates for TeamMember with image upload.
```

**Backend**

```
Task: TeamMember model & APIs (A13)
Deliverable: model, admin endpoints, image validations.
```

**Testing**

```
Task: Test Team Admin (A13)
Deliverable: CRUD tests and image processing tests.
```

---

## A14 — SEO Metadata Manager

**Description:** Admin tool to configure meta titles/descriptions and schema for pages.
**Acceptance:** Meta values applied on public pages; preview provided.

**Design**

```
Task: Design SEO Manager (A14)
Deliverable: UI for page selection and meta field editing, preview panel.
```

**Frontend**

```
Task: Implement SEO Manager (A14)
Deliverable: admin UI to edit SEO fields stored in Setting model or per-page objects.
```

**Backend**

```
Task: SEO storage & application (A14)
Deliverable: store SEO fields and serve to templates; API to fetch/edit.
```

**Testing**

```
Task: Test SEO Manager (A14)
Deliverable: ensure meta fields propagate to public pages and schema present.
```

---

## A15 — Bookings Overview (Admin)

**Description:** Master bookings list with filters and quick actions.
**Acceptance:** Table shows status, client info, service, date; bulk actions.

**Design**

```
Task: Design Bookings Overview (A15)
Deliverable: bookings table mock with status badges and filters.
```

**Frontend**

```
Task: Implement Bookings Overview (A15)
Deliverable: admin template with server-side pagination and filters.
```

**Backend**

```
Task: Bookings admin endpoints (A15)
Deliverable: filtered booking list API with export option.
```

**Testing**

```
Task: Test Bookings Overview (A15)
Deliverable: filter tests, bulk action tests, export validation.
```

---

## A16 — Booking Detail Page (Admin)

**Description:** Detailed booking view to update status, add admin notes, reschedule.
**Acceptance:** Update changes persisted and emails sent on status change (mock).

**Design**

```
Task: Design Booking Detail (A16)
Deliverable: detail view mock with timeline and action buttons.
```

**Frontend**

```
Task: Implement Booking Detail (A16)
Deliverable: admin detail template, status change modal, note entry.
```

**Backend**

```
Task: Booking update handlers (A16)
Deliverable: endpoints to update status, add admin notes, and log audit entries.
```

**Testing**

```
Task: Test Booking Detail (A16)
Deliverable: status transition tests and audit log creation tests.
```

---

## A17 — Inquiry Management

**Description:** List and manage customer inquiries; assign to staff.
**Acceptance:** Assignment persists, notifications queued.

**Design**

```
Task: Design Inquiry Management (A17)
Deliverable: list with assignment UI and quick reply mock.
```

**Frontend**

```
Task: Implement Inquiry Management (A17)
Deliverable: admin list with assign dropdown and quick email reply modal.
```

**Backend**

```
Task: Inquiry endpoints (A17)
Deliverable: assign API, status update, email template send.
```

**Testing**

```
Task: Test Inquiry Management (A17)
Deliverable: assign tests and quick reply email tests (mock).
```

---

## A18 — Quotation Management

**Description:** Create, edit, send, track quotations.
**Acceptance:** Generate PDF, set expiry, track acceptance via tokenized link.

**Design**

```
Task: Design Quotation Management (A18)
Deliverable: quotation editor mock, line item editor, send flow UI.
```

**Frontend**

```
Task: Implement Quotation Editor (A18)
Deliverable: admin UI for quote lines, totals, preview PDF, send email action.
```

**Backend**

```
Task: Quotation model & send flow (A18)
Deliverable: Quotation model, PDF render endpoint, tokenized accept/reject endpoint.
```

**Testing**

```
Task: Test Quotation Management (A18)
Deliverable: PDF generation test, accept token validation tests.
```

---

## A19 — Calendar & Scheduling (Admin)

**Description:** Calendar view for bookings with drag/reschedule support.
**Acceptance:** Visual calendar displays bookings; drag triggers reschedule API.

**Design**

```
Task: Design Admin Calendar (A19)
Deliverable: month/week/day views mock, reschedule UX.
```

**Frontend**

```
Task: Implement Calendar (A19)
Deliverable: calendar view integrated with bookings API, drag-and-drop reschedule (UI).
```

**Backend**

```
Task: Calendar reschedule API (A19)
Deliverable: endpoint to update booking date/time with validation.
```

**Testing**

```
Task: Test Calendar (A19)
Deliverable: reschedule tests and conflict checks.
```

---

## A20 — Website Traffic Dashboard (GA4)

**Description:** Admin page summarizing GA4 metrics (requires GA id).
**Acceptance:** Show pageviews, sessions, top pages (using GA API or placeholder).

**Design**

```
Task: Design Traffic Dashboard (A20)
Deliverable: chart layouts and panels for key metrics.
```

**Frontend**

```
Task: Implement Traffic Dashboard (A20)
Deliverable: charts pulling from backend summary endpoint; placeholder if GA not configured.
```

**Backend**

```
Task: GA4 sync or aggregator (A20)
Deliverable: endpoint to fetch cached GA metrics or accept manual upload for Phase 1.
```

**Testing**

```
Task: Test Traffic Dashboard (A20)
Deliverable: API tests for metrics aggregator and chart rendering tests.
```

---

## A21 — Leads & Conversion Analytics

**Description:** Detailed lead funnel analytics.
**Acceptance:** charts for lead sources, conversion rates, exported CSV.

**Design**

```
Task: Design Leads Analytics (A21)
Deliverable: funnel UI mock and filters.
```

**Frontend**

```
Task: Implement Leads Analytics (A21)
Deliverable: charts and table views, CSV export button.
```

**Backend**

```
Task: Leads analytics aggregator (A21)
Deliverable: job to aggregate lead metrics by source and date.
```

**Testing**

```
Task: Test Leads Analytics (A21)
Deliverable: aggregator unit tests and export validation.
```

---

## A22 — Booking Performance Dashboard

**Description:** Metrics and KPIs specific to bookings (volume, cancellations).
**Acceptance:** date-range filters and service breakdown.

**Design**

```
Task: Design Booking Performance (A22)
Deliverable: KPI cards and drilldown mock.
```

**Frontend**

```
Task: Implement Booking Performance (A22)
Deliverable: charts and drilldown UI.
```

**Backend**

```
Task: Booking performance endpoints (A22)
Deliverable: aggregated booking metrics and per-service breakdown.
```

**Testing**

```
Task: Test Booking Performance (A22)
Deliverable: tests for aggregation correctness.
```

---

## A23 — Revenue Reports & Exports

**Description:** Financial reporting view and export to CSV/PDF.
**Acceptance:** export for date range and service filters.

**Design**

```
Task: Design Revenue Reports (A23)
Deliverable: table & export UI mock.
```

**Frontend**

```
Task: Implement Revenue Reports (A23)
Deliverable: report UI with export endpoints integration.
```

**Backend**

```
Task: Revenue aggregation (A23)
Deliverable: endpoints to compute revenue approximations from quotations/invoices and export.
```

**Testing**

```
Task: Test Revenue Reports (A23)
Deliverable: export and data integrity tests.
```

---

## A24 — SEO Performance Report

**Description:** Admin page surfacing SEO metrics (indexing, top keywords — manual for Phase1).
**Acceptance:** sitemap status and GSC hints (manual fields ok).

**Design**

```
Task: Design SEO Report (A24)
Deliverable: panels for indexing status and top pages mock.
```

**Frontend**

```
Task: Implement SEO Report (A24)
Deliverable: UI to paste GSC data or show sitemap indexing summary.
```

**Backend**

```
Task: SEO status endpoint (A24)
Deliverable: endpoint to show sitemap last submitted and indexing flag.
```

**Testing**

```
Task: Test SEO Report (A24)
Deliverable: validate status endpoints and UI display.
```

---

## A25 — General Settings

**Description:** Site configuration (business hours, emergency contact, logo).
**Acceptance:** Save & apply changes, settings stored in DB.

**Design**

```
Task: Design General Settings (A25)
Deliverable: settings form layout and save confirmation UI.
```

**Frontend**

```
Task: Implement General Settings (A25)
Deliverable: admin form to update settings and preview site header/footer changes.
```

**Backend**

```
Task: Settings model & endpoints (A25)
Deliverable: Setting key/value store and admin API to update.
```

**Testing**

```
Task: Test General Settings (A25)
Deliverable: persistency tests and preview verification tests.
```

---

## A26 — Email Template Management

**Description:** Manage email templates for booking, inquiry, quote.
**Acceptance:** Template variables documented and working in previews.

**Design**

```
Task: Design Email Template Manager (A26)
Deliverable: template editor mock with variable insertion helper.
```

**Frontend**

```
Task: Implement Email Template Manager (A26)
Deliverable: editor UI with preview and save actions.
```

**Backend**

```
Task: Email template storage & render (A26)
Deliverable: store templates, render with context, preview endpoint.
```

**Testing**

```
Task: Test Email Templates (A26)
Deliverable: rendering tests for placeholders and preview.
```

---

## A27 — Notification Center (Logs & Config)

**Description:** View sent notifications and adjust settings.
**Acceptance:** list of notifications with status and error details.

**Design**

```
Task: Design Notification Center (A27)
Deliverable: list view mock and retry action UI.
```

**Frontend**

```
Task: Implement Notification Center (A27)
Deliverable: admin list with retry actions and search.
```

**Backend**

```
Task: Notification model & API (A27)
Deliverable: Notification model with status, retry endpoints, and logs storage.
```

**Testing**

```
Task: Test Notification Center (A27)
Deliverable: create/retry tests and error logging checks.
```

---

## A28 — API Key & Integrations Management

**Description:** Manage third-party API keys (maps, GA, SMTP) with secure handling.
**Acceptance:** Keys saved to secret store (placeholder), front-end shows masked values.

**Design**

```
Task: Design Integrations UI (A28)
Deliverable: masked key inputs mock and test connectivity button.
```

**Frontend**

```
Task: Implement Integrations UI (A28)
Deliverable: admin page to input keys; UI calls backend test connection endpoint.
```

**Backend**

```
Task: Integrations endpoints & secret placeholders (A28)
Deliverable: endpoints to store placeholders, test connection logic (mock), and instruct humans to add real secrets.
```

**Testing**

```
Task: Test Integrations (A28)
Deliverable: test connection mocks and UI masking tests.
```

---

## A29 — Audit Logs & Backups

**Description:** Manage backups and view system audit logs; trigger backup/restore.
**Acceptance:** Trigger backup job and list restore points.

**Design**

```
Task: Design Backups UI (A29)
Deliverable: backup/restore mock and retention settings UI.
```

**Frontend**

```
Task: Implement Backups UI (A29)
Deliverable: trigger backup, show status, and list snapshots.
```

**Backend**

```
Task: Backup job endpoints (A29)
Deliverable: endpoint to call backup script (CI/ops) and list snapshots (mock if managed).
```

**Testing**

```
Task: Test Backups (A29)
Deliverable: simulate backup triggers and list snapshot responses.
```

---

## A30 — Admin Help Center & Guides

**Description:** Admin help docs, onboarding guides, and support links.
**Acceptance:** Searchable help content; versioned docs.

**Design**

```
Task: Design Help Center (A30)
Deliverable: help page layout and article templates.
```

**Frontend**

```
Task: Implement Help Center (A30)
Deliverable: admin help articles list, search, and article detail views.
```

**Backend**

```
Task: Help article model & API (A30)
Deliverable: store help docs in CMS with versioning and API for search.
```

**Testing**

```
Task: Test Help Center (A30)
Deliverable: search tests and article render checks.
```

---

# CLIENT PORTAL — Tasks C1–C20 (20 pages)

## C1 — Client Login Page

**Description:** Client authentication, keep separate from admin.
**Acceptance:** Secure auth, forgot password.

**Design**

```
Task: Design Client Login (C1)
Deliverable: login mock with signup & forgot password links.
```

**Frontend**

```
Task: Implement Client Login (C1)
Deliverable: login template, redirect to /client/dashboard on success.
```

**Backend**

```
Task: Client auth endpoints (C1)
Deliverable: client login view, password reset flows.
```

**Testing**

```
Task: Test Client Login (C1)
Deliverable: auth tests and forgot-password token test.
```

---

## C2 — Client Registration

**Description:** Sign-up flow for clients (option to link existing booking).
**Acceptance:** Account created and optionally linked to booking reference.

**Design**

```
Task: Design Client Registration (C2)
Deliverable: sign-up flow mock with link-to-booking option.
```

**Frontend**

```
Task: Implement Client Registration (C2)
Deliverable: registration form, validation, and onboarding CTA.
```

**Backend**

```
Task: Registration handler (C2)
Deliverable: create client account, optional link to booking via reference token.
```

**Testing**

```
Task: Test Registration (C2)
Deliverable: account creation tests and booking linking tests.
```

---

## C3 — Forgot / Reset Password

**Description:** Password reset flow for clients.
**Acceptance:** Secure token flow, expiry, and email placeholder.

**Design**

```
Task: Design Reset Password (C3)
Deliverable: reset request & new password forms mock.
```

**Frontend**

```
Task: Implement Reset Password (C3)
Deliverable: templates and flows to request token and set new password.
```

**Backend**

```
Task: Password reset endpoints (C3)
Deliverable: token generation, email send placeholder, token validation on reset.
```

**Testing**

```
Task: Test Password Reset (C3)
Deliverable: token expiry and reset test cases.
```

---

## C4 — Client Dashboard

**Description:** Overview of upcoming bookings, recent quotes, quick actions.
**Acceptance:** Data aggregated and linked to detail pages.

**Design**

```
Task: Design Client Dashboard (C4)
Deliverable: widget mock for bookings, quotes, invoices, and quick actions.
```

**Frontend**

```
Task: Implement Client Dashboard (C4)
Deliverable: dashboard template fetching data from client APIs.
```

**Backend**

```
Task: Client dashboard API (C4)
Deliverable: endpoint returning upcoming bookings, recent quotes, notifications.
```

**Testing**

```
Task: Test Dashboard (C4)
Deliverable: API response tests and dashboard rendering tests.
```

---

## C5 — Profile Overview

**Description:** Show contact details and business info.
**Acceptance:** Editable fields and avatar upload.

**Design**

```
Task: Design Profile Overview (C5)
Deliverable: profile card mock and edit CTA.
```

**Frontend**

```
Task: Implement Profile Overview (C5)
Deliverable: profile display template with edit link.
```

**Backend**

```
Task: Client profile endpoints (C5)
Deliverable: endpoints to fetch and update profile; avatar upload.
```

**Testing**

```
Task: Test Profile (C5)
Deliverable: update tests and avatar upload tests.
```

---

## C6 — Profile Edit Page

**Description:** Edit client profile, contact preferences, business details.
**Acceptance:** Changes saved and reflected in bookings communications.

**Design**

```
Task: Design Profile Edit (C6)
Deliverable: edit form mock with preference toggles.
```

**Frontend**

```
Task: Implement Profile Edit (C6)
Deliverable: form submission to update profile and show success banner.
```

**Backend**

```
Task: Profile update handlers (C6)
Deliverable: update endpoint and audit log creation.
```

**Testing**

```
Task: Test Profile Edit (C6)
Deliverable: field validation tests and preference persistence tests.
```

---

## C7 — Notifications Center (Client)

**Description:** Client notifications list and preferences.
**Acceptance:** Mark read/unread; preference toggles persist.

**Design**

```
Task: Design Client Notifications (C7)
Deliverable: list mock with read/unread states and preference switches.
```

**Frontend**

```
Task: Implement Client Notifications (C7)
Deliverable: UI to show notifications and update preferences.
```

**Backend**

```
Task: Notifications client endpoints (C7)
Deliverable: store notifications per user and preference toggles.
```

**Testing**

```
Task: Test Client Notifications (C7)
Deliverable: read/unread tests and preference persistence tests.
```

---

## C8 — My Bookings Overview

**Description:** List of bookings for the client with status badges.
**Acceptance:** Status updates pulled in real-time (polling acceptable).

**Design**

```
Task: Design My Bookings (C8)
Deliverable: list and card mock for bookings and quick actions.
```

**Frontend**

```
Task: Implement My Bookings (C8)
Deliverable: client view with filter and action (reschedule/cancel).
```

**Backend**

```
Task: Client bookings endpoint (C8)
Deliverable: endpoint returning bookings for authenticated client.
```

**Testing**

```
Task: Test My Bookings (C8)
Deliverable: retrieval and action permission tests.
```

---

## C9 — Booking Detail (Client)

**Description:** View booking status, assigned technician, notes, and timeline.
**Acceptance:** Display technician contact (if assigned) and allow reschedule request.

**Design**

```
Task: Design Booking Detail (C9)
Deliverable: timeline view mock and reschedule CTA placement.
```

**Frontend**

```
Task: Implement Booking Detail (C9)
Deliverable: detail template with timeline and reschedule/cancel actions.
```

**Backend**

```
Task: Booking detail API (C9)
Deliverable: endpoint returning detailed booking info and allowed actions.
```

**Testing**

```
Task: Test Booking Detail (C9)
Deliverable: permission tests and reschedule request test.
```

---

## C10 — New Booking Request (Client)

**Description:** Client portal booking form that may prefill client info.
**Acceptance:** Prefill fields, creates booking and sends confirmation.

**Design**

```
Task: Design New Booking (C10)
Deliverable: prefilled form mock and availability check UI.
```

**Frontend**

```
Task: Implement New Booking (C10)
Deliverable: form POST to /api/v1/bookings/ with prefilling and success redirect.
```

**Backend**

```
Task: Booking create for client (C10)
Deliverable: create booking referencing client account and return booking token.
```

**Testing**

```
Task: Test New Booking (C10)
Deliverable: end-to-end booking tests and prefill verification.
```

---

## C11 — Reschedule / Cancel Booking Flow

**Description:** Client request for reschedule or cancel with confirmation.
**Acceptance:** Creates reschedule request and notifies admin.

**Design**

```
Task: Design Reschedule Flow (C11)
Deliverable: confirm modal mock and reason input UI.
```

**Frontend**

```
Task: Implement Reschedule/Cancel (C11)
Deliverable: request form to /api/v1/bookings/{id}/reschedule/ or /cancel/.
```

**Backend**

```
Task: Reschedule & cancel endpoints (C11)
Deliverable: create a RescheduleRequest model and admin notification endpoint.
```

**Testing**

```
Task: Test Reschedule Flow (C11)
Deliverable: request creation tests and status change assertions.
```

---

## C12 — Service History

**Description:** Past services, reports, attached documents.
**Acceptance:** Downloadable service reports; filters by date.

**Design**

```
Task: Design Service History (C12)
Deliverable: list layout with download actions and filter UI.
```

**Frontend**

```
Task: Implement Service History (C12)
Deliverable: client view listing past services and report download links.
```

**Backend**

```
Task: Service history endpoint (C12)
Deliverable: endpoint returning past bookings with attachments.
```

**Testing**

```
Task: Test Service History (C12)
Deliverable: data integrity tests and attachment access tests.
```

---

## C13 — Quotations Overview (Client)

**Description:** List of quotations with status.
**Acceptance:** Accept/reject actions call tokenized endpoints.

**Design**

```
Task: Design Quotations Overview (C13)
Deliverable: list mock with status badges and accept/reject buttons.
```

**Frontend**

```
Task: Implement Quotations Overview (C13)
Deliverable: list fetching /api/v1/quotations/?client=me and handling accept/reject flows.
```

**Backend**

```
Task: Quotations API for client (C13)
Deliverable: ensure tokenized accept/reject endpoints and email hooks.
```

**Testing**

```
Task: Test Quotations (C13)
Deliverable: accept token tests and status update verification.
```

---

## C14 — Quotation Detail Page (Client)

**Description:** Detailed quote breakdown with PDF download and accept/reject.
**Acceptance:** Accept triggers status update and notifications.

**Design**

```
Task: Design Quotation Detail (C14)
Deliverable: breakdown layout, line items, totals, action CTA placement.
```

**Frontend**

```
Task: Implement Quotation Detail (C14)
Deliverable: render quote, PDF link, accept/reject UI calling tokenized endpoints.
```

**Backend**

```
Task: Quotation detail endpoints (C14)
Deliverable: serve quote data and process accept/reject with audit.
```

**Testing**

```
Task: Test Quotation Detail (C14)
Deliverable: PDF access test and accept/reject workflow tests.
```

---

## C15 — Request New Quotation (Client)

**Description:** Client form to request a new tailored quotation within portal.
**Acceptance:** Creates inquiry under client and notifies admin.

**Design**

```
Task: Design Request Quotation (C15)
Deliverable: request form mock with service selection and attachments.
```

**Frontend**

```
Task: Implement Request Quotation (C15)
Deliverable: client form -> POST /api/v1/inquiries/ with client reference.
```

**Backend**

```
Task: Client inquiry creation (C15)
Deliverable: create Inquiry linked to client, and admin notification.
```

**Testing**

```
Task: Test Request Quotation (C15)
Deliverable: create test and admin notification simulation.
```

---

## C16 — Invoices Overview (Client)

**Description:** List invoices with status and download/pay links.
**Acceptance:** Download PDF, mark paid (mock), show due dates.

**Design**

```
Task: Design Invoices Overview (C16)
Deliverable: list mock with status colors and action buttons.
```

**Frontend**

```
Task: Implement Invoices Overview (C16)
Deliverable: list and filters, download link, pay button placeholder.
```

**Backend**

```
Task: Invoice endpoints (C16)
Deliverable: invoice model, list endpoint, PDF link generation.
```

**Testing**

```
Task: Test Invoices (C16)
Deliverable: retrieval and PDF test.
```

---

## C17 — Invoice Detail (Client)

**Description:** View and download individual invoice; pay link placeholder.
**Acceptance:** PDF correct and data accurate.

**Design**

```
Task: Design Invoice Detail (C17)
Deliverable: invoice layout mock and download CTA.
```

**Frontend**

```
Task: Implement Invoice Detail (C17)
Deliverable: detail template with PDF link and payment CTA placeholder.
```

**Backend**

```
Task: Invoice detail & PDF (C17)
Deliverable: endpoint produce invoice PDF and detail data.
```

**Testing**

```
Task: Test Invoice Detail (C17)
Deliverable: PDF content validation and link tests.
```

---

## C18 — Support Center (KB)

**Description:** Knowledge base for self-help with search.
**Acceptance:** Search works and articles editable in CMS.

**Design**

```
Task: Design Support Center (C18)
Deliverable: KB list with categories and search UI mock.
```

**Frontend**

```
Task: Implement Support Center (C18)
Deliverable: KB listing and search with article detail pages.
```

**Backend**

```
Task: KB model & API (C18)
Deliverable: articles model, search endpoint, category tagging.
```

**Testing**

```
Task: Test Support Center (C18)
Deliverable: search tests and article render tests.
```

---

## C19 — Submit Support Ticket (Client)

**Description:** Create ticket with attachments and urgency selection.
**Acceptance:** Ticket created, admin notified, ticket appears in client ticket list.

**Design**

```
Task: Design Submit Ticket (C19)
Deliverable: multi-step ticket creation mock and file upload UX.
```

**Frontend**

```
Task: Implement Submit Ticket (C19)
Deliverable: form POST to /api/v1/tickets/ and attachment upload handling.
```

**Backend**

```
Task: Ticket model & endpoints (C19)
Deliverable: create ticket, store attachments, notify assigned support staff.
```

**Testing**

```
Task: Test Submit Ticket (C19)
Deliverable: create ticket tests and attachment tests.
```

---

## C20 — Ticket Status & Chat

**Description:** View ticket status and chat inside ticket; attachments supported.
**Acceptance:** Chat messages stored and displayed, file attachments downloadable.

**Design**

```
Task: Design Ticket Status & Chat (C20)
Deliverable: chat UI mock and message input with attachment.
```

**Frontend**

```
Task: Implement Ticket Chat (C20)
Deliverable: chat UI for ticket with polling/websocket placeholder, upload support.
```

**Backend**

```
Task: Ticket messages endpoints (C20)
Deliverable: message model, endpoints to send/receive, attachment handling.
```

**Testing**

```
Task: Test Ticket Chat (C20)
Deliverable: message create/retrieve tests and attachment integrity tests.
```

---

# How to run these prompts automatically

1. Feed each prompt to your Orchestrator Agent which will: create issue/task in tracker, create branch `feature/<task-id>`, and dispatch to target agent with the prompt text.
2. Ensure agents return PR URLs, test artifacts, and acceptance evidence.
3. Use the QA Agent to run the combined acceptance checklist for each page before merge.

---

If you want, I can:

* Export these as a **JSON backlog** ready to import into Jira/GitHub Issues.
* Generate **GitHub Actions** PR templates and issue templates for each task automatically.
* Produce **branch names and PR descriptions** for each task pre-filled.

Which next step would you like?
