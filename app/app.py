from flask import Flask, render_template
import templates
from routes.home import home_bp
from routes.cipher_routes.autokey_route import autokey_bp
<<<<<<< HEAD
from routes.cipher_routes.Extended_route import extended_bp
=======
from routes.cipher_routes.affine_route import affine_bp
from routes.cipher_routes.playfair_route import playfair_bp
from routes.cipher_routes.Route_Vigenere_standard import Vigenere_bp
from routes.cipher_routes.hill_route import hill_bp
>>>>>>> 6b1f72f18d78ff0c831226a3f318a2c87efd617a

app = Flask(__name__, template_folder='templates')

app.register_blueprint(home_bp)
app.register_blueprint(autokey_bp)
<<<<<<< HEAD
app.register_blueprint(extended_bp)
=======
app.register_blueprint(affine_bp)
app.register_blueprint(playfair_bp)
app.register_blueprint(Vigenere_bp)
app.register_blueprint(hill_bp)
>>>>>>> 6b1f72f18d78ff0c831226a3f318a2c87efd617a

if __name__ == "__main__":
    app.run(debug=True)