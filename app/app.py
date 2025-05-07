from flask import Flask, render_template
import templates
from routes.home import home_bp
from routes.cipher_routes.autokey_route import autokey_bp
from routes.cipher_routes.affine_route import affine_bp
from routes.cipher_routes.playfair_route import playfair_bp
from routes.cipher_routes.Route_Vigenere_standard import Vigenere_bp
from routes.cipher_routes.hill_route import hill_bp

app = Flask(__name__, template_folder='templates')

app.register_blueprint(home_bp)
app.register_blueprint(autokey_bp)
app.register_blueprint(affine_bp)
app.register_blueprint(playfair_bp)
app.register_blueprint(Vigenere_bp)
app.register_blueprint(hill_bp)

if __name__ == "__main__":
    app.run(debug=True)