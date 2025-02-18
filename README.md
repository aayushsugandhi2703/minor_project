# Cloud based automated Nginx logs parser

<html>
<head></head>
<body>
<h2>This will be the structure of Application</h2>
<pre>
Parser/
├── setup.py                    # Python package setup file
├── secrets.py                  # Stores sensitive credentials (database URL, API keys, secret keys)
├── config.py                   # Configuration file (settings for Flask, database, logging)
├── run.py                      # Entry point for the Flask application
├── app/
│   ├── __init__.py             # Initializes the Flask app and registers Blueprints
│   ├── Forms.py                # Defines WTForms for user authentication and other inputs
│   ├── models.py           # Database models for user authentication (User table, tokens)
│   ├── auth/                  
│   │   ├── __init__.py         
│   │   └── routes.py           # Defines authentication-related routes (login, logout, register)
│   ├── service/                
│   │   ├── __init__.py         
│   │   └── routes.py           # Defines routes related to log parsing and processing
│   ├── test/                
│   │   ├── __init__.py         
│   │   └── test_functions.py   # Testing the functions  
│   ├── function/                
│   │   ├── __init__.py         
│   │   └── functions.py        # Reusable function for APIs
│   └── templates/              
│       ├── Auth.html           # Login/Register page template
│       ├── Home.html           # Home page template
│       └── Index.html          # Main index page template
├── dockerfile                  
└── docker-compose.yml          # Docker Compose configuration for running the app with dependencies
</pre>
</body>
</html>