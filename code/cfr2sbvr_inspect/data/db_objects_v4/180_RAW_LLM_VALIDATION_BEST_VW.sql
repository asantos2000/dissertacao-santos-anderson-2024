CREATE OR REPLACE VIEW RAW_LLM_VALIDATION_BEST_VW AS (
SELECT
    source,
    doc_id,
    statement_sources,
    checkpoint,
    statement_title,
    statement_text,
    statement_classification_type,
    statement_classification_type_confidence,
    statement_classification_type_explanation,
    statement_classification_subtype,
    statement_classification_subtype_confidence,
    statement_classification_subtype_explanation,
    transformation_confidence,
    transformation_reason,
    transformed,
    transformation_template_ids,
    semscore,
    similarity_score,
    similarity_score_confidence,
    transformation_accuracy,
    grammar_syntax_accuracy,
    findings,
    terms,
    verb_symbols,
    id,
    statement_id
FROM
	(
	SELECT
		*,
		ROW_NUMBER() OVER ( PARTITION BY source,
		doc_id,
		statement_sources
	ORDER BY
		semscore DESC,
		similarity_score DESC ) AS rn
	FROM
		RAW_LLM_VALIDATION_VW ) t
WHERE
	rn = 1
ORDER BY
	source,
	doc_id,
	statement_sources
);

SELECT * FROM main.RAW_LLM_VALIDATION_BEST_VW;