from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a JSON 404 status response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage on teardown."""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
