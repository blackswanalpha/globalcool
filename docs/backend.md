Alright ✅ — I'll prepare a **comprehensive Backend Design Document** for the **Global Cool-Light E.A LTD** platform, covering the **Public Website**, **Admin Portal**, and **Client Portal**.
This document will define the **backend architecture**, **API design**, **database schema**, **microservices/monolithic strategy**, **business logic workflows**, **security measures**, and **integration plans**.

---

# **Backend Design Document**

**Project:** Global Cool-Light E.A LTD — HVAC Portfolio & Management Platform
**Technology:** **Django 5+** (Monolithic Architecture)
**Database:** PostgreSQL (Production) + SQLite (Development)
**API:** Django REST Framework (DRF)
**Deployment:** DigitalOcean Droplet + Nginx + Gunicorn + SSL
**Total Pages:** 70 (Public 20 + Admin 30 + Client 20)

---

## **1. Overview**

The backend is designed using **Django 5+** in a **monolithic architecture** to ensure high maintainability, better security, and easy integration between modules. It powers three main environments:

* **Public Website (20 pages)** → Portfolio, services, bookings, inquiries, content pages.
* **Admin Portal (30 pages)** → System management, analytics, bookings, quotes, portfolio.
* **Client Portal (20 pages)** → Service tracking, invoices, quotes, account details.

---

## **2. Architecture Overview**

### **2.1 High-Level Architecture**

```
┌───────────────────────────────────────────┐
│            Public Website (UI)            │
│    React / Next.js + Tailwind CSS         │
└───────────────────────────────────────────┘
              │  (REST API)
              ▼
┌───────────────────────────────────────────┐
│        Django 5 Monolithic Backend        │
│───────────────────────────────────────────│
│  Authentication & Authorization Module    │
│  Booking & Quotation Management          │
│  Portfolio & Services Module             │
│  Client Management                       │
│  Analytics & Reporting                  │
│  Notification & Email Engine            │
└───────────────────────────────────────────┘
              │
              ▼
┌───────────────────────────────────────────┐
│             PostgreSQL Database           │
│  Relational DB with optimized indexing   │
└───────────────────────────────────────────┘
              │
              ▼
┌───────────────────────────────────────────┐
│       External Integrations (Optional)    │
│  Google Analytics | Email API | Maps API  │
└───────────────────────────────────────────┘
```

---

## **3. Module Breakdown**

### **3.1 Authentication & Authorization**

* **Features**

  * JWT-based authentication (DRF SimpleJWT)
  * Role-based access (Public, Admin, Client)
  * Social login (optional future extension)
  * Two-factor authentication (optional)
* **Tables**

  * `users`
  * `roles`
  * `permissions`
  * `sessions`

---

### **3.2 Booking & Quotation Management**

* **Features**

  * Online service booking
  * Dynamic time slot availability
  * Quotation generation (PDF)
  * Booking status updates
  * Customer notifications (Email/SMS)
* **Tables**

  * `bookings`
  * `services`
  * `quotation_requests`
  * `quotations`
* **APIs**

  * `POST /api/bookings/`
  * `GET /api/bookings/<id>/`
  * `POST /api/quotations/`
  * `GET /api/quotations/<id>/`

---

### **3.3 Services & Portfolio Management**

* **Features**

  * Full service catalog
  * Image uploads for HVAC projects
  * Portfolio categorization
  * Filtering and sorting for projects
* **Tables**

  * `services`
  * `projects`
  * `project_images`
* **APIs**

  * `GET /api/services/`
  * `POST /api/projects/`
  * `GET /api/projects/<id>/`

---

### **3.4 Inquiry Management**

* **Features**

  * Inquiry forms with customer details
  * CRM-lite customer follow-up system
  * Quote requests auto-routing to admins
* **Tables**

  * `inquiries`
  * `inquiry_responses`
* **APIs**

  * `POST /api/inquiries/`
  * `GET /api/inquiries/<id>/`

---

### **3.5 Analytics & Reporting**

* **Features**

  * Website traffic analysis (Google Analytics API)
  * Booking conversion tracking
  * Quotation acceptance/rejection statistics
  * Dashboard with visual KPIs
* **Tables**

  * `analytics`
  * `kpis`
* **APIs**

  * `GET /api/analytics/dashboard/`
  * `GET /api/analytics/reports/`

---

### **3.6 Notifications & Email Engine**

* **Features**

  * Email templates for booking confirmations, quotations, invoices
  * Automated reminders
  * Bulk mailing system
* **Tables**

  * `email_templates`
  * `notifications`
* **Tools**

  * Django Email Backend + Celery + Redis (optional)
* **APIs**

  * `POST /api/notifications/send/`

---

## **4. Database Schema (Key Tables)**

### **Users Table**

| Field       | Type     | Description             |
| ----------- | -------- | ----------------------- |
| id          | UUID     | Primary key             |
| email       | String   | Unique user email       |
| password    | String   | Hashed password         |
| role        | Enum     | Public / Admin / Client |
| is\_active  | Boolean  | Status                  |
| created\_at | DateTime | Creation timestamp      |

---

### **Bookings Table**

| Field       | Type | Description                |
| ----------- | ---- | -------------------------- |
| id          | UUID | Primary key                |
| user\_id    | FK   | References `users`         |
| service\_id | FK   | References `services`      |
| date        | Date | Booking date               |
| status      | Enum | Pending / Confirmed / Done |

---

### **Quotations Table**

| Field       | Type    | Description             |
| ----------- | ------- | ----------------------- |
| id          | UUID    | Primary key             |
| inquiry\_id | FK      | References `inquiries`  |
| amount      | Decimal | Total quotation cost    |
| status      | Enum    | Draft / Sent / Approved |

---

## **5. API Layer**

### **Authentication APIs**

* `POST /api/auth/register`
* `POST /api/auth/login`
* `POST /api/auth/logout`
* `GET /api/auth/profile`

### **Booking APIs**

* `POST /api/bookings/`
* `GET /api/bookings/<id>/`
* `PATCH /api/bookings/<id>/`

### **Quotation APIs**

* `POST /api/quotations/`
* `GET /api/quotations/<id>/`

### **Admin APIs**

* `GET /api/admin/dashboard/`
* `GET /api/admin/users/`

---

## **6. Security Measures**

* **HTTPS** with Let's Encrypt SSL
* CSRF protection
* SQL injection prevention via Django ORM
* XSS prevention via template escaping
* Password hashing using PBKDF2
* Rate-limiting for APIs (DRF Throttling)
* Role-based access control for portals

---

## **7. Deployment Plan**

* **Server:** DigitalOcean Droplet (2GB RAM, 2 vCPUs)
* **Web Server:** Nginx + Gunicorn
* **Database:** PostgreSQL (production), SQLite (dev)
* **CI/CD:** GitHub Actions → Auto deploy on merge
* **SSL:** Let's Encrypt Free SSL
* **Monitoring:** UptimeRobot + Sentry

---

## **8. Scalability Plan**

* Use **PostgreSQL partitioning** for large datasets
* Enable caching using **Redis**
* Introduce **Celery + RabbitMQ** for background tasks
* Optionally refactor into **microservices** later if traffic grows

---

## **9. Deliverables**

* Backend source code (Django project)
* API documentation (Swagger + Redoc)
* Database ER diagram
* Admin credentials & role setup
* Deployment pipeline documentation

---

Do you want me to now **design a full ERD (Entity Relationship Diagram)** and **API schema** to visually map all **70 pages' backend flows**?
It’ll make the document developer-ready. Should I proceed?
