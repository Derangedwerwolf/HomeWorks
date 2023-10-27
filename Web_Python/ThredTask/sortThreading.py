from pathlib import Path
import os
import re
import shutil
import sys
from threading import Thread
import CONSTANTS


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, 
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return=None
        
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args):
        Thread.join(self)
        return self._return

def normalizer(file_handling_foo):
    
    def inner_search_list(*args, **kwargs):
        for old_file_name in args[0].iterdir():
        
            if old_file_name.is_dir() and any(Path(old_file_name).iterdir()):
                normalizer(old_file_name)
        
            new_name = os.path.basename(old_file_name).translate(CONSTANTS.TRANS)
            new_name = re.sub(r'[!@#$%^&*]', "_", new_name)
            old_file_name.rename(os.path.join(os.path.dirname(old_file_name),new_name))
            
        file_handling_foo(*args, **kwargs)
            
    return inner_search_list

def search_list(name, path_to_folder):
    indx = 0
    for file_category in CONSTANTS.FILES_COLLECTIONS.values():
        for file_extension in file_category:
            if name.lower() == file_extension.lower():
                add_path = list(CONSTANTS.FILES_COLLECTIONS)[indx]
                
                path_to_folder = path_to_folder.joinpath(add_path)
                
                if not os.path.exists(path_to_folder):
                    path_to_folder.mkdir()     

                return path_to_folder
        indx += 1
    return 0

@normalizer
def folder_sort(path_to_folder: Path, path_to_folder_origin: Path):
    for file in path_to_folder.iterdir():
        
        if file.is_dir():
            innerThread = ThreadWithReturnValue(target=folder_sort, args=(file, path_to_folder_origin), name='folderSorter')
            innerThread.start()
            innerThread.join()
            
            #folder_sort(file, path_to_folder_origin)
            
            if not any(Path(file).iterdir()):
                file.rmdir()
        
        elif file.is_file():
            file_ext = (os.path.splitext(file))[-1].replace('.', '')
            
            searchThread = ThreadWithReturnValue(target=search_list, args=(file_ext, path_to_folder_origin), name='fileTransferThread')
            searchThread.start()
            #searchThread.start()
            file_transfer_to = searchThread.join()
            
            if file_transfer_to:
                file_new_holder = os.path.join(file_transfer_to, os.path.basename(file))
                os.replace(file, file_new_holder)
                
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()
    
    path_to_folder = Path(sys.argv[1])
    
    if not (os.path.exists(path_to_folder) and Path(path_to_folder).is_dir()):
        exit()
    
    folder_sort(path_to_folder, path_to_folder)