import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.cluster import KMeans


class User:
    def __init__(self, user_id, device, login_frequency):
        self.user_id = user_id
        self.device = device
        self.login_frequency = login_frequency


class Content:
    def __init__(self, content_type, duration):
        self.content_type = content_type
        self.duration = duration


class WatchHistory:
    def __init__(self, watch_time, pause_count, replay_count, duration):
        self.watch_time = watch_time
        self.pause_count = pause_count
        self.replay_count = replay_count
        self.duration = duration

    def watch_percentage(self):
        return (self.watch_time / self.duration) * 100


class QuizResult:
    def __init__(self, quiz_score, quiz_attempts):
        self.quiz_score = quiz_score
        self.quiz_attempts = quiz_attempts


class EngagementAnalyzer:
    def __init__(self, df):
        self.df = df

    def most_engaged_content(self):
        return self.df.groupby("Content_Type")["Engagement_Score"].mean().sort_values(ascending=False)

    def average_completion_by_device(self):
        temp = self.df.copy()
        temp["Completed_Flag"] = temp["Completion_Status"].apply(lambda x: 1 if x == "Completed" else 0)
        return temp.groupby("Device_Type")["Completed_Flag"].mean() * 100


class PredictionEngine:
    def __init__(self):
        self.encoders = {}
        self.models = {}
        self.results = {}
        self.best_model_name = None
        self.best_model = None

    def prepare_data(self, df):
        data = df.copy()
        cat_cols = ["Content_Type", "Device_Type", "Time_of_Day", "Previous_Content_Completion"]
        for col in cat_cols:
            le = LabelEncoder()
            data[col + "_enc"] = le.fit_transform(data[col])
            self.encoders[col] = le

        target_le = LabelEncoder()
        data["Completion_enc"] = target_le.fit_transform(data["Completion_Status"])
        self.encoders["Completion_Status"] = target_le

        feature_cols = ["Content_Type_enc", "Watch_Percentage", "Pause_Count", "Replay_Count",
                         "Notes_Count", "Quiz_Attempts", "Quiz_Score", "Login_Frequency",
                         "Session_Duration", "Previous_Content_Completion_enc", "Device_Type_enc",
                         "Time_of_Day_enc"]
        X = data[feature_cols]
        y = data["Completion_enc"]
        return X, y

    def train_all(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

        knn = KNeighborsClassifier(n_neighbors=5)
        nb = GaussianNB()
        dt = DecisionTreeClassifier(max_depth=6, random_state=5)
        rf = RandomForestClassifier(n_estimators=100, random_state=5)

        model_list = {"KNN": knn, "Naive Bayes": nb, "Decision Tree": dt, "Random Forest": rf}

        for name, model in model_list.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            acc = accuracy_score(y_test, pred)
            prec = precision_score(y_test, pred, zero_division=0)
            rec = recall_score(y_test, pred, zero_division=0)
            self.results[name] = {
                "Accuracy": round(acc * 100, 2),
                "Precision": round(prec * 100, 2),
                "Recall": round(rec * 100, 2)
            }
            self.models[name] = model

        self.best_model_name = max(self.results, key=lambda k: self.results[k]["Accuracy"])
        self.best_model = self.models[self.best_model_name]
        return self.results


def clean_and_engineer(df):
    df = df.drop_duplicates()
    df = df.dropna()

    df["Watch_Percentage"] = (df["Watch_Time"] / df["Content_Duration"]) * 100
    df["Average_Session_Time"] = df.groupby("User_ID")["Session_Duration"].transform("mean")
    df["Replay_Ratio"] = df["Replay_Count"] / (df["Pause_Count"] + 1)
    df["Quiz_Performance"] = df["Quiz_Score"] / (df["Quiz_Attempts"] + 1)

    df["Engagement_Score"] = (
        df["Watch_Percentage"] * 0.4
        + df["Quiz_Score"] * 0.3
        + df["Login_Frequency"] * 2
        + df["Replay_Count"] * 3
    )

    return df


def numpy_stats(df):
    watch_array = df["Watch_Percentage"].to_numpy()
    print("\n===== NUMPY STATISTICS (Watch Percentage) =====")
    print("Mean:", round(np.mean(watch_array), 2))
    print("Max:", round(np.max(watch_array), 2))
    print("Min:", round(np.min(watch_array), 2))
    print("Std Dev:", round(np.std(watch_array), 2))

    normalized = (watch_array - np.min(watch_array)) / (np.max(watch_array) - np.min(watch_array))
    df["Watch_Percentage_Normalized"] = normalized
    return df


def make_visualizations(df):
    plt.figure(figsize=(8, 5))
    trend = df.groupby("Content_Type").apply(
        lambda g: (g["Completion_Status"] == "Completed").mean() * 100)
    trend.sort_values().plot(kind="bar", color="teal")
    plt.title("Content Completion Trend")
    plt.ylabel("Completion %")
    plt.tight_layout()
    plt.savefig("content_completion_trend.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    df["Watch_Percentage"].plot(kind="hist", bins=20, color="orange")
    plt.title("Watch Time Distribution")
    plt.xlabel("Watch Percentage")
    plt.tight_layout()
    plt.savefig("watch_time_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    df["Quiz_Score"].plot(kind="hist", bins=20, color="purple")
    plt.title("Quiz Score Distribution")
    plt.tight_layout()
    plt.savefig("quiz_score_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    login_pattern = df.groupby("Time_of_Day")["Login_Frequency"].mean()
    login_pattern.plot(kind="bar", color="green")
    plt.title("Daily Login Pattern")
    plt.tight_layout()
    plt.savefig("login_pattern.png")
    plt.close()

    plt.figure(figsize=(7, 6))
    corr_cols = ["Watch_Time", "Replay_Count", "Quiz_Score", "Login_Frequency", "Session_Duration"]
    temp = df.copy()
    temp["Completed_Num"] = temp["Completion_Status"].apply(lambda x: 1 if x == "Completed" else 0)
    corr_cols.append("Completed_Num")
    sns.heatmap(temp[corr_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png")
    plt.close()

    print("\nAll visualizations saved as PNG files.")


def run_kmeans(df):
    features = df[["Watch_Percentage", "Replay_Count", "Quiz_Score", "Login_Frequency", "Session_Duration"]]
    kmeans = KMeans(n_clusters=3, random_state=5, n_init=10)
    df["Behavior_Cluster"] = kmeans.fit_predict(features)

    cluster_summary = df.groupby("Behavior_Cluster")["Watch_Percentage"].mean().sort_values()
    cluster_order = list(cluster_summary.index)
    labels = ["Passive Users", "Regular Learners", "Highly Engaged Learners"]

    cluster_names = {}
    for i, cluster_id in enumerate(cluster_order):
        cluster_names[cluster_id] = labels[i]

    df["Cluster_Name"] = df["Behavior_Cluster"].map(cluster_names)

    print("\n===== K-MEANS BEHAVIOR SEGMENTATION =====")
    print(df.groupby("Cluster_Name")["Watch_Percentage"].mean())
    return df


def main():
    df = pd.read_csv("watch_history.csv")
    df = clean_and_engineer(df)
    df = numpy_stats(df)
    make_visualizations(df)

    analyzer = EngagementAnalyzer(df)
    print("\n===== TOP ENGAGING CONTENT =====")
    print(analyzer.most_engaged_content())

    print("\n===== COMPLETION RATE BY DEVICE =====")
    print(analyzer.average_completion_by_device())

    engine = PredictionEngine()
    X, y = engine.prepare_data(df)
    results = engine.train_all(X, y)

    df = run_kmeans(df)

    print("\n===== MODEL COMPARISON =====")
    for name, metrics in results.items():
        print(name, ":", metrics)

    print("\nBest Performing Model:", engine.best_model_name)

    print("\n===== SAMPLE PREDICTION =====")
    sample = pd.DataFrame([{
        "Content_Type_enc": engine.encoders["Content_Type"].transform(["Python"])[0],
        "Watch_Percentage": 90,
        "Pause_Count": 2,
        "Replay_Count": 3,
        "Notes_Count": 5,
        "Quiz_Attempts": 1,
        "Quiz_Score": 85,
        "Login_Frequency": 6,
        "Session_Duration": 60,
        "Previous_Content_Completion_enc": engine.encoders["Previous_Content_Completion"].transform(["Yes"])[0],
        "Device_Type_enc": engine.encoders["Device_Type"].transform(["Laptop"])[0],
        "Time_of_Day_enc": engine.encoders["Time_of_Day"].transform(["Evening"])[0],
    }])

    pred_num = engine.best_model.predict(sample)[0]
    pred_label = engine.encoders["Completion_Status"].inverse_transform([pred_num])[0]

    print("Content: Python Tutorial")
    print("Duration: 40 minutes | Watched: 36 minutes")
    print("Predicted Completion:", pred_label)
    if pred_label == "Completed":
        print("Engagement Level: HIGH")
    else:
        print("Engagement Level: LOW")


if __name__ == "__main__":
    main()
