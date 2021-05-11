from flask import Flask
from routes import app, socketio

if __name__ == "__main__":
    socketio.run(app, debug=True)