import os
from app import create_app

# Create application instance
app = create_app(os.environ.get("FLASK_APP", "production"))

if __name__ == "__main__":
    app.run()
