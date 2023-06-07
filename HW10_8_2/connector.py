import configparser
import pathlib

from mongoengine import connect



db_name = 'mail_test'


file_config = pathlib.Path(__file__).parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
cache_prefix = config.get('DEV_DB', 'PREFIX')

# Подключение к MongoDB
connection = connect(host=f"mongodb+srv://{username}:{password}@testcluster.7cbltnk.mongodb.net/?retryWrites=true&w=majority")

#list_of_collections = connection.get_database(db_name).list_collection_names()

