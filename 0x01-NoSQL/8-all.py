#!/usr/bin/env python3
"""Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """ 
    List all documents in a collection or an empty list
    """
    return [each for each in mongo_collection.find()]
