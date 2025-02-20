import psutil
import time
import datetime
import matplotlib.pyplot as plt
import logging
import configparser
import argparse
import smtplib
from email.mime.text import MIMEText
import os

# ------------------------------
# Logging Configuration
# ------------------------------
logging.basicConfig(
    filename='logs/monitor.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------------------
# Configuration File Parsing
# ------------------------------
config = configparser.ConfigParser()
config.read('config.ini')  # Ensure you have a config.ini in the project root
# Example config.ini content:
# [DEFAULT]
# threshold_cpu = 80
threshold_cpu = float(config['DEFAULT'].get('threshold_cpu', 80))

# ------------------------------
# Command-Line Argument Parsing
# ------------------------------
parser = argparse.ArgumentParser(description="System Monitor Data Collection")
parser.add_argument('--interval', type=int, default=5, help='Sampling interval in seconds')
parser.add_argument('--duration', type=int, default=60, help='Total duration in seconds for data collection')
args = parser.parse_args()

# ------------------------------
# Alert Function
# ------------------------------
def send_alert(subject, message, to_email):
    # Retrieve SMTP configuration from environment variables
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.example.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    sender_email = os.getenv('ALERT_EMAIL', 'monitor@example.com')
    sender_password = os.getenv('ALERT_PASS', 'yourpassword')
    
    # Create the email message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            logging.info("Alert sent successfully!")
            print("Alert sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")
        print(f"Failed to send alert: {e}")

# ------------------------------
# Data Collection
# ------------------------------
timestamps = []
cpu_usages = []

logging.info("Starting system monitoring...")
end_time = time.time() + args.duration

while time.time() < end_time:
    cpu_percent = psutil.cpu_percent(interval=None)
    now = datetime.datetime.now().strftime('%H:%M:%S')
    logging.info(f"CPU usage: {cpu_percent}%")
    timestamps.append(now)
    cpu_usages.append(cpu_percent)
    
    # Trigger alert if CPU usage exceeds threshold
    if cpu_percent > threshold_cpu:
        alert_subject = "High CPU Usage Alert"
        alert_message = f"Warning: CPU usage is at {cpu_percent}% at {now}"
        logging.warning(alert_message)
        send_alert(alert_subject, alert_message, "admin@example.com")
    
    time.sleep(args.interval)

logging.info("Data collection complete.")

# ------------------------------
# Data Visualization
# ------------------------------
plt.figure(figsize=(10, 5))
plt.plot(timestamps, cpu_usages, marker='o', linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('docs/cpu_usage_report.png')
plt.show()

