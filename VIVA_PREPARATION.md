# Viva-Voce Preparation Guide
**EverAfter Events — PBL Python Framework Project**  
**Examination Board:** ITM SLS BU, School of Computer Science, Engineering & Technology, Vadodara  
**B.Tech Semester-5, Winter-2026**

---

## 1. Core Architectural & Theoretical Questions

### Q1: Why did you choose Python Flask for this web application?
**Answer:**  
Flask is a lightweight, flexible WSGI micro-framework written in Python. Unlike monolithic frameworks like Django, Flask does not enforce rigid boilerplate; it gives developers complete architectural control over routing, database connectors, and template structures. In EverAfter Events, Flask allows us to maintain a clean separation of concerns between our data models (`models.py`), database layer (`database.py`), configuration (`config.py`), and Jinja2 templates, while offering native integration with Python’s cryptographic (`hmac`, `hashlib`), SMTP (`smtplib`), and SQLite (`sqlite3`) standard libraries.

### Q2: What is Jinja2 and how does template inheritance work in your project?
**Answer:**  
Jinja2 is Flask's default fast, expressive templating engine. In our project, we implemented template inheritance through a master layout file (`templates/layout.html`). The layout defines the HTML boilerplate, Google Fonts, stylesheets, top navigation bar, flash notification container, and site footer. Child templates (such as `home.html`, `payment.html`, `register.html`) declare `{% extends "layout.html" %}` and inject page-specific content within `{% block content %} ... {% endblock %}`. This eliminates HTML duplication and ensures visual consistency across the entire website.

### Q3: How do you handle client sessions and route authentication?
**Answer:**  
Flask manages user sessions through cryptographically signed cookies using the `SECRET_KEY` configured in `.env`. When a user registers or logs in, their identity (`user_id`, `user_name`, `user_email`) is stored in the `session` dictionary. On subsequent HTTP requests, Flask decodes the session cookie and validates the cryptographic signature. In our templates and routes, we check `session.get('user_id')` to dynamically adjust navigation buttons (showing the user's name and Logout link when logged in, or Login and Register when logged out).

---

## 2. PBL Tasks Technical Defense

### Q4: Explain Task 2 — How do you validate and hash user passwords?
**Answer:**  
In `POST /register`, we perform both frontend HTML5 validation and strict backend Python validation:
1. Verify all fields are present and non-empty.
2. Verify that the mobile number contains exactly 10 digits (`len(mobile) == 10 and mobile.isdigit()`).
3. Verify that `password == confirm_password`.
4. Check email uniqueness against the SQLite `users` table (`SELECT * FROM users WHERE email = ?`).
5. For security, we never store plain-text passwords. We hash the password using `werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256')`. This generates a salted, 260,000-iteration PBKDF2 hash using SHA-256. During login, we verify credentials using `check_password_hash(stored_hash, submitted_password)`.

### Q5: Explain Task 3 — How is the registration data processed and displayed on the Home page?
**Answer:**  
When the registration form is submitted:
1. Flask creates the user in SQLite and retrieves the newly inserted user ID.
2. The user's details (`full_name`, `email`, `mobile`, `city`) are set in the `session`.
3. Flask redirects the user to the homepage (`redirect(url_for('home') + '#registration-banner')`).
4. On the `GET /` route, Flask checks `session.get('user_id')` and queries `models.get_user_by_id(user_id)`.
5. In `templates/home.html`, a dedicated luxury customer banner (`.reg-welcome-banner`) is rendered with the client's Name, Email, Mobile Contact, City, and an "Active Account" verification badge.

### Q6: Explain Task 4 — How does the SMTP email notification work during login?
**Answer:**  
In `POST /login`, we verify credentials against SQLite:
- **Valid Login:** If the email and password hash match, we invoke `email_service.send_login_notification(email, is_valid=True, user_name=user['full_name'], ip_address=client_ip)`. This constructs a multipart MIME email (plain-text + responsive HTML) and connects to the SMTP server (e.g. Gmail SMTP on port 587) using `smtplib.SMTP(host, port)`. It invokes `starttls()` to establish an encrypted TLS tunnel, authenticates using environment-configured credentials, and dispatches the security login confirmation to the user.
- **Invalid Login:** If the password does not match or the user does not exist, `is_valid=False` is passed. The service sends an alert to `ADMIN_SECURITY_EMAIL` documenting the target email, timestamp, and client IP address.
- **Fault-Tolerance:** The SMTP call is enclosed in a `try...except` block with a 5-second socket timeout. If the SMTP service is unavailable (e.g. offline examination room), the login flow continues smoothly without crashing, logging a simulated alert.

### Q7: Explain Task 5 — How is the Razorpay payment gateway integrated and verified?
**Answer:**  
We implemented a two-step server-verified payment workflow:
1. **Order Creation (`POST /payment/create-order`):** When the client selects a wedding package on `/payment`, the frontend issues an asynchronous fetch request to Flask. The server creates an order record in the SQLite `payments` table with status `'created'` and returns the `order_id`, `amount_paise`, and `key_id`.
2. **Checkout Modal:** The frontend passes these parameters to `Razorpay(options)` and opens the checkout modal in Test Mode.
3. **Cryptographic Signature Verification (`POST /payment/verify`):** Upon payment authorization, Razorpay returns `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature`. The frontend transmits these to `/payment/verify`.
4. The Flask backend verifies the authenticity of the transaction by computing an HMAC-SHA256 digest:
   $$\text{Expected Signature} = \text{HMAC-SHA256}(\text{Key Secret}, \text{order\_id} + "|" + \text{payment\_id})$$
   We compare the expected signature with the received signature. Only if they match do we update the database status to `'success'`. This prevents client-side tampering or forged success messages.

---

## 3. Database & SQL Questions

### Q8: What database are you using and how do you prevent SQL Injection?
**Answer:**  
We use SQLite3 (`instance/everafter.db`), Python's native relational database engine. To prevent SQL Injection attacks, we strictly use **parameterized queries** with `?` placeholders (e.g. `cursor.execute("SELECT * FROM users WHERE email = ?", (email,))`). We never concatenate user inputs directly into SQL strings. Additionally, foreign key constraints are enabled via `PRAGMA foreign_keys = ON;` in our database connector.

---

## 4. Security Considerations & Best Practices

- **Zero Hardcoded Secrets:** All sensitive credentials (Flask `SECRET_KEY`, SMTP passwords, and Razorpay API keys) are loaded from `.env` using pure Python environment parsing.
- **Cross-Site Scripting (XSS) Prevention:** Jinja2 automatically escapes HTML entities in variables (e.g. `{{ user.full_name }}`).
- **Session Security:** Session cookies are configured with `HTTPOnly=True` and `SameSite=Lax` to prevent client-side JavaScript theft.
- **Timing-Attack Resistance:** Password verification uses `werkzeug.security.check_password_hash`, which performs constant-time comparisons.
