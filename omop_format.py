import glob
import json
import re
import os
import numpy as np
from datetime import datetime
from typing import Dict, Any


def generate_omop_format(root_path):
    '''
    Takes in JSON files and outputs dictionary of column names and their associated data types

    Args:
        root_path: ./aou_ehr_validator/resources/omop

    Returns:
        omop_files: dictionary of column names and their data type

    Raises:
        N/A
    '''
    all_json = glob.glob(os.path.join(f'{root_path}','*.json'), recursive=True)
    omop_files = {}
    parse_date_dict = {}

    for file_path in all_json:
        file_found = re.search(r"omop(\\|\/)(.+).json", file_path)
        col_list: Dict[Any, Any] = {}
        parse_date_list: Dict[Any, Any]= {}
        date_fmt = '%Y-%m-%d'
        timestamp_fmt = '%Y-%m-%d %H:%M:%S'
        if type(file_found) != 'NoneType':
            file_name = file_found.group(2)
            with open(file_path, encoding="utf8") as file:
                content = json.load(file)
                for col in content:
                    if col['type'] == 'integer':
                        col_list[col['name']] = 'Int64'
                    elif col['type'] == 'string':
                        col_list[col['name']] = str
                    elif col['type'] == 'float':
                        col_list[col['name']] = np.float64
                    elif col['type'] == 'date':
                        parse_date_list[col['name']] = date_fmt
                    elif col['type'] == 'timestamp':
                        parse_date_list[col['name']] = timestamp_fmt 
                omop_files[file_name] = col_list
                parse_date_dict[file_name] = parse_date_list
    return omop_files, parse_date_dict
