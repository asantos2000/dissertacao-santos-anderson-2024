
from typing import List, Dict, Optional, Any, Tuple, Set
from pydantic import BaseModel, Field
import logging
import json
from json import JSONDecodeError

# Set up basic logging configuration for the checkpoint module
logging.basicConfig(
    level=logging.INFO,  # Set to INFO or another level as needed
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def convert_set_to_list(data: Any) -> Any:
    """
    Recursively converts sets to lists in the data structure.

    Args:
        data (Any): The data structure to process, which can be a dict, list, set, or other types.

    Returns:
        Any: The data structure with all sets converted to lists.
    """
    if isinstance(data, dict):
        return {key: convert_set_to_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_set_to_list(item) for item in data]
    elif isinstance(data, set):
        return list(data)
    else:
        return data


# Define a model for the Document
class Document(BaseModel):
    id: str
    type: str  # New field to represent the type of the document
    content: Any  # Content can be any data type: list, dict, string, etc.

# Define the DocumentManager class
class DocumentManager(BaseModel):
    documents: Dict[Tuple[str, str], Document] = Field(default_factory=dict)  # Keys are tuples (id, type)

    def add_document(self, doc: Document) -> None:
        """
        Adds a document to the manager.

        Args:
            doc (Document): The document to add.
        """
        key = (doc.id, doc.type)
        self.documents[key] = doc

    def retrieve_document(self, doc_id: str, doc_type: str) -> Optional[Document]:
        """
        Retrieves a document by its id and type.

        Args:
            doc_id (str): The ID of the document.
            doc_type (str): The type of the document.

        Returns:
            Optional[Document]: The retrieved document, or None if not found.
        """
        key = (doc_id, doc_type)
        return self.documents.get(key)

    def list_document_ids(self, doc_type: Optional[str] = None) -> List[str]:
        """
        Lists all document ids, optionally filtered by type.

        Args:
            doc_type (Optional[str], optional): The type of documents to list. Defaults to None.

        Returns:
            List[str]: A list of document ids.
        """
        if doc_type:
            return [doc_id for (doc_id, d_type) in self.documents.keys() if d_type == doc_type]
        else:
            return [doc_id for (doc_id, _) in self.documents.keys()]

    def exclude_document(self, doc_id: str, doc_type: str) -> None:
        """
        Excludes a document by its id and type.

        Args:
            doc_id (str): The ID of the document to exclude.
            doc_type (str): The type of the document.
        """
        key = (doc_id, doc_type)
        if key in self.documents:
            del self.documents[key]

    def persist_to_file(self, filename: str) -> None:
        """
        Persists the current state to a file, converting tuple keys to strings and sets to lists.

        Args:
            filename (str): The filename to save the documents.
        """
        serializable_documents = {f"{doc_id}|{doc_type}": convert_set_to_list(doc.dict()) for (doc_id, doc_type), doc in self.documents.items()}
        with open(filename, 'w') as file:
            json.dump(serializable_documents, file, indent=4)

    @classmethod
    def restore_from_file(cls, filename: str) -> 'DocumentManager':
        """
        Restores the state from a file, converting string keys back to tuples.

        Args:
            filename (str): The filename to restore the documents from.

        Returns:
            DocumentManager: The restored DocumentManager instance.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            documents = {(doc_id.split('|')[0], doc_id.split('|')[1]): Document(**doc_data) for doc_id, doc_data in data.items()}
            return cls(documents=documents)

def restore_checkpoint(filename: Optional[str]) -> DocumentManager:
    """
    Restores the document manager from a checkpoint file.

    Args:
        filename (str, optional): The path to the checkpoint file. Defaults to DEFAULT_CHECKPOINT_FILE.

    Returns:
        DocumentManager: The restored DocumentManager instance.

    Raises:
        FileNotFoundError: If the checkpoint file does not exist.

    See Also:
        - Reset the values delete the documents.json file and run: manager = DocumentManager()
        - Restore the state from the documents.json file, run: DocumentManager.restore_from_file("documents.json")
        - Exclue a document: manager.exclude_document(doc_id="§ 275.0-2", doc_type="section")
        - List documents: manager.list_document_ids(doc_type="section")
        - Get a document: manager.retrieve_document(doc_id=doc, doc_type="section")
    """

    try:
        restored_docs = DocumentManager.restore_from_file(filename)
        logger.info(f"Checkpoint restored from {filename}.")
    except (FileNotFoundError, JSONDecodeError):
        restored_docs = DocumentManager()
        logger.error(f"Checkpoint file '{filename}' not found or is empty, initializing new checkpoint.")
    return restored_docs

def save_checkpoint(filename: Optional[str], manager: DocumentManager) -> None:
    """
    Saves the current state of the DocumentManager to a checkpoint file.

    Args:
        manager (DocumentManager): The DocumentManager instance to save.

    Raises:
        Exception: If there is an error saving the checkpoint.
    """
    try:
        manager.persist_to_file(filename=filename)
        logger.info("Checkpoint saved.")
    except FileNotFoundError:
        logger.error("Error saving checkpoint. Check the directory path and permissions.")

def get_all_checkpoints(checkpoint_dir, prefix="documents", extension="json"):
    managers = []

    path = Path(checkpoint_dir)

    path.mkdir(parents=True, exist_ok=True)

    files = list(path.glob(f"{file_prefix}-*.{extension}"))
    file_info_list = []

    pattern = re.compile(rf'^{file_prefix}-(\d{{4}}-\d{{2}}-\d{{2}})-(\d+)\.{extension}$')
    for filepath in files:
        match = pattern.match(filepath.name)
        if match:
            date_str = match.group(1)
            number = int(match.group(2))
            file_info_list.append({'filename': filepath.name, 'date': date_str, 'number': number})
            
            print(filepath)
            managers.append(manager.restore_from_file(filepath))
    
    return managers, file_info_list

class DocumentProcessor:
    """
    DocumentProcessor is responsible for processing documents and categorizing elements such as terms, names, facts, and rules.

    Attributes:
        manager: Object used to manage document retrieval.
        elements_terms_set (set): Set of unique terms found in the documents.
        elements_names_set (set): Set of unique names found in the documents.
        elements_terms (list): List of detailed information about terms.
        elements_names (list): List of detailed information about names.
        elements_facts (list): List of facts extracted from documents.
        elements_rules (list): List of rules extracted from documents.
        elements_terms_definition (dict): Dictionary to store terms definitions by document ID.
    """

    def __init__(self, manager):
        """
        Initializes the DocumentProcessor instance and processes the documents.

        Args:
            manager: Object used to manage document retrieval.
        """
        self.manager = manager
        self.elements_terms_set = set()
        self.elements_names_set = set()
        self.elements_terms = []
        self.elements_names = []
        self.elements_facts = []
        self.elements_rules = []
        self.elements_terms_definition = {}
        
        # Automatically process definitions and elements when instantiated
        self.process_definitions()
        self.process_elements()

    def add_definition(self, doc_id, term, definition):
        """
        Adds a term definition to the elements_terms_definition dictionary.

        Args:
            doc_id (str): Identifier of the document.
            term (str): The term to be defined.
            definition (str): The definition of the term.
        """
        self.elements_terms_definition.setdefault(doc_id, {})[term] = definition

    def process_definitions(self):
        """
        Processes document terms definitions and stores them in elements_terms_definition.
        """
        docs_p2 = [s for s in self.manager.list_document_ids(doc_type="llm_response") if s.endswith("_P2")]

        for doc in docs_p2:
            doc_id = doc.replace("_P2", "")
            doc_content = self.manager.retrieve_document(doc, doc_type="llm_response").content
            doc_terms = doc_content.get("terms", [])
            for term in doc_terms:
                self.add_definition(doc_id, term.get("term"), term.get("definition"))

    def process_elements(self):
        """
        Processes elements from documents and categorizes them into terms, names, facts, and rules.
        """
        docs_p1 = [s for s in self.manager.list_document_ids(doc_type="llm_response") if s.endswith("_P1")]

        for doc in docs_p1:
            doc_content = self.manager.retrieve_document(doc, doc_type="llm_response").content
            doc_id = doc_content.get("section")
            doc_elements = doc_content.get("elements", [])
            for element in doc_elements:
                element_classification = element.get("classification")
                element_id = element.get("id")
                verb_symbols = element.get("verb_symbols") or element.get("verb_symbol")
                if isinstance(verb_symbols, str):
                    verb_symbols = [verb_symbols]
                elif verb_symbols is None:
                    verb_symbols = []
                element_dict = {
                    "doc_id": doc_id,
                    "expression_id": element_id,
                    "expression": element.get("expression"),
                    "source": element.get("source"),
                    "terms": element.get("terms", []),
                    "verb_symbols": verb_symbols
                }

                match element_classification:
                    case "Fact" | "Fact Type":
                        self.elements_facts.append(element_dict)
                    case "Operative Rule":
                        self.elements_rules.append(element_dict)

                element_terms = element.get("terms", [])
                if element_terms:
                    for term in element_terms:
                        signifier = term.get("term")
                        term_dict = {
                            "doc_id": doc_id,
                            "signifier": signifier,
                            "expression_id": element_id,
                            "definition": self.elements_terms_definition.get(doc_id, {}).get(signifier),
                            "source": element.get("source")
                        }
                        if term.get("classification") == "Common Noun":
                            self.elements_terms.append(term_dict)
                            self.elements_terms_set.add(signifier)
                        else:
                            self.elements_names.append(term_dict)
                            self.elements_names_set.add(signifier)

    # def get_unique_terms(self):
    #     """
    #     Returns the set of unique terms found in the documents.

    #     Returns:
    #         set: Set of unique terms.
    #     """
    #     return self.elements_terms_set

    # def get_unique_names(self):
    #     """
    #     Returns the set of unique names found in the documents.

    #     Returns:
    #         set: Set of unique names.
    #     """
    #     return self.elements_names_set

    def get_unique_terms(self, doc_id=None):
        """
        Returns the set of unique terms found in the documents. If doc_id is provided,
        returns only the unique terms for that specific document.

        Args:
            doc_id (str, optional): Identifier of the document. Defaults to None.

        Returns:
            set: Set of unique terms.
        """
        if doc_id:
            return {term["signifier"] for term in self.elements_terms if term["doc_id"] == doc_id}
        return self.elements_terms_set

    def get_unique_names(self, doc_id=None):
        """
        Returns the set of unique names found in the documents. If doc_id is provided,
        returns only the unique names for that specific document.

        Args:
            doc_id (str, optional): Identifier of the document. Defaults to None.

        Returns:
            set: Set of unique names.
        """
        if doc_id:
            return {name["signifier"] for name in self.elements_names if name["doc_id"] == doc_id}
        return self.elements_names_set

    def get_terms(self):
        """
        Returns the list of terms with detailed information.

        Returns:
            list: List of terms.
        """
        return self.elements_terms

    def get_names(self):
        """
        Returns the list of names with detailed information.

        Returns:
            list: List of names.
        """
        return self.elements_names

    def get_facts(self):
        """
        Returns the list of facts extracted from documents.

        Returns:
            list: List of facts.
        """
        return self.elements_facts

    def get_rules(self):
        """
        Returns the list of rules extracted from documents.

        Returns:
            list: List of rules.
        """
        return self.elements_rules

    def get_term_info(self, doc_id, term):
        """
        Retrieves information about a specific term from elements.

        Args:
            doc_id (str): Document identifier.
            term (str): Term to retrieve information for.

        Returns:
            dict or None: A dictionary containing term information if found, otherwise None.
        """
        definition = self.elements_terms_definition.get(doc_id, {}).get(term)
        if definition:
            for term_dict in self.elements_terms + self.elements_names:
                if term_dict["doc_id"] == doc_id and term_dict["signifier"] == term:
                    return {
                        "definition": definition,
                        "source": term_dict["source"],
                        "expression_id": term_dict["expression_id"]
                    }
        return None

    def get_name_info(self, doc_id, name):
        """
        Retrieves information about a specific name from elements.

        Args:
            doc_id (str): Document identifier.
            name (str): Name to retrieve information for.

        Returns:
            dict or None: A dictionary containing name information if found, otherwise None.
        """
        for name_dict in self.elements_names:
            if name_dict["doc_id"] == doc_id and name_dict["signifier"] == name:
                return {
                    "definition": name_dict.get("definition"),
                    "source": name_dict["source"],
                    "expression_id": name_dict["expression_id"]
                }
        return None

    def get_fact_info(self, doc_id, expression_id):
        """
        Retrieves information about a specific fact from elements.

        Args:
            doc_id (str): Document identifier.
            expression_id (str): Expression identifier of the fact.

        Returns:
            dict or None: A dictionary containing fact information if found, otherwise None.
        """
        for fact_dict in self.elements_facts:
            if fact_dict["doc_id"] == doc_id and fact_dict["expression_id"] == expression_id:
                terms = [term.get("term") for term in fact_dict.get("terms", []) if term.get("classification") == "Common Noun"]
                names = [term.get("term") for term in fact_dict.get("terms", []) if term.get("classification") == "Proper Noun"]
                return {
                    "expression": fact_dict["expression"],
                    "source": fact_dict["source"],
                    "terms": terms,
                    "names": names,
                    "verb_symbols": fact_dict.get("verb_symbols", [])
                }
        return None

    def get_rule_info(self, doc_id, expression_id):
        """
        Retrieves information about a specific rule from elements.

        Args:
            doc_id (str): Document identifier.
            expression_id (str): Expression identifier of the rule.

        Returns:
            dict or None: A dictionary containing rule information if found, otherwise None.
        """
        for rule_dict in self.elements_rules:
            if rule_dict["doc_id"] == doc_id and rule_dict["expression_id"] == expression_id:
                terms = [term.get("term") for term in rule_dict.get("terms", []) if term.get("classification") == "Common Noun"]
                names = [term.get("term") for term in rule_dict.get("terms", []) if term.get("classification") == "Proper Noun"]
                return {
                    "expression": rule_dict.get("expression"),
                    "source": rule_dict.get("source"),
                    "terms": terms,
                    "names": names,
                    "verb_symbols": rule_dict.get("verb_symbols", [])
                }
        return None

# # Example usage
# processor = DocumentProcessor(manager)

# # Access processed data
# unique_terms = processor.get_unique_terms()
# unique_names = processor.get_unique_names()
# terms = processor.get_terms()
# names = processor.get_names()
# facts = processor.get_facts()
# rules = processor.get_rules()

# print(f"Unique terms: {len(unique_terms)}")
# print(f"Unique names: {len(unique_names)}")

# print(f'Rules from § 275.0-2: {processor.get_rule_info("§ 275.0-2", 3)}')
# print(f'Facts from § 275.0-2: {processor.get_fact_info("§ 275.0-2", 2)}')
