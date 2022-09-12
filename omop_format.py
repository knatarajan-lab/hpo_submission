import glob
import json
import re
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
    all_json = glob.glob(f'{root_path}/*.json', recursive=True)
    omop_files = {}
    parse_date_dict = {}
    pattern = "omop/(.*?).json"
    for file_path in all_json:
        file_name = re.search(pattern, file_path).group(1)
        with open(file_path) as file:
            content = json.load(file)
            col_list: Dict[Any, Any] = {}
            parse_date_list = []
            for col in content:
                if col['type'] == 'integer':
                    col_list[col['name']] = 'Int64'
                elif col['type'] == 'string':
                    col_list[col['name']] = str
                elif col['type'] == 'float':
                    col_list[col['name']] = np.float64
                elif col['type'] in ('date', 'timestamp'):
                    parse_date_list.append(col['name'])
            omop_files[file_name] = col_list
            parse_date_dict[file_name] = parse_date_list
    return omop_files, parse_date_dict
