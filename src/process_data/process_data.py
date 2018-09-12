import pymongo
from hidden.MongoDBKey import *
import json
import re
import logging
import datetime


def connect_mongodb(database_name, collection_name):
    """Connect to MongoDB

    Connect to MongoDB - database - collection, and then return it.

    Args:
        database_name: str, the name of database
        collection_name: str, the name of collection

    Returns:
        the collection in MongoDB, will create the collection if it doesn't exist

    Raises:
        OperationFailure: the host, user, or password information is wrong.
    """
    my_client = pymongo.MongoClient(AUTH["HOST"],
                                    username=AUTH['USER'],
                                    password=AUTH['PASSWORD'])
    my_db = my_client[database_name]
    my_collection = my_db[collection_name]
    return my_collection


def push_data_from_file(filename):
    """Upload data to MongoDB from JSON file

    Read data from a JSON file, and then upload
    all the data to MongoDB. If there is a course
    in database having same quarter, year, and
    CRN, the program will update the course.
    Otherwise, the program will insert a new
    course into database.

    Args:
        filename: str, the name of JSON file

    Returns:
        None

    Raises:
        FileNotFoundError: There is no such file or directory.
    """
    # load json file
    with open(filename) as json_file:
        json_dict = json.load(json_file)

    # upload data to MongoDB
    push_data_to_mongodb(json_dict)


def push_data_to_mongodb(json_dict):
    """Create/update data to MongoDB from raw data

    If there is a course in database having same quarter,
    year, and CRN, the program will update the course.
    Otherwise, the program will insert a new course into
    database.

    Args:
        json_dict: dict, the dict generated from JSON file

    Returns:
        None

    Raises:
        KeyError: an error occurred when the key in JSON file
                  doesn't match the rules.
    """
    # connect to MongoDB
    my_collection = connect_mongodb("FHDATime", "class_info")

    # update MongoDB
    for catalog in json_dict:

        # extract year, quarter, school from json file into string catalog_info
        # for school: Foothill is 1, De Anza is 2
        # for quarter: Summer is 1, Fall is 2, Winter is 3, Spring is 4

        try:
            info_dict = re.search(r'^(?P<year>\d+) (?P<quarter>\w+) (?P<school>\w+[\s\w+]*)$', catalog).groups()
            year, quarter, school = info_dict
        except:
            logging.warning(catalog + ' can not match current setting. Data skipped.')
            continue
        quarter_dict = {"Summer": "1", "Fall": "2", "Winter": "3", "Spring": "4"}
        school_dict = {"Foothill": "1", "De Anza": "2"}
        catalog_info = year + quarter_dict[quarter] + school_dict[school]

        try:
            course_data = json_dict[catalog]['CourseData']
        except:
            logging.warning(catalog + ' does not contain key "CourseData"')
            continue

        for department in course_data:
            for course in course_data[department]:
                unique_id = catalog_info + course['CRN']
                my_query = {"ID": unique_id}
                current = my_collection.find(my_query)
                # check if the course exists in database
                if current.count() == 0:
                    # the course doesn't exist in database, insert it
                    item = {
                            "ID": unique_id,
                            "Term": catalog_info,
                            "Department": department,
                            "Year": year,
                            "Quarter": quarter,
                            "School": school,
                            "CRN": course['CRN'],
                            "Crse": course['Crse'],
                            "Sec": course['Sec'],
                            "Cmp": course['Cmp'],
                            "Cred": course['Cred'],
                            "Title": course['Title'],
                            "Days": course['Days'],
                            "Time": course['Time'],
                            "Cap": [int(course['Cap'])],
                            "Act": [int(course['Act'])],
                            "WL Cap": [int(course['WL Cap'])],
                            "WL Act": [int(course['WL Act'])],
                            "Instructor": course['Instructor'],
                            "Date": course['Date'],
                            "Location": course['Location'],
                            "Attribute": course['Attribute'],
                            "Lab Time": course['Lab Time'],
                            "FetchTime": [datetime.datetime.utcnow()]
                        }
                    my_collection.insert_one(item)

                else:
                    current = [i for i in current]
                    # the course exists in db, update it
                    new_value = {"$set": {"Cap": current[0]["Cap"] + [int(course['Cap'])],
                                          "Act": current[0]["Act"] + [int(course["Act"])],
                                          "WL Cap": current[0]["WL Cap"] + [int(course["WL Cap"])],
                                          "WL Act": current[0]["WL Act"] + [int(course["WL Act"])],
                                          "FetchTime": current[0]["FetchTime"] + [datetime.datetime.utcnow()]
                                          }}
                    my_collection.update_one(my_query, new_value)
