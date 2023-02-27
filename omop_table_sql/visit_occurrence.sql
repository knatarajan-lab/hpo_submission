SELECT DISTINCT
       [visit_occurrence_id]
      ,v.[person_id]
      ,[visit_concept_id]
      ,[visit_start_date]
      ,[visit_start_datetime]
      , case
			when [visit_end_date] < visit_start_date 
				then visit_start_date
				else visit_end_date
			end 
		as visit_end_date
      , case
			when [visit_end_datetime] < visit_start_datetime
				then visit_start_datetime
				else visit_end_datetime
			end 
		as visit_end_datetime
      ,[visit_type_concept_id]
      ,[provider_id]
      ,[care_site_id]
      ,[visit_source_value]
      ,[visit_source_concept_id]
      ,[admitting_source_concept_id]
      ,[admitting_source_value]
      ,[discharge_to_concept_id]
      ,[discharge_to_source_value]
      ,[preceding_visit_occurrence_id]
  FROM [{}].[{}].[visit_occurrence] v
  left join death d
  on v.person_id = d.person_id
  where (d.death_date > '2017-07-01'
         and v.visit_start_date <= DATEADD(day, 30, d.death_date)
         or d.death_date <= '2017-07-01'
         or d.death_date is null)
  and visit_end_date is not null
  AND v.person_id in ({})