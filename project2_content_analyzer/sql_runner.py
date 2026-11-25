import sqlite3

conn = sqlite3.connect("content_analyzer.db")
cur = conn.cursor()

with open("database_setup.sql", "r") as f:
    script = f.read()

cur.executescript(script)
conn.commit()

print("---- Most watched content ----")
query1 = """
SELECT c.content_type, COUNT(*) AS watch_count
FROM watch_history w
JOIN content c ON w.content_id = c.content_id
GROUP BY c.content_type
ORDER BY watch_count DESC
"""
for row in cur.execute(query1):
    print(row)

print("\n---- Average watch time ----")
for row in cur.execute("SELECT AVG(watch_time) FROM watch_history"):
    print(row)

print("\n---- Users with low completion ----")
query2 = """
SELECT u.user_id, w.completion_status
FROM watch_history w
JOIN users u ON w.user_id = u.user_id
WHERE w.completion_status = 'Not Completed'
"""
for row in cur.execute(query2):
    print(row)

print("\n---- Highest replay content (HAVING) ----")
query3 = """
SELECT c.content_type, SUM(w.replay_count) AS total_replays
FROM watch_history w
JOIN content c ON w.content_id = c.content_id
GROUP BY c.content_type
HAVING SUM(w.replay_count) > 0
ORDER BY total_replays DESC
"""
for row in cur.execute(query3):
    print(row)

print("\n---- CASE statement: user status ----")
query4 = """
SELECT user_id,
    CASE
        WHEN completion_status = 'Completed' THEN 'Engaged User'
        ELSE 'Needs Attention'
    END AS user_status
FROM watch_history
"""
for row in cur.execute(query4):
    print(row)

print("\n---- Subquery: above average login frequency ----")
for row in cur.execute("SELECT user_id FROM users WHERE login_frequency > (SELECT AVG(login_frequency) FROM users)"):
    print(row)

conn.close()
print("\ncontent_analyzer.db created successfully")
