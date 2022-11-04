
  SELECT TOP(2)(SELECT [note_id]
      ,n.[person_id]
      ,[note_date]
      ,[note_datetime]
      ,[note_type_concept_id]
      ,[note_class_concept_id]
      ,[note_title]
      ,[note_text]
      ,[encoding_concept_id]
      ,[language_concept_id]
      ,n.[provider_id]
      ,n.[visit_occurrence_id]
      ,n.[visit_detail_id]
      ,[note_source_value]
	  FOR JSON PATH)
  FROM [ohdsi_cumc_hpo].[dbo].[note] n
    left join [ohdsi_cumc_hpo].[dbo].visit_occurrence v
    on n.visit_occurrence_id = v.visit_occurrence_id
    and n.person_id = v.person_id
  left join death d
  on n.person_id = d.person_id
  where (d.death_date > '2015-12-31' 
         and n.note_date <= d.death_date 
         or d.death_date <= '2015-12-31'
         or d.death_date is null)
         and n.note_text is not null
         and n.note_text != ''

