Alright ✅ — I’ll prepare a **comprehensive Product Requirements Document (PRD)** for the **Global Cool-Light E.A LTD Website, Admin Portal & Client Portal**.

This PRD will fully describe the **vision**, **goals**, **functional requirements**, **non-functional requirements**, **technical constraints**, **user stories**, and **acceptance criteria** for the entire 70-page system.

---

# **Product Requirements Document (PRD)**

**Project Name:** Global Cool-Light E.A LTD Digital Platform
**Document Version:** v1.0
**Date:** 3rd September 2025
**Author:** \[Your Name]
**Status:** Draft

---

## **1. Executive Summary**

Global Cool-Light E.A LTD requires a **comprehensive digital platform** that integrates a **public website**, **admin portal**, and **client portal** into a single ecosystem.
The platform will:

* Establish a strong **online presence**
* Provide **HVAC service booking** and **quotation management**
* Enable **portfolio showcasing**
* Enhance **customer engagement**
* Provide **business analytics and reporting**
* Streamline internal and client-facing operations.

**Technology Stack**

* **Backend:** Django 5 (Monolithic) + DRF
* **Frontend:** Next.js 15 + TailwindCSS + TypeScript
* **Database:** PostgreSQL (Production) / SQLite (Development)
* **Deployment:** DigitalOcean + Nginx + Gunicorn + SSL
* **Total Pages:** 70

  * Public Website → **20 pages**
  * Admin Portal → **30 pages**
  * Client Portal → **20 pages**

---

## **2. Goals & Objectives**

### **2.1 Primary Goals**

* Build a **modern, scalable** HVAC business platform
* Streamline **service booking and quotations**
* Provide **client self-service features**
* Enable **real-time business analytics**
* Showcase **company portfolio & expertise**
* Improve **customer acquisition and retention**

### **2.2 Success Metrics**

| Metric                  | Target           |
| ----------------------- | ---------------- |
| Service bookings online | +70% in 6 months |
| Quotation turnaround    | < 24 hours       |
| Customer satisfaction   | ≥ 90%            |
| Website uptime          | 99.9% SLA        |
| Page load speed         | < 3 seconds      |

---

## **3. Scope**

### **3.1 In Scope**

* **Public Website**

  * HVAC services, portfolio, blog, company profile, contact forms
* **Admin Portal**

  * Dashboard, analytics, booking management, quotation approvals, content management
* **Client Portal**

  * Service booking, invoice tracking, quotation requests, account profile
* **Integrated Booking System**
* **Analytics Dashboard**
* **Email & Notification Engine**
* **Basic SEO Optimization**

### **3.2 Out of Scope**

* Native mobile apps (future phase)
* Advanced CRM system
* Multilingual content support
* Payment gateway integrations (future enhancement)

---

## **4. User Personas**

### **4.1 Public Users**

* Browse HVAC services, portfolio, and contact company
* Submit inquiries and book services

### **4.2 Clients**

* Existing customers with accounts
* Manage bookings, invoices, quotations, and profiles

### **4.3 Admins / Staff**

* Manage portfolio, bookings, quotations, and analytics
* Respond to client inquiries
* Configure services and content

---

## **5. Functional Requirements**

### **5.1 Public Website (20 Pages)**

| Page              | Features                                                  |
| ----------------- | --------------------------------------------------------- |
| Home              | Hero banner, services highlights, portfolio preview, CTAs |
| About Us          | Mission, vision, team, certifications                     |
| Services          | List of HVAC services with details                        |
| Service Details   | Specifications, pricing, booking                          |
| Portfolio         | Project gallery, filters, case studies                    |
| Project Details   | Before/after images, success metrics                      |
| Booking Page      | Service booking form with calendar                        |
| Quotation Request | Online quotation submission                               |
| Contact Us        | Contact form, map integration, social links               |
| Blog              | HVAC tips, company updates                                |
| Blog Details      | Article page with SEO                                     |
| FAQs              | Customer support questions                                |
| Testimonials      | Client feedback                                           |
| Careers           | Job postings and applications                             |
| Privacy Policy    | Compliance page                                           |
| Terms of Service  | Legal page                                                |
| Sitemap           | SEO-oriented index                                        |
| 404 Page          | Custom error page                                         |
| Search Results    | Dynamic search for content                                |
| Live Chat         | AI-powered chat widget                                    |

