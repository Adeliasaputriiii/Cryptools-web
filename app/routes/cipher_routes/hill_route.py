from flask import Blueprint, render_template, request, redirect, url_for, send_file
import io
from ciphers.hill_cipher import HillCipher  # Mengimpor HillCipher yang sudah mencakup metode parse_key_matrix

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
            return redirect(url_for('hill.hillCipherEncrypt'))
        else:
            return redirect(url_for('hill.hillCipherDecrypt'))

    return render_template('pages/hill_page.html',
                           encrypt=encrypt,
                           result_ciphertext=result_ciphertext,
                           result_plaintext=result_plaintext,
                           error=error,
                           form=request.form)

@hill_bp.route('/hill-cipher/encrypt', methods=['POST'])
def hillCipherEncrypt():
    try:
        key_input = request.form.get('key', '').strip()
        plaintext = request.form.get('plaintext', '').strip()
        format_mode = request.form.get('format', 'normal')  # Ambil format

        # Validasi dan parsing key matrix melalui kelas HillCipher
        cipher = HillCipher(key_string=key_input)
        encrypted_text = cipher.encrypt(plaintext)

        formatted_result = format_result(encrypted_text, format_mode)

        return render_template('pages/hill_page.html',
                               encrypt=True,
                               result_ciphertext=formatted_result,
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
def hillCipherDecrypt():
    try:
        key_input = request.form.get('key', '').strip()
        ciphertext = request.form.get('ciphertext', '').strip()
        format_mode = request.form.get('format', 'normal')  # Ambil format

        cipher = HillCipher(key_string=key_input)
        decrypted_text = cipher.decrypt(ciphertext)

        formatted_result = format_result(decrypted_text, format_mode)

        return render_template('pages/hill_page.html',
                               encrypt=False,
                               result_ciphertext=None,
                               result_plaintext=formatted_result,
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

    file_stream = io.StringIO(result_text)
    return send_file(
        io.BytesIO(file_stream.getvalue().encode()),
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

def format_result(text, mode):
    if mode == 'group5':
        cleaned = text.replace(" ", "")
        return ' '.join(cleaned[i:i+5] for i in range(0, len(cleaned), 5))
    return text.replace(" ", "")
