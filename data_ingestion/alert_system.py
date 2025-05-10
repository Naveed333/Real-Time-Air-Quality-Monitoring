def send_alert(data):
    pm25_level = data["pm25"]
    if pm25_level > 100:
        print(f"ALERT: PM2.5 level ({pm25_level}) exceeds threshold!")


# Integrate this function in Spark Structured Streaming
def alert_on_threshold(row):
    send_alert(row.asDict())


# Example Spark stream
filtered_data.foreach(lambda row: alert_on_threshold(row))
