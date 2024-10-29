
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
