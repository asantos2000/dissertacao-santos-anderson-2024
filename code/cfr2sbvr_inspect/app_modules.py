import re
import html
import logging
import os

import jellyfish
from dotenv import load_dotenv
import duckdb

import rules_taxonomy_provider.main as rules_taxonomy_provider
from rules_taxonomy_provider.main import RuleInformationProvider

import streamlit as st

logger = logging.getLogger(__name__)

# Highlight term in the statement
def highlight_statement(
    line_id,
    doc_id,
    element_id,
    classification_type,
    classification_subtype,
    terms,
    verb_symbols,
    statement,
    sources,
):
    sources_links = []
    for source in sources:
        doc_id_url = doc_id.replace("§ ", "")
        url = f"https://www.ecfr.gov/current/title-17/part-275#p-{doc_id_url}{source}"
        sources_links.append(f'<a href="{url}">{source}</a>')
    sources = ", ".join(sources_links)

    classification = classification_type
    if classification_subtype:
        classification += f" | {classification_subtype}"

    # Clean up the statement
    statement = statement.replace("$", "\\$")

    def highlight_match_term(term_info):
        def replace_term(match):
            original = match.group(0)
            if term_info["classification"] == "Common Noun":
                # Aqui apenas inserimos um placeholder. Depois criaremos o tooltip.
                return (
                    f'<span style="text-decoration: underline; '
                    f'text-decoration-color: green;">{original}</span>'
                )
            elif term_info["classification"] == "Proper Noun":
                return (
                    f'<span style="text-decoration: underline double; '
                    f'text-decoration-color: green;">{original}</span>'
                )
            return original
        return replace_term

    # Apply term substitutions (without inserting the tooltip yet).
    for t in terms:
        term_regex = rf"\b{re.escape(t['term'])}\b"
        statement = re.sub(term_regex,
                           highlight_match_term(t),
                           statement,
                           flags=re.IGNORECASE)

    # Highlight verb symbols
    def highlight_match_verb(match):
        original = match.group(0)
        return f'<span style="font-style: italic; color: blue;">{original}</span>'

    for verb in verb_symbols:
        verb_regex = rf"\b{re.escape(verb)}\b"
        statement = re.sub(verb_regex, highlight_match_verb, statement, flags=re.IGNORECASE)

    def add_tooltip(term_info):
        definition = html.escape(term_info.get("definition", "") or "Missing")
        confidence = term_info.get("confidence", "")
        reason = html.escape(term_info.get("reason", "") or "")
        isLocalScope = term_info.get("isLocalScope", False)
        if isLocalScope:
            scope = "📍"
        else:
            scope = "🌎"

        tooltip_content = (
            f"{scope} "
            f"Definition: {definition} - "
            f"Confidence: {confidence} - "
            f"Reason: {reason}"
        )

        # Regext to capture the tag generated above (simple or double underline) with the corresponding text.
        if term_info["classification"] == "Common Noun":
            # Simple underline
            tag_pattern = (
                r'<span style="text-decoration: underline; text-decoration-color: green;">'
                rf"(?P<content>{re.escape(term_info['term'])}|{re.escape(term_info['term'].lower())}|{re.escape(term_info['term'].capitalize())})"
                r"</span>"
            )
        else:
            # Double underline
            tag_pattern = (
                r'<span style="text-decoration: underline double; text-decoration-color: green;">'
                rf"(?P<content>{re.escape(term_info['term'])}|{re.escape(term_info['term'].lower())}|{re.escape(term_info['term'].capitalize())})"
                r"</span>"
            )

        def insert_title(match):
            original_span = match.group(0)
            content = match.group("content")
            # Insert the title attribute without changing the inner text
            return original_span.replace(
                ';">' + content,  # ponto de inserção
                f';" title="{tooltip_content}">' + content
            )

        return tag_pattern, insert_title

    for t in terms:
        tag_pattern, insert_title_fn = add_tooltip(t)
        statement = re.sub(tag_pattern, insert_title_fn, statement, flags=re.IGNORECASE)

    sup = f" [{classification}]"
    final_text = f"{line_id}: <strong>{sources}</strong> {statement}{sup}"
    return final_text



def display_section(conn, doc_id):
    doc_id_url = doc_id.replace("§ ", "")
    section_url = f"https://www.ecfr.gov/current/title-17/section-{doc_id_url}"

    content = conn.sql(
        f"SELECT content FROM RAW_SECTION WHERE id = '{doc_id}'"
    ).fetchall()[0][0]
    content = content.replace("\n", "<br>")
    content = content.replace("$", "\$")
    content = content.replace(doc_id, f'<a href="{section_url}">{doc_id}</a>')

    #st.write(content, unsafe_allow_html=True)
    return content

