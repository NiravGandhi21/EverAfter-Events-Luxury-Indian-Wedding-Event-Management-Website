from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

# User Management (Task 2 & 3)
def create_user(full_name, email, mobile, city, password):
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (full_name, email, mobile, city, password_hash)
        VALUES (?, ?, ?, ?, ?)
        """, (full_name.strip(), email.strip().lower(), mobile.strip(), city.strip() if city else '', password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        return get_user_by_id(user_id)
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user_credentials(email, password):
    user = get_user_by_email(email)
    if not user:
        return None
    if check_password_hash(user['password_hash'], password):
        return user
    return None

def get_recent_users(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email, mobile, city, created_at FROM users ORDER BY id DESC LIMIT ?", (limit,))
    users = cursor.fetchall()
    conn.close()
    return users

# Contact Inquiries
def create_contact_inquiry(name, email, mobile, event_type, event_date, budget, guest_count, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO contact_inquiries (name, email, mobile, event_type, event_date, budget, guest_count, message)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name.strip(), email.strip(), mobile.strip(), event_type, event_date, budget, guest_count, message.strip()))
    conn.commit()
    inquiry_id = cursor.lastrowid
    conn.close()
    return inquiry_id

# Payments (Task 5)
def create_payment_order(order_id, package_name, amount, customer_name, customer_email, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO payments (user_id, order_id, package_name, amount, currency, status, customer_name, customer_email)
    VALUES (?, ?, ?, ?, 'INR', 'created', ?, ?)
    """, (user_id, order_id, package_name, amount, customer_name, customer_email))
    conn.commit()
    payment_id = cursor.lastrowid
    conn.close()
    return payment_id

def update_payment_success(order_id, payment_id, signature):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE payments 
    SET payment_id = ?, signature = ?, status = 'success'
    WHERE order_id = ?
    """, (payment_id, signature, order_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def update_payment_failure(order_id, payment_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE payments 
    SET payment_id = ?, status = 'failed'
    WHERE order_id = ?
    """, (payment_id, order_id))
    conn.commit()
    conn.close()

def get_payment_by_order_id(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE order_id = ?", (order_id,))
    payment = cursor.fetchone()
    conn.close()
    return payment

# Blog Posts & Comments
def get_all_blog_posts(category=None, query=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM blog_posts WHERE 1=1"
    params = []
    if category and category.lower() != 'all':
        sql += " AND LOWER(category) = LOWER(?)"
        params.append(category)
    if query:
        sql += " AND (title LIKE ? OR excerpt LIKE ? OR content LIKE ?)"
        q = f"%{query}%"
        params.extend([q, q, q])
    sql += " ORDER BY id DESC"
    cursor.execute(sql, tuple(params))
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_blog_post_by_slug(slug):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blog_posts WHERE slug = ?", (slug,))
    post = cursor.fetchone()
    conn.close()
    return post

def get_comments_for_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY id DESC", (post_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def add_comment_to_post(post_id, name, email, comment):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO comments (post_id, name, email, comment)
    VALUES (?, ?, ?, ?)
    """, (post_id, name.strip(), email.strip(), comment.strip()))
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    return comment_id

# Email Logs (Task 4)
def log_email(recipient, subject, body_text, body_html, status, error_message=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO email_logs (recipient, subject, body_text, body_html, status, error_message)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (recipient.strip(), subject.strip(), body_text, body_html, status, error_message))
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id

def get_recent_emails(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_logs ORDER BY id DESC LIMIT ?", (limit,))
    emails = cursor.fetchall()
    conn.close()
    return emails
