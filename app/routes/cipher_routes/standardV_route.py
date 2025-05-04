from flask import Blueprint, render_template

autokey_bp = Blueprint('autokey',__name__)

@autokey_bp.route('/ciphers/standard vigenere cipher')
def autokey():
    return render_template('layout base/base_cipher.html', title='Standard Vigenere Cipher')

