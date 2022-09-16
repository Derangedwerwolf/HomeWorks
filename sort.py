from asyncio import constants
from pathlib import Path
import os
import re
import shutil
import sys
import CONSTANS


def normalize(file_name):
    for old_file_name in file_name.iterdir():
        
        if old_file_name.is_dir() and any(Path(old_file_name).iterdir()):
            normalize(old_file_name)
        
        new_name = os.path.basename(old_file_name).translate(CONSTANS.TRANS)
        new_name = re.sub(r'[!@#$%^&*]', "_", new_name)
        old_file_name.rename(os.path.join(os.path.dirname(old_file_name),new_name))

def search_list(name, path_to_folder):
    indx = 0
    for file_category in CONSTANS.FILES_COLLECTIONS.values():
        for file_extension in file_category:
            if name.lower() == file_extension.lower():
                add_path = list(CONSTANS.FILES_COLLECTIONS)[indx]
                
                path_to_folder = path_to_folder.joinpath(add_path)
                
                if not os.path.exists(path_to_folder):
                    path_to_folder.mkdir()     

                return path_to_folder
        indx += 1
    return 0

def folder_sort(path_to_folder: Path, path_to_folder_origin: Path):
    for file in path_to_folder.iterdir():
        
        if file.is_dir():
            folder_sort(file, path_to_folder_origin)
            
            if not any(Path(file).iterdir()):
                file.rmdir()
        
        elif file.is_file():
            file_ext = (os.path.splitext(file))[-1].replace('.', '')
            file_transfer_to = search_list(file_ext, path_to_folder_origin)
            
            if file_transfer_to:
                file_new_holder = os.path.join(file_transfer_to, os.path.basename(file))
                os.replace(file, file_new_holder)
            
            if str(CONSTANS.FILES_COLLECTIONS['archives']).find(file_ext.upper()) != -1:
                new_archive_folder = os.path.join(file_transfer_to, os.path.basename(file).split('.')[0])
                old_path_to_file = os.path.join(file_transfer_to, os.path.basename(file))
                try:
                    shutil.unpack_archive(old_path_to_file, new_archive_folder)
                except TypeError:
                    print(f"{file_ext} is unsupported file format")
                    continue

def main():
    if len(sys.argv) < 2:
        print('Enter path tofolder which should be cleaned')
        exit()
    
    path_to_folder = Path(sys.argv[1])
    
    if not (os.path.exists(path_to_folder) and Path(path_to_folder).is_dir()):
        exit()
        
    normalize(path_to_folder)
    folder_sort(path_to_folder, path_to_folder)
    
if __name__ == '__main__':
    exit(main())
