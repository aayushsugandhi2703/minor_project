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
│   ├── api/                  
│   │   ├── __init__.py         
│   │   └── routes.py           # Defines authentication-related routes (login, logout, register)
│   ├── service/                
│   │   ├── __init__.py         
│   │   └── routes.py           # Defines routes related to log parsing and processing
│   ├── test/                
│   │   ├── __init__.py         
│   │   └── test_functions.py   # Testing the functions  
│   ├── Forms/                
│   │   ├── __init__.py         
│   │   └── forms.py            # Defines WTForms for user authentication and other inputs
│   ├── Models/                
│   │   ├── __init__.py         
│   │   └── models.py           # Database models for user authentication (User table, tokens)
│   ├── Static/                
│   │   ├── img/                # Contain all images videos as per needed
│   │   └── css                 # contain all the css files
│   └── templates/              
│       ├── Auth.html           # Login/Register page template
│       └── Home.html           # Home page template
├── dockerfile                  
├── requirements.txt                  
└── docker-compose.yml          # Docker Compose configuration for running the app with dependencies
</pre>
</body>
</html>