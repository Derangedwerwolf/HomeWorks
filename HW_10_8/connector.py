import argparse

import configparser
import pathlib

from mongoengine import connect


db_name = 'test'


file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')

connection = connect(host=f"mongodb+srv://{username}:{password}@testcluster.7cbltnk.mongodb.net/?retryWrites=true&w=majority")
list_of_collections = connection.get_database(db_name).list_collection_names()

print(f"\nCollections in '{db_name}' db : ", list_of_collections, "\n")

"""list_len = len(list_of_collections)

if list_len > 1:
    #input(f"Please choose your collection from 1 to {list_len} to choose your collection for save : ")
    input(f"Please choose your collection from 1 to {list_len} to choose your collection for search : ")
else:
    print("There are no your's collections in DB.")"""
