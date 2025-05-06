from flask import Flask, render_template
import templates
from routes.home import home_bp
from routes.cipher_routes.autokey_route import autokey_bp
from routes.cipher_routes.Route_Vigenere_standard import Vigenere_bp


app = Flask(__name__, template_folder='templates')

app.register_blueprint(home_bp)
app.register_blueprint(autokey_bp)
app.register_blueprint(Vigenere_bp)

if __name__ == "__main__":
    app.run(debug=True)