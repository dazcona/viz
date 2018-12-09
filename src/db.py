#!/usr/bin/python

import sys
from pymongo import MongoClient
import random
from datetime import datetime
import config
import os


def get_db():
    """
    Set up MongoDB
    """

    db_uri = os.environ["DATABASE_URI"]
    db_name = os.environ["DATABASE_NAME"]
    username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

    uri = 'mongodb://%s:%s@mongo:27017' % (username, password)
    conn = MongoClient(uri)
    return conn[db_name]

def populate():
    """
    Inserts items to DB
    """
    db = get_db()

    if db.students.count() == 0:

        print('Generating data')

        items = [ 
            { 
                'name': random.choice(config.NAMES), 
                'activity': random.choice(config.ACTIVITY),
                'duration': random.randint(0, 10),
                'date': datetime(
                    year=2018, month=1, day=random.randint(1, 8), 
                    hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59)
                )
            } 
            for _ in range(config.NUM_ROWS)
        ]

        x = db.students.insert_many(items)

        print('Elements inserted on DB')


def get_student_names(offset):
    """
    Get student names
    """

    return get_db().students.distinct( "name" )[offset:offset + config.N_PER_PAGE]


def get_student_data(name, offset = 0):
    """
    Get student's data
    """

    return get_db().students.find(
        { "name": name }, # search criteria
        { "_id": 0, "date": 1, "duration": 1, "activity": 1 } # projection
    ).sort(
        "date", 1 # reverse: -1
    )


def get_student_rows(name, offset = 0):
    """
    Get student's rows
    """

    return get_db().students.find(
        { "name": name }, # search criteria
        { "_id": 0, "date": 1, "duration": 1, "activity": 1 } # projection
    ).sort(
        "date", 1 # reverse: -1
    ).skip(offset).limit(config.N_PER_PAGE)


def get_student_data_grouped(name):
    """
    Get student's data grouped
    """

    return get_db().students.aggregate(
        [
            {
                '$group' : {
                    '_id' : { 'month': { '$month': "$date" }, 
                                'day': { '$dayOfMonth': "$date" }, 
                                'year': { '$year': "$date" } 
                            },
                    'total_duration': { '$sum': '$duration' },
                    'average_duration': { '$avg': "$duration" },
                    'count': { '$sum': 1 }
                }
            }
        ]
    )

"""
    patterns = db.patterns.find().sort(
        "number", -1
    )

    paths = db.paths.find().sort(
        [
            ("pct_failed", -1),
            ("pct_success", -1)
        ]
    )

    assessments = db.assessments.find(
        { "student_name": student }
    ).sort(
        "end_time_ms", 1 # -1
    ).limit(N)
    # .skip(offset).limit(config.N_PER_PAGE)

"""