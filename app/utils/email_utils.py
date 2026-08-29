import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_otp_email(recipient_email, otp_code, recipient_name="Student"):
    """
    Sends a 6-digit verification code to the recipient's email address.
    If SMTP credentials are not configured, logs the OTP to server console
    so local development and presentations are never blocked.
    """
    mail_server = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    mail_port = int(os.environ.get("MAIL_PORT", 587))
    mail_username = os.environ.get("MAIL_USERNAME")
    mail_password = os.environ.get("MAIL_PASSWORD")
    sender = os.environ.get("MAIL_DEFAULT_SENDER") or mail_username or "EXPadviser <noreply@expadvisor.com>"

    print("\n" + "=" * 41)
    print(f"[AUTH OTP DISPATCH] -> {recipient_email}")
    print(f"[CODE]: {otp_code} (Valid for 10 minutes)")
    print("=" * 41 + "\n")

    if not mail_username or not mail_password:
        print("[EMAIL NOTICE] SMTP credentials not set in .env. Falling back to console OTP.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"{otp_code} is your EXPadviser verification code"
        msg["From"] = sender
        msg["To"] = recipient_email

        plain_text = (
            f"Hello {recipient_name},\n\n"
            f"Your EXPadviser email verification code is: {otp_code}\n\n"
            "This code is valid for 10 minutes. Please enter this code to verify your account.\n\n"
            "If you did not request this code, please ignore this email.\n\n"
            "Best regards,\nEXPadviser Campus Hub Team"
        )

        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; color: #1e293b; }}
    .container {{ max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
    .header {{ background: #0f172a; padding: 28px; text-align: center; color: #ffffff; }}
    .brand {{ font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }}
    .content {{ padding: 32px; }}
    .otp-box {{ background: #eff6ff; border: 2px dashed #93c5fd; border-radius: 14px; padding: 20px; text-align: center; margin: 24px 0; }}
    .otp-code {{ font-size: 34px; font-weight: 800; letter-spacing: 8px; color: #1d4ed8; font-family: monospace; }}
    .footer {{ padding: 20px 32px; background: #f1f5f9; text-align: center; font-size: 11px; color: #64748b; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">EXPadviser · Campus Hub</div>
    </div>
    <div class="content">
      <h2 style="margin-top: 0; font-size: 18px; color: #0f172a;">Verify Your Email Address</h2>
      <p style="font-size: 14px; line-height: 1.6; color: #475569;">
        Hello <strong>{recipient_name}</strong>,<br>
        Thank you for creating an account on EXPadviser. Please use the following 6-digit verification code to authenticate your email:
      </p>
      <div class="otp-box">
        <div class="otp-code">{otp_code}</div>
      </div>
      <p style="font-size: 12px; color: #64748b; line-height: 1.5;">
        ⏱️ <strong>This code will expire in 10 minutes.</strong><br>
        Never share this verification code with anyone. If you did not sign up for EXPadviser, you can safely ignore this email.
      </p>
    </div>
    <div class="footer">
      © 2026 EXPadviser Platform · Engineered for Campus Problem Solving
    </div>
  </div>
</body>
</html>"""

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(mail_server, mail_port, timeout=10) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(sender, [recipient_email], msg.as_string())

        print(f"[EMAIL SUCCESS] Verification email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email via SMTP: {str(e)}")
        return False