@st.dialog("Witt (2012) taxonomy", width="large")
def witt_taxonomy_dialog(classification): 
    rule_provider = RuleInformationProvider("code/cfr2sbvr_inspect/data")
    markdown_data = rule_provider.get_classification_and_templates(classification, return_forms="fact_type")
    st.markdown(markdown_data)


@st.dialog("ⓘ Info", width="large")
def info_dialog(topic):
    if topic == "process":
        st.markdown(
            """
            ### Process
            - Extraction: Extracts the fact types and operative rules statements from the CFR sections.
            - Classification: Classifies the statements extracted with Witt (2012) taxonomy.
            - Transformation: Transform the statements into SBVR using Witt (2012) templates.
            - Validation: Validates the extraction, classification, and transformation processes against a golden dataset calculating precision, accuracy, and other scores.
            """)
        st.image("code/cfr2sbvr_inspect/static/cfr2sbvr-process.png")
        st.write("> Witt, Graham. Writing effective business rules. Elsevier, 2012.")


def list_to_markdown(list, ordered=True):
    if ordered:
       prefix = "1."
    else:
         prefix = "-"
    return "\n".join([f"{prefix} {item}" for item in list])

def disconnect_db(conn):
    st.write("called")
    # conn.close()


def db_connection(local_db=False, default_data_dir="data"):
    # Connect to the database
    if local_db:
        conn = duckdb.connect(f"{default_data_dir}/database_v4.db", read_only=True)
    else:
        load_dotenv()
        mother_duck_token = os.getenv("MOTHER_DUCK_TOKEN")
        conn = duckdb.connect(f"md:cfr2sbvr_db?motherduck_token={mother_duck_token}", read_only=True)
    
    return conn

# @st.cache_data
def load_data(conn, table, checkpoints, doc_ids, process_selected):
    where_clause = ""

    # where_clause += f' AND file_source=\'{filters["checkpoint"]}\''
    checkpoints_string = ", ".join(f"'{item}'" for item in checkpoints)
    doc_ids_string = ", ".join(f"'{item}'" for item in doc_ids)
    if checkpoints_string:
        where_clause += f" AND checkpoint in ({checkpoints_string})"

    if doc_ids_string:
        where_clause += f" AND doc_id in ({doc_ids_string})"

    data_query = f"""
    SELECT *
    FROM {table}
    WHERE 1 = 1
    {where_clause}
    ORDER BY *
    ;
    """

    logger.debug(data_query)

    return conn.sql(query=data_query).fetchdf()


def calculate_statements_similarity(statement1, statement2):
    # Calculate the similarity score using the Levenshtein distance
    score = jellyfish.levenshtein_distance(statement1.lower(), statement2.lower())
    similarity_score = 1 - (
        score / max(len(statement1), len(statement2))
    )  # Normalize to a similarity score
    return similarity_score


def get_doc_ids(conn):
    return conn.sql("select distinct id.replace('_P1', '') as doc_id from RAW_SECTION_P1_EXTRACTED_ELEMENTS order by id")


def get_table_names(conn, process_dict, process_selected):
    query = f"""
    SELECT DISTINCT TABLE_NAME,
    FROM CHECKPOINT_METADATA
    WHERE doc_source in ('both')
    AND process='{process_dict[process_selected]}'
    ORDER BY 1 DESC;
    """

    all_tables = conn.sql(query).fetchall()

    return [table_name[0] for table_name in all_tables]


def get_checkpoints(conn, table_selected):
    return conn.sql(f"select distinct checkpoint from {table_selected} order by 1")


