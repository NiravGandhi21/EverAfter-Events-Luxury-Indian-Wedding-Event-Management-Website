# PowerPoint Presentation (PPT) Outline
**Project Title:** EverAfter Events — Luxury Wedding & Event Management System  
**Subject:** PBL Python Framework (B.Tech Semester-5, Winter-2026)  
**Institution:** ITM SLS BU, School of Computer Science, Engineering & Technology, Vadodara  

---

## Slide 1: Title Slide
* **Title:** EverAfter Events — Luxury Wedding & Event Management Portal
* **Subtitle:** Final Practical-Based Learning (PBL) Project Submission using Python Flask
* **Course:** B.Tech Semester-5, Academic Year 2026–2027 (Winter-2026)
* **Department:** School of Computer Science, Engineering & Technology, ITM SLS BU
* **Presented by:** [Student Name(s) & Enrollment Number(s)]
* **Supervised by:** Course Faculty, Python Framework Laboratory

---

## Slide 2: Project Introduction & Problem Statement
* **Background:** Indian luxury weddings require meticulous, multi-day coordination spanning venue logistics, décor styling, vendor management, guest hospitality, and secure client communication.
* **Problem Statement:** Existing event platforms are either generic CMS templates or fragmented into separate tools for inquiry, customer registration, security alerts, and payment verification.
* **Project Vision:** Develop an end-to-end, visually stunning luxury wedding management website with Python Flask, marrying high-fashion editorial aesthetics with robust backend engineering.

---

## Slide 3: Project Objectives & University Task Scope
* Recreate a luxury Bolt AI editorial frontend in native Python Flask + Jinja2.
* Replace synthetic CSS gradient artwork with authentic, high-resolution wedding photography.
* Implement all 5 mandatory university PBL evaluation tasks:
  1. Complete website page integration using Flask routing.
  2. Separate, user-friendly Login and Registration modules.
  3. Real-time registration data display on the Home page.
  4. Automated SMTP email security alerts during login.
  5. Razorpay payment gateway integration in test mode with backend signature verification.

---

## Slide 4: System Architecture & Technology Stack
* **Architecture:** Model-View-Controller (MVC) implemented via Flask blueprints/controllers, Jinja2 views, and SQLite data models.
* **Backend:** Python 3.12, Flask 3.1.3, Werkzeug Security, Python `smtplib`.
* **Frontend:** Jinja2 Template Inheritance (`layout.html`), custom CSS (`everafter.css`), vanilla JavaScript (`everafter.js`), Google Fonts (Playfair Display & DM Sans).
* **Database:** SQLite3 (`everafter.db`) with relational integrity and foreign keys.
* **External APIs:** Razorpay Test Payment Gateway SDK and Google SMTP Mail Server.

---

## Slide 5: Database Schema & Entity Relationships
* **`users` Table:** `id`, `full_name`, `email` (unique), `mobile`, `city`, `password_hash`, `created_at`.
* **`contact_inquiries` Table:** `id`, `name`, `email`, `mobile`, `event_type`, `event_date`, `budget`, `guest_count`, `message`.
* **`payments` Table:** `id`, `user_id`, `order_id`, `payment_id`, `signature`, `package_name`, `amount`, `status`, `created_at`.
* **`blog_posts` Table:** `id`, `title`, `slug`, `category`, `excerpt`, `content`, `image_url`, `author`, `published_at`.
* **`comments` Table:** `id`, `post_id`, `name`, `email`, `comment`, `created_at` (foreign key cascade).

---

## Slide 6: Task 1 & Task 2 Implementation
* **Task 1 — Flask Website Integration:**
  * Master `layout.html` sharing header, navigation, and footer across 12 routes (`/`, `/about`, `/services`, `/gallery`, `/contact`, `/blog`, `/payment`, etc.).
  * Elimination of CSS gradients in favor of 37 locally curated high-resolution wedding photographs.
* **Task 2 — Separate Login & Registration Pages:**
  * Derived from the Contact page card layout.
  * Form validation for mobile numbers (10 digits) and password matching.
  * Werkzeug PBKDF2:SHA256 cryptographic password hashing (zero plain-text passwords).

---

## Slide 7: Task 3 & Task 4 Implementation
* **Task 3 — Registration Data Display on Home Page:**
  * Form processed in Flask -> stored in SQLite -> user session established -> redirected to `/`.
  * Dedicated luxury welcome card displays client's Name, Email, Phone, City, and Verification status.
* **Task 4 — Automated Email Notifications on Login:**
  * **Valid Login:** Dispatches login confirmation email to user with timestamp, client IP, and security advice.
  * **Invalid Login:** Dispatches failed login security alert to system administrator.
  * Fault-tolerant architecture prevents offline socket errors from breaking authentication.

---

## Slide 8: Task 5 — Razorpay Payment Gateway Demonstration
* **Package Tiers:** Essential Wedding Package, Signature Heritage Package, Royal Destination Package.
* **Order Creation:** Client requests order -> Flask creates order and pending record in SQLite (`POST /payment/create-order`).
* **Client Modal:** Razorpay checkout modal opens in test mode.
* **Cryptographic Verification:** Backend verifies `HMAC-SHA256(secret, order_id + "|" + payment_id)`.
* **Status Persistence:** Payment record updated to `'success'` only upon mathematical signature match.

---

## Slide 9: Testing & Verification Results
* **Automated Test Suite:** `test_everafter.py` with 6 comprehensive test cases.
* **Task 1:** All 12 page routes return HTTP 200 OK.
* **Task 2:** Password validation, duplicate email rejection, and PBKDF2 hashing verified.
* **Task 3:** Dynamic Home page registration display confirmed.
* **Task 4:** Valid and invalid login authentication and email triggers verified.
* **Task 5:** Payment order generation and cryptographic verification verified.
* **Result:** 100% test pass rate (`Ran 6 tests in 3.633s — OK`).

---

## Slide 10: Advantages, Limitations & Security Measures
* **Advantages:**
  * Preserves high-end luxury brand identity.
  * Lightweight, starts instantly without complex build steps or node mismatch issues.
  * Strict adherence to academic requirements and security best practices.
* **Security Measures:**
  * Zero hardcoded credentials (all secrets in `.env`).
  * Parameterized SQL queries against SQL injection.
  * XSS prevention through Jinja2 auto-escaping.
* **Limitations:**
  * SQLite is optimal for single-server prototypes; production would use PostgreSQL.
  * Background celery queue recommended for high-volume email dispatch.

---

## Slide 11: Conclusion & Future Scope
* **Conclusion:** EverAfter Events successfully integrates an editorial luxury wedding frontend with a production-grade Python Flask backend, fulfilling all five mandatory university tasks for B.Tech Semester-5.
* **Future Scope:**
  * Interactive 3D mandap venue customizer.
  * SMS notifications via Twilio API.
  * Dedicated vendor bidding portal and multi-currency international billing.
* **Q&A:** Open for examination questions and live system demonstration.
