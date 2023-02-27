SELECT DISTINCT
visit_detail_id,
v.person_id,
visit_detail_concept_id,
visit_detail_start_date,
visit_detail_start_datetime,
visit_detail_end_date,
visit_detail_end_datetime,
visit_detail_type_concept_id,
provider_id,
care_site_id,
visit_detail_source_value,
visit_detail_source_concept_id,
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
where (d.death_date > '2017-07-01'
     and v.visit_detail_start_date <= DATEADD(day, 30, d.death_date)
     or d.death_date <= '2017-07-01'
     or d.death_date is null)
and v.person_id in ({})
