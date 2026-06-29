import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_mail import Mail

from config import Config
from database.db import init_db
from routes.contact_routes import contact_bp

mail = Mail()

# Database table create/update on app start
init_db()

app = Flask(__name__, template_folder="template")
app.config.from_object(Config)

CORS(app)
mail.init_app(app)
app.register_blueprint(contact_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
