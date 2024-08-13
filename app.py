from flask import Flask, request, jsonify
import os
from uuid import uuid4
from helper import sender,zip_maker
app = Flask(__name__)


DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'speciality' not in request.form:
        return jsonify({'error': 'Speciality is required'}), 400

    speciality = request.form['speciality']
    phone = request.form['phone']
    diploma = request.files.get('diploma')
    passport = request.files.get('passport')
    certificate = request.files.get('certificate')
    sud = request.files.get('sud')

    if not diploma or not passport:
        return jsonify({'error': 'Diploma and passport are required'}), 400

    file_paths = []

    def save_file(file, folder):
        if file:
            # Fayl nomini olish
            original_filename = file.filename
            # Yangi fayl nomi yaratish (UUID bilan)
            new_filename = f"{uuid4().hex}_{original_filename}"
            filepath = os.path.join(folder, new_filename)
            file.save(filepath)
            return filepath
        return None


    diploma_path = save_file(diploma, DOWNLOAD_FOLDER)
    passport_path = save_file(passport, DOWNLOAD_FOLDER)
    certificate_path = save_file(certificate, DOWNLOAD_FOLDER) if certificate else None
    sud_path = save_file(sud, DOWNLOAD_FOLDER) if sud else None

    file_paths.extend(filter(None, [diploma_path, passport_path, certificate_path, sud_path]))
    zip_name = str(uuid4())+".zip"
    zip_file_path = zip_maker.zip_files(file_paths,zip_name)
    zip_caption = f"{speciality} : {phone}"
    sender.zip_sender(zip_file_path,zip_caption)
    return jsonify({'speciality': speciality, 'phone': phone, 'file_paths': file_paths,'zip': zip_file_path})

