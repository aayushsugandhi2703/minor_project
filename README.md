# minor_project : Cloud based automated Nginx logs parser

This will be the structure of Application
Parser/
├── secrets.py                  # Stores sensitive credentials (e.g., database URL, API keys, secret keys)
├── config.py                   # Configuration file (e.g., settings for Flask, database, logging, and environment variables)
├── run.py                      # Entry point for the Flask application
├── app/
│   ├── __init__.py             # Initializes the Flask app and registers Blueprints
│   ├── Forms.py                # Defines WTForms for user authentication and other inputs
│   ├── auth/                   # Authentication module (User login, registration, and authentication)
│   │   ├── __init__.py         # Initializes the authentication Blueprint
│   │   ├── routes.py           # Defines authentication-related routes (login, logout, register)
│   │   └── models.py           # Database models for user authentication (User table, tokens)
│   ├── service/                # Main business logic for log processing
│   │   ├── __init__.py         # Initializes the service Blueprint
│   │   ├── routes.py           # Defines routes related to log parsing and processing
│   │   └── models.py           # Database models for storing parsed logs, user interactions
│   ├── templates/              # HTML templates for rendering the web interface
│   │   ├── Auth.html           # Login/Register page template
│   │   ├── Home.html           # Home page template
│   │   └── Index.html          # Main index page template
│   └── logging_service/        # Handles log parsing, storage, and analytics
│       ├── __init__.py         # Initializes the logging service Blueprint
│       ├── logic.py            # These will contain the Log for our application
│       └── log_storage/        # Stores processed log data (Consider using SQLite/Redis)
└── docker-compose.yml          # Docker Compose configuration for running the app with dependencies (DB, Redis, etc.)
