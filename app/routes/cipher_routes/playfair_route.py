from flask import Blueprint, render_template, request, redirect, url_for, send_file
import io
from ciphers.playfair_cipher import PlayfairCipher
from werkzeug.utils import secure_filename

playfair_bp = Blueprint('playfair', __name__)

@playfair_bp.route('/playfair-cipher', methods=['GET', 'POST'])
def playfair():
    mode = request.args.get('mode', 'encrypt')
    encrypt = True if mode == 'encrypt' else False

    result_ciphertext = None
    result_plaintext = None
    error = None

    if request.method == 'POST':
        if encrypt:
            return redirect(url_for('playfair.playfairEncrypt'))
        else:
            return redirect(url_for('playfair.playfairDecrypt'))

    return render_template('pages/playfair_page.html', 
                           encrypt=encrypt,
                           result_ciphertext=result_ciphertext,
                           result_plaintext=result_plaintext,
                           error=error,
                           form=request.form)

@playfair_bp.route('/playfair-cipher/encrypt', methods=['POST'])
def playfairEncrypt():
    try:
        key = request.form.get('key', '').strip()
        plaintext = request.form.get('plaintext', '').strip()
        file = request.files.get('file-plaintext')
        format_mode = request.form.get('format', 'normal')

        file_text = ''
        if not plaintext and file:
            content = file.read()
            try:
                file_text = content.decode('utf-8').strip()
            except UnicodeDecodeError:
                raise ValueError("File tidak dapat dibaca sebagai teks (bukan file teks UTF-8).")

            plaintext = file_text  # overwrite kosong

        if not key:
            raise ValueError("Key tidak boleh kosong.")
        if not plaintext:
            raise ValueError("Plaintext tidak boleh kosong (baik dari form maupun file).")

        cipher = PlayfairCipher(key=key, plaintext=plaintext)
        result = cipher.encrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/playfair_page.html',
                               encrypt=True,
                               result_ciphertext=formatted_result,
                               result_plaintext=None,
                               form={'plaintext': plaintext, 'key': key})
    except Exception as e:
        return render_template('pages/playfair_page.html',
                               encrypt=True,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)

@playfair_bp.route('/playfair-cipher/decrypt', methods=['POST'])
def playfairDecrypt():
    try:
        key = request.form.get('key', '').strip()
        ciphertext = request.form.get('ciphertext', '').strip()
        file = request.files.get('file-ciphertext')
        format_mode = request.form.get('format', 'normal')

        file_text = ''
        if not ciphertext and file:
            content = file.read()
            try:
                file_text = content.decode('utf-8').strip()
            except UnicodeDecodeError:
                raise ValueError("File tidak dapat dibaca sebagai teks (bukan file teks UTF-8).")

            ciphertext = file_text

        if not key:
            raise ValueError("Key tidak boleh kosong.")
        if not ciphertext:
            raise ValueError("Ciphertext tidak boleh kosong (baik dari form maupun file).")

        cipher = PlayfairCipher(key=key, ciphertext=ciphertext)
        result = cipher.decrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/playfair_page.html',
                               encrypt=False,
                               result_plaintext=formatted_result,
                               result_ciphertext=None,
                               form={'ciphertext': ciphertext, 'key': key})
    except Exception as e:
        return render_template('pages/playfair_page.html',
                               encrypt=False,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)


@playfair_bp.route('/playfair-cipher/download', methods=['POST'])
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