---

### **5.2 Admin Portal (30 Pages)**

**Modules:**

* **Dashboard** → KPIs, traffic stats, bookings analytics
* **Bookings Management** → Approve, reject, update bookings
* **Quotations Management** → Create, edit, send, track approvals
* **Portfolio Management** → Upload images, add project details
* **Services Management** → CRUD operations for HVAC services
* **Analytics Dashboard** → Booking trends, revenue stats, conversions
* **Content Management** → Blog, testimonials, FAQs, careers
* **User Management** → Manage admins, clients, and roles
* **System Settings** → Notifications, email templates, backups

---

### **5.3 Client Portal (20 Pages)**

**Modules:**

* **Dashboard** → Overview of active services & invoices
* **Book a Service** → Booking calendar with service selection
* **Quotation Requests** → Request, view, and download quotations
* **Invoices** → View, download, and track payment statuses
* **Profile Management** → Update contact details, passwords
* **Support Center** → Submit tickets and view responses
* **Notifications** → Track real-time updates and reminders

---

## **6. Non-Functional Requirements**

| Requirement         | Target                                     |
| ------------------- | ------------------------------------------ |
| **Performance**     | Page load < 3 sec, API response < 500ms    |
| **Scalability**     | Support up to 10,000 concurrent users      |
| **Security**        | HTTPS, CSRF, XSS, SQL Injection prevention |
| **SEO**             | Google PageSpeed score > 90                |
| **Accessibility**   | WCAG 2.1 AA compliance                     |
| **Reliability**     | 99.9% uptime                               |
| **Maintainability** | Modular monolithic architecture            |
| **Backup Policy**   | Daily backups, 30-day retention            |

---

## **7. API Requirements**

* **Authentication**

  * `POST /api/auth/register`
  * `POST /api/auth/login`
  * `GET /api/auth/profile`
* **Bookings**

  * `POST /api/bookings/`
  * `GET /api/bookings/<id>/`
* **Quotations**

  * `POST /api/quotations/`
  * `GET /api/quotations/<id>/`
* **Portfolio**

  * `GET /api/projects/`
  * `POST /api/projects/`
* **Analytics**

  * `GET /api/admin/analytics/`

---

## **8. Acceptance Criteria**

* **Website**: All 20 public pages must load under **3 seconds**.
* **Admin Portal**: Bookings, quotations, portfolio, and analytics must work without errors.
* **Client Portal**: Clients can book services, request quotations, and download invoices.
* **Security**: All endpoints secured with JWT + HTTPS.
* **SEO**: Google Lighthouse score ≥ 90.

---

## **9. Risks & Mitigation**

| Risk                 | Impact | Mitigation                                            |
| -------------------- | ------ | ----------------------------------------------------- |
| Slow booking flows   | High   | Optimize DB & caching                                 |
| SEO underperformance | Medium | Dedicated SEO testing                                 |
| Security breaches    | High   | Apply Django’s built-in security, penetration testing |
| Downtime             | High   | Load balancing + backups                              |

---

## **10. Deliverables**

* ✅ 70-page website, admin portal, and client portal
* ✅ API documentation
* ✅ Database schema
* ✅ Admin credentials
* ✅ Deployment pipeline
* ✅ SEO setup
* ✅ Training + 30 days support

---

Do you want me to now **prepare a full System Requirements Specification (SRS)** that breaks down **every API, database entity, and data flow** for all 70 pages?
It’ll make development smoother and align frontend + backend teams. Should I proceed?
