SELECT [person_id]
      ,[death_date]
      ,[death_datetime]
      ,[death_type_concept_id]
      ,[cause_concept_id]
      ,[cause_source_value]
      ,[cause_source_concept_id]
  FROM [{}].[{}].[death]
  where death_date > '2017-07-01' and death_date is not null
  and person_id in ({})