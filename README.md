
THIS WILL BE GETTING UPDATED OVER TIME AS EACH NEW FEATURE IS PUT OUT

Secure Login App

This is a Flask based authentication app that I desployed to AWS using 
    Docker and PostgreSQL.

Features:
    User registration
    User login/logout
    Password hashing
    User profiles
    PostgreSQL database integration
    Docker containerization
    AWS EC2 deployment
    Gunicorn production server

Stack I used:
    Python
    Flask
    SQLAlchemy
    PostgreSQL (Neon)
    Docker
    AWS EC2
    Gunicorn
    GitHub

My local setup:
    1. I clone the repository
        git clone <repository-url> 
        cd secure-login-app
    
    2. Created a virtual environment
        python -m venv .venv

    3. Installing dependencies
        pip install -r requirements.txt

    4. Created a .env file
        Refer to .env.example for how my actual .env is set up
            The real one stays local and is set for .gitignore

    5. Running the app
        python app.py

Deployment:
    The app is contained with Docker and is deployed to AWS EC2
        while using Gunicorn as the application server.

Future Improvements:
    Google OAuth
    HTTPS / SSL
    Custom domain
    CI/CD with GitHub Actions
    Password reset functionality
    Profile image uploads
    Security monitoring