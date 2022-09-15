from pathlib import Path
import os
import re
import shutil
import sys

TRANS = {
    1072: 'a' , 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 
    1042: 'V' , 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 
    1077: 'e' , 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 
    1046: 'J' , 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 
    1081: 'j' , 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 
    1051: 'L' , 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 
    1086: 'o' , 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 
    1056: 'R' , 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 
    1091: 'u' , 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 
    1061: 'H' , 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 
    1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 
    1066: ''  , 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 
    1101: 'e' , 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 
    1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 
    1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
}

files_collections = {
    'images'   : ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video'    : ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio'    : ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives' : ['ZIP', 'GZ', 'TAR']
}

def normalize(file_name):
    for jjj in file_name.iterdir():
        
        if jjj.is_dir() and any(Path(jjj).iterdir()):
            normalize(jjj)
        
        new_name = (os.path.basename(jjj).translate(TRANS))
        new_name = re.sub(r'[!@#$%^&*]', "", new_name)
        jjj.rename( os.path.dirname(jjj) + '/' + new_name)

def search_list(name):
    indx = 0
    for file_category in files_collections.values():
        for iii in file_category:
            if name.lower() == iii.lower():
                add_path = list(files_collections.keys())[indx]
                
                if not (os.path.exists(path_to_folder/add_path)):
                    (path_to_folder/add_path).mkdir()        

                return (path_to_folder/add_path)
        indx += 1
    return 0

def folder_sort(path_to_folder):
    for iii in path_to_folder.iterdir():
        
        if iii.is_dir():
            folder_sort(iii)
            
            if not any(Path(iii).iterdir()):
                iii.rmdir()
        
        elif iii.is_file():
            file_ext = (os.path.splitext(iii))[-1].replace('.', '')
            file_transfer_to = search_list(file_ext)
            
            if file_transfer_to:
                os.replace(path_to_folder/iii, file_transfer_to/os.path.basename(iii))
            
            if str(files_collections['archives']).find(file_ext.upper()) != -1:
                new_archive_folder = os.path.basename(iii).split('.')[0]

                shutil.unpack_archive(file_transfer_to/iii, file_transfer_to/new_archive_folder)

def main():
    if len(sys.argv) < 2:
        print('Enter path tofolder which should be cleaned')
        exit()
    
    path_to_folder = sys.argv[1]
    
    if not (os.path.exists(path_to_folder) and Path(path_to_folder).is_dir()):
        exit()
    
    folder_sort(path_to_folder)
    
if __name__ == '__main__':
    exit(main())
