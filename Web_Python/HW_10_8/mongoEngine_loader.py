import argparse
import pathlib
import re

import json

from mongoengine import *
from mongoengine.connection import disconnect

from HW_10_8.models import Authors, Quotes


coll_name1 = 'authors'
coll_name2 = 'quotes'

"""
Спрацює лише у папці з файлом :)
"""

def main():
    #print("MAIN")

    arg_name = input("\nPlease input your javascript file (only one): ")
    input_name = re.findall(r"[\w']+", arg_name)[0]

    arg_name = pathlib.Path(arg_name).absolute()
    print(arg_name, input_name)
    
    if coll_name1 == input_name:
        with open(arg_name, 'r', encoding="utf-8") as f:
            file_data = json.load(f)
            print(type(file_data))

            for jsonOb in file_data:

                author_subst = Authors(**jsonOb)

                print("---------------------------------------")
                
                author_subst.save()
    
    if coll_name2 == input_name:
        with open(arg_name, 'r', encoding="utf-8") as f:
            file_data = json.load(f)
            print(type(file_data))

            for jsonOb in file_data:

                quotes_subst = Quotes(**jsonOb)
                print(quotes_subst['author'])
                aut = Authors.objects(fullname__contains=(quotes_subst['author'])).first()

                quotes_subst.author_ref = aut

                
                print("---------------------------------------")
                
                quotes_subst.save()
    
    
    #disconnect()
    
if __name__ =='__main__':
    main()

