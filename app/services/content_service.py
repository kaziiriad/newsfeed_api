import httpx
from core.config import settings

async def fetch_news(categories: list[str]):
    articles = []
    async with httpx.AsyncClient() as client:
        for category in categories:
            try:
                response = await client.get(
                    "https://newsapi.org/v2/top-headlines",
                    params={
                        "category": category,
                        "language": "en",
                        "apiKey": settings.NEWSAPI_KEY,
                        "pageSize": 10  # Limit results
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    articles.extend(response.json()["articles"])
            except Exception as e:
                print(f"Failed to fetch {category} news: {str(e)}")
    return articles
