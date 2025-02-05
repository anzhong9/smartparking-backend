from flask import Flask
from flask_cors import CORS
from routes.checkin import checkin_bp
from routes.checkout import checkout_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(checkin_bp)
app.register_blueprint(checkout_bp)

if __name__ == "__main__":
    app.run(debug=True)
