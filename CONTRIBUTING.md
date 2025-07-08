# Contributing to Hospital Management System

Thank you for your interest in contributing to the Hospital Management System! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
- Go to the main repository page
- Click the "Fork" button in the top right
- Clone your forked repository to your local machine

### 2. Set Up Development Environment
```bash
# Clone your fork
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Write clean, well-documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run tests
pytest

# Run linting
flake8 app/
black --check app/
isort --check-only app/
mypy app/

# Run security checks
bandit -r app/
safety check
```

### 6. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 7. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with a clear description of your changes.

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows the project's style guidelines
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced

### Pull Request Template
```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No security issues introduced
```

## 🏗️ Project Structure

```
hospital-management-system/
├── app/                    # FastAPI Backend
│   ├── core/              # Core configuration
│   │   ├── config.py      # Settings and configuration
│   │   ├── database.py    # Database connection
│   │   └── security.py    # Authentication and security
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── main.py           # FastAPI application
├── tests/                 # Test files
├── docs/                  # Documentation
├── alembic/               # Database migrations
└── requirements.txt       # Python dependencies
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use fixtures for common setup

Example test:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_patient_success():
    """Test successful patient creation"""
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890"
    }
    
    response = client.post("/api/patients", json=patient_data)
    assert response.status_code == 201
    assert response.json()["first_name"] == "John"
```

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused

### API Design
- Use RESTful conventions
- Return consistent JSON responses
- Include proper error handling
- Use appropriate HTTP status codes

### Database
- Use migrations for schema changes
- Write efficient queries
- Add proper indexes
- Handle database errors gracefully

## 🔒 Security Guidelines

### Authentication & Authorization
- Always validate user permissions
- Use secure password hashing
- Implement proper session management
- Validate all inputs

### Data Protection
- Never log sensitive information
- Use environment variables for secrets
- Implement proper CORS policies
- Validate file uploads

## 📚 Documentation

### Code Documentation
- Write clear docstrings
- Include examples in docstrings
- Document complex algorithms
- Keep README updated

### API Documentation
- Use OpenAPI/Swagger annotations
- Provide clear endpoint descriptions
- Include request/response examples
- Document error responses

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

## 💡 Feature Requests

When requesting features, please include:
- Clear description of the feature
- Use cases and benefits
- Implementation suggestions (if any)
- Priority level

## 🏷️ Version Control

### Commit Message Format
Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

### Branch Naming
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation
- `refactor/component-name` - Refactoring

## 🤝 Community Guidelines

### Be Respectful
- Be kind and respectful to all contributors
- Provide constructive feedback
- Help newcomers get started

### Communication
- Use clear and concise language
- Ask questions when unsure
- Share knowledge and best practices

### Recognition
- All contributors will be recognized
- Significant contributions will be highlighted
- Contributors will be added to the README

## 📞 Getting Help

If you need help:
1. Check the documentation
2. Search existing issues
3. Ask in discussions
4. Create an issue for complex problems

## 🎉 Thank You

Thank you for contributing to the Hospital Management System! Your contributions help make healthcare management better for everyone.

---

**Happy Coding! 🚀** 