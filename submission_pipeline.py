from db_connection import *
import argparse
import configparser
from constant import file_name_list, empty_table_list
from omop_format import generate_omop_format
from extract_person_table import read_write_person_file
from export_data import export_omop_file
from patient_status import extract_patient_status
from extract_note_txt import extract_note_txt


def main():
    try:
        parser = argparse.ArgumentParser(description='Arguments for data updates')
        parser.add_argument('-db_ini',
                            '--database_setting_path',
                            help='Database setting file',
                            required=True)
        parser.add_argument('-sql',
                            '--omop_table_query_folder',
                            help='OMOP table query folder',
                            required=True)
        parser.add_argument('-r',
                            '--resource_folder',
                            help='OMOP table format resource folder',
                            required=True)
        parser.add_argument('-o',
                            '--output_folder',
                            help='Output folder for submission')
        parser.add_argument('-ops',
                            '--output_folder_patient_status',
                            help='Output folder for patient status')
        ARGS = parser.parse_args()
        db_config = configparser.ConfigParser()
        db_settings_path = ARGS.database_setting_path
        db_config.read(db_settings_path)
        db_settings = db_config.defaults()
        conn = test_conn(db_settings)

        query_path = ARGS.omop_table_query_folder
        root_path = ARGS.resource_folder
        output_path = ARGS.output_folder
        output_path_patient_status = ARGS.output_folder_patient_status
        omop_files = generate_omop_format(root_path)
        participant_list = read_write_person_file(db_settings, conn, omop_files)
        print("patient_status extraction")
        extract_patient_status(db_settings, conn)
        for file in file_name_list:
            export_omop_file(file, query_path, output_path, conn, omop_files, empty_table_list, db_settings, participant_list)
        export_omop_file('patient_status', query_path, output_path_patient_status, conn, omop_files, empty_table_list, db_settings,
                         participant_list)
        #extract_note_txt()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()