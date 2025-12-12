# 🎯 AppInfluencers Platform

Platform for connecting businesses with influencers, featuring trial periods, payments via Stripe, and social media analytics.

## 🌟 Features

- **User Management**
  - Three roles: EMPRESA (business), INFLUENCER, ADMIN
  - JWT authentication with httpOnly cookies
  - Trial period for businesses (24 hours, 1 free profile)

- **Profile Management**
  - Influencer profiles with social media insights
  - Instagram, Facebook, TikTok integration
  - Real-time metrics and analytics

- **Payment System**
  - Stripe integration for subscriptions
  - Transaction history
  - Platform commission tracking

- **Social Media Integration**
  - Facebook/Instagram Graph API
  - TikTok API support
  - Automated insights fetching

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM with async support
- **MySQL** - Relational database
- **Alembic** - Database migrations
- **Stripe** - Payment processing
- **JWT** - Authentication

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - API client
- **Shadcn UI** - Component library

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- MySQL 8

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/dcastill92/appinfluencers.git
   cd appinfluencers
   ```

2. **Configure environment variables**
   ```bash
   # Backend
   cp app/.env.example app/.env
   # Edit app/.env with your configuration
   
   # Frontend
   cp frontend/.env.example frontend/.env.local
   # Edit frontend/.env.local
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend

```bash
cd app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📁 Project Structure

```
appinfluencers/
├── app/                      # Backend (FastAPI)
│   ├── alembic/             # Database migrations
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Configuration, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── repositories/    # Data access layer
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── scripts/             # Utility scripts
│   └── tests/               # Unit & integration tests
│
├── frontend/                 # Frontend (Next.js)
│   ├── app/                 # Next.js 14 app directory
│   │   ├── (auth)/          # Authentication pages
│   │   └── (plataforma)/    # Protected platform pages
│   ├── components/          # React components
│   ├── contexts/            # React contexts
│   ├── hooks/               # Custom hooks
│   ├── lib/                 # Utilities
│   └── services/            # API services
│
├── .do/                      # Digital Ocean configuration
├── docker-compose.yml        # Local development
├── DEPLOY_DIGITALOCEAN.md   # Deployment guide
└── DEPLOYMENT_CHECKLIST.md  # Pre-deployment checklist
```

## 🔧 Configuration

### Environment Variables

#### Backend (`app/.env`)

```bash
DATABASE_URL=mysql://user:password@host:port/database
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=480
STRIPE_SECRET_KEY=sk_test_...
FACEBOOK_APP_ID=...
FACEBOOK_APP_SECRET=...
INSTAGRAM_ACCESS_TOKEN=...
```

#### Frontend (`frontend/.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FACEBOOK_APP_ID=...
```

See `.env.example` files for complete configuration.

## 🚢 Deployment

### Digital Ocean App Platform (Recommended)

1. **Read the deployment guide**
   ```bash
   cat DEPLOY_DIGITALOCEAN.md
   ```

2. **Complete the checklist**
   ```bash
   cat DEPLOYMENT_CHECKLIST.md
   ```

3. **Generate SECRET_KEY**
   ```bash
   python app/scripts/generate_secret.py
   ```

4. **Deploy**
   - Push to GitHub
   - Create app from `.do/app.yaml`
   - Configure environment variables
   - Deploy!

**Estimated cost:** ~$25/month (API + Frontend + MySQL)

### Other Platforms

The app can also be deployed to:
- Render.com
- Railway.app
- AWS/GCP/Azure
- Heroku

See platform-specific guides in the `docs/` directory.

## 📚 API Documentation

Once running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd app
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

## 🔒 Security

- JWT tokens stored in httpOnly cookies
- CORS configured for security
- Password hashing with bcrypt
- SQL injection prevention via ORM
- XSS protection
- CSRF protection with SameSite cookies

## 📊 Database Schema

Key models:
- **User**: Authentication and roles
- **InfluencerProfile**: Influencer details and social media
- **Transaction**: Payment records
- **SubscriptionPlan**: Subscription tiers

See `app/models/` for complete schema.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Add your license here]

## 👥 Authors

- Yoiner Castillo - Initial work

## 🆘 Support

For issues and questions:
- GitHub Issues: https://github.com/dcastill92/appinfluencers/issues
- Documentation: See `/docs` directory

## 🗺️ Roadmap

- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Campaign management
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] AI-powered influencer matching

---

Made with ❤️ for connecting businesses with influencers
