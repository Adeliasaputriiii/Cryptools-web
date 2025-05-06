from flask import Blueprint, render_template, request, redirect, url_for, send_file
import io
from ciphers.affine_cipher import AffineCipher  # Pastikan file AffineCipher class ada di folder ciphers

affine_bp = Blueprint('affine', __name__)

@affine_bp.route('/affine-cipher', methods=['GET', 'POST'])
def affineCipher():
    mode = request.args.get('mode', 'encrypt')
    encrypt = True if mode == 'encrypt' else False

    result_ciphertext = None
    result_plaintext = None
    error = None

    if request.method == 'POST':
        if encrypt:
            return redirect(url_for('affine.affineCipherEncrypt'))
        else:
            return redirect(url_for('affine.affineCipherDecrypt'))

    return render_template('pages/affine_chiper_page.html',
                           encrypt=encrypt,
                           result_ciphertext=result_ciphertext,
                           result_plaintext=result_plaintext,
                           error=error,
                           form=request.form)

@affine_bp.route('/affine-cipher/encrypt', methods=['POST'])
def affineCipherEncrypt():
    try:
        a = int(request.form.get('a', '').strip())
        b = int(request.form.get('b', '').strip())
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

            plaintext = file_text

        if not plaintext:
            raise ValueError("Plaintext tidak boleh kosong.")

        cipher = AffineCipher(a=a, b=b, plaintext=plaintext)
        result = cipher.encrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/affine_chiper_page.html',
                               encrypt=True,
                               result_ciphertext=formatted_result,
                               result_plaintext=None,
                               form={'plaintext': plaintext, 'a': a, 'b': b})
    except Exception as e:
        return render_template('pages/affine_chiper_page.html',
                               encrypt=True,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)

@affine_bp.route('/affine-cipher/decrypt', methods=['POST'])
def affineCipherDecrypt():
    try:
        a = int(request.form.get('a', '').strip())
        b = int(request.form.get('b', '').strip())
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

        if not ciphertext:
            raise ValueError("Ciphertext tidak boleh kosong.")

        cipher = AffineCipher(a=a, b=b, ciphertext=ciphertext)
        result = cipher.decrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/affine_chiper_page.html',
                               encrypt=False,
                               result_plaintext=formatted_result,
                               result_ciphertext=None,
                               form={'ciphertext': ciphertext, 'a': a, 'b': b})
    except Exception as e:
        return render_template('pages/affine_chiper_page.html',
                               encrypt=False,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)

@affine_bp.route('/affine-cipher/download', methods=['POST'])
def download_affine_result():
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
