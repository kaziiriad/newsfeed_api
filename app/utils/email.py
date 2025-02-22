from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from core.config import settings

async def send_subscription_email(to_email: str, categories: list):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL", "no-reply@example.com"),
        to_emails=to_email,
        subject="Subscription Confirmation",
        html_content=f"""
        <h3>You've successfully subscribed to:</h3>
        <ul>
            {"".join([f"<li>{cat}</li>" for cat in categories])}
        </ul>
        """
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Email error: {str(e)}")