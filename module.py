from Crypto import Random
from Crypto.Cipher import AES
import os
import sys
import os.path
from os import listdir
from os.path import isfile, join
import time
import common
import base64
import hashlib


def pad(byte_array):
    BLOCK_SIZE = 16
    pad_len = BLOCK_SIZE - len(byte_array) % BLOCK_SIZE
    return byte_array + (bytes([pad_len]) * pad_len)


def encrypt(key, message):
    try:
        byte_array = message
        padded = pad(byte_array)
        iv = base64.b64decode(key)
        cipher = AES.new( key, AES.MODE_OFB,iv)
        encrypted = cipher.encrypt(padded)
        return(encrypted)
    except Exception as e :
        error = common.get_error_traceback(sys,e)
        print (error)


def decrypt(key, message):
    try:
        byte_array = message
        iv = base64.b64decode(key)
        messagebytes = byte_array
        cipher = AES.new(key.encode("UTF-8"), AES.MODE_OFB, iv)
        decrypted_padded = cipher.decrypt(messagebytes)
        return decrypted_padded
    except Exception as e :
        error = common.get_error_traceback(sys,e)
        print (error)



def aes_encrypt_file(file_name,secret_key):
    '''
    Encrypt Video File Script
    '''
    try:
        key = secret_key
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = encrypt(message=plaintext,key=key)
        with open(file_name.replace('.mp4', '').replace('.m4v', '') + ".nsf", 'wb') as fo:  
            fo.write(enc)
        os.remove(file_name)
        pass
    except Exception as e :
        error = common.get_error_traceback(sys,e)
        print (error)
        raise


def aes_decrypt_file(file_name,secret_key):
    '''
    Decrypt Video File Script
    '''
    try:
        key = secret_key
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = decrypt(message=ciphertext, key=key)
        with open(file_name[:-4] +'.mp4', 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)
        pass
    except Exception as e :
        error = common.get_error_traceback(sys,e)
        print (error)



def get_all_files(args):
    dir_path = os.path.dirname(os.path.realpath(args))
    # target_folder = dir_path +"/"+ args 
    dirs = []
    for dirName, subdirList, fileList in os.walk(dir_path):
        for fname in fileList:
            vide_format = ('.mp4', '.m4v','.webm', '.mkv','.flv', '.vob	', '.avi','m4p', '.svi', '.3gp', '.nsf')
            if (fname.lower().endswith(vide_format)):
                dirs.append(dirName + "/" + fname)
    return dirs


def get_all_files_dec(args):
    dir_path = os.path.dirname(os.path.realpath(args))
    # target_folder = dir_path +"/"+ args 
    dirs = []
    for dirName, subdirList, fileList in os.walk(dir_path):
        for fname in fileList:
            vide_format = ('.nsf')
            if (fname.lower().endswith(vide_format)):
                dirs.append(dirName + "/" + fname)
    return dirs


def aes_encrypt_all_files(args,secret_key):
    dirs = get_all_files(args)
    for file_name in dirs:
        aes_encrypt_file(file_name,secret_key=secret_key)


    
def aes_decrypt_all_files(args,secret_key):
    dirs = get_all_files_dec(args)
    for file_name in dirs:
        aes_decrypt_file(file_name,secret_key=secret_key)
