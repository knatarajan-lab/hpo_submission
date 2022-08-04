/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [condition_occurrence_id]
      ,[person_id]
      ,[condition_concept_id]
      ,[condition_start_date]
      ,[condition_start_datetime]
      ,[condition_end_date]
      ,[condition_end_datetime]
      ,[condition_type_concept_id]
      ,[condition_status_concept_id]
      ,[stop_reason]
      ,[provider_id]
      ,[visit_occurrence_id]
      ,[visit_detail_id]
      ,[condition_source_value]
      ,[condition_source_concept_id]
      ,[condition_status_source_value]

FROM(
SELECT c.[condition_occurrence_id]
      ,c.[person_id]
      ,c.[condition_concept_id]
      ,c.[condition_start_date]
      ,c.[condition_start_datetime]
      ,c.[condition_end_date]
      ,c.[condition_end_datetime]
      ,c.[condition_type_concept_id]
      ,c.[stop_reason]
      ,c.[provider_id]
      ,c.[visit_occurrence_id]
      ,c.[visit_detail_id]
      ,v.[visit_start_date]
      ,v.[visit_end_date]
      ,c.[condition_source_value]
      ,c.[condition_source_concept_id]
      ,c.[condition_status_source_value]
      ,c.[condition_status_concept_id]
  FROM [{}].[{}].[condition_occurrence] c
  left join visit_occurrence v
  on c.visit_occurrence_id = v.visit_occurrence_id
  and c.person_id = v.person_id
  left join death d
  on c.person_id = d.person_id
  where (d.death_date > '2015-12-31' 
         and c.condition_start_date <= d.death_date 
         or d.death_date <= '2015-12-31'
         or d.death_date is null)) a
WHERE a.person_id in ({})
