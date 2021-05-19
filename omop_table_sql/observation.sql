SELECT [observation_id]
      ,[person_id]
      ,[observation_concept_id]
      ,[observation_date]
      ,[observation_datetime]
      ,[observation_type_concept_id]
      ,[value_as_number]
      ,[value_as_string]
      ,[value_as_concept_id]
      ,[qualifier_concept_id]
      ,[unit_concept_id]
      ,[provider_id]
      ,[visit_occurrence_id]
      --,[visit_detail_id]
      ,[observation_source_value]
      ,[observation_source_concept_id]
      ,[unit_source_value]
      ,[qualifier_source_value]
FROM(
SELECT o.[observation_id]
      ,o.[person_id]
      ,o.[observation_concept_id]
      ,o.[observation_date]
      ,o.[observation_datetime]
      ,o.[observation_type_concept_id]
      ,o.[value_as_number]
      ,o.[value_as_string]
      ,o.[value_as_concept_id]
      ,o.[qualifier_concept_id]
      ,o.[unit_concept_id]
      ,o.[provider_id]
      ,v.[visit_occurrence_id]
      --,o.[visit_detail_id]
      ,v.[visit_end_date]
      ,v.[visit_start_date]
      ,o.[observation_source_value]
      ,o.[observation_source_concept_id]
      ,o.[unit_source_value]
      ,o.[qualifier_source_value]
FROM [{}].[{}].[observation] o
left join [visit_occurrence] v
on o.visit_occurrence_id = v.visit_occurrence_id
and o.person_id = v.person_id
  left join death d
  on o.person_id = d.person_id
  where (d.death_date > '2015-12-31' 
         and o.observation_date <= d.death_date 
         or d.death_date is null
         or d.death_date <='2015-12-31')) a
WHERE a.person_id in ({})
