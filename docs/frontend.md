Alright ✅ — I’ll prepare a **comprehensive Frontend Design Document** for the **Global Cool-Light E.A LTD** platform.
This document will define the **design principles**, **UI architecture**, **component library**, **responsive grid system**, **interaction models**, **styling standards**, and **developer handoff guidelines** for building the **Public Website**, **Admin Portal**, and **Client Portal**.

This document will serve as the **single source of truth** for frontend developers and UI/UX designers.

---

# **Frontend Design Document**

**Project:** Global Cool-Light E.A LTD Website & Management Platform
**Pages Covered:** 70 (Public Website: 20, Admin Portal: 30, Client Portal: 20)
**Tech Stack:** Next.js 15 + Tailwind CSS 3 + TypeScript + ShadCN UI + Framer Motion

---

## **1. Project Overview**

The frontend will provide a **modern, responsive, and interactive** interface for **customers**, **admins**, and **clients**. It must be **scalable**, **accessible**, and **optimized for performance**, while integrating seamlessly with the **Django backend APIs**.

---

## **2. Objectives**

* Deliver a **consistent, intuitive, and branded** user experience across all 70 pages.
* Ensure **mobile-first** responsive layouts with **100% device compatibility**.
* Use a **unified component-based design system** for reusable UI elements.
* Integrate **animations, transitions, and micro-interactions** to enhance UX.
* Implement **accessibility standards** (WCAG 2.2 AA).

---

## **3. Frontend Architecture**

### **3.1 Technology Stack**

| Layer         | Technology / Library      | Purpose                                   |
| ------------- | ------------------------- | ----------------------------------------- |
| Framework     | **Next.js 15**            | Routing, server-side rendering (SSR), SEO |
| Styling       | **Tailwind CSS 3**        | Utility-first responsive design           |
| Component Lib | **ShadCN/UI + Radix UI**  | Pre-built accessible components           |
| Animations    | **Framer Motion**         | Page transitions & micro-interactions     |
| State Mgmt    | **React Query + Zustand** | API data fetching & local state control   |
| Forms         | **React Hook Form + Zod** | Form validation and management            |
| Charts        | **Recharts**              | Analytics dashboards (Admin/Client)       |
| Icons         | **Lucide React**          | Consistent scalable vector icons          |

---

### **3.2 Frontend Folder Structure**

```
/frontend
 ├── public/                 # Static assets
 ├── src/
 │    ├── app/               # Next.js App Router
 │    ├── components/        # Reusable UI components
 │    ├── features/          # Feature-based modules (Booking, Quotation, etc.)
 │    ├── layouts/           # Page layouts (Public, Admin, Client)
 │    ├── pages/             # Static marketing pages
 │    ├── hooks/             # Custom React hooks
 │    ├── store/             # Zustand state management
 │    ├── styles/            # Global styles & Tailwind configs
 │    ├── utils/             # Helper functions
 │    └── types/             # TypeScript types
 └── package.json
```

---

## **4. Design System**

### **4.1 Branding**

* **Primary Color:** `#004AAD` → Corporate Blue (HVAC brand identity)
* **Secondary Color:** `#00AEEF` → Cool Light Cyan
* **Accent Color:** `#F8C102` → Highlight & CTA buttons
* **Neutral Colors:** `#111827`, `#6B7280`, `#F3F4F6`

### **4.2 Typography**

| Type      | Font  | Weight  | Use Case          |
| --------- | ----- | ------- | ----------------- |
| Headings  | Inter | 600–800 | Titles & sections |
| Body Text | Inter | 400–500 | Paragraphs        |
| Captions  | Inter | 400     | Labels, tooltips  |

### **4.3 Grid & Spacing**

* **Grid System:** 12-column responsive grid.
* **Breakpoints:**

  * `sm`: 640px → Mobile
  * `md`: 768px → Tablets
  * `lg`: 1024px → Desktop
  * `xl`: 1280px → Large screens
* **Spacing Scale:** Tailwind's `0.5rem` increments.

---

## **5. Components & Patterns**

### **5.1 Reusable Components**

| Component        | Use Case                      | Portal(s)           |
| ---------------- | ----------------------------- | ------------------- |
| Navbar & Sidebar | Navigation                    | Public/Admin/Client |
| Hero Sections    | Landing highlights            | Public              |
| Service Cards    | Show services & pricing       | Public              |
| Booking Forms    | HVAC service scheduling       | Public/Client       |
| Data Tables      | Lists & management dashboards | Admin/Client        |
| Charts & Graphs  | Analytics & KPIs              | Admin/Client        |
| Notifications    | Alerts, toasts, confirmations | All                 |
| Modals & Drawers | Actions & forms               | All                 |

---

## **6. Interaction & Animations**

* **Framer Motion** used for:

  * Smooth **page transitions**.
  * **Hover effects** on cards and buttons.
  * **Collapsible menus** in admin/client portals.
  * **Loading skeletons** and progressive disclosure.
* **Micro-interactions**:

  * Form submission success/failure states.
  * Real-time booking confirmations.
  * Dynamic counters for KPIs.

---

## **7. Accessibility Guidelines**

* WCAG 2.2 AA compliance.
* Proper heading hierarchy (H1 → H6).
* Keyboard navigation support.
* ARIA labels for all components.
* High contrast ratio for readability.

---

## **8. Performance Optimization**

* Image optimization with **Next/Image**.
* Code splitting and lazy loading.
* Prefetching critical routes.
* Tailwind JIT for optimized CSS bundles.
* Caching strategy via **service workers**.

---

## **9. Developer Handoff Guidelines**

* Figma components mapped to React components.
* Design tokens exported to Tailwind config.
* Naming conventions standardized across repo.
* Storybook for documenting components.
* API contract alignment with Django REST backend.

---

## **10. Deliverables**

* 📄 **Frontend Design System** (Figma + Tokens)
* 🎨 **High-Fidelity Mockups** for all 70 pages
* 📦 **Reusable Component Library**
* 🧩 **Interaction Prototypes** (Framer Motion)
* 📘 **Developer Handoff Documentation**

---

Do you want me to **also develop a full Figma UI kit** with **high-fidelity screens** for **all 70 pages** based on this document?
That will give us a **pixel-perfect blueprint** for development. Should I proceed?
