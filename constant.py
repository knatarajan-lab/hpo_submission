import os

# required tables for All of Us
table_name_list = ['care_site', 'condition_occurrence', 'death', 'device_exposure', 'drug_exposure',
                    'fact_relationship', 'location', 'measurement', 'note', 'observation',
                    'procedure_occurrence', 'visit_occurrence', 'visit_detail', 'provider', 'pii_address', 'pii_email',
                    'pii_name','pii_mrn', 'pii_phone_number', 'specimen', 'participant_match', 'patient_status']


root_path = os.path.join('.','aou-ehr-file-check', 'resources','omop')
query_path = os.path.join('.','omop_table_sql')
output_path = os.path.join('.','HPO_submission')
note_txt_folder = os.path.join('.','HPO_submission','clinical_documents')
patient_status_folder = os.path.join('.','patient_status')

delimiter_hpo = ','
quotechar_hpo = '"'

# empty tables
empty_table_list = ['fact_relationship', 'pii_address', 'pii_email', 'pii_mrn', 'specimen']
# tables containing pii
pii_table_list = ['pii_name', 'pii_phone_number', 'participant_match']

rows_allowed = 5000
