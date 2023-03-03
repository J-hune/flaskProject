from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from blueprints.api.routes import api
from events import connect, disconnect

app = Flask(__name__)
app.register_blueprint(api)
app.secret_key = "4f75177439a4bb0b5494d3ce5fd4727fe7b0d61d17ffd81d6420e40c9dc7d9da"

cors = CORS(
    app, resources={r"/*": {"origins": "http://localhost:8080"}},
    supports_credentials=True
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SAMESITE="Lax"
)

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, async_mode='eventlet')

socketio.on_event('connect', connect)
socketio.on_event('disconnect', disconnect)

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
