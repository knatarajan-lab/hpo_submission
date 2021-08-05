SELECT [procedure_occurrence_id]
      ,[person_id]
      ,[procedure_concept_id]
      ,[procedure_date]
      ,[procedure_datetime]
      ,[procedure_type_concept_id]
      ,[modifier_concept_id]
      ,[quantity]
      ,[provider_id]
      ,[visit_occurrence_id]
      ,[visit_detail_id]
      ,[procedure_source_value]
      ,[procedure_source_concept_id]
      ,[modifier_source_value]
FROM(
SELECT  
[procedure_occurrence_id]
      ,p.[person_id]
      ,p.[procedure_concept_id]
      ,p.[procedure_date]
      ,p.[procedure_datetime]
      ,p.[procedure_type_concept_id]
      ,p.[modifier_concept_id]
      ,p.[quantity]
      ,p.[provider_id]
      ,v.[visit_occurrence_id]
      ,p.[visit_detail_id]
      ,p.[procedure_source_value]
      ,p.[procedure_source_concept_id]
      ,p.[modifier_source_value]
  FROM [{}].[{}].[procedure_occurrence] p
 left  join [visit_occurrence] v
  on p.visit_occurrence_id = v.visit_occurrence_id
  and p.person_id = v.person_id
  left join death d
  on p.person_id = d.person_id
  where (d.death_date > '2015-12-31' 
         and p.procedure_date <= d.death_date 
         or d.death_date <= '2015-12-31'
         or d.death_date is null)) a
where a.person_id in ({})