#!/bin/sh
cd /Users/zoeyjiang/PycharmProjects/hpo_submission/
. ./venv/bin/activate && python3 ./submission_pipeline.py -db_ini _dm_aou.ini -sql omop_table_sql/ -r aou_ehr_validator/resources/omop/ -o HPO_submission/