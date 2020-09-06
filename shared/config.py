import os

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5000)
    
config = dict(
    URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite3"),
    # URI="sqlite:///:memory:",
    DEBUG = True if os.environ.get("DEBUG") else False,
    HOST = HOST,
    PORT = PORT,
    DOMAIN = os.environ.get("DOMAIN", f"http://{HOST}:{PORT}"),
)