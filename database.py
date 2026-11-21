import sqlite3
import os
from config import Config

def get_db_connection():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. users table (Task 2 & 3)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mobile TEXT NOT NULL,
        city TEXT,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. contact_inquiries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        mobile TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_date TEXT,
        budget TEXT,
        guest_count TEXT,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 3. payments table (Task 5)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_id TEXT NOT NULL,
        payment_id TEXT,
        signature TEXT,
        package_name TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT DEFAULT 'INR',
        status TEXT NOT NULL, -- 'created', 'success', 'failed'
        customer_name TEXT,
        customer_email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)
    
    # 4. blog_posts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        excerpt TEXT NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT NOT NULL,
        author TEXT DEFAULT 'Amara Mehta',
        published_at TEXT NOT NULL
    );
    """)
    
    # 5. comments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES blog_posts(id) ON DELETE CASCADE
    );
    """)

    # 6. email_logs table (Task 4: Permanent audit trail for viva demonstration)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient TEXT NOT NULL,
        subject TEXT NOT NULL,
        body_text TEXT NOT NULL,
        body_html TEXT NOT NULL,
        status TEXT NOT NULL, -- 'sent', 'simulated', 'failed'
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    seed_db(conn)
    conn.close()
    print("Database initialized and verified.")

def seed_db(conn):
    cursor = conn.cursor()
    
    # Check if blog posts exist
    cursor.execute("SELECT COUNT(*) FROM blog_posts")
    count = cursor.fetchone()[0]
    
    if count == 0:
        posts = [
            (
                "How to plan a wedding that feels like you",
                "how-to-plan-a-wedding-that-feels-like-you",
                "The Guide",
                "There is an art to making space for a celebration — and a quiet confidence in knowing when to let the room do the talking.",
                """There is an art to making space for a celebration — and a quiet confidence in knowing when to let the room do the talking.

When couples sit across from us at our studio table, they often arrive carrying binders of other people’s weddings. The pressure to conform to traditions that feel hollow or trends that will date within a season can be overwhelming.

Our approach begins with subtraction. What if you stripped away the obligatory favors, the scripted speeches that don't sound like your friends, and the rigid timelines that leave no room to breathe?

What remains is the heartbeat of your gathering: the warmth of candlelight against aged stone, the intimacy of conversations over slow-poured wine, and the joyful abandon of dancing until your feet are bruised and your spirit is soaring.

Design intentionally. Choose materials that age gracefully — linen, raw silk, hand-thrown ceramics, and seasonal flora that looks gathered rather than engineered. Most importantly, give yourself permission to be a guest at your own celebration.""",
                "images/blog/blog_1.jpg",
                "Amara Mehta",
                "May 14, 2024"
            ),
            (
                "The art of the destination celebration",
                "the-art-of-the-destination-celebration",
                "Journeys",
                "From the lake palaces of Udaipur to sun-drenched coastal forts, taking your guests on a journey changes the cadence of the entire weekend.",
                """A destination celebration is rarely about the postcard backdrop alone. It is about removing your dearest people from their everyday rhythms and placing them in an immersive world where time bends.

When you invite guests to spend three days in Udaipur or on the quiet cliff tops of Goa, the energy shifts from a hurried Saturday evening sprint into a collective vacation. Welcome dinners under banyan trees bleed into lazy poolside mornings, which gently gather momentum into the sacred spectacle of the pheras.

Logistics in destination planning require radical hospitality. From the welcome basket filled with local artisanal treats to thoughtfully timed transfers and curated downtime, every touchpoint must communicate: 'You are held. You are cared for.'

When selecting a heritage venue, honor its architecture. Don't fight centuries-old sandstone with modern synthetic structures; illuminate the arches with hundreds of hand-lit clay diyas, perfume the courtyard with night-blooming jasmine, and let the history sing.""",
                "images/blog/blog_2.jpg",
                "Rohan Kapoor",
                "April 29, 2024"
            ),
            (
                "Flowers that set the whole mood",
                "flowers-that-set-the-whole-mood",
                "Details",
                "How sculptural florals, wild greenery and botanical scents transform architectural spaces into unforgettable sensorial sanctuaries.",
                """Floristry at EverAfter is treated less like floristry and more like living sculpture. We rarely favor tightly packed, uniform spheres of imported roses. Instead, we look for branchiness, gesture, and natural imperfection.

Consider how fragrance operates in memory. Long after the music fades, the scent of crushed tuberoses, marigold garlands, and damp vetiver will instantly transport you back to the threshold of your mandap.

By blending wild local blooms with sculptural greenery, we create organic transitions between interior courtyards and open skies. In evening lighting, floral silhouettes cast dramatic, painterly shadows against warm plaster walls, turning every corner into an editorial tableau.""",
                "images/blog/blog_3.jpg",
                "Nisha Jain",
                "April 06, 2024"
            )
        ]
        
        cursor.executemany("""
        INSERT INTO blog_posts (title, slug, category, excerpt, content, image_url, author, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, posts)
        
        # Seed initial comments
        cursor.execute("SELECT id FROM blog_posts WHERE slug = 'how-to-plan-a-wedding-that-feels-like-you'")
        post1_id = cursor.fetchone()[0]
        cursor.execute("""
        INSERT INTO comments (post_id, name, email, comment)
        VALUES (?, ?, ?, ?)
        """, (post1_id, "Devika Sharma", "devika@gmail.com", "This perspective is so refreshing! In the middle of all the wedding planning noise, reading this gave me a sense of calm."))
        
        cursor.execute("""
        INSERT INTO comments (post_id, name, email, comment)
        VALUES (?, ?, ?, ?)
        """, (post1_id, "Kunal Singhania", "kunal@gmail.com", "The concept of subtraction resonated deeply with us. Beautiful writing."))
        
        conn.commit()

if __name__ == "__main__":
    init_db()
