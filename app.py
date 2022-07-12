import os, sys
import json
import zipfile
from os.path import dirname, join, abspath
from flask import Flask
from flask import Flask, jsonify, request, render_template,redirect,url_for,flash,send_file
from . import module
import common
from werkzeug.utils import secure_filename
import pathlib
import shutil
import base64


UPLOAD_FOLDER = pathlib.Path(__file__).parent.absolute()


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/generate_key')
def generate_key():
    key = os.urandom(16)
    enc_key = base64.b64encode(key)
    completeName = os.path.join(UPLOAD_FOLDER, "SecretKey"+".txt")         
    file1 = open(completeName, "w")
    toFile = str(enc_key.decode('UTF-8'))
    file1.write(toFile)
    file1.close()
    return send_file(completeName, as_attachment=True)


@app.route('/encrypt-folder', methods=['GET', 'POST'])
def upload_folder_encrypt():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            key = request.form['key']
            common.file_remover()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = str(pathlib.Path(__file__).parent.absolute())+'/' +filename
            unziper(path=file_path)
            nsf_folder = filename.replace('.zip', '')
            os.remove(file_path)
            name_of_file = key.encode('UTF_8')
            completeName = os.path.join(nsf_folder, "SecretKey"+".txt")         
            file1 = open(completeName, "w")
            toFile = str(key)
            file1.write(toFile)
            file1.close()
            module.aes_encrypt_all_files(nsf_folder,secret_key=name_of_file)
            nsf_path = str(UPLOAD_FOLDER)+'/' + nsf_folder
            common.ziper_(folder= nsf_path, filename=nsf_folder)
            download_path = str(UPLOAD_FOLDER)+ '/'+ nsf_folder+'_nsf.zip'
            path = download_path
            shutil.rmtree(nsf_path)
            return send_file(path, as_attachment=True)
    return render_template('encrypt_folder.html')


def unziper(path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(app.config['UPLOAD_FOLDER']))


@app.route('/encrypt-file', methods=['GET', 'POST'])
def upload_file_encrypt():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        common.file_remove_for_videos()
        file = request.files['file']
        key = request.form['key']
        sec_key = key.encode('UTF_8')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and common.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            module.aes_encrypt_file(file_name=filename,secret_key=sec_key)
            nsf_path = filename.replace('.mp4','')
            download_path = str(UPLOAD_FOLDER)+ '/'+ nsf_path+'.nsf'
            path = download_path
            return send_file(path, as_attachment=True)
            

    return render_template('encrypt_file.html')


@app.route('/decrypt-folder', methods=['GET', 'POST'])
def upload_folder_decrypt():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            key = request.form['key']
            common.file_remover()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = str(pathlib.Path(__file__).parent.absolute())+'/' +filename
            unziper(path=file_path)
            nsf_folder = filename.replace('.zip', '')
            os.remove(file_path)
            module.aes_decrypt_all_files(nsf_folder,secret_key=key)
            nsf_path = str(UPLOAD_FOLDER)+'/' + nsf_folder
            common.ziper_dec(folder= nsf_path, filename=nsf_folder)
            download_path = str(UPLOAD_FOLDER)+ '/'+ nsf_folder +'.zip'
            path = download_path
            return send_file(path, as_attachment=True)
    return render_template('decrypt_folder.html')



@app.route('/decrypt-file', methods=['GET', 'POST'])
def upload_file_decrypt():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        common.file_remove_for_videos()
        file = request.files['file']
        key = request.form['key']
        sec_key = key.encode('UTF_8')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and common.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            module.aes_decrypt_file(file_name=filename,secret_key=key)
            nsf_path = filename.replace('.nsf','')
            download_path = str(UPLOAD_FOLDER)+ '/'+ nsf_path+'.mp4'
            path = download_path
            return send_file(path, as_attachment=True)
    return render_template('decrypt_file.html')

if __name__ == "__main__":
    app.run(debug=True,host= '0.0.0.0', port='5000')




