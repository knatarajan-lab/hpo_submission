import glob
import json
import re
from typing import Dict, Any


def generate_omop_format(root_path):
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
