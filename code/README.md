# CFR2SBVR

The primary objective of this project is to create a Knowledge Graph in RDF format, composed of three named graphs:

- **FIBO**: This graph contains the [Financial Industry Business Ontology (FIBO)](https://github.com/edmcouncil/fibo). Specifically, it includes the [Fibo Production Quickstart](https://spec.edmcouncil.org/fibo/ontology/master/2024Q2/prod.fibo-quickstart.ttl) from [EDM Council](https://edmcouncil.org/). Additional resources are available under [Product Downloads](https://edmconnect.edmcouncil.org/okgspecialinterestgroup/resources-sig-link/resources-sig-link-fibo-products-download).

- **CFR**: This graph includes the Code of Federal Regulations (CFR) from [eCFR](https://www.ecfr.gov/), specifically [Chapter 17, Part 275](https://www.ecfr.gov/current/title-17/chapter-II/part-275). It is encoded in RDF/OWL format using the [Financial Regulation Ontology (FRO)](https://finregont.com/), provided by [Jayzed Data Models Inc.](https://jayzed.com/), and available in [FRO_CFR_Title_17_Part_275.ttl](https://finregont.com/fro/cfr/FRO_CFR_Title_17_Part_275.ttl). This ontology is distributed under the [FIB-DM Open-Source, core](https://jayzed.com/terms-of-use/) license, using the GNU General Public License (GPL-3.0).

- **SBVR**: This graph includes definitional rules from FIBO and CFR, as well as behavioral rules extracted from CFR. These rules are extracted, transformed, and their relationships to the original source are tracked using the cfr2sbvr tool. More information about this tool will be made available in an upcoming publication [TODO: Publishing an article](some-url).

## Project Structure

- **src**: Contains the Python source code. Refer to `src/README` for requirements and setup instructions.
- **data**: Stores the FIBO and FRO turtle files as well as the final Knowledge Graph (cfr_title_17_part_275_sbvr.ttl) in turtle format.
- **README.md**: The main documentation file.
- **doc**: Contains additional documentation about the tool.
- **misc**: Other auxiliary files.

## Dependencies

- Python 3.11 or higher
  - [agraph-python](https://github.com/edmcouncil/agraph-python)
  - [sparqlwrapper](https://github.com/rdflib/sparqlwrapper)
  - [rdflib](https://github.com/RDFLib/rdflib)
  - [pandas](https://pandas.pydata.org/)
- [AllegroGraph 8.2 or higher](https://franz.com/agraph/support/documentation/8.2.1/agraph-quick-start.html)
- Linux / MacOS or Windows WSL2 running Ubuntu 20.04 LTS or higher
- Miniconda 24.4.0 or higher

## Python Environment Setup

It is recommended to create a virtual environment using [conda](https://docs.conda.io/en/latest/).

After installing conda, create and activate the environment using the following commands:

```bash
conda create -n ipt-cfr2sbvr python=3.11
conda activate ipt-cfr2sbvr
pip install -r requirements.txt
# Optional alternative:
# conda install -c conda-forge -c franzinc -n cfr2sbvr --file requirements.txt
```

## Running the Project

Before running the scripts, configure the environment variables in the `.env` file and export them to the shell:

```bash
set -a
.env
set +a
```

### Available Scripts

- **Load CFR and FIBO Data**: Run `src/create_kg.py` to load CFR and FIBO data into the graph database.
- **Create FIBO Vector Store**: Run `scripts/fibo-vector-store.sh` to create a vector store for FIBO.
- **Generate SBVR Graph (FIBO Terms)**: Run `src/fibo2sbvr.py`.
- **Generate SBVR Graph (CFR Terms and Rules)**: Run `src/cfr2sbvr.py`.
- **Export SBVR Graph to TTL Format**: Run `src/export_to_ttl.py`.

### Notebook Sequence

1. **Semantic Annotation Elements Extraction**: Run `src/chap_6_semantic_annotation_elements_extraction.ipynb` to extract elements.
2. **Rules Classification**: Run `src/chap_6_semantic_annotation_rules_classification.ipynb` to classify rules.
3. **NLP to SBVR Transformation**: Run `src/chap_6_nlp2sbvr_transform.ipynb` to transform rules.
4. **Element Association Creation**: Run `src/chap_6_nlp2sbvr_elements_association_creation.ipynb` to populate the CFR-SBVR graph.
5. **Validation**: Run `src/chap_7_validation.ipynb` to validate the entire pipeline.

## Contributing

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to the project.

## License

This project is distributed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.

