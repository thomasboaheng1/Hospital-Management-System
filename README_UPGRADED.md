# 🏥 Hospital Management System v2.0

A comprehensive, modern hospital management system built with **FastAPI** and **React**, featuring advanced security, real-time updates, and a beautiful user interface.

## ✨ New Features in v2.0

### 🔐 Enhanced Security
- **JWT Authentication** with access and refresh tokens
- **Role-based access control** (Admin, Doctor, Nurse, Receptionist)
- **Password hashing** with bcrypt
- **CORS protection** with configurable origins
- **Rate limiting** to prevent abuse
- **Input validation** with Pydantic models

### 🚀 Performance Improvements
- **Async/await** support throughout the application
- **Database connection pooling** for better performance
- **Caching** for frequently accessed data
- **Optimized SQL queries** with proper indexing
- **Static file serving** for uploads

### 🛠️ Modern Development Features
- **Hot reload** for both backend and frontend
- **Comprehensive logging** with configurable levels
- **Health checks** and monitoring endpoints
- **API documentation** with Swagger UI and ReDoc
- **Type hints** throughout the codebase
- **Error handling** with detailed error messages

### 📊 Enhanced Dashboard
- **Real-time analytics** and statistics
- **Interactive charts** with Recharts
- **Responsive design** for all devices
- **Dark/Light mode** support
- **Modern UI components** with Headless UI

## 🏗️ Architecture

```
hospital-management-system/
├── app/                    # FastAPI Backend
│   ├── core/              # Core configuration
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── main.py           # FastAPI application
├── frontend/              # React Frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   └── package.json
├── alembic/               # Database migrations
├── uploads/               # File uploads
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Git**

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hospital-management-system
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Start development server
python start_dev.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 📋 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout

### Patients
- `GET /api/patients` - List all patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/{id}` - Get patient details
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient

### Doctors
- `GET /api/doctors` - List all doctors
- `POST /api/doctors` - Create new doctor
- `GET /api/doctors/{id}` - Get doctor details
- `PUT /api/doctors/{id}` - Update doctor
- `DELETE /api/doctors/{id}` - Delete doctor

### Appointments
- `GET /api/appointments` - List all appointments
- `POST /api/appointments` - Create new appointment
- `GET /api/appointments/{id}` - Get appointment details
- `PUT /api/appointments/{id}` - Update appointment
- `DELETE /api/appointments/{id}` - Delete appointment

### Medical Records
- `GET /api/medical-records` - List all medical records
- `POST /api/medical-records` - Create new medical record
- `GET /api/medical-records/{id}` - Get medical record details
- `PUT /api/medical-records/{id}` - Update medical record
- `DELETE /api/medical-records/{id}` - Delete medical record

### Prescriptions
- `GET /api/prescriptions` - List all prescriptions
- `POST /api/prescriptions` - Create new prescription
- `GET /api/prescriptions/{id}` - Get prescription details
- `PUT /api/prescriptions/{id}` - Update prescription
- `DELETE /api/prescriptions/{id}` - Delete prescription

### Billing
- `GET /api/billing` - List all bills
- `POST /api/billing` - Create new bill
- `GET /api/billing/{id}` - Get bill details
- `PUT /api/billing/{id}` - Update bill
- `DELETE /api/billing/{id}` - Delete bill

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/analytics` - Get analytics data
- `GET /api/dashboard/reports` - Get reports

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///./hospital.db

# Security Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000"]

# Email Configuration
SMTP_TLS=true
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=5242880
ALLOWED_FILE_TYPES=[".jpg",".jpeg",".png",".pdf",".doc",".docx"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Cache Configuration
CACHE_TTL=300
```

## 🗄️ Database

### Supported Databases
- **SQLite** (default, for development)
- **PostgreSQL** (recommended for production)
- **MySQL** (supported)

### Migration
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest test_auth.py
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 🚀 Deployment

### Production Setup
1. **Set environment variables** for production
2. **Use PostgreSQL** instead of SQLite
3. **Configure CORS** for your domain
4. **Set up SSL/TLS** certificates
5. **Configure logging** for production
6. **Set up monitoring** and health checks

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individual containers
docker build -t hospital-backend .
docker build -t hospital-frontend ./frontend
```

## 📊 Monitoring

### Health Checks
- `GET /api/health` - Basic health check
- `GET /api/info` - System information

### Logging
- **Structured logging** with JSON format
- **Configurable log levels**
- **Request/response logging**
- **Error tracking**

## 🔒 Security Features

- **JWT Authentication** with refresh tokens
- **Password hashing** with bcrypt
- **Role-based access control**
- **Input validation** and sanitization
- **CORS protection**
- **Rate limiting**
- **SQL injection protection**
- **XSS protection**

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests for new features
5. **Run** the test suite
6. **Submit** a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the API docs at `/api/docs`
- **Issues**: Create an issue on GitHub
- **Email**: support@hospital-system.com

## 🎯 Roadmap

### v2.1 (Next Release)
- [ ] **Real-time notifications** with WebSockets
- [ ] **Mobile app** with React Native
- [ ] **Advanced reporting** with charts
- [ ] **Email notifications** for appointments
- [ ] **File upload** improvements
- [ ] **API rate limiting** per user
- [ ] **Audit logging** for all actions

### v2.2 (Future)
- [ ] **Multi-tenant support**
- [ ] **Advanced analytics**
- [ ] **Integration with external systems**
- [ ] **Machine learning** for predictions
- [ ] **Voice commands** support
- [ ] **Offline mode** support

---

**Built with ❤️ using FastAPI and React** 