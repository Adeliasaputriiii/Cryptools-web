from flask import Blueprint, render_template, request, redirect, url_for, send_file
import io
from ciphers.extended_chiper import ExtendedVigenereCipher
from werkzeug.utils import secure_filename

extended_bp = Blueprint('extended', __name__)

@extended_bp.route('/extended-vigenere-cipher', methods=['GET', 'POST'])
def extendedVigenere():
    mode = request.args.get('mode', 'encrypt')
    encrypt = True if mode == 'encrypt' else False

    result_ciphertext = None
    result_plaintext = None
    error = None

    if request.method == 'POST':
        if encrypt:
            return redirect(url_for('extended.extendedVigenereEncrypt'))
        else:
            return redirect(url_for('extended.extendedVigenereDecrypt'))

    return render_template('pages/extended_page.html', 
                           encrypt=encrypt,
                           result_ciphertext=result_ciphertext,
                           result_plaintext=result_plaintext,
                           error=error,
                           form=request.form)

@extended_bp.route('/extended-vigenere-cipher/encrypt', methods=['POST'])
def extendedVigenereEncrypt():
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

        cipher = ExtendedVigenereCipher(key=key, plaintext=plaintext)
        result = cipher.encrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/extended_page.html',
                               encrypt=True,
                               result_ciphertext=formatted_result,
                               result_plaintext=None,
                               form={'plaintext': plaintext, 'key': key})
    except Exception as e:
        return render_template('pages/extended_page.html',
                               encrypt=True,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)

@extended_bp.route('/extended-vigenere-cipher/encrypt-byte', methods=['POST'])
def extendedVigenereEncryptByte():
    try:
        key = request.form.get('key', '').strip()
        file = request.files.get('file-plaintext')

        if not key:
            raise ValueError("Key tidak boleh kosong.")
        if not file:
            raise ValueError("File harus diunggah untuk mode byte.")

        data = file.read()
        cipher = ExtendedVigenereCipher(key=key, plaintext=data)
        encrypted_bytes = cipher.encryptByte()

        original_name = file.filename.replace(".enc", "")
        return send_file(
            io.BytesIO(encrypted_bytes),
            as_attachment=True,
            download_name=original_name,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        return f"Gagal enkripsi byte: {str(e)}", 400
    
@extended_bp.route('/extended-vigenere-cipher/decrypt', methods=['POST'])
def extendedVigenereDecrypt():
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

        cipher = ExtendedVigenereCipher(key=key, ciphertext=ciphertext)
        result = cipher.decrypt()
        formatted_result = format_result(result, format_mode)

        return render_template('pages/extended_page.html',
                               encrypt=False,
                               result_plaintext=formatted_result,
                               result_ciphertext=None,
                               form={'ciphertext': ciphertext, 'key': key})
    except Exception as e:
        return render_template('pages/extended_page.html',
                               encrypt=False,
                               error=str(e),
                               result_ciphertext=None,
                               result_plaintext=None,
                               form=request.form)

@extended_bp.route('/extended-vigenere-cipher/decrypt-byte', methods=['POST'])
def extendedVigenereDecryptByte():
    try:
        key = request.form.get('key', '').strip()
        file = request.files.get('file-ciphertext')

        if not key:
            raise ValueError("Key tidak boleh kosong.")
        if not file:
            raise ValueError("File harus diunggah untuk mode byte.")

        encrypted_data = file.read()
        cipher = ExtendedVigenereCipher(key=key, ciphertext=encrypted_data)
        decrypted_bytes = cipher.decryptByte()

        original_name = file.filename.replace(".enc", "")
        return send_file(
            io.BytesIO(decrypted_bytes),
            as_attachment=True,
            download_name=original_name or "decrypted_output",
            mimetype='application/octet-stream'
        )
    except Exception as e:
        return f"Gagal dekripsi byte: {str(e)}", 400


@extended_bp.route('/extended-vigenere-cipher/download', methods=['POST'])
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

