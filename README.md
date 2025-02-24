# Newsfeed API 🚀

A FastAPI-based backend service for managing user subscriptions, payments, and content delivery. Integrated with Stripe for payments, SendGrid for email notifications, and JWT for authentication.

## Features ✨
- **JWT Authentication**: Secure user registration/login
- **Category Subscriptions**: Subscribe/unsubscribe to content categories
- **Personalized Content**: Fetch articles based on subscriptions (NewsAPI integration)
- **Stripe Payments**: Premium content purchase flow
- **Email Notifications**: SendGrid integration for subscription confirmations
- **Dockerized**: Ready for local development and production deployment
- **Async Ready**: Full async support for high performance

## Prerequisites 📋
- Python 3.10+
- Docker & Docker Compose
- [Stripe Account](https://dashboard.stripe.com/register)
- [SendGrid Account](https://signup.sendgrid.com/)
- [NewsAPI Key](https://newsapi.org/register)

## Installation 🛠️
1. Clone repository:
    
    ``` bash
    git clone https://github.com/kaziiriad/newsfeed_api.git
    cd  newsfeed_api
    ```
2. Create `.env` file:

    ``` bash
    cp .env.example .env
    # Fill in your credentials
    ```
3. Start the services:

    ``` bash
    docker-compose up --build -d
    ```

### API Documentation 📖
- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## Key Endpoints 🛤️

Endpoint | Method | Description
--- | --- | ---
`/auth/register` | POST | Register a new user
`/auth/login` | POST | Login and get JWT token
`/subscription/subscribe` | POST | Subscribe to categories
`/subscription/unsubscribe` | POST | Unubscribe to categories
`/content` | GET | Get perosnalized content
`/content/premium` | GET | Get premium content
`/payment/create-intent` | POST | Initiate Stripe payment
`/payment/webhook` | POST | Stripe webhook handler

## Project Structure 📁
```
.
├── app
│   ├── core              # Config and database setup
│   ├── models           # Database models and schemas
│   ├── routes           # API endpoints
│   ├── services         # Business logic
│   ├── utils            # Email and external API helpers
│   ├── main.py          # App entrypoint
│   └── dependencies.py  # Dependency injection
├── static               # Frontend files (HTML/CSS/JS)
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .dockerignore
├── README.md
└── Dockerfile
````
## Deployment
**Deployed on Render with automatic CI/CD from GitHub.**

[![Live Link](https://render.com/images/deploy-to-render-button.svg)](https://newsfeed-api-wpsl.onrender.com/)

## License 📝
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏
- [FastAPI](https://fastapi.tiangolo.com/)
- [Stripe](https://stripe.com/docs)
- [SendGrid](https://sendgrid.com/docs)
- [NewsAPI](https://newsapi.org/docs)
- [Render](https://render.com/docs)
- [Docker](https://docs.docker.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)

**Happy coding!** 🎉 Built with ❤️ using FastAPI, Stripe, and SendGrid