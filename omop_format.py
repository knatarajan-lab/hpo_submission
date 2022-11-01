import glob
import json
import re
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
    pattern = "omop/(.*?).json"
    for file_path in all_json:
        file_name = re.search(pattern, file_path).group(1)
        with open(file_path) as file:
            content = json.load(file)
            col_list: Dict[Any, Any] = {}
            for col in content:
                col_list[col['name']] = col['type']
            omop_files[file_name] = col_list
    return omop_files
