# -*- coding: utf-8 -*-

import os
import sys
import base64
import subprocess

from random import randint

# base64 string could contains /, which is invalid for a file name, we need to replace it with ! 
special_character={"key":'/',"value":'!'}

def encrypt(plain_text):
    return base64.b64encode(plain_text.encode('utf-8')).decode().replace(special_character.get('key'),special_character.get('value'))

def decrypt(encrypted_text):
    return base64.b64decode(encrypted_text.replace(special_character.get('value'),special_character.get('key'))).decode('utf-8')

def get_all_sub_folders(target_path):
    folders=[]
    for root, dirnames, filenames in os.walk(target_path):
        for dirname in dirnames:
            folders.append({"root":root,"dir":dirname})
    # prapre for renaming folders, rename deeper folders firstly
    folders.reverse()
    return folders

def rename_all_sub_folders(target_path,handler):
    for f in get_all_sub_folders(target_path):
        dirPath=os.path.join(f.get('root'), f.get('dir'))
        new_dirPath=os.path.join(f.get('root'), handler(f.get('dir')))
        os.rename(dirPath,new_dirPath)
    
def rename_all_files(target_path,handler):
    for root, dirnames, filenames in os.walk(target_path):
        for filename in filenames:
            filePath=os.path.join(root, filename)
            print('filename',filename)
            newFileName=handler(filename)
            print('newFileName',newFileName)
            newFilePath=os.path.join(root, newFileName)
            print('newFilePath',newFilePath)
            os.rename(filePath,newFilePath)

def encrypt_folder(target_path):
    rename_all_sub_folders(target_path,encrypt)
    rename_all_files(target_path,encrypt)

def decrypt_folder(target_path):
    rename_all_sub_folders(target_path,decrypt)
    rename_all_files(target_path,decrypt)

def random_play(target_path):
    all_files=[]
    videoTypes = ['.mp4', '.rmvb', '.avi', '.m4v', '.xltd', '.wmv', 'mkv', '.smi', '.mpg', '.rm', '.flv']
    for root, dirnames, filenames in os.walk(target_path):
        for filename in filenames:
            filename_without_extension, file_extension = os.path.splitext(filename.lower())
            if file_extension in videoTypes:
                filePath=os.path.join(root, filename)
                all_files.append(filePath)
    print('haha: '+str(len(all_files)))
    index=randint(0,len(all_files))
    subprocess.call(['D:\\Program Files (x86)\\Tencent\\QQPlayer\\QQPlayer.exe', all_files[index]])

def get_random_picture(target_path):
    all_files=[]
    picture_types = ['.jpg','.png']
    for root, dirnames, filenames in os.walk(target_path):
        for filename in filenames:
            filename_without_extension, file_extension = os.path.splitext(filename.lower())
            if file_extension in picture_types:
                filePath=os.path.join(root, filename)
                all_files.append(filePath)
    index=randint(0,len(all_files))
    print('index:%s'%index)
    print('len:%s'%len(all_files))
    return all_files[index]

def random_play_picture(target_path):
    subprocess.call(["C:\\Program Files\\Internet Explorer\\iexplore.exe",get_random_picture()])

def main(argv):
    target_path='D:\\PUA\\new\\自拍'
    if len(argv)>0:
        func_dicts={"d":decrypt_folder,
         "e":encrypt_folder,
         "r":random_play,
         "rp":random_play_picture }
        if argv[0] in func_dicts:
            func_dicts[argv[0]](target_path);
        else:
            print('invalid parameters')    
    else:
        print('parameters are required')

if __name__=='__main__':
    main(sys.argv[1:])