def extract_row_values(data_df, row):
    # Try get values dependent of the process
    missing_messages = []
    row_values = {}

    # Extract values
    # doc_id = data_df.at[row, "doc_id"]
    # title = data_df.at[row, "statement_title"]
    # statement = data_df.at[row, "statement_text"]
    # statement_id = data_df.at[row, "statement_id"]
    # checkpoint = data_df.at[row, "checkpoint"]
    # sources = data_df.at[row, "statement_sources"]

    row_values["doc_id"] = data_df.at[row, "doc_id"]
    row_values["statement_title"] = data_df.at[row, "statement_title"]
    row_values["statement_text"] = data_df.at[row, "statement_text"]
    row_values["statement_id"] = data_df.at[row, "statement_id"]
    row_values["checkpoint"] = data_df.at[row, "checkpoint"]
    row_values["statement_sources"] = data_df.at[row, "statement_sources"]

    try:
        #transformed_statement = data_df.at[row, "transformed"]
        row_values["transformed"] = data_df.at[row, "transformed"]
    except Exception as e:
        missing_messages.append(f"{e}")
        #transformed_statement = None
        # row_values["transformed_statement"] = None
    try:
        #classification_type = data_df.at[row, "statement_classification_type"]
        row_values["statement_classification_type"] = data_df.at[row, "statement_classification_type"]
    except Exception as e:
        missing_messages.append(f"{e}")
        #classification_type = ""
        # row_values["classification_type"] = None
    # statement_classification_type_confidence
    try:
        #classification_type_confidence = data_df.at[row, "statement_classification_type_confidence"]
        row_values["statement_classification_type_confidence"] = data_df.at[row, "statement_classification_type_confidence"]
        #classification_type_explanation = data_df.at[row, "statement_classification_type_explanation"]
        row_values["statement_classification_type_explanation"] = data_df.at[row, "statement_classification_type_explanation"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # classification_type_confidence = None
        # classification_type_explanation = None
        # row_values["classification_type_confidence"] = None
        # row_values["classification_type_explanation"] = None
    # statement_classification_subtype
    try:
        # classification_subtype = data_df.at[row, "statement_classification_subtype"]
        # classification_subtype_confidence = data_df.at[row, "statement_classification_subtype_confidence"]
        # classification_subtype_explanation = data_df.at[row, "statement_classification_subtype_explanation"]
        row_values["statement_classification_subtype"] = data_df.at[row, "statement_classification_subtype"]
        row_values["statement_classification_subtype_confidence"] = data_df.at[row, "statement_classification_subtype_confidence"]
        row_values["statement_classification_subtype_explanation"] = data_df.at[row, "statement_classification_subtype_explanation"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # classification_subtype = ""
        # classification_subtype_confidence = None
        # classification_subtype_explanation = None
        # row_values["classification_subtype"] = None
        # row_values["classification_subtype_confidence"] = None
        # row_values["classification_subtype_explanation"] = None
    # terms
    try:
        # terms = data_df.at[row, "terms"]
        row_values["terms"] = data_df.at[row, "terms"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # terms = []
    # verb_symbols
    try:
        # verb_symbols = data_df.at[row, "verb_symbols"]
        row_values["verb_symbols"] = data_df.at[row, "verb_symbols"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # verb_symbols = []
    # transformation_template_ids
    try:
        # template_ids = data_df.at[row, "transformation_template_ids"]
        row_values["transformation_template_ids"] = data_df.at[row, "transformation_template_ids"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # template_ids = []
    # transformation_confidence
    try:
        # transformation_confidence = data_df.at[row, "transformation_confidence"]
        # transformation_reason = data_df.at[row, "transformation_reason"]
        row_values["transformation_confidence"] = data_df.at[row, "transformation_confidence"]
        row_values["transformation_reason"] = data_df.at[row, "transformation_reason"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # transformation_confidence = None
        # transformation_reason = None
    # transformation scores
    try:
        # transformation_semscore = data_df.at[row, "semscore"]
        # transformation_similarity_score = data_df.at[row, "similarity_score"]
        # transformation_similarity_score_confidence = data_df.at[row, "similarity_score_confidence"]
        # transformation_findings = data_df.at[row, "findings"]
        # transformation_accuracy = data_df.at[row, "transformation_accuracy"]
        # transformation_grammar_syntax_accuracy = data_df.at[row, "grammar_syntax_accuracy"]
        row_values["transformation_semscore"] = data_df.at[row, "semscore"]
        row_values["transformation_similarity_score"] = data_df.at[row, "similarity_score"]
        row_values["transformation_similarity_score_confidence"] = data_df.at[row, "similarity_score_confidence"]
        row_values["transformation_findings"] = data_df.at[row, "findings"]
        row_values["transformation_accuracy"] = data_df.at[row, "transformation_accuracy"]
        row_values["transformation_grammar_syntax_accuracy"] = data_df.at[row, "grammar_syntax_accuracy"]
    except Exception as e:
        missing_messages.append(f"{e}")
        # transformation_semscore = None
        # transformation_similarity_score = None
        # transformation_similarity_score_confidence = None
        # transformation_findings = None
        # transformation_accuracy = None
        # transformation_grammar_sintaxe_accuracy = None
    # source of statement
    try:
        # statament_from = data_df.at[row, "source"]
        row_values["statament_from"] = data_df.at[row, "source"]
    except Exception as e:
        missing_messages.append(f"from {e}")
        # statament_from = []

    return row_values, missing_messages


def format_score(score, THRESHOLD):
    if score < THRESHOLD:
        return f'<span style="color:red;">{score:.2f}</span>'
    else:
        return f'{score:.2f}'