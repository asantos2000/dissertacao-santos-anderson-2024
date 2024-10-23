from franz.openrdf.connect import ag_connect
from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.sail.allegrographserver import Catalog
from franz.openrdf.repository.repository import Repository
from franz.openrdf.rio.rdfformat import RDFFormat
import os

# Force run the script. 
# If set to True, the script will run regardless of risk of data loss.
FORCE = True
CLEAN_BEFORE_RUN = True
REPO = os.getenv('AG_REPOSITORY')
CATALOG = os.getenv('AG_CATALOG')
HOST = os.getenv('AG_HOST')
PORT = os.getenv('AG_PORT')
USER = os.getenv('AG_USER')
PASSWORD = os.getenv('AG_PASSWORD')

# Connection
with ag_connect(repo=REPO, catalog=CATALOG, host=HOST, port=PORT,
                user=USER, password=PASSWORD) as conn:

    print (conn.isEmpty())

    # If true will clean all data
    if CLEAN_BEFORE_RUN:
        conn.clear()

    # If FORCE is true will run anyway
    if conn.isEmpty() or FORCE:
        #
        # Create graph nodes
        #

        # Language
        result = conn.executeUpdate("""
PREFIX sbvr: <https://www.omg.org/spec/SBVR/20190601#>
PREFIX cfr-sbvr: <http://cfr2sbvr.com/cfr#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT DATA {
cfr-sbvr:EnglishLanguage
    a sbvr:Language ;
    skos:label "English" ;
    sbvr:signifier "English" .
}
        """)

        # CFR vocabulary namespace
        result = conn.executeUpdate("""
# Insert CFR-FRO graph metadata
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX fro-cfr: <http://finregont.com/fro/cfr/Code_Federal_Regulations.ttl#>
PREFIX sbvr: <https://www.omg.org/spec/SBVR/20190601#>
PREFIX cfr-sbvr: <http://cfr2sbvr.com/cfr#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT DATA {
fro-cfr:CFR_Title_17_Part_275_VOC
    a owl:Class, sbvr:Vocabulary .

fro-cfr:CFR_Title_17_Part_275_NS
    a owl:Class, sbvr:VocabularyNamespace;
    sbvr:vocabularyNamespaceIsDerivedFromVocabulary fro-cfr:CFR_Title_17_Part_275_VOC ;
    sbvr:namespaceHasURI <http://finregont.com/fro/cfr/Code_Federal_Regulations.ttl#> ;
    sbvr:vocabularyIsExpressedInLanguage cfr-sbvr:EnglishLanguage ;
    dct:title "RULES AND REGULATIONS, INVESTMENT ADVISERS ACT OF 1940" ;
    skos:definition "Financial Regulation Ontology: FRO CFR Title 17 Part 275" ;
    dct:source <https://finregont.com/fro/cfr/FRO_CFR_Title_17_Part_275.ttl> .
}
        """)

         # CFR vocabulary and vocabulary namespace
        result = conn.executeUpdate("""
# Insert FIBO graph metadata
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX fibo: <https://spec.edmcouncil.org/fibo/ontology/QuickFIBOProd#>
PREFIX sbvr: <https://www.omg.org/spec/SBVR/20190601#>
PREFIX cfr-sbvr: <http://cfr2sbvr.com/cfr#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT DATA {
fibo:FIBO_VOC
    a owl:Class, sbvr:Vocabulary .

fibo:FIBO_NS
    a owl:Class, sbvr:VocabularyNamespace ;
    sbvr:vocabularyNamespaceIsDerivedFromVocabulary fibo:FIBO_VOC ;
    sbvr:namespaceHasURI <https://spec.edmcouncil.org/fibo/ontology/QuickFIBOProd#> ;
    sbvr:vocabularyIsExpressedInLanguage cfr-sbvr:EnglishLanguage ;
    dct:title "Financial Business Ontology" ;
    skos:definition "This ontology is provided for the convenience of FIBO users. It loads all of the very latest FIBO production ontologies based on the contents of GitHub, rather than those that comprise a specific version, such as a quarterly release. Note that metadata files and other 'load' files, such as the various domain-specific 'all' files, are intentionally excluded." ;
    dct:source <https://spec.edmcouncil.org/fibo/ontology/master/2024Q2/LoadFIBOProd.ttl> .
}
        """)

        # CFR_SBVR
        result = conn.executeUpdate("""
# Insert SBVR graph metadata
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX cfr-sbvr: <http://cfr2sbvr.com/cfr#>
PREFIX sbvr: <https://www.omg.org/spec/SBVR/20190601#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT DATA {
cfr-sbvr:CFR_SBVR_VOC
    a owl:Class, sbvr:Vocabulary .
                        
cfr-sbvr:CFR_SBVR_NS
    a owl:Class, sbvr:VocabularyNamespace;
    sbvr:namespaceHasURI <http://cfr2sbvr.com/cfr#> ;
    sbvr:vocabularyIsExpressedInLanguage cfr-sbvr:EnglishLanguage ;
    sbvr:vocabularyNamespaceIsDerivedFromVocabulary cfr-sbvr:CFR_SBVR_VOC ;
    dct:title "Semantics of Business Vocabulary and Business Rules (SBVR) for Code of Federal Regulations (CFR)" ;
    skos:definition "SBVR-CFR is an adopted standard of the Object Management Group (OMG) intended to be the basis for formal and detailed natural language declarative description of CFR regulations" ;
    dct:source <https://github.com/asantos2000/dissertacao-santos-anderson-2024> .
}
        """)

        #
        # Load data to graphs
        #

        # CFR - US_LegalReference.ttl
        conn.addFile(filePath='../data/US_LegalReference.ttl', 
                context="<http://finregont.com/fro/cfr/Code_Federal_Regulations.ttl#CFR_Title_17_Part_275>", 
                format=RDFFormat.TURTLE)

        # FRO_CFR_Title_17_Part_275.ttl
        conn.addFile(filePath='../data/FRO_CFR_Title_17_Part_275.ttl', 
                context="<http://finregont.com/fro/cfr/Code_Federal_Regulations.ttl#CFR_Title_17_Part_275>", 
                format=RDFFormat.TURTLE)

        # Code_Federal_Regulations.ttl
        conn.addFile(filePath='../data/Code_Federal_Regulations.ttl', 
                context="<http://finregont.com/fro/cfr/Code_Federal_Regulations.ttl#CFR_Title_17_Part_275>", 
                format=RDFFormat.TURTLE)

        #
        # FIBO
        #
        # prod.fibo-quickstart-2024Q2.ttl
        conn.addFile(filePath='../data/prod.fibo-quickstart-2024Q2.ttl', 
                context="<https://spec.edmcouncil.org/fibo/ontology/master/2024Q2/QuickFIBOProd#FIBO>", 
                format=RDFFormat.TURTLE)
