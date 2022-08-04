SELECT [device_exposure_id]
      ,de.[person_id]
      ,[device_concept_id]
      ,[device_exposure_start_date]
      ,[device_exposure_start_datetime]
      ,[device_exposure_end_date]
      ,[device_exposure_end_datetime]
      ,[device_type_concept_id]
      ,[unique_device_id]
      ,[quantity]
      ,[provider_id]
      ,[visit_occurrence_id]
      ,[visit_detail_id]
      ,[device_source_value]
      ,[device_source_concept_id]
FROM [{}].[{}].[device_exposure] de
  left join death d
  on de.person_id = d.person_id
  where (d.death_date > '2015-12-31' 
         and de.device_exposure_start_date <= d.death_date 
         or d.death_date <= '2015-12-31'
         or d.death_date is null)
  and de.person_id in ({})