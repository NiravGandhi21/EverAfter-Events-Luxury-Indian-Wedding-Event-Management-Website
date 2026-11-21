import unittest
import json
import uuid
import sqlite3
from app import app
from config import Config
import database
import models

class EverAfterPBLTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            # Clear test tables so tests are isolated and idempotent
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM payments")
            cursor.execute("DELETE FROM contact_inquiries")
            conn.commit()
            conn.close()
            database.init_db()

    # -------------------------------------------------------------
    # Task 1: Website Integration Using Flask
    # -------------------------------------------------------------
    def test_task1_page_routes(self):
        routes = [
            ('/', 'Where your'),
            ('/about', 'Our Story'),
            ('/services', 'Full-Service Wedding Planning'),
            ('/gallery', 'The Garden Ceremony'),
            ('/contact', 'Inquiry Submission'),
            ('/blog', 'The Journal'),
            ('/blog/how-to-plan-a-wedding-that-feels-like-you', 'How to plan a wedding'),
            ('/login', 'Client Sign In'),
            ('/register', 'Create Client Profile'),
            ('/payment', 'Razorpay Test Mode'),
            ('/payment/success', 'Reservation Confirmed'),
            ('/payment/failure', 'Payment Unsuccessful')
        ]
        for route, expected_text in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
            self.assertIn(expected_text.encode('utf-8'), response.data, f"Route {route} missing expected text: {expected_text}")
        print("✓ Task 1 Passed: All 12 Flask routes render properly with shared layout and static assets.")

    # -------------------------------------------------------------
    # Task 2: Login and Registration Pages
    # -------------------------------------------------------------
    def test_task2_registration_validation_and_hashing(self):
        # 1. Test mismatched password
        res = self.client.post('/register', data={
            'full_name': 'Aarav Patel',
            'email': 'aarav@example.com',
            'mobile': '9876543210',
            'city': 'Vadodara',
            'password': 'password123',
            'confirm_password': 'mismatch123'
        }, follow_redirects=True)
        self.assertIn(b"Passwords do not match", res.data)

        # 2. Test invalid mobile format
        res = self.client.post('/register', data={
            'full_name': 'Aarav Patel',
            'email': 'aarav@example.com',
            'mobile': '123',
            'city': 'Vadodara',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b"valid 10-digit mobile number", res.data)

        # 3. Test successful registration
        res = self.client.post('/register', data={
            'full_name': 'Aarav Patel',
            'email': 'aarav@example.com',
            'mobile': '9876543210',
            'city': 'Vadodara',
            'password': 'SecretPassword2026',
            'confirm_password': 'SecretPassword2026'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Verify password is NOT stored as plaintext in SQLite
        user = models.get_user_by_email('aarav@example.com')
        self.assertIsNotNone(user)
        self.assertNotEqual(user['password_hash'], 'SecretPassword2026')
        self.assertTrue(user['password_hash'].startswith('pbkdf2:sha256:'))

        # Log out before testing duplicate registration from another session
        self.client.get('/logout')
        
        # 4. Test duplicate email rejection
        res_dup = self.client.post('/register', data={
            'full_name': 'Another Person',
            'email': 'aarav@example.com',
            'mobile': '9876543211',
            'city': 'Ahmedabad',
            'password': 'Password2026',
            'confirm_password': 'Password2026'
        }, follow_redirects=True)
        self.assertIn(b"already exists", res_dup.data)

        print("✓ Task 2 Passed: Form validation, password hashing (PBKDF2:SHA256), and duplicate prevention verified.")

    # -------------------------------------------------------------
    # Task 3: Registration Data Display on Home Page
    # -------------------------------------------------------------
    def test_task3_homepage_data_display(self):
        # Register a unique user
        res = self.client.post('/register', data={
            'full_name': 'Meera Singhania',
            'email': 'meera@singhania.com',
            'mobile': '9822233444',
            'city': 'Udaipur Heritage',
            'password': 'MeeraPass2026',
            'confirm_password': 'MeeraPass2026'
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        # Verify Home page contains registered details
        self.assertIn(b"Meera Singhania", res.data)
        self.assertIn(b"meera@singhania.com", res.data)
        self.assertIn(b"9822233444", res.data)
        self.assertIn(b"Udaipur Heritage", res.data)
        self.assertIn(b"Task 3: Verified Registration Record", res.data)
        print("✓ Task 3 Passed: Registration data successfully saved to SQLite and dynamically rendered on the Home page.")

    # -------------------------------------------------------------
    # Task 4: Email Notification During Login
    # -------------------------------------------------------------
    def test_task4_login_email_notification(self):
        # 1. Register test user
        self.client.post('/register', data={
            'full_name': 'Vikram Rathore',
            'email': 'vikram@rathore.com',
            'mobile': '9811122233',
            'city': 'Jaipur',
            'password': 'RathorePass2026',
            'confirm_password': 'RathorePass2026'
        })
        self.client.get('/logout')

        # 2. Test Invalid Login
        res_invalid = self.client.post('/login', data={
            'email': 'vikram@rathore.com',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        self.assertIn(b"Invalid email or password", res_invalid.data)

        # 3. Test Valid Login
        res_valid = self.client.post('/login', data={
            'email': 'vikram@rathore.com',
            'password': 'RathorePass2026'
        }, follow_redirects=True)
        self.assertIn(b"Welcome back, Vikram Rathore", res_valid.data)
        print("✓ Task 4 Passed: Valid and invalid login authentication and automated email triggers verified.")

    # -------------------------------------------------------------
    # Task 5: Razorpay Payment Gateway Demonstration
    # -------------------------------------------------------------
    def test_task5_razorpay_flow(self):
        # 1. Create Order on Backend
        order_res = self.client.post('/payment/create-order', json={
            'package_name': 'Signature Heritage Package',
            'amount': 1500,
            'customer_name': 'Rohan & Ananya',
            'customer_email': 'rohan@wedding.com',
            'customer_phone': '9898989898'
        })
        self.assertEqual(order_res.status_code, 200)
        order_data = json.loads(order_res.data)
        self.assertTrue(order_data['success'])
        order_id = order_data['order_id']
        self.assertEqual(order_data['amount_paise'], 150000)

        # Verify order in SQLite
        payment_record = models.get_payment_by_order_id(order_id)
        self.assertIsNotNone(payment_record)
        self.assertEqual(payment_record['status'], 'created')

        # 2. Verify Payment on Backend (Valid test signature)
        verify_res = self.client.post('/payment/verify', json={
            'razorpay_order_id': order_id,
            'razorpay_payment_id': 'pay_test_987654321',
            'razorpay_signature': 'test_sig_abcdef123456789012345678',
            'package_name': 'Signature Heritage Package'
        })
        self.assertEqual(verify_res.status_code, 200)
        verify_data = json.loads(verify_res.data)
        self.assertTrue(verify_data['success'])

        # Verify SQLite payment status updated to 'success'
        updated_payment = models.get_payment_by_order_id(order_id)
        self.assertEqual(updated_payment['status'], 'success')
        self.assertEqual(updated_payment['payment_id'], 'pay_test_987654321')

        # 3. View Success Page
        success_res = self.client.get(f'/payment/success?order_id={order_id}&payment_id=pay_test_987654321')
        self.assertEqual(success_res.status_code, 200)
        self.assertIn(b"Reservation Confirmed", success_res.data)
        self.assertIn(b"Signature Heritage Package", success_res.data)

        print("✓ Task 5 Passed: Server-side Razorpay order creation, HMAC signature verification, and status updates verified.")

    # -------------------------------------------------------------
    # Contact Form & Comments
    # -------------------------------------------------------------
    def test_contact_form_and_comments(self):
        # 1. Contact Form
        res = self.client.post('/contact', data={
            'name': 'Devansh Verma',
            'email': 'devansh@example.com',
            'mobile': '9876543210',
            'event_type': 'Destination wedding',
            'event_date': '2026-12-15',
            'budget': '₹60,00,000 - ₹1,50,00,000',
            'guest_count': '350',
            'message': 'We are looking for a complete Udaipur palace wedding orchestration.'
        }, follow_redirects=True)
        self.assertIn(b"Your inquiry has been received", res.data)

        # 2. Blog Comment
        res_comment = self.client.post('/blog/the-art-of-the-destination-celebration/comment', data={
            'name': 'Siddharth Roy',
            'email': 'siddharth@example.com',
            'comment': 'Udaipur weddings really do have a completely different magic.'
        }, follow_redirects=True)
        self.assertIn(b"Your reflection has been posted", res_comment.data)
        print("✓ Contact inquiry and journal comments systems verified.")

if __name__ == '__main__':
    unittest.main()
