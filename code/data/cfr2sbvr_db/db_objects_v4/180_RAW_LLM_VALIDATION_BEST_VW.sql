CREATE OR REPLACE VIEW RAW_LLM_VALIDATION_BEST_VW AS (
SELECT
	source,
	doc_id,
	statement_sources,
	MAX(checkpoint) as checkpoint,
	MAX(statement_title) as statement_title,
	MAX(statement_text) as statement_text,
	MAX(statement_classification_type) as statement_classification_type,
	MAX(statement_classification_type_confidence) as statement_classification_type_confidence,
	MAX(statement_classification_type_explanation) as statement_classification_type_explanation,
	MAX(statement_classification_subtype) as statement_classification_subtype,
	MAX(statement_classification_subtype_confidence) as statement_classification_subtype_confidence,
	MAX(statement_classification_subtype_explanation) as statement_classification_subtype_explanation,
	MAX(transformation_confidence) as transformation_confidence,
	MAX(transformation_reason) as transformation_reason,
	MAX(transformed) as transformed,
	MAX(transformation_template_ids) as transformation_template_ids,
	MAX(semscore) as semscore,
	MAX(similarity_score) as similarity_score,
	MAX(similarity_score_confidence) as similarity_score_confidence,
	MAX(transformation_accuracy) as transformation_accuracy,
	MAX(grammar_syntax_accuracy) as grammar_syntax_accuracy,
	MAX(findings) as findings,
	MAX(terms) as terms,
	MAX(verb_symbols) as verb_symbols,
	id,
	'' as statement_id
	FROM
		main.RAW_LLM_VALIDATION_VW
	WHERE checkpoint <> 'documents_true_table.json'
GROUP BY
	source,
	doc_id,
	--statement_id,
	statement_sources,
	id
ORDER BY
	source,
	doc_id,
	--statement_id,
	statement_sources,
	id
);

SELECT * FROM main.RAW_LLM_VALIDATION_BEST_VW;