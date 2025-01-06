
CREATE OR REPLACE VIEW RAW_CLASSIFY_P1_OPERATIVE_RULES_VW AS (
SELECT
	CLASS.id,
	CLASS."checkpoint",
	CLASS.doc_id,
	CLASS.statement_id,
	CLASS.statement_title,
	CLASS.statement_text,
	CLASS.statement_sources,
	CLASS.created_at,
	max(CLASS.statement_classification_type) AS statement_classification_type,
	max(CLASS.statement_classification_explanation) AS statement_classification_explanation,
	max(CLASS.statement_classification_confidence) AS statement_classification_confidence,
	EXTRACT.terms,
	EXTRACT.verb_symbols
FROM
	(
	SELECT
		id,
		file_source AS "checkpoint",
		"content".doc_id,
		"content".statement_id,
		"content".statement_title,
		"content".statement_text,
		"content".statement_sources,
		(unnest("content".classification))."type" AS statement_classification_type,
		(unnest("content".classification)).explanation AS statement_classification_explanation,
		(unnest("content".classification)).confidence AS statement_classification_confidence,
		created_at
	FROM
		main.RAW_CLASSIFY_P1_OPERATIVE_RULES) AS CLASS
LEFT JOIN main.RAW_SECTION_EXTRACTED_ELEMENTS_VW as EXTRACT
  ON
	(CLASS.statement_id::STRING = EXTRACT.statement_id::STRING)
	AND (CLASS.doc_id = EXTRACT.doc_id)
	AND (CLASS."checkpoint" = EXTRACT.checkpoint)
	AND list_has_all(CLASS.statement_sources,
	EXTRACT.statement_sources)
	AND (CLASS.statement_text = EXTRACT.statement_text)
GROUP BY
	CLASS.id,
	CLASS."checkpoint",
	CLASS.doc_id,
	CLASS.statement_id,
	CLASS.statement_title,
	CLASS.statement_text,
	CLASS.statement_sources,
	CLASS.created_at,
	EXTRACT.terms,
	EXTRACT.verb_symbols
UNION ALL
SELECT
	CLASS.id,
	CLASS.file_source as checkpoint,
	CLASS.content.doc_id,
	CLASS.content.statement_id,
	EXTRACT.statement_title as statement_title,
	CLASS.content.statement as statement_text,
	CLASS.content.sources as statement_sources,
	CLASS.created_at,
	CLASS.content.type as statement_classification_type,
	'' as statement_classification_explanation,
	0 as statement_classification_confidence,
	EXTRACT.terms as terms,
	EXTRACT.verb_symbols as verb_symbols
FROM
	main.RAW_CLASSIFY_P1_OPERATIVE_RULES_TRUE as CLASS
LEFT JOIN main.RAW_SECTION_EXTRACTED_ELEMENTS_VW as EXTRACT
  ON
	(CLASS.content.statement_id::STRING = EXTRACT.statement_id::STRING)
	AND (CLASS.content.doc_id = EXTRACT.doc_id)
	AND (CLASS.file_source = EXTRACT.checkpoint)
	AND list_has_all(CLASS.content.sources,
	EXTRACT.statement_sources)
	AND (CLASS.content.statement = EXTRACT.statement_text)
);

SELECT * FROM RAW_CLASSIFY_P1_OPERATIVE_RULES_VW;

