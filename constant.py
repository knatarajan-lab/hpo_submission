file_name_list = ['care_site', 'condition_occurrence', 'death', 'device_exposure', 'drug_exposure',
                  'fact_relationship', 'location', 'measurement', 'note', 'observation',
                  'procedure_occurrence', 'visit_occurrence', 'provider', 'pii_address', 'pii_email',
                  'pii_name', 'pii_mrn', 'pii_phone_number', 'specimen', 'participant_match']

root_path = './aou_ehr_validator/resources/omop'
query_path = './omop_table_sql'
output_path = './HPO_submission/'

delimiter_hpo = ','
quotechar_hpo = '"'

empty_table_list = ['care_site', 'provider', 'fact_relationship', 'pii_address', 'pii_email', 'pii_mrn', 'specimen']
pii_table_list = ['pii_name', 'pii_phone_number', 'participant_match']
