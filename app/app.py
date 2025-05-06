from flask import Flask, render_template
import templates
from routes.home import home_bp
from routes.cipher_routes.autokey_route import autokey_bp
<<<<<<< HEAD
from routes.cipher_routes.playfair_route import playfair_bp
=======
from routes.cipher_routes.Route_Vigenere_standard import Vigenere_bp
>>>>>>> 46b0b698ee45abedcca6f2cf03a0c861cd303509


app = Flask(__name__, template_folder='templates')

app.register_blueprint(home_bp)
app.register_blueprint(autokey_bp)
<<<<<<< HEAD
app.register_blueprint(playfair_bp)

=======
app.register_blueprint(Vigenere_bp)
>>>>>>> 46b0b698ee45abedcca6f2cf03a0c861cd303509

if __name__ == "__main__":
    app.run(debug=True)