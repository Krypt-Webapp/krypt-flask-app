import os, sys
from flask import jsonify
import pathlib
import zipfile

UPLOAD_FOLDER = pathlib.Path(__file__).parent.absolute()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mp3', 'mkv', 'm4v', 'mp4', 'nsf', 'zip'}


def send_error_msg(param={}):
    param['Sucess'] : False
    return jsonify(param), 500


def send_sucess_msg(param = {}):
    try:
        param['Sucess'] = True
        return jsonify(param), 200
    except Exception as e:
        print (e)


def get_error_traceback(sys, e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return "%s || %s || %s || %s" %(exc_type, fname, exc_tb.tb_lineno,e)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def ziper_(folder, filename):
    zipf = zipfile.ZipFile(filename+'_nsf.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder, zipf)
    zipf.close()

def ziper_dec(folder, filename):
    zipf = zipfile.ZipFile(filename+'decrypted.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder, zipf)
    zipf.close()


def file_remover():
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".zip"):
            os.remove(filename)
        else:
            continue

def file_remove_for_videos():
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".nsf"):
            os.remove(filename)
        else:
            continue

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
