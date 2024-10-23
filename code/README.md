# CFR2SBVR

The main goal is create a Knowledge Graph in RDF format with three named graphs:

- **FIBO**: Contains [FIBO (Financial Bussiness Ontology)](https://github.com/edmcouncil/fibo), more specific the [Fibo Production Quickstart](https://spec.edmcouncil.org/fibo/ontology/master/2024Q2/prod.fibo-quickstart.ttl) from [EDM Council](https://edmcouncil.org/). Other resources can be found in [Product Downloads](https://edmconnect.edmcouncil.org/okgspecialinterestgroup/resources-sig-link/resources-sig-link-fibo-products-download). 
- **CFR**: The Code of Federal Regulation (CFR) from [eCFR](https://www.ecfr.gov/), more specific [the chapter 17, part 275](https://www.ecfr.gov/current/title-17/chapter-II/part-275) encoded in RDF/OWL / [Financial Regulation Ontology (FRO)](https://finregont.com/) format by [Jayzed Data Models Inc.](https://jayzed.com/) available at [FRO_CFR_Title_17_Part_275.ttl](https://finregont.com/fro/cfr/FRO_CFR_Title_17_Part_275.ttl) under [3.1 FIB-DM Open-Source, core.](https://jayzed.com/terms-of-use/) / GNU General Public License (GPL-3.0).
- **SBVR**: This graph contains definitional rules from FIBO and CFR and behavioral rules from CFR. Those rules are extracted, transformed and relationship with their source are recorded using cfr2sbvr tool. More about this tool can be found at [TODO: Publishing an article](some-url).

## Project structure

- **src**: source code in python. See src/README to check requirements to run.
- **data**: FIBO and FRO turtle files and the final result (cfr_title_17_part_275_sbvr.ttl) in turtle format.
- **README.md**: this file.
- **doc**: Documentation about the tool.
- **misc**: Other files.

## Dependencies

- Python 3.11 or higher
    - [agraph-python](https://github.com/edmcouncil/agraph-python)
    - [sparqlwrapper](https://github.com/rdflib/sparqlwrapper)
    - [rdflib](https://github.com/RDFLib/rdflib)
    - [pandas](https://pandas.pydata.org/)
- [AllegroGraph 8.2 or higher](https://franz.com/agraph/support/documentation/8.2.1/agraph-quick-start.html)
- Linux / MacOS or Windows WSL2 running Ubuntu 20.04 LTS or higher
- Miniconda 24.4.0 or higher

## Python environment

It is recommended to create a virtual environment. To do so, install [conda](https://docs.conda.io/en/latest/).

After installation, create an environment with the following commands:

```bash
conda create -n ipt-cfr2sbvr python=3.11
conda activate ipt-cfr2sbvr
pip install -r requirements.txt
#conda install -c conda-forge -c franzinc -n cfr2sbvr --file requirements.txt 
```

## Running

Before running configure the environment variables in `.env` file and export it to the shell.

```bash
set -a
.env
set +a 
```

- Run src/create_kg.py to load CFR and FIBO data into the graph database.
- Run scripts/fibo-vector-store.sh to create the FIBO vector store.
- Run src/fibo2sbvr.py to generate the sbvr graph (fibo terms).
- Run src/cfr2sbvr.py to generate the sbvr graph (cfr terms and rules).
- Run src/export_to_ttl.py to export the sbvr graph to ttl format.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

This project is licensed under the [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)