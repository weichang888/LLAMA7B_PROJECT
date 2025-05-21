import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

# Email settings
gmail_user = "your@gmail.com"
gmail_app_password = "your_app_password"
receiver_email = "your@gmail.com"
subject = "AI News Summary Report"
body = "Please see today's AI news summary in the attached Word document."

# Word file location
today_str = datetime.now().strftime("%Y-%m-%d")
filename = f"AINEWS_{today_str}.docx"
filepath = os.path.join("word", filename) 

# Prepare Email
msg = EmailMessage()
msg["Subject"] = subject
msg["From"] = gmail_user
msg["To"] = receiver_email
msg.set_content(body)

# Add attachment
with open(filepath, "rb") as f:
    file_data = f.read()
    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename
    )

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(gmail_user, gmail_app_password)
    smtp.send_message(msg)

print(f"Email has been sent to {receiver_email} with attachment: {filename}")
