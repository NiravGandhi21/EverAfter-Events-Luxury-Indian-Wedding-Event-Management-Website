import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Pure Python .env loader (zero external dependencies required)
env_path = BASE_DIR / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "everafter-luxury-secret-key-2026")
    
    # Database - Supports local instance and Vercel/Render serverless ephemeral paths
    if os.getenv("VERCEL"):
        DATABASE_PATH = Path("/tmp") / "everafter.db"
    else:
        DATABASE_PATH = BASE_DIR / "instance" / "everafter.db"
    
    # SMTP Email Settings (Task 4)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "EverAfter Events <hello@everafter.events>")
    ADMIN_SECURITY_EMAIL = os.getenv("ADMIN_SECURITY_EMAIL", "security@everafter.events")
    
    # Razorpay Payment Gateway (Task 5)
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_60v2W0km5tB9fH")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "test_secret_everafter_2026")
    RAZORPAY_CURRENCY = os.getenv("RAZORPAY_CURRENCY", "INR")
    
    # Session Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
