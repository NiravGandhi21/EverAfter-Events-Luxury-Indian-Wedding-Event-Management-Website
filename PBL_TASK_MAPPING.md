# PBL Task-to-Code Mapping Document
**EverAfter Events — Luxury Wedding & Event Management System**  
**University Examination Reference:** B.Tech Semester-5, Winter-2026 | ITM SLS BU

This document details the exact file locations, function names, routes, and database operations implementing each of the five mandatory PBL tasks.

---

## Task 1: Website Integration Using Flask
*Integrate all web pages in the template using Python Flask. Create appropriate Flask routes to navigate between all the pages.*

### Implementation Details:
* **Master Layout Template:** [`templates/layout.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/layout.html)
  * Implements Jinja2 template inheritance with `{% block content %}` and `{% block scripts %}`.
  * Shared header with EverAfter wordmark, navigation links, session authentication badge, and mobile drawer.
  * Shared footer with studio branding, quick links, and viva copyright notice.
  * Global flash messaging toast container.
* **Child Templates:**
  * [`templates/home.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/home.html) (`GET /`)
  * [`templates/about.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/about.html) (`GET /about`)
  * [`templates/services.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/services.html) (`GET /services`)
  * [`templates/gallery.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/gallery.html) (`GET /gallery`)
  * [`templates/contact.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/contact.html) (`GET /contact`, `POST /contact`)
  * [`templates/blog.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/blog.html) (`GET /blog`)
  * [`templates/blog_detail.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/blog_detail.html) (`GET /blog/<slug>`, `POST /blog/<slug>/comment`)
* **Flask Controller:** [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py) lines 36-120.
* **Static Assets:** [`static/css/everafter.css`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/static/css/everafter.css) and [`static/js/everafter.js`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/static/js/everafter.js) linked using `url_for('static', filename=...)`.

---

## Task 2: Login and Registration Pages
*Using the provided Contact page as a reference, design and develop separate Login and Registration pages with appropriate form fields and user-friendly interfaces.*

### Implementation Details:
* **Stylistic Model:** The Contact card (`.form-card` in [`templates/contact.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/contact.html)) provides the styling reference.
* **Separate Registration Page:** [`templates/register.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/register.html)
  * Form Fields: Full Name, Email, Mobile (10 digits), City, Password, Confirm Password.
  * Route: `GET /register`, `POST /register` in [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  * Server-side Validation: Missing field checks, mobile digit check (`len(mobile) == 10`), password confirmation check, and duplicate email prevention.
  * Password Security: Password is encrypted using `werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256')` in [`models.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/models.py).
* **Separate Login Page:** [`templates/login.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/login.html)
  * Form Fields: Email Address, Password, Remember Me checkbox.
  * Route: `GET /login`, `POST /login` in [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  * Verification: `werkzeug.security.check_password_hash` in `models.verify_user_credentials()`.
  * Quick-Fill Helper: Displays recent registered accounts for fast demonstration during the viva.

---

## Task 3: Registration Data Display
*When a user submits the Registration form, the entered data must be processed and displayed on the Home page.*

### Implementation Details:
* **Registration Submission Handler:** `register()` function in [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  1. Validates submitted form fields.
  2. Calls `models.create_user(full_name, email, mobile, city, password)`.
  3. Inserts record into SQLite `users` table via parameterized query.
  4. Stores registered customer's identity in `session`.
  5. Sets `session['just_registered'] = True`.
  6. Flashes registration confirmation message.
  7. Redirects user to `url_for('home') + '#registration-banner'`.
* **Homepage Display Banner:** [`templates/home.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/home.html) lines 25-58.
  * Conditionally renders when `registered_user` or `session.get('user_id')` exists.
  * Displays:
    * Client Full Name (`registered_user.full_name`)
    * Registered Email (`registered_user.email`)
    * Mobile Number (`registered_user.mobile`)
    * City / Preferred Destination (`registered_user.city`)
    * Database Verification Status (`Active Account`)
  * Styled in the EverAfter champagne/sand palette (`.reg-welcome-banner`).

---

## Task 4: Email Notification During Login
*Implement an email notification system during login. Send an appropriate email message to the registered recipient based on whether the login credentials are valid or invalid.*

### Implementation Details:
* **Dedicated Email Module:** [`email_service.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/email_service.py) -> `send_login_notification()`
* **Configuration:** Loaded from [`config.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/config.py) and [`.env`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/.env).
  * `SMTP_SERVER=smtp.gmail.com`
  * `SMTP_PORT=587`
  * `SMTP_USERNAME`, `SMTP_PASSWORD`
  * `ADMIN_SECURITY_EMAIL=security@everafter.events`
* **Valid Login Workflow:**
  * Triggered in `login()` inside [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  * Sends an HTML + plain-text security alert directly to the logged-in user's email.
  * Includes customer name, login timestamp, client IP address, and security guidance.
* **Invalid Login Workflow:**
  * When invalid password or non-existent email is submitted, sends an alert email to `ADMIN_SECURITY_EMAIL`.
  * Public UI displays a generic security error message to prevent account enumeration.
* **Resilience & Fallback:** Wrapped in `try...except` with a 5-second socket timeout. If SMTP is offline or credentials are not configured, the login is not blocked; it falls back to simulation logging.

---

## Task 5: Payment Gateway Integration Demonstration
*Create a separate page to demonstrate the integration of a payment gateway. The page should illustrate the payment process, including payment initiation and the appropriate success or failure response.*

### Implementation Details:
* **Dedicated Payment Portal:** [`templates/payment.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/payment.html) (`GET /payment`)
  * Package Tiers: Essential Package (₹500 test fee), Signature Heritage Package (₹1,500 test fee), Royal Destination Package (₹3,000 test fee).
  * Pre-fills client name, email, and mobile from session.
* **Order Creation Endpoint:** `POST /payment/create-order` in [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  * Creates an order record in SQLite `payments` table with status `'created'`.
  * Returns JSON containing `order_id`, `amount_paise`, `currency`, and `key_id`.
* **Client Checkout Script:** `initiateRazorpayPayment()` in [`static/js/everafter.js`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/static/js/everafter.js).
  * Opens the official Razorpay Checkout modal in test mode.
* **Server-Side Signature Verification:** `POST /payment/verify` in [`app.py`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/app.py).
  * Computes expected HMAC-SHA256 signature using Python's standard `hmac` and `hashlib` modules:
    `hmac.new(Config.RAZORPAY_KEY_SECRET, f"{order_id}|{payment_id}", hashlib.sha256).hexdigest()`
  * Verifies received signature.
  * Updates SQLite record to `'success'` or `'failed'`.
* **Success & Failure Views:**
  * [`templates/payment_success.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/payment_success.html) (`GET /payment/success`)
  * [`templates/payment_failure.html`](file:///C:/Users/Gandhi%20Nirav%20P/Downloads/project-bolt-sb1-wjop5a3y/templates/payment_failure.html) (`GET /payment/failure`)
