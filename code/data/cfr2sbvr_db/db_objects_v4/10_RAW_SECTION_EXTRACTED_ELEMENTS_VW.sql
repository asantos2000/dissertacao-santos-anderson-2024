CREATE OR REPLACE VIEW RAW_SECTION_EXTRACTED_ELEMENTS_VW AS (
(WITH P1 AS (
SELECT
    id,
    doc_id,
    prompt,
    file_source AS checkpoint,
    id_1 AS statement_id,
    title AS statement_title,
    statement AS statement_text,
    (unnest(terms)).term AS term,
    (unnest(terms)).classification AS term_classification,
    verb_symbols,
    classification,
    sources AS statement_sources,
    created_at
FROM (
        SELECT
            id,
            id.REPLACE('_P1', '') AS doc_id,
            prompt,
            file_source,
            unnest(elements) AS ELEMENT,
            created_at
        FROM
            RAW_SECTION_P1_EXTRACTED_ELEMENTS_TRUE
            )
)
SELECT
    P1.id,
    P1.doc_id,
    P1.checkpoint,
    P1.statement_id,
    P1.statement_title,
    P1.statement_text,
    P1.verb_symbols,
    P1.classification as statement_classification_type,
    1.00::DOUBLE as statement_classification_type_confidence,
    ''::VARCHAR as statement_classification_type_explanation,
    P1.statement_sources,
    P1.created_at,
    array_agg(struct_pack(term := P1.term,
    classification := term_classification,
    isLocalScope := term_isLocalScope,
    definition := term_definition,
    confidence := 0.0,
    reason := NULL,
    isLocalScope_confidence := 0.0,
    isLocalScope_reason := NULL)) AS terms,
    P1.classification.REPLACE(' ', '_') as source
FROM P1
LEFT JOIN 
	(select 
		id, 
		id.REPLACE('_P2', '') AS doc_id,
		prompt,
		file_source as checkpoint,
		terms.term as term,
		terms.definition as term_definition,
		terms.isLocalScope as term_isLocalScope,
		created_at
		from RAW_SECTION_P2_EXTRACTED_NOUN_TRUE) AS P2
ON (P1.doc_id = P2.doc_id)
AND(P1.checkpoint = P2.checkpoint)
AND (P1.term = P2.term)
GROUP BY
    P1.id,
    P1.doc_id,
    P1.checkpoint,
    P1.statement_id,
    P1.statement_title,
    P1.statement_text,
    P1.verb_symbols,
    P1.classification,
    P1.statement_sources,
    P1.created_at)
UNION ALL
(WITH P1 AS (
SELECT
    id,
    doc_id,
    prompt,
    file_source AS checkpoint,
    id_1 AS statement_id,
    title AS statement_title,
    statement AS statement_text,
    (unnest(terms)).term AS term,
    (unnest(terms)).classification AS term_classification,
    verb_symbols,
    classification,
    confidence,
    reason,
    sources AS statement_sources,
    created_at
FROM (
        SELECT
            id,
            id.REPLACE('_P1', '') AS doc_id,
            prompt,
            file_source,
            unnest(elements) AS ELEMENT,
            created_at
        FROM
            RAW_SECTION_P1_EXTRACTED_ELEMENTS
            )
)
SELECT
    P1.id,
    P1.doc_id,
    P1.checkpoint,
    P1.statement_id,
    P1.statement_title,
    P1.statement_text,
    P1.verb_symbols,
    P1.classification as statement_classification_type,
    P1.confidence as statement_classification_type_confidence,
    P1.reason as statement_classification_type_explanation,
    P1.statement_sources,
    P1.created_at,
    array_agg(struct_pack(term := P1.term,
    classification := term_classification,
    isLocalScope := term_isLocalScope,
    definition := term_definition,
    confidence := term_confidence,
    reason := term_reason,
    isLocalScope_confidence := isLocalScope_confidence,
    isLocalScope_reason := isLocalScope_reason)) AS terms,
    P1.classification.REPLACE(' ', '_') as source
FROM P1
LEFT JOIN 
	(select 
		id, 
		id.REPLACE('_P2', '') AS doc_id,
		prompt,
		file_source as checkpoint,
		terms.term as term,
		terms.definition as term_definition,
		terms.isLocalScope as term_isLocalScope,
		terms.confidence as term_confidence,
		terms.reason as term_reason,
		terms.local_scope_confidence as isLocalScope_confidence,
        terms.local_scope_reason as isLocalScope_reason,
		created_at
		from RAW_SECTION_P2_EXTRACTED_NOUN) AS P2
ON (P1.doc_id = P2.doc_id)
AND(P1.checkpoint = P2.checkpoint)
AND (P1.term = P2.term)
GROUP BY
    P1.id,
    P1.doc_id,
    P1.checkpoint,
    P1.statement_id,
    P1.statement_title,
    P1.statement_text,
    P1.verb_symbols,
    P1.classification,
    P1.confidence,
    P1.reason,
    P1.statement_sources,
    P1.created_at)
);

SELECT * FROM RAW_SECTION_EXTRACTED_ELEMENTS_VW;

