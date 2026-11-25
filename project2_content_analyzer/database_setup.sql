DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS content;
DROP TABLE IF EXISTS watch_history;
DROP TABLE IF EXISTS quiz_results;
DROP TABLE IF EXISTS login_activity;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    device_type TEXT,
    login_frequency INTEGER
);

CREATE TABLE content (
    content_id INTEGER PRIMARY KEY,
    content_type TEXT,
    duration INTEGER
);

CREATE TABLE watch_history (
    watch_id INTEGER PRIMARY KEY,
    user_id TEXT,
    content_id INTEGER,
    watch_time REAL,
    pause_count INTEGER,
    replay_count INTEGER,
    completion_status TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id)
);

CREATE TABLE quiz_results (
    quiz_id INTEGER PRIMARY KEY,
    user_id TEXT,
    content_id INTEGER,
    quiz_score INTEGER,
    quiz_attempts INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id)
);

CREATE TABLE login_activity (
    login_id INTEGER PRIMARY KEY,
    user_id TEXT,
    time_of_day TEXT,
    session_duration INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, device_type, login_frequency) VALUES
('U101', 'Mobile', 3),
('U102', 'Laptop', 8),
('U103', 'Laptop', 5),
('U104', 'Mobile', 5),
('U105', 'Tablet', 2);

INSERT INTO content (content_id, content_type, duration) VALUES
(1, 'Python', 40),
(2, 'ML', 45),
(3, 'SQL', 30),
(4, 'WebDev', 45),
(5, 'AI Basics', 20);

INSERT INTO watch_history (watch_id, user_id, content_id, watch_time, pause_count, replay_count, completion_status) VALUES
(1, 'U101', 1, 36, 2, 3, 'Completed'),
(2, 'U102', 2, 20, 0, 0, 'Not Completed'),
(3, 'U103', 3, 25, 1, 2, 'Completed'),
(4, 'U104', 4, 15, 4, 0, 'Not Completed'),
(5, 'U105', 5, 18, 0, 1, 'Completed');

INSERT INTO quiz_results (quiz_id, user_id, content_id, quiz_score, quiz_attempts) VALUES
(1, 'U101', 1, 88, 1),
(2, 'U102', 2, 42, 2),
(3, 'U103', 3, 76, 1),
(4, 'U104', 4, 30, 1),
(5, 'U105', 5, 70, 1);

INSERT INTO login_activity (login_id, user_id, time_of_day, session_duration) VALUES
(1, 'U101', 'Evening', 55),
(2, 'U102', 'Night', 30),
(3, 'U103', 'Morning', 60),
(4, 'U104', 'Afternoon', 20),
(5, 'U105', 'Night', 45);

SELECT c.content_type, COUNT(*) AS watch_count
FROM watch_history w
JOIN content c ON w.content_id = c.content_id
GROUP BY c.content_type
ORDER BY watch_count DESC;

SELECT AVG(watch_time) AS avg_watch_time FROM watch_history;

SELECT c.content_type, AVG(w.watch_time * 100.0 / c.duration) AS avg_engagement
FROM watch_history w
JOIN content c ON w.content_id = c.content_id
GROUP BY c.content_type
ORDER BY avg_engagement DESC;

SELECT u.user_id, w.completion_status
FROM watch_history w
JOIN users u ON w.user_id = u.user_id
WHERE w.completion_status = 'Not Completed';

SELECT AVG(quiz_score) AS average_quiz_score FROM quiz_results;

SELECT c.content_type, SUM(w.replay_count) AS total_replays
FROM watch_history w
JOIN content c ON w.content_id = c.content_id
GROUP BY c.content_type
HAVING SUM(w.replay_count) > 0
ORDER BY total_replays DESC;

SELECT user_id,
    CASE
        WHEN completion_status = 'Completed' THEN 'Engaged User'
        ELSE 'Needs Attention'
    END AS user_status
FROM watch_history;

SELECT user_id FROM users
WHERE login_frequency > (SELECT AVG(login_frequency) FROM users);
