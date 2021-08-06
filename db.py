import random

from flask import g, current_app
from pymongo import MongoClient

from ratings_sessions import COMPARE_TYPE

DB_NAME = "default_database"


def get_db(database_name):
    if 'db' not in g:
        client = MongoClient('localhost', 27017)

        # Getting the database instance
        g.db = client[database_name]
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_stuff(cur_type, db):
    """
    Gets entries from db for match ups
    """
    collection = db['entries']
    count = collection.countDocuments({})

    list_of_nums = [i for i in range(0, count)]

    vibes_coll = g.db['vibes']
    vibes_count = vibes_coll.countDocuments({})
    vibes_nums = [i for i in range(0, vibes_count)]

    #if cur_type ==

    if cur_type == COMPARE_TYPE.DIRECT:
        list_of_nums = [i for i in range(0, count)]
        choice_1 = list_of_nums.pop(random.choice(list_of_nums))
        choice_2 = random.choice(list_of_nums)

        entry_1 = collection.find_one({'id': choice_1})
        entry_2 = collection.find_one({'id': choice_2})

        vibe_choice = random.choice(vibes_nums)

        return (choice_1, choice_2), vibe_choice

    elif cur_type == COMPARE_TYPE.MULTI:
        max_multi = count
        end_range = min(max_multi, random.randint(1, 5))

        choices = []
        entries = []
        for i in range(0, end_range):
            pass
            cur_choice = list_of_nums.pop(random.choice(list_of_nums))
            cur_entry = collection.find_one({'id': cur_choice})

            choices.append(cur_choice)
            entries.append(cur_entry)

        vibe_choice = random.choice(vibes_nums)

        return choices, vibe_choice

    elif cur_type == COMPARE_TYPE.RATE:
        #count = collection.countDocuments({})
        choice = random.randint(0, count-1)
        vibe = random.randint(0, vibes_count-1)
        return (choice, vibe)

    elif cur_type == COMPARE_TYPE.TWO_VIBE:
        vibes_coll = g.db['vibes']

        entry_choice = list_of_nums.pop(random.choice(list_of_nums))

        vibes_choice_1 = vibes_nums.pop(random.choice(vibes_nums))
        vibes_choice_2 = random.choice(vibes_nums)

        return entry_choice, (vibes_choice_1, vibes_choice_2)