from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from sqlalchemy import select
from models.db_models import ContentCategory
from core.config import settings
from core.database import AsyncSessionLocal  # Import session factory

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
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Email error: {str(e)}")
        finally:
            await db.close()  # Close the session explicitly
