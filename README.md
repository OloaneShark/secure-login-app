
THIS WILL BE GETTING UPDATED OVER TIME AS EACH NEW FEATURE IS PUT OUT

Secure Login App

This is a Flask based authentication app that I desployed to AWS using 
    Docker and PostgreSQL.

Features:
    User registration
    User login/logout
    Password hashing
    Google OAuth login
    User profiles
    Role-based access control (Admin/User)
    Audit logging
    Login rate limiting
    Security headers
    PostgreSQL database integration
    Docker containerization
    AWS EC2 deployment
    Gunicorn production server
    Automated CI/CD pipeline
    Dependency vulnerability scanning
    Container vulnerability scanning

Security Features:
    Password hashing using Werkzeug
    Google OAuth authentication
    Role-based access control (RBAC)
    Audit logging for security events
    Login rate limiting against brute-force attacks
    Security response headers
    Dependency vulnerability scanning
    Container vulnerability scanning

Stack I Used:
    Python
    Flask
    SQLAlchemy
    PostgreSQL (Neon)
    Docker
    AWS EC2
    Gunicorn
    GitHub
    GitHub Actions
    Google OAuth
    pip-audit
    Trivy

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
    HTTPS / SSL
    Custom domain
    Password reset functionality
    Profile image uploads
    Advanced security monitoring
    Redis-backed rate limiting
    Nginx reverse proxy