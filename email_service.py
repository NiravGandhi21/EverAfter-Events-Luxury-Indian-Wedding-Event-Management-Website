import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config
import models

def send_login_notification(recipient_email, is_valid=True, user_name="Valued Guest", ip_address="127.0.0.1"):
    """
    Mandatory PBL Task 4: Automated SMTP email notification during login.
    - If credentials are valid: sends success confirmation to user with timestamp & security tips.
    - If credentials are invalid: sends security alert to configured admin/security inbox.
    - Permanently logs every dispatched email into the SQLite `email_logs` table for viva evaluation.
    - Gracefully handles connection timeouts and offline states so user authentication flow is never blocked.
    """
    now_str = datetime.now().strftime("%B %d, %Y at %I:%M %p IST")
    
    msg = MIMEMultipart("alternative")
    msg["From"] = Config.MAIL_DEFAULT_SENDER
    
    if is_valid:
        msg["To"] = recipient_email
        msg["Subject"] = "EverAfter Events — Security Alert: Successful Account Login"
        
        text_body = f"""Dear {user_name},

This is an automated security notification from EverAfter Events.

Your account was successfully accessed on:
Date & Time: {now_str}
Client IP: {ip_address}

If you initiated this session, no further action is required.
If you did not perform this login, please contact our security team immediately at {Config.ADMIN_SECURITY_EMAIL}.

Warm regards,
EverAfter Events & Celebrations
Where your forever begins.
"""
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{ font-family: 'DM Sans', Arial, sans-serif; background-color: #f3f0ea; margin: 0; padding: 20px; color: #272320; }}
            .container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }}
            .header {{ background-color: #272725; color: #f3f0ea; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-family: Georgia, serif; font-size: 26px; font-weight: normal; letter-spacing: -0.02em; }}
            .header p {{ margin: 6px 0 0; font-size: 11px; text-transform: uppercase; letter-spacing: 0.18em; color: #bd9a86; }}
            .body {{ padding: 35px 30px; line-height: 1.6; font-size: 14px; color: #4a4541; }}
            .badge-success {{ display: inline-block; background-color: #e8f5e9; color: #2e7d32; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 18px; }}
            .meta-box {{ background-color: #f8f6f2; border-left: 3px solid #9a7966; padding: 15px 20px; margin: 20px 0; border-radius: 0 6px 6px 0; }}
            .meta-box p {{ margin: 5px 0; font-size: 13px; color: #5c5550; }}
            .footer {{ background-color: #f3f0ea; padding: 20px; text-align: center; font-size: 11px; color: #8a827b; border-top: 1px solid #e5dfd7; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>Ever<em>After</em></h1>
              <p>Events & Celebrations</p>
            </div>
            <div class="body">
              <span class="badge-success">&#10003; Login Confirmed</span>
              <p>Hello <strong>{user_name}</strong>,</p>
              <p>We are writing to confirm that a successful login to your EverAfter Events portal was registered.</p>
              <div class="meta-box">
                <p><strong>Date & Time:</strong> {now_str}</p>
                <p><strong>Client Address:</strong> {ip_address}</p>
                <p><strong>Device Status:</strong> Verified Session</p>
              </div>
              <p>If this was you, you can safely disregard this email. If you did not sign in at this time, please notify our concierge team immediately.</p>
            </div>
            <div class="footer">
              &copy; 2026 EverAfter Events. All rights reserved.<br>
              PBL Python Framework Viva Demonstration | ITM SLS BU
            </div>
          </div>
        </body>
        </html>
        """
    else:
        # Invalid login alert to admin/security
        msg["To"] = Config.ADMIN_SECURITY_EMAIL
        msg["Subject"] = f"EverAfter Security Alert — Failed Login Attempt for {recipient_email}"
        
        text_body = f"""Security Alert: A failed login attempt was detected.

Target Email Attempted: {recipient_email}
Date & Time: {now_str}
Client IP: {ip_address}

The login attempt failed due to invalid credentials.
"""
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body {{ font-family: 'DM Sans', Arial, sans-serif; background-color: #f3f0ea; margin: 0; padding: 20px; color: #272320; }}
            .container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; }}
            .header {{ background-color: #3b2222; color: #f3f0ea; padding: 25px; text-align: center; }}
            .badge-danger {{ display: inline-block; background-color: #ffebee; color: #c62828; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
            .body {{ padding: 30px; font-size: 14px; color: #4a4541; }}
            .meta-box {{ background-color: #fdf5f5; border-left: 3px solid #d32f2f; padding: 15px; margin: 15px 0; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h2 style="margin:0; font-family: Georgia, serif;">Security Monitoring Alert</h2>
            </div>
            <div class="body">
              <span class="badge-danger">&#9888; Failed Login Attempt</span>
              <p>A login attempt failed with incorrect credentials on the EverAfter Events portal.</p>
              <div class="meta-box">
                <p><strong>Target Email:</strong> {recipient_email}</p>
                <p><strong>Attempt Timestamp:</strong> {now_str}</p>
                <p><strong>Origin IP:</strong> {ip_address}</p>
              </div>
              <p>This event has been logged for security auditing and university viva evaluation.</p>
            </div>
          </div>
        </body>
        </html>
        """
        
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    
    # 1. Attempt SMTP network delivery
    smtp_success = False
    error_detail = ""
    
    if Config.SMTP_USERNAME and Config.SMTP_PASSWORD and Config.SMTP_PASSWORD != "your_app_password_here":
        try:
            # First attempt TLS on configured port (default 587)
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=5) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.sendmail(Config.MAIL_DEFAULT_SENDER, [msg["To"]], msg.as_string())
            smtp_success = True
            print(f"[SMTP SUCCESS] Live email delivered to {msg['To']}")
        except Exception as e1:
            # Fallback attempt port 465 SSL if port 587 had issues
            try:
                with smtplib.SMTP_SSL(Config.SMTP_SERVER, 465, timeout=5) as server_ssl:
                    server_ssl.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                    server_ssl.sendmail(Config.MAIL_DEFAULT_SENDER, [msg["To"]], msg.as_string())
                smtp_success = True
                print(f"[SMTP SSL SUCCESS] Live email delivered to {msg['To']}")
            except Exception as e2:
                error_detail = f"TLS Error: {e1} | SSL Error: {e2}"
                print(f"[SMTP DISPATCH WARNING] Live SMTP delivery failed: {error_detail}")
    else:
        error_detail = "SMTP credentials not configured in .env (running in audit simulation mode)."

    # 2. Record permanent email audit log in SQLite for academic viva inspection
    status = "sent" if smtp_success else "logged_locally"
    try:
        models.log_email(
            recipient=msg["To"],
            subject=msg["Subject"],
            body_text=text_body,
            body_html=html_body,
            status=status,
            error_message=error_detail if not smtp_success else None
        )
    except Exception as log_err:
        print(f"[LOG ERROR] Could not log email to SQLite: {log_err}")

    if smtp_success:
        return True, f"Security confirmation email sent to {msg['To']}."
    else:
        return False, f"Email notification recorded in SQLite security log (Audit Status: {status}). To deliver live to your Gmail inbox, update SMTP_USERNAME and SMTP_PASSWORD in .env."
