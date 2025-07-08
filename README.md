# 🏥 Hospital Management System

A comprehensive, modern hospital management system built with **FastAPI** and **React**, featuring advanced security, real-time updates, and a beautiful user interface.

## ✨ Features

### 🔐 Security & Authentication
- **JWT Authentication** with access and refresh tokens
- **Role-based access control** (Admin, Doctor, Nurse, Receptionist)
- **Password hashing** with bcrypt
- **CORS protection** with configurable origins
- **Rate limiting** to prevent abuse
- **Input validation** with Pydantic models

### 🚀 Performance & Modern Development
- **Async/await** support throughout the application
- **Database connection pooling** for better performance
- **Caching** for frequently accessed data
- **Optimized SQL queries** with proper indexing
- **Static file serving** for uploads
- **Hot reload** for both backend and frontend
- **Comprehensive logging** with configurable levels
- **Health checks** and monitoring endpoints

### 📊 Dashboard & Analytics
- **Real-time analytics** and statistics
- **Interactive charts** with Recharts
- **Responsive design** for all devices
- **Dark/Light mode** support
- **Modern UI components** with Headless UI

### 🏗️ Core Modules
- **Patient Management** - Complete patient records and history
- **Doctor Management** - Doctor profiles, specialties, and schedules
- **Appointment Scheduling** - Smart appointment booking system
- **Medical Records** - Comprehensive medical history tracking
- **Prescriptions** - Digital prescription management
- **Billing System** - Automated billing and payment tracking
- **Reports & Analytics** - Detailed reports and insights

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
git clone https://github.com/yourusername/hospital-management-system.git
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
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Frontend
- **React** - JavaScript library for building user interfaces
- **TypeScript** - Typed JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Headless UI** - Unstyled, accessible UI components
- **Recharts** - Composable charting library
- **React Router** - Declarative routing for React
- **Axios** - HTTP client

### Database
- **SQLite** - Lightweight, serverless database (development)
- **PostgreSQL** - Advanced open-source database (production)

## 📦 Installation

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system

# Build and run with Docker Compose
docker-compose up --build
```

### Manual Installation

1. **Backend Setup**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

If you have any questions or need help, please:

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/yourusername/hospital-management-system/issues)
3. Create a new issue

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- React team for the amazing frontend library
- All contributors who helped improve this project

---

**Made with ❤️ for better healthcare management** 