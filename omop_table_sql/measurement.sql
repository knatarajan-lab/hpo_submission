SELECT DISTINCT
       [measurement_id]
      ,m.[person_id]
      ,[measurement_concept_id]
      ,[measurement_date]
      ,[measurement_datetime]
      ,[measurement_datetime] as [measurement_time]
      ,[measurement_type_concept_id]
      ,[operator_concept_id]
      ,[value_as_number]
      ,[value_as_concept_id]
      ,[unit_concept_id]
      ,[range_low]
      ,[range_high]
      ,[provider_id]
      ,[visit_occurrence_id]
      ,[visit_detail_id]
      ,[measurement_source_value]
      ,[measurement_source_concept_id]
      ,[unit_source_value]
      ,[value_source_value]

from [{}].[{}].[measurement] m
left join death d
on m.person_id = d.person_id
where (d.death_date > '2017-07-01'
         and m.measurement_date <= DATEADD(day, 30, d.death_date)
         or d.death_date is null
         or d.death_date <='2017-07-01')
and m.person_id in ({})