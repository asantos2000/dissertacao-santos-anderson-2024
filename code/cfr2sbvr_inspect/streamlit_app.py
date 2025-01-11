import datetime as dt
from itertools import combinations
import logging

import streamlit as st

from app_modules import (
    display_section,
    highlight_statement,
    list_to_markdown,
    witt_taxonomy_dialog,
    info_dialog,
    load_data,
    calculate_statements_similarity,
    db_connection,
    get_doc_ids,
    get_table_names,
    get_checkpoints,
    extract_row_values
)


# Config logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="streamlit_app.log", level=logging.INFO)

# Constants
QUALITY_THRESHOLD = 0.8
LOCAL_DB = True  # Use cloud database - False or local database - True
DEFAULT_DATA_DIR = "code/cfr2sbvr_inspect/data"


#
# Main
#

st.set_page_config(page_title="CFR2SBVR Inspect", page_icon="🏛️", layout="wide")

st.sidebar.title(":material/assured_workload: CFR2SBVR Inspect")

# Connect to the database
conn = db_connection(LOCAL_DB, DEFAULT_DATA_DIR)

st.sidebar.header("Checkpoints", divider="red")

# Sidebar selectbox to choose a process
process_dict = {
    "Extraction": "extraction",
    "Classification": "classification",
    "Transformation": "transformation",
    "Validation": "validation",
}

process_icon = {
    "Extraction": ":material/colorize:",
    "Classification": ":material/category:",
    "Transformation": ":material/move_down:",
    "Validation": ":material/fact_check:",
}

process_selected = st.sidebar.selectbox("Choose a process", process_dict.keys())

if st.sidebar.button(
    "About process",
    key="process_info",
    type="tertiary",
    icon=":material/info:",
    help="Click to see more information about the process",
):
    info_dialog("process")

doc_ids = get_doc_ids(conn)

# Sidebar selectbox to choose a file
doc_id_selected = st.sidebar.multiselect("Choose a doc_id", doc_ids)

table_names = get_table_names(conn, process_dict, process_selected)

# Sidebar selectbox to choose a file
table_selected = st.sidebar.selectbox("Choose a table", table_names)

table_markdown = "\n".join([f"- {table}" for table in table_names])

st.title(f"{process_icon[process_selected]} {process_selected} process")
# Display the tables available for the selected process
st.markdown(
    f"""
CFR2SBVR Inspect is a tool to inspect CFR2SBVR checkpoint files.

Tables available for {process_selected}:

{table_markdown}
"""
)

checkpoints = get_checkpoints(conn, table_selected)

# Sidebar selectbox to choose a file
checkpoints_selected = st.sidebar.multiselect("Choose checkpoints", checkpoints)

st.header("Dataset", divider="red")

#
# Load the selected data
#
data_df = load_data(
    conn, table_selected, checkpoints_selected, doc_id_selected, process_selected
)

event = st.dataframe(
    data_df,
    key="id",
    on_select="rerun",
    use_container_width=True,
    selection_mode=["multi-row"],
)

st.sidebar.header("Dataset info", divider="red")
st.sidebar.write(f"Content from: {table_selected}")
st.sidebar.write(f"Loaded {len(data_df)} line(s)")

st.header("Evaluate", divider="rainbow")

comp_tab, feedback_tab = st.tabs(["Compare", "Feedback"])

