CREATE OR REPLACE VIEW RAW_ELAPSED_TIME_VW AS (
SELECT
id,
file_source as checkpoint,
elapsed_times,
created_at
FROM main.RAW_ELAPSED_TIME
);

SELECT * FROM RAW_ELAPSED_TIME_VW;


CREATE OR REPLACE VIEW RAW_LLM_COMPLETION_VW AS (
SELECT 
id,
checkpoint,
completions_id,
completions_choices,
completions_usage.prompt_tokens,
completions_usage.total_tokens,
--completions_usage.completion_tokens_details,
--completions_usage.prompt_tokens_details,
created_at
FROM (
SELECT
id,
file_source as checkpoint,
UNNEST(completions) as completions,
completions.id as completions_id,
completions.choices as completions_choices,
completions.usage as completions_usage,
created_at
FROM main.RAW_LLM_COMPLETION
)
);

SELECT * FROM RAW_LLM_COMPLETION_VW;


CREATE OR REPLACE VIEW RAW_LLM_VALIDATION_VW AS (
SELECT
	VAL.id,
	VAL.file_source as checkpoint,
	VAL.content.doc_id,
	VAL.content.statement_id,
	TRANSF.statement_title,
	VAL.content.statement as statement_text,
	VAL.content.sources as statement_sources,
	VAL.content.semscore,
	VAL.content.similarity_score,
	VAL.content.similarity_score_confidence,
	VAL.content.transformation_accuracy,
	VAL.content.grammar_syntax_accuracy,
	VAL.content.findings,
	VAL.created_at,
	TRANSF.transformed,
	TRANSF.transformation_template_ids,
	TRANSF.transformation_confidence,
	TRANSF.transformation_reason,
	-- CLASS
	TRANSF.statement_classification_type,
	TRANSF.statement_classification_type_confidence,
	TRANSF.statement_classification_type_explanation,
	TRANSF.statement_classification_subtype,
	TRANSF.statement_classification_subtype_confidence,
	TRANSF.statement_classification_subtype_explanation,
	-- EXTRACT
	TRANSF.terms,
	TRANSF.verb_symbols,
	VAL.id.REPLACE('validation_judge_', '') as source,
	IF (TRANSF.statement_text = VAL.content.statement, TRUE, FALSE) as dbl_check
FROM
	main.RAW_LLM_VALIDATION as VAL
LEFT JOIN main.RAW_TRANSFORM_ELEMENTS_VW as TRANSF
  ON
	(VAL.content.statement_id::STRING = TRANSF.statement_id::STRING)
	AND (VAL.id.REPLACE('validation_judge_', '') = TRANSF.source)
	AND (VAL.content.doc_id = TRANSF.doc_id)
	AND (VAL.file_source = TRANSF.checkpoint)
	AND list_has_all(VAL.content.sources, TRANSF.statement_sources)
	AND (VAL.content.statement = TRANSF.statement_text)
--LEFT JOIN main.RAW_CLASSIFY_VW as CLASS
--  ON
--	(VAL.content.statement_id::STRING = CLASS.statement_id::STRING)
--	AND (VAL.id.REPLACE('validation_judge_', '') = CLASS.source)
--	AND (VAL.content.doc_id = CLASS.doc_id)
--	AND (VAL.file_source = CLASS.checkpoint)
--	AND list_has_all(VAL.content.sources, CLASS.statement_sources)
--	AND (VAL.content.statement = CLASS.statement_text)
--LEFT JOIN main.RAW_SECTION_EXTRACTED_ELEMENTS_VW as EXTRACT
--  ON
--	(VAL.content.statement_id::STRING = EXTRACT.statement_id::STRING)
--	AND (VAL.content.doc_id = EXTRACT.doc_id)
--	AND (VAL.file_source = EXTRACT.checkpoint)
--	--AND (EXTRACT.checkpoint = 'documents_true_table.json')
--	AND list_has_all(VAL.content.sources, EXTRACT.statement_sources)
--	AND (VAL.content.statement = EXTRACT.statement_text)
);

SELECT * FROM RAW_LLM_VALIDATION_VW;




-- Utils

select *
FROM main.RAW_SECTION_P1_EXTRACTED_ELEMENTS_VW as EXTRACT
WHERE 
	EXTRACT.statement_id::STRING = '3'
	AND EXTRACT.checkpoint = 'documents-2024-11-29-4.json'
	AND list_has_all(['(a)(2)'], EXTRACT.statement_sources)
	AND EXTRACT.statement_text = 'The Secretary of the Commission (Secretary) will promptly forward a copy to each named party by registered or certified mail at that party''s last address filed with the Commission.'

SELECT * FROM main.RAW_TRANSFORM_OPERATIVE_RULES_VW
WHERE checkpoint = 'documents-2024-12-08-9.json'
AND statement_id = '4'
AND list_has_all(statement_sources, ['(a)(3)'])

SELECT * FROM main.RAW_TRANSFORM_TERMS_VW
WHERE checkpoint = 'documents-2024-12-08-9.json'
AND statement_id = 'Order disposing of the matter'
AND list_has_all(statement_sources, ['(a)','(b)'])

SELECT * FROM main.RAW_TRANSFORM_FACT_TYPES_VW
WHERE checkpoint = 'documents-2024-12-08-8.json'
AND statement_id = '1'
AND list_has_all(statement_sources, ['(a)'])


