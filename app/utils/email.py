from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from sqlalchemy import select
from models.db_models import ContentCategory
from core.config import settings
from core.database import AsyncSessionLocal  # Import session factory
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_subscription_email(to_email: str, categories: list):
    """
    Sends an email to the specified recipient with subscription details.
    """
    async with AsyncSessionLocal() as db:

        try:
            # Fetch sample articles from the database
            articles_by_category = {}
            for category in categories:
                result = await db.execute(
                    select(ContentCategory.sample_articles)
                    .where(ContentCategory.name == category)
                )
                articles = result.scalar()  # Get JSON array
                articles_by_category[category] = articles or []  # Handle None
            
            # Build email content
            html_content = "<h3>Your Subscriptions:</h3>"
            for category, articles in articles_by_category.items():
                html_content += f"<h4>{category}</h4><ul>"
                for article in articles:
                    html_content += f'<li><a href="{article["url"]}">{article["title"]}</a></li>'
                html_content += "</ul>"

            message = Mail(
                from_email=settings.SENDGRID_FROM_EMAIL,
                to_emails=to_email,
                subject="Subscription Confirmation",
                html_content=html_content
            )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(f"Email sent to {to_email}. Status: {response}")
        except Exception as e:
            logger.error(f"Email failed: {str(e)}")
        finally:
            await db.close()  # Close the session explicitly

async def send_digest_email(to_email: str, articles: list):
    # Build HTML content
    html_content = """
    <h1>Your Weekly Content Digest</h1>
    <p>Here are your recommended articles:</p>
    """
    for article in articles:
        html_content += f"""
        <div style="margin-bottom: 20px;">
            <h3>{article.get('title', 'No title')}</h3>
            <p>{article.get('description', '')}</p>
            <a href="{article.get('url', '#')}">Read Article</a>
        </div>
        """
    
    # Send email via SendGrid
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject="Weekly Digest - New Articles for You!",
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {to_email}. Status: {response}")
    except Exception as e:
        logger.info(f"Email to {to_email} failed. Status: {response}")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def send_payment_confirmation(email: str):
    """
    Sends a confirmation email to the specified recipient after successful payment.
    """
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject="Payment Confirmed",
        html_content="<h3>Thank you for your payment!</h3>"
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent to {email}. Status: {response}")
    except Exception as e:
        logger.error(f"Email to {email} failed: {str(e)}")
        