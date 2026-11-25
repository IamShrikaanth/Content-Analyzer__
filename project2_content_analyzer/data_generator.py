import random
import csv

random.seed(21)

content_types = ["Python", "ML", "SQL", "DataScience", "WebDev", "AI Basics"]
devices = ["Mobile", "Laptop", "Tablet"]
times = ["Morning", "Afternoon", "Evening", "Night"]

rows = []

for i in range(700):
    user_id = "U" + str(101 + i % 250)
    content = random.choice(content_types)
    duration = random.choice([20, 30, 40, 45, 60])

    engagement_type = random.random()
    if engagement_type < 0.4:
        watch_time = round(duration * random.uniform(0.7, 1.0), 1)
        pause_count = random.randint(0, 2)
        replay_count = random.randint(1, 4)
        notes_count = random.randint(2, 6)
        quiz_attempts = random.randint(1, 2)
        quiz_score = random.randint(65, 100)
        login_freq = random.randint(4, 10)
        session_duration = random.randint(40, 90)
        prev_completion = random.choice(["Yes", "Yes", "No"])
    elif engagement_type < 0.75:
        watch_time = round(duration * random.uniform(0.4, 0.7), 1)
        pause_count = random.randint(1, 4)
        replay_count = random.randint(0, 2)
        notes_count = random.randint(0, 3)
        quiz_attempts = random.randint(1, 2)
        quiz_score = random.randint(40, 75)
        login_freq = random.randint(2, 5)
        session_duration = random.randint(20, 50)
        prev_completion = random.choice(["Yes", "No"])
    else:
        watch_time = round(duration * random.uniform(0.1, 0.4), 1)
        pause_count = random.randint(2, 6)
        replay_count = 0
        notes_count = 0
        quiz_attempts = random.randint(0, 1)
        quiz_score = random.randint(0, 45)
        login_freq = random.randint(0, 2)
        session_duration = random.randint(5, 20)
        prev_completion = "No"

    device = random.choice(devices)
    time_of_day = random.choice(times)

    watch_pct = (watch_time / duration) * 100
    if watch_pct >= 75 and quiz_score >= 55:
        completion = "Completed"
    elif watch_pct >= 60 and quiz_score >= 40:
        completion = random.choice(["Completed", "Not Completed"])
    else:
        completion = "Not Completed"

    rows.append([
        user_id, content, duration, watch_time, pause_count, replay_count,
        notes_count, quiz_attempts, quiz_score, login_freq, session_duration,
        prev_completion, device, time_of_day, completion
    ])

with open("watch_history.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "User_ID", "Content_Type", "Content_Duration", "Watch_Time", "Pause_Count",
        "Replay_Count", "Notes_Count", "Quiz_Attempts", "Quiz_Score", "Login_Frequency",
        "Session_Duration", "Previous_Content_Completion", "Device_Type", "Time_of_Day",
        "Completion_Status"
    ])
    writer.writerows(rows)

print("watch_history.csv created with", len(rows), "rows")
