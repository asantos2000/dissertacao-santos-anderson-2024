CREATE OR REPLACE VIEW RAW_TRANSFORM_ELEMENTS_VW AS (
SELECT
	*,
	'Operative_Rules' as source
FROM
	main.RAW_TRANSFORM_OPERATIVE_RULES_VW
UNION ALL
SELECT
	*,
	'Terms' as source
FROM
	main.RAW_TRANSFORM_TERMS_VW
UNION ALL
SELECT
	*,
	'Names' as source
FROM
	main.RAW_TRANSFORM_NAMES_VW
UNION ALL
SELECT
	*,
	'Fact_Types' as source
FROM
	main.RAW_TRANSFORM_FACT_TYPES_VW
);

SELECT * FROM RAW_TRANSFORM_ELEMENTS_VW;
