from flask import Blueprint, render_template, request, redirect, url_for, send_file
import io
from ciphers import hill_cipher
from werkzeug.utils import secure_filename

hill_bp = Blueprint('hill', __name__)

@hill_bp.route('/hill-cipher', methods=['GET', 'POST'])
def hillCipher():
    mode = request.args.get('mode', 'encrypt')
    encrypt = True if mode == 'encrypt' else False

    result_ciphertext = None
    result_plaintext = None
    error = None

    if request.method == 'POST':
        if encrypt:
            return redirect(url_for('hill.hillEncrypt'))
        else:
            return redirect(url_for('hill.hillDecrypt'))

    return render_template('pages/hill_page.html', 
                           encrypt=encrypt,
                           result_ciphertext=result_ciphertext,
                           result_plaintext=result_plaintext,
                           error=error,
                           form=request.form)

@hill_bp.route('/hill-cipher/encrypt', methods=['POST'])
def hillEncrypt():
    try:
        key = request.form.get('key', '').strip()
        plaintext = request.form.get('plaintext', '').strip()
        file = request.files.get('file-plaintext')
        format_mode = request.form.get('format', 'nospace')

        file_text = ''
        if not plaintext and file:
            content = file.read()
            try:
                file_text = content.decode('utf-8').strip()
            except UnicodeDecodeError:
                raise ValueError("File harus dalam format UTF-8.")
        text_to_encrypt = plaintext if plaintext else file_text

        if not key or not text_to_encrypt:
            raise ValueError("Key dan Plaintext harus diisi.")

        result_ciphertext = hill_cipher.encrypt_text(text_to_encrypt, key, format_mode)

        return render_template('pages/hill_page.html', 
                               encrypt=True,
                               result_ciphertext=result_ciphertext,
                               result_plaintext=None,
                               error=None,
                               form=request.form)
    except Exception as e:
        return render_template('pages/hill_page.html', 
                               encrypt=True,
                               result_ciphertext=None,
                               result_plaintext=None,
                               error=str(e),
                               form=request.form)

@hill_bp.route('/hill-cipher/decrypt', methods=['POST'])
def hillDecrypt():
    try:
        key = request.form.get('key', '').strip()
        ciphertext = request.form.get('ciphertext', '').strip()
        file = request.files.get('file-ciphertext')

        file_text = ''
        if not ciphertext and file:
            content = file.read()
            try:
                file_text = content.decode('latin1').strip()
            except UnicodeDecodeError:
                raise ValueError("File harus dalam format latin1.")
        text_to_decrypt = ciphertext if ciphertext else file_text

        if not key or not text_to_decrypt:
            raise ValueError("Key dan Ciphertext harus diisi.")

        result_plaintext = hill_cipher.decrypt_text(text_to_decrypt, key)

        return render_template('pages/hill_page.html', 
                               encrypt=False,
                               result_ciphertext=None,
                               result_plaintext=result_plaintext,
                               error=None,
                               form=request.form)
    except Exception as e:
        return render_template('pages/hill_page.html', 
                               encrypt=False,
                               result_ciphertext=None,
                               result_plaintext=None,
                               error=str(e),
                               form=request.form)

@hill_bp.route('/hill-cipher/download', methods=['POST'])
def download_result():
    result_text = request.form.get('result', '')
    filename = request.form.get('filename', 'hasil.txt')

    # Buat file teks di memory
    file_stream = io.StringIO(result_text)
    return send_file(
        io.BytesIO(file_stream.getvalue().encode()),
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

def format_result(text, mode):
    if mode == 'group5':
        cleaned = text.replace(" ", "")  # hilangkan spasi dulu
        return ' '.join(cleaned[i:i+5] for i in range(0, len(cleaned), 5))
    return text.replace(" ", "")