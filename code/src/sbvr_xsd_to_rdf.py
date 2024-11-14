import argparse
from defusedxml import ElementTree as ET
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD


def xsd_to_rdf(xsd_file, rdf_output, format="turtle"):
    # Define namespaces
    namespaces = {
        "xs": "http://www.w3.org/2001/XMLSchema",
        "xmi": "http://www.omg.org/spec/XMI/20110701",
        "sbvr": "https://www.omg.org/spec/SBVR/20190601",
    }

    # Create the RDF graph and bind namespaces
    g = Graph()
    XS = Namespace("http://www.w3.org/2001/XMLSchema#")
    XMI = Namespace("http://www.omg.org/spec/XMI/20110701#")
    SBVR = Namespace("https://www.omg.org/spec/SBVR/20190601#")

    g.bind("xs", XS)
    g.bind("xmi", XMI)
    g.bind("sbvr", SBVR)

    # Parse the XSD file using defusedxml for security
    tree = ET.parse(xsd_file)
    root = tree.getroot()

    # Process xs:element elements (your existing code)
    for element in root.findall("xs:element", namespaces):
        name = element.get("name")
        type_ = element.get("type")
        class_uri = SBVR[name]
        g.add((class_uri, RDF.type, OWL.Class))
        g.add((class_uri, RDFS.label, Literal(name)))
        if type_:
            type_uri = get_type_uri(type_, namespaces)
            if type_uri:
                g.add((class_uri, RDFS.subClassOf, type_uri))

    # Additional processing here (your existing code)

    # Serialize the graph to RDF/XML or Turtle
    g.serialize(destination=rdf_output, format=format)
    print(f"RDF file has been generated: {rdf_output}")


def get_type_uri(type_str, namespaces):
    if ":" in type_str:
        prefix, localname = type_str.split(":")
        ns_uri = namespaces.get(prefix)
        if ns_uri:
            return URIRef(ns_uri + "#" + localname)
        else:
            print(f"Unknown namespace prefix: {prefix}")
            return None
    else:
        # Default to SBVR namespace
        return URIRef(namespaces["sbvr"] + "#" + type_str)


def process_element(element, class_uri, graph, namespaces):
    elem_name = element.get("name")
    elem_type = element.get("type")
    elem_ref = element.get("ref")

    # Create a property
    if elem_ref:
        ref_uri = get_type_uri(elem_ref, namespaces)
        if ref_uri:
            prop_uri = ref_uri
            graph.add((prop_uri, RDF.type, RDF.Property))
            graph.add((prop_uri, RDFS.domain, class_uri))
            graph.add((prop_uri, RDFS.range, ref_uri))
    else:
        prop_uri = URIRef(namespaces["sbvr"] + "#" + elem_name)
        graph.add((prop_uri, RDF.type, RDF.Property))
        graph.add((prop_uri, RDFS.domain, class_uri))
        if elem_type:
            type_uri = get_type_uri(elem_type, namespaces)
            if type_uri:
                graph.add((prop_uri, RDFS.range, type_uri))
        else:
            graph.add((prop_uri, RDFS.range, XSD.string))


def process_attribute(attribute, class_uri, graph, namespaces):
    attr_name = attribute.get("name")
    attr_type = attribute.get("type")
    attr_ref = attribute.get("ref")

    # Create a property
    if attr_ref:
        ref_uri = get_type_uri(attr_ref, namespaces)
        if ref_uri:
            prop_uri = ref_uri
            graph.add((prop_uri, RDF.type, RDF.Property))
            graph.add((prop_uri, RDFS.domain, class_uri))
            graph.add((prop_uri, RDFS.range, ref_uri))
    else:
        prop_uri = URIRef(namespaces["sbvr"] + "#" + attr_name)
        graph.add((prop_uri, RDF.type, RDF.Property))
        graph.add((prop_uri, RDFS.domain, class_uri))
        if attr_type:
            type_uri = get_type_uri(attr_type, namespaces)
            if type_uri:
                graph.add((prop_uri, RDFS.range, type_uri))
        else:
            graph.add((prop_uri, RDFS.range, XSD.string))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an XSD file to RDF.")
    parser.add_argument("xsd_file", nargs="?", help="The path to the input XSD file.")
    parser.add_argument("rdf_output", nargs="?", help="The path to the output RDF file.")
    parser.add_argument("--format", default="turtle", choices=["turtle", "xml", "n3", "nt"],
                        help="The output format (default: turtle).")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the output file if it exists.")

    args = parser.parse_args()

    # Determine the output file extension based on the format
    extension_map = {
        "turtle": ".ttl",
        "xml": ".rdf",
        "n3": ".n3",
        "nt": ".nt"
    }
    extension = extension_map.get(args.format, ".ttl")

    # Set default rdf_output based on xsd_file if not provided
    if not args.rdf_output:
        rdf_output = Path(args.xsd_file).with_suffix(extension)
    else:
        rdf_output = args.rdf_output
    
    output_path = Path(rdf_output)
    if output_path.exists() and not args.overwrite:
        raise FileExistsError(f"The file '{rdf_output}' already exists. Use 'overwrite=True' to overwrite it.")

    xsd_to_rdf(args.xsd_file, rdf_output, format=args.format)