with comp_tab:
    if event.selection:
        try:
            columns = st.columns(len(event.selection["rows"]))

            # Loop through the rows and assign each row to a column
            for col, row in zip(columns, event.selection["rows"]):
                with col:
                    row_values, missing_messages = extract_row_values(data_df, row)

                    #st.write(row_values)

                    # Statement
                    st.subheader("Statement")
                    # Display selected row number
                    checkpoint = row_values.get("checkpoint")
                    st.write(f"Selected checkpoint '{checkpoint}', row: {row}")

                    # Display frozen section
                    doc_id = row_values.get("doc_id")
                    if doc_id:
                        with st.expander(f"Section {doc_id} (frozen)"):
                            content = display_section(conn, doc_id)
                            st.write(content, unsafe_allow_html=True)

                    # Display the title
                    title = row_values.get("statement_title")
                    if title:
                        st.write(f"Title: **{title}**")

                    # Generate highlighted text
                    statement_id = row_values.get("statement_id")
                    statement = row_values.get("statement_text")
                    classification_type = row_values.get("statement_classification_type")
                    classification_subtype = row_values.get("statement_classification_subtype")
                    terms = row_values.get("terms")
                    verb_symbols = row_values.get("verb_symbols")
                    sources = row_values.get("statement_sources")
                    highlighted_text = highlight_statement(
                        f"OS{row}",
                        doc_id,
                        statement_id,
                        classification_type,
                        classification_subtype,
                        terms,
                        verb_symbols,
                        statement,
                        sources,
                    )
                    # Display the statement_text
                    st.write(highlighted_text, unsafe_allow_html=True)

                    # Display the transformed statement
                    transformed_statement = row_values.get("transformed")
                    if transformed_statement:
                        st.write("**Rule**")

                        highlighted_text = highlight_statement(
                            f"TS{row}",
                            doc_id,
                            statement_id,
                            classification_type,
                            classification_subtype,
                            terms,
                            verb_symbols,
                            transformed_statement,
                            sources,
                        )
                        st.markdown(highlighted_text, unsafe_allow_html=True)

                    # Display the source of the statement
                    statement_from = row_values.get("source")
                    if statement_from:
                        st.write(f"**From**: {statement_from}")
                    # display the terms and verb symbols
                    terms_list = [
                        dict(t) for t in terms
                    ]  # if each item in terms is already a dict
                    verb_symbols_list = verb_symbols.tolist()
                    st.json(
                        {"terms": terms_list, "verb_symbols": verb_symbols_list},
                        expanded=1,
                    )

                    # display the classification type and subtype
                    with st.expander("Details"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Classification**")
                            if classification_type:
                                if st.button(
                                    f"type: {classification_type}",
                                    key=f"classification_type_{row}",
                                    type="tertiary",
                                    icon=":material/info:",
                                    help="Click to see more information about the classification type",
                                ):
                                    if classification_type == "Fact Type":
                                        classification_type = "Definitional rules"
                                    if classification_type == "Operative Rule":
                                        classification_type = "Operative rules"
                                    witt_taxonomy_dialog(classification_type)
                                
                                classification_type_confidence = row_values.get("statement_classification_type_confidence")
                                st.write(
                                    f"Confidence: {classification_type_confidence}"
                                )
                                classification_type_explanation = row_values.get("statement_classification_type_explanation")
                                st.write(
                                    f"Explanation: {classification_type_explanation}"
                                )
                            if classification_subtype:
                                if st.button(
                                    f"subtype: {classification_subtype}",
                                    key=f"classification_subtype_{row}",
                                    type="tertiary",
                                    icon=":material/info:",
                                    help="Click to see more information about the classification subtype",
                                ):
                                    witt_taxonomy_dialog(classification_subtype)
                                
                                classification_subtype_confidence = row_values.get("statement_classification_subtype_confidence")
                                st.write(
                                    f"Confidence: {classification_subtype_confidence}"
                                )

                                classification_subtype_explanation = row_values.get("statement_classification_subtype_explanation")
                                st.write(
                                    f"Explanation: {classification_subtype_explanation}"
                                )

                            template_ids = row_values.get("transformation_template_ids")
                            if template_ids:
                                st.write(
                                    f"Template(s): \n\n {list_to_markdown(template_ids, ordered=False)}"
                                )
                        with col2:
                            transformation_confidence = row_values.get("transformation_confidence")
                            transformation_reason = row_values.get("transformation_reason")
                            if transformation_confidence:
                                st.write("**Transformation**")
                                st.write(f"Confidence: {transformation_confidence}")
                                st.write(f"Reason: {transformation_reason}")
                            
                            transformation_semscore = row_values.get("transformation_semscore")
                            if transformation_semscore:
                                st.write("**Validation**")
                                transformation_similarity_score = row_values.get("transformation_similarity_score")
                                st.metric(
                                    label="Semantic Score",
                                    value=round(transformation_semscore, 2),
                                    delta=round(
                                        transformation_semscore
                                        - transformation_similarity_score,
                                        2,
                                    ),
                                    help="Semantic score of the transformation and the difference with the similarity score",
                                )
                                st.metric(
                                    label="Similarity Score",
                                    value=round(transformation_similarity_score, 2),
                                    delta=round(
                                        transformation_similarity_score
                                        - transformation_semscore,
                                        2,
                                    ),
                                    help="Similarity score of the transformation and the difference with the semantic score",
                                )

                                transformation_similarity_score_confidence = row_values.get("transformation_similarity_score_confidence")
                                st.write(
                                    f"Similarity score confidence: {transformation_similarity_score_confidence}"
                                )

                                transformation_findings = row_values.get("transformation_findings")
                                st.write(
                                    f"Similarity score findings: \n\n {list_to_markdown(transformation_findings)}"
                                )

                                transformation_accuracy = row_values.get("transformation_accuracy")
                                st.write(f"Accuracy: {transformation_accuracy}")

                                transformation_grammar_syntax_accuracy = row_values.get("transformation_grammar_syntax_accuracy")
                                st.write(
                                    f"Grammar/Sintax Accuracy: {transformation_grammar_syntax_accuracy}"
                                )

                    # Display what is missing
                    with st.expander("Missing"):
                        if missing_messages:
                            for missing_message in missing_messages:
                                st.write(f":material/error: {missing_message}")
        except Exception as e:
            st.write("There is nothing to see here yet, select at least one row.")
            logger.info(f"Error {e}.")

        # Display similarity scores
        with st.expander("Levenshtein Distance (LD)"):
            rows_selected = event.selection["rows"]
            if len(rows_selected) > 1:
                for column in ("statement_title", "statement_text", "transformed"):
                    st.markdown(f"*{column}:*")
                    for row1, row2 in combinations(rows_selected, 2):
                        try:
                            score = calculate_statements_similarity(
                                str(data_df.at[row1, column]),
                                str(data_df.at[row2, column]),
                            )
                            if score < QUALITY_THRESHOLD:
                                st.markdown(
                                    f"- ({row1}, {row2}) = <span style='color:red;'>{score:.2f}</span>",
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(f"- ({row1}, {row2}) = {score:.2f}")
                        except Exception as e:
                            st.write(f"- No {e} available")

with feedback_tab:
    st.write(
        "The best option is SMEs' feedback about which statements are best for keeping the meaning."
    )

    filtered_df = data_df.iloc[event.selection["rows"], :]

    st.dataframe(filtered_df)

    if st.button("Save as best option(s)"):
        st.json(filtered_df.to_json(orient="records"))
        st.info(f"Best option(s) saved at {dt.datetime.now()}")
