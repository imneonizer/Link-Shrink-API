export HOST="0.0.0.0"
export PORT=8080
export DEBUG=False
export DOMAIN="http://localhost:8080"

# For development use (simple logging, etc):
# python app.py

# For production use:
gunicorn --bind $HOST:$PORT -w 1 --log-file - app:app