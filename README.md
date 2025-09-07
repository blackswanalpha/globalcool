# Global Cool-Light E.A LTD - HVAC Platform

A comprehensive Django-based HVAC portfolio and management platform for Global Cool-Light E.A LTD, featuring modern web technologies and responsive design.

## 🚀 Features

### Public Website
- **Modern Landing Page** - Professional HVAC company presentation
- **Service Showcase** - Detailed HVAC services and products catalog
- **Portfolio Gallery** - Project case studies with before/after images
- **Contact & Booking** - Lead generation and service booking system
- **Blog System** - Content management for industry insights
- **Responsive Design** - Mobile-first approach with TailwindCSS

### Admin Dashboard
- **Customer Management** - Complete CRM functionality
- **Lead Tracking** - Inquiry and quotation management
- **Service Management** - HVAC services and product catalog
- **Portfolio Management** - Project showcase administration
- **Booking System** - Service appointment scheduling
- **Email Templates** - Automated communication system
- **User Management** - Role-based access control

## 🛠 Technology Stack

- **Backend**: Django 4.2.16 (Python)
- **Frontend**: TailwindCSS 3.x + HTMX
- **Database**: SQLite (development) / PostgreSQL (production)
- **Cache/Queue**: Redis + Celery
- **Media Storage**: Local/DigitalOcean Spaces
- **Email**: SMTP integration
- **Admin**: Custom admin interface with Bootstrap

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- Redis (for production)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/blackswanalpha/globalcool.git
   cd globalcool
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Build CSS assets**
   ```bash
   npm run build
   ```

7. **Run development server**
   ```bash
   # Option 1: Django only
   python manage.py runserver
   
   # Option 2: With CSS watching
   npm run dev
   ```

## 🎨 Development

### CSS Development
- **Input**: `static/css/input.css`
- **Output**: `static/css/output.css`
- **Watch mode**: `npm run build-css`
- **Production build**: `npm run build-css-prod`

### Project Structure
```
globalcool/
├── apps/                   # Django applications
│   ├── core/              # Core functionality
│   ├── users/             # User management
│   ├── services/          # HVAC services
│   ├── portfolio/         # Project showcase
│   ├── leads/             # Lead management
│   ├── cms/               # Content management
│   └── blog/              # Blog system
├── config/                # Django settings
├── templates/             # HTML templates
├── static/                # Static assets
├── media/                 # User uploads
└── docs/                  # Documentation
```

## 🚀 Deployment

### Production Setup
1. Set environment variables
2. Configure PostgreSQL database
3. Set up Redis for caching/queues
4. Configure email settings
5. Set up static file serving
6. Run migrations and collect static files

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
```

## 📱 Features Overview

### Customer Portal
- Service booking and scheduling
- Quotation requests
- Project progress tracking
- Communication history

### Admin Features
- Dashboard with KPIs
- Customer relationship management
- Service and product catalog
- Portfolio project management
- Lead and quotation tracking
- Email template management
- User role management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python manage.py test`
5. Submit a pull request

## 📄 License

This project is proprietary software owned by Global Cool-Light E.A LTD.

## 📞 Support

For support and inquiries:
- Email: info@globalcool-light.com
- Website: https://globalcool-light.com

---

**Global Cool-Light E.A LTD** - Professional HVAC Solutions in East Africa
