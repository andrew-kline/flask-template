import os
from app import create_app

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host=host, port=port)
