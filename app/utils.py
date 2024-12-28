# Utilities
import sys
import os
import json
import copy
import pandas as pd
from pprint import pprint


def flatten_json(data, prefix=''):
    """
    Recursively flattens a nested JSON object.
    """
    flattened_data = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                flattened_data.update(flatten_json(value, f"{prefix}{key}-"))
            else:
                flattened_data[f"{prefix}{key}"] = value
    elif isinstance(data, list):
        for index, item in enumerate(data):
            flattened_data.update(flatten_json(item, f"{prefix}-"))
    else:
        flattened_data[prefix[:-1]] = data

    return flattened_data


def flatten_dict_to_list(data: dict, separator: str = "-", prefix: str = "", parent_record: dict = {}) -> list:
    new_data = []
    list_detected = False
    new_record = copy.deepcopy(parent_record)
    # Get all values which are not dict or list
    for key, value in data.items(): 
        if not isinstance(value, dict) and not isinstance(value, list):
            new_record[prefix + separator + key] = value
    for key, value in data.items(): 
        # value is dict
        if isinstance(value, dict):
            if len(list(value.keys())) > 0:
                d = flatten_dict_to_list(value, "-", prefix + separator + key, new_record)
                for elem in copy.deepcopy(d):
                    new_record.update(elem)
            else:
                # empty dict
                new_record[prefix + separator + key] = ""
    for key, value in data.items():
        # value is list
        if isinstance(value, list):
            # list not empty
            if len(value) > 0:
                list_detected = True
                if not isinstance(value[0], dict) and not isinstance(value[0], list):
                    # if list is just the list of values
                    new_record[prefix + separator + key] = ", ".join(value)
                elif isinstance(value[0], dict):
                    for sub_item in value:
                        d = flatten_dict_to_list(sub_item, "-", prefix + separator + key, new_record)
                        for elem in copy.deepcopy(d):
                            new_data.append(elem)
            else:
                # list is empty
                #new_record[prefix + separator + key] = ""
                pass
    
    if not list_detected:
        new_data.append(new_record)
    return new_data 


def process_json(json_data, base_key=None):
    """
    Process JSON data to a flattened structure based on a specified key.
    """
    # Extract the main data based on the given key
    if base_key is not None:
        data_to_process = json_data.get('data', {}).get(base_key, {})
    else:
        data = json_data.get('data', {})
        data_to_process = data.get(list(data.keys())[0], {})
       
    rows = []

    for item in data_to_process:
        for row in flatten_dict_to_list(item, separator="", prefix="", parent_record={}):
            rows.append(row)

    return rows