#!/bin/sh
cd /project/hpo/hpo_submission/

rm patient_status/patient_status_union.csv
rm patient_status/patient_status_diff.csv
rm -r patient_status_old
cp -r patient_status/ patient_status_old
cat patient_status_old/*csv > patient_status_old/patient_status_union_old.csv

. ./venv/bin/activate && python3 ./submission_pipeline.py -db_ini a_dm_aou.ini -sql omop_table_sql/ -r aou-ehr-file-check/resources/omop/ -o HPO_submission/

cat patient_status/*csv > patient_status/patient_status_union.csv
`bash -c "comm -2 -3 <(sort patient_status/patient_status_union.csv) <(sort patient_status_old/patient_status_union_old.csv) >patient_status/patient_status_diff.csv" ` 

cd /project/hpo/submission_folder
mkdir "$(date +'%Y-%m-%d')-v1"

cd /project/hpo/hpo_submission/HPO_submission
for f in *.csv
do
  cp -v "$f" /project/hpo/submission_folder/"$(date +'%Y-%m-%d')-v1"/${f%.csv}.csv

done
