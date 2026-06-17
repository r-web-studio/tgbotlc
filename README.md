# EduBot AI - Telegram Chatbot for Educational Centers

A production-ready AI Telegram chatbot for educational centers, built with Python, aiogram 3, PostgreSQL, and OpenRouter API.

## Features

- **AI-Powered Chat**: Natural conversations using OpenRouter API with RAG
- **Multi-Language**: Auto-detects Russian, Uzbek, English
- **Lead Qualification**: Automatically classifies users as hot/warm/cold leads
- **Enrollment Flow**: FSM-based enrollment form with admin notifications
- **Long-Term Memory**: Remembers user information across conversations
- **Conversation Summaries**: Auto-summarizes conversations
- **Admin Panel**: Web-based admin dashboard with user management
- **Follow-Up System**: Automatic follow-ups for inactive users

## Deployment on Render

### Prerequisites

1. A Render account
2. A PostgreSQL database (Render provides this)
3. An OpenRouter API key
4. A Telegram Bot Token from @BotFather

### Step 1: Fork/Clone Repository

Fork or clone this repository to your GitHub account.

### Step 2: Create Render Account

Sign up at [render.com](https://render.com)

### Step 3: Deploy with Blueprint

1. Go to Render Dashboard
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create services

### Step 4: Set Environment Variables

In Render Dashboard, go to your web service → **Environment** → **Environment Variables**:

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token | `8013423981:AAH...` |
| `OPENROUTER_API_KEY` | OpenRouter API key | `sk-or-v1-...` |
| `ADMIN_IDS` | Comma-separated admin Telegram IDs | `123456789` |
| `ADMIN_USERNAME` | Admin panel username | `admin` |
| `ADMIN_PASSWORD` | Admin panel password | `mypassword123` |
| `SESSION_SECRET` | Random string for session encryption | `randomstring123` |

**Note:** `DATABASE_URL` is automatically set by Render when you create the PostgreSQL database.

### Step 5: Deploy

Click **Create Web Service** and wait for deployment to complete.

### Step 6: Access

- **Bot**: Find your bot on Telegram and send `/start`
- **Admin Panel**: `https://your-service.onrender.com/api/admin/`
- **Health Check**: `https://your-service.onrender.com/`

## Local Development

### Using Docker Compose

```bash
cd docker
docker-compose up --build
```

### Manual Setup

1. Install PostgreSQL with pgvector:
```sql
CREATE EXTENSION vector;
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy and edit `.env`:
```bash
cp .env.example .env
```

4. Run the bot:
```bash
python main.py
```

## Project Structure

```
├── main.py              # Entry point (web server + bot polling)
├── render.yaml          # Render deployment config
├── requirements.txt     # Python dependencies
├── app/
│   ├── ai/              # OpenRouter AI client
│   ├── bot/             # Telegram bot handlers
│   ├── config/          # Configuration
│   ├── database/        # SQLAlchemy models & repos
│   ├── memory/          # Long-term memory
│   ├── rag/             # RAG system
│   ├── scheduler/       # Follow-up scheduler
│   ├── admin_panel/     # Web admin panel
│   └── utils/           # Utilities
├── knowledge/           # Knowledge base
├── docker/              # Docker configuration
├── migrations/          # Alembic migrations
└── tests/               # Test files
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Health check |
| `/api/admin/` | GET | Admin dashboard |
| `/api/admin/login` | GET/POST | Admin login |
| `/api/admin/users` | GET | User management |
| `/api/admin/conversations` | GET | Conversation history |
| `/api/admin/leads` | GET | Lead management |
| `/api/admin/export/users` | GET | Export users to Excel |

## Tech Stack

- **Python 3.12**
- **aiogram 3** - Telegram Bot Framework
- **SQLAlchemy** - Async ORM
- **PostgreSQL** - Database
- **pgvector** - Vector similarity search
- **OpenRouter API** - AI chat completions
- **aiohttp** - Web server for admin panel
- **Render** - Cloud deployment

## License

MIT
