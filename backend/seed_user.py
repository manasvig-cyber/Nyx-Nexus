import sqlite3
from datetime import datetime

db_path = 'f:/nyx nexus/CyberSpace-Frontend/CyberSpace-Frontend/backend/nyxnexus.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Clear existing admin user if any
c.execute("DELETE FROM users WHERE username='admin'")

# Insert admin user with id 1
c.execute("""
    INSERT INTO users (id, username, email, password_hash, xp, rank, created_at) 
    VALUES (1, 'admin', 'admin@nyxnexus.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31S.', 0, 'Novice', ?)
""", (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))

# Insert into leaderboard
c.execute("DELETE FROM leaderboard WHERE user_id=1")
c.execute("INSERT INTO leaderboard (user_id, xp, rank_position) VALUES (1, 0, 0)")

conn.commit()
conn.close()
print("User 'admin' with ID 1 seeded successfully.")
