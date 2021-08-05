select
visit_detail_id,
v.person_id,
visit_detail_concept_id,
visit_start_date as visit_detail_start_date,
visit_start_datetime as visit_detail_start_datetime,
visit_end_date as visit_detail_end_date,
visit_end_datetime as visit_detail_end_datetime,
visit_type_concept_id as visit_detail_type_concept_id,
provider_id,
care_site_id,
visit_source_value as visit_detail_source_value,
visit_source_concept_id as visit_detail_source_concept_id,
admitting_source_value,
admitting_source_concept_id,
discharge_to_source_value,
discharge_to_concept_id,
preceding_visit_detail_id,
visit_detail_parent_id,
visit_occurrence_id
from [{}].[{}].[visit_detail] v
left join death d
on v.person_id = d.person_id
where (d.death_date > '2015-12-31'
     and v.visit_start_date <= d.death_date
     or d.death_date <= '2015-12-31'
     or d.death_date is null)
and v.person_id in ({})
