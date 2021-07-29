import os.path
import argparse

import os
import sys

from pymongo import MongoClient

parser = argparse.ArgumentParser(description="Setup OR modify a nosql database with directories for file entries OR a vibe to rate against")
parser.add_argument('FolderPath', metavar='folderPath', type=str, help="path to folder with entries")  # optional argument
parser.add_argument('-d', '--database', type=str, help="optional database name", default="mydb")
parser.add_argument('-v', '--vibes', type=str, nargs='?', help="to add to vibes list")  # optional argument
parser.add_argument('--delete', type=str, nargs='?', help="to attempt to remove vibe from database")

args = parser.parse_args()

folder_path = args.FolderPath


if not os.path.isdir(folder_path):
    print('The path specified for the folder does not exist')
    sys.exit()


def get_database(folder_path, database_name):
    # Cerating a pymongo client
    client = MongoClient('localhost', 27017)

    # Getting the database instance
    db = client[database_name]

    return db


def add_vibes_to_database(vibes_list, database_name):
    client = MongoClient('localhost', 27107)

    db = client[database_name]

    #vibes_list = [ ]

    collection = db['vibes_collection']
    count = collection.countDocuments({})
    for vibe in vibes_list:
        vibe_lower = vibe.lower()
        if not collection.find_one({'name'}, vibe_lower):
            cur_doc = {'name': vibe_lower, 'id': count }
            collection.insert(cur_doc)

            count += 1


def remove_vibe_from_database(vibes_list, database_name):
    pass


###images###?
def add_directory_to_database(directory, database_name):
    client = MongoClient('localhost', 27107)

    db = client[database_name]

    collection = db['entry_collection']
    count = collection.countDocuments({})

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if not collection.find_one({"fullPath": full_path}):
            cur_doc = {'fullPath': full_path, 'entry': entry, 'id': count}
            collection.insert_one(cur_doc)

            count += 1


if __name__ == "__main__":
    pass
