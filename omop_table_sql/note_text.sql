SELECT [note_id]
      ,[note_text]
FROM(
SELECT [note_id]
      ,[note_text]
      ,n.[person_id]
      --,v.[visit_end_date]
FROM [{}].[{}].[note] n
--left join visit_occurrence v
--on n.visit_occurrence_id = v.visit_occurrence_id
--and n.person_id = v.person_id
  left join death d
  on n.person_id = d.person_id
  where (d.death_date > '2015-12-31'
         and n.note_date <= d.death_date
         or d.death_date <= '2015-12-31'
         or d.death_date is null)
         and n.note_text is not null
         and n.note_text != '') a
WHERE
--a.visit_end_date is not null
a.person_id in ({})