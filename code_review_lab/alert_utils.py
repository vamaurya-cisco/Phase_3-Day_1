import os
import sqlite3


ALERT_THRESHOLD_MULTIPLIER = 1.5

DB_PASSWORD = os.getenv("DB_PASSWORD")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


def format_alert_message(level, title, source, metric_name, metric_value, threshold):
    if level not in ("CRITICAL", "WARNING"):
        raise ValueError(f"Unknown alert level: {level}")

    message = (
        f"{level} ALERT: {title} from {source}. "
        f"{metric_name} reached {metric_value}, threshold is {threshold}."
    )
    if metric_value > threshold * ALERT_THRESHOLD_MULTIPLIER:
        message += " This is over 150% of threshold -- page on-call immediately."
    return message


def get_alerts_by_source(db_path, source_name):
    if not isinstance(source_name, str) or not source_name.strip():
        raise ValueError("source_name must be a non-empty string")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts WHERE source = ?", (source_name,))
    return cursor.fetchall()


if __name__ == "__main__":
    print(
        format_alert_message(
            "CRITICAL", "CPU spike", "api-gateway",
            "cpu_utilization", 96.5, 85.0,
        )
    )