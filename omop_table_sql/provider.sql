select
provider_id,
'NO INFO' as provider_name,
'NO INFO' as npi,
DEA as dea,
specialty_concept_id,
care_site_id,
year_of_birth,
gender_concept_id,
provider_source_value,
specialty_source_value,
specialty_source_concept_id,
gender_source_value,
gender_source_concept_id
from [{}].[{}].[provider]
