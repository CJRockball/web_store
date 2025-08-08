# Kids Web Store - Improved FastAPI Application

A secure, scalable, and maintainable online store application designed for kids, built with FastAPI and modern web development best practices.

## 🌟 Features

### Core Functionality
- **Interactive Store Interface**: Kid-friendly design with colorful UI
- **Smart Shopping Cart**: Session-based cart management with persistence
- **Secure Checkout**: Complete order processing with validation
- **Menu Management**: Categorized food items (healthy vs. fun foods)
- **Responsive Design**: Mobile-first responsive interface

### Security & Quality
- **Input Sanitization**: XSS protection using nh3
- **Session Management**: Secure session handling with middleware
- **CORS Protection**: Configurable CORS settings
- **Error Handling**: Comprehensive error handling and logging
- **Data Validation**: Pydantic models for all data structures
- **Type Safety**: Full type hints and validation

### Architecture
- **Clean Architecture**: Separation of concerns with services, models, and routers
- **Dependency Injection**: FastAPI dependency system for clean code
- **Configuration Management**: Environment-based configuration
- **Testing Suite**: Comprehensive test coverage
- **Docker Support**: Containerized deployment ready

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Method 1: Using Make (Recommended)
```bash
# Clone and enter directory
git clone <repository-url>
cd web_store_improved

# Set up development environment
make dev

# Run the application
make run
```

### Method 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

### Method 3: Using Docker
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t kids-web-store .
docker run -p 8000:8000 kids-web-store
```

### Method 4: Using Startup Script
```bash
# Make script executable (Unix/Linux/Mac)
chmod +x start.sh

# Run startup script
./start.sh
```

## 📁 Project Structure

```
web_store_improved/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app instance and configuration
│   ├── config.py                 # Application configuration
│   ├── dependencies.py           # Dependency injection functions
│   ├── models/                   # Pydantic models
│   │   ├── __init__.py
│   │   └── items.py             # Food items and cart models
│   ├── routers/                  # API route handlers
│   │   ├── __init__.py
│   │   ├── store.py             # Store-related endpoints
│   │   └── checkout.py          # Checkout and cart management
│   └── services/                 # Business logic layer
│       ├── __init__.py
│       └── store_service.py     # Store business logic
├── templates/                    # Jinja2 HTML templates
│   ├── index.html               # Main store page
│   ├── checkout.html            # Checkout page
│   ├── checkout_success.html    # Order success page
│   ├── welcome.html             # Welcome/landing page
│   └── error.html               # Error page
├── static/                       # Static assets (CSS, images, JS)
│   └── *.jpg                    # Food item images
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_store.py            # Application tests
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker container definition
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                      # Development commands
├── start.sh                      # Startup script
└── README.md                     # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
BASE_URL=http://localhost:8000
CORS_ORIGINS=["http://localhost:8000", "http://127.0.0.1:8000"]
REDIS_URL=redis://localhost:6379
```

### Application Settings
Configuration is managed through `app/config.py` using Pydantic Settings:

- **Session Management**: Configurable session expiration
- **Cart Limits**: Maximum items per cart
- **CORS Settings**: Allowed origins for cross-origin requests
- **Debug Mode**: Development vs. production settings

## 🍎 Adding Food Items

Food items are defined in `app/services/store_service.py`. Each item includes:

- **Name**: Display name
- **Price**: Cost in dollars
- **Category**: Healthy or junk food
- **Image**: Filename in static directory
- **Description**: Item description

### Adding Static Images
Place food item images in the `static/` directory:

```
static/
├── pizza.jpg
├── carrot.jpg
├── fries.jpg
├── tomato.jpg
└── ... (other food images)
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_store.py -v
```

### Test Coverage
- Unit tests for all services
- Integration tests for API endpoints
- Security testing for input validation
- Session management testing

## 🚢 Deployment

### Docker Deployment
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment
1. Set `DEBUG=False` in environment
2. Use a proper secret key
3. Configure proper CORS origins
4. Set up reverse proxy (nginx)
5. Use a proper database for sessions
6. Set up monitoring and logging

### Environment-Specific Settings
- **Development**: Debug mode, local CORS, file-based sessions
- **Production**: Secure settings, database sessions, proper logging

## 🔒 Security Features

### Input Validation
- **Pydantic Models**: All input validated through Pydantic
- **HTML Sanitization**: User input sanitized with nh3
- **Type Checking**: Full type safety with mypy

### Session Security
- **Secure Sessions**: Cryptographically signed sessions
- **Session Expiration**: Configurable timeout
- **CSRF Protection**: Ready for CSRF middleware

### Error Handling
- **Graceful Degradation**: User-friendly error messages
- **Security Logging**: Comprehensive security event logging
- **Input Sanitization**: Protection against XSS attacks

## 🛠 Development

### Code Quality
```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Run all checks
make check-all
```

### Development Workflow
1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Run quality checks
5. Submit pull request

### Adding New Features
1. **Models**: Define data structures in `app/models/`
2. **Services**: Implement business logic in `app/services/`
3. **Routes**: Add API endpoints in `app/routers/`
4. **Templates**: Create HTML templates in `templates/`
5. **Tests**: Add tests in `tests/`

## 📊 API Endpoints

### Store Endpoints
- `GET /store/` - Main store page
- `POST /store/add-item` - Add item to cart (API)
- `POST /store/add-item-form` - Add item to cart (Form)
- `GET /store/menu` - Get menu items (API)
- `GET /store/cart` - Get cart contents (API)

### Checkout Endpoints
- `GET /checkout/` - Checkout page
- `POST /checkout/` - Process checkout action
- `DELETE /checkout/clear` - Clear cart (API)
- `POST /checkout/remove-item` - Remove item from cart

### Utility Endpoints
- `GET /` - Welcome page
- `GET /health` - Health check
- `GET /api/info` - API information

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Missing Static Files**
- Ensure food images are in `static/` directory
- Check file permissions
- Verify image filenames match service configuration

**Session Issues**
- Check SECRET_KEY configuration
- Verify session middleware is enabled
- Clear browser cookies if needed

**Import Errors**
- Ensure virtual environment is activated
- Check Python path: `export PYTHONPATH="${PYTHONPATH}:."`
- Verify all dependencies are installed

## 📝 Changelog

### Version 2.0.0 (Current)
- ✅ Complete architecture overhaul
- ✅ Added session-based cart management
- ✅ Implemented comprehensive security measures
- ✅ Added full test coverage
- ✅ Created Docker deployment support
- ✅ Improved UI/UX with responsive design
- ✅ Added proper error handling and logging

### Version 1.0.0 (Original)
- Basic FastAPI application
- Single file structure
- Global state management
- Minimal error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pydantic for data validation
- Jinja2 for templating
- The Python community for great tools and libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the test cases for examples
3. Check application logs for error details
4. Open an issue on the repository

---

Made with ❤️ for kids learning about web development and healthy choices!
