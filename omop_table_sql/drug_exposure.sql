/****** Script for SelectTopNRows command from SSMS  ******/
SELECT 
[drug_exposure_id]
,[person_id]
,[drug_concept_id]
,[drug_exposure_start_date]
,[drug_exposure_start_datetime]
,[drug_exposure_end_date]
,[drug_exposure_end_datetime]
,[verbatim_end_date]
,[drug_type_concept_id]
,[stop_reason]
,[refills]
,[quantity]
,[days_supply]
,[sig]
,[route_concept_id]
,[lot_number]
,[provider_id]
,[visit_occurrence_id]
--,[visit_detail_id]
,[drug_source_value]
,[drug_source_concept_id]
,[route_source_value]
,[dose_unit_source_value]
FROM(
SELECT d.[drug_exposure_id]
      ,d.[person_id]
      ,d.[drug_concept_id]
      ,d.[drug_exposure_start_date]
      ,d.[drug_exposure_start_datetime]
      ,d.[drug_exposure_end_date]
      ,d.[drug_exposure_end_datetime]
      ,d.[verbatim_end_date]
      ,d.[drug_type_concept_id]
      ,d.[stop_reason]
      ,d.[refills]
      ,d.[quantity]
      ,d.[days_supply]
      ,null as [sig]
      ,d.[route_concept_id]
      ,d.[lot_number]
      ,d.[provider_id]
      ,v.[visit_occurrence_id]
      --,d.[visit_detail_id]
      ,v.[visit_end_date]
      ,v.[visit_start_date]
      ,d.[drug_source_value]
      ,d.[drug_source_concept_id]
      ,d.[route_source_value]
      ,d.[dose_unit_source_value]
FROM [{}].[{}].[drug_exposure] d
left join visit_occurrence v
on d.visit_occurrence_id = v.visit_occurrence_id
and d.person_id = v.person_id
left join death dea
on d.person_id = dea.person_id
where (dea.death_date > '2015-12-31' 
         and d.drug_exposure_start_date <= dea.death_date 
         or dea.death_date <= '2015-12-31'
         or dea.death_date is null)) a
WHERE a.person_id in ({})
