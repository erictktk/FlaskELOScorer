""" This module factors out functions that are used for comparator """

from pymongo import MongoClient


def add_direct_comparison(db, vibe_id, a_id, b_id, index):
    collection = db['direct_results']
    count = collection.countDocuments({})

    doc = {'id': count, 'vibe_id': vibe_id, 'a_id': a_id, 'b_id': b_id}

    collection.insert_one(doc)


def add_multi_result(db, vibe_id, entry_ids, index):
    collection = db['representative_results']
    count = collection.countDocuments({})

    doc = {'vibe_id': vibe_id, 'entry_ids': entry_ids, 'index': index, "id": count}

    collection.insert_one(doc)


def add_vibe_rating(db, vibe_id, rating):
    collection = db['single_vibe_rating']

    count = collection.countDocuments({})

    doc = {'vibe_id': vibe_id, 'rating': rating, 'id': count}

    collection.insert_one(doc)


def comparison_vibe():
    pass


