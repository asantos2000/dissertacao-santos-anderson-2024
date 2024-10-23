import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD

def xsd_to_rdf(xsd_file, rdf_output, format='turtle'):
    # Define the namespaces used in the XSD
    namespaces = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'xmi': 'http://www.omg.org/spec/XMI/20110701',
        'sbvr': 'https://www.omg.org/spec/SBVR/20190601'
    }

    # Create the RDF graph
    g = Graph()

    # Bind namespaces
    XS = Namespace('http://www.w3.org/2001/XMLSchema#')
    XMI = Namespace('http://www.omg.org/spec/XMI/20110701#')
    SBVR = Namespace('https://www.omg.org/spec/SBVR/20190601#')

    g.bind('xs', XS)
    g.bind('xmi', XMI)
    g.bind('sbvr', SBVR)

    # Parse the XSD file
    tree = ET.parse(xsd_file)
    root = tree.getroot()

    # Process xs:element elements
    for element in root.findall('xs:element', namespaces):
        name = element.get('name')
        type_ = element.get('type')
        # Create a class for this element
        class_uri = SBVR[name]
        g.add((class_uri, RDF.type, OWL.Class))
        g.add((class_uri, RDFS.label, Literal(name)))
        # If type is specified, create a subclass relationship
        if type_:
            type_uri = get_type_uri(type_, namespaces)
            if type_uri:
                g.add((class_uri, RDFS.subClassOf, type_uri))

    # Process xs:complexType elements
    for ctype in root.findall('xs:complexType', namespaces):
        name = ctype.get('name')
        class_uri = SBVR[name]
        g.add((class_uri, RDF.type, OWL.Class))
        g.add((class_uri, RDFS.label, Literal(name)))

        # Process child elements
        for child in ctype:
            tag = child.tag
            if tag.endswith('sequence') or tag.endswith('choice'):
                for element in child.findall('xs:element', namespaces):
                    process_element(element, class_uri, g, namespaces)
            elif tag.endswith('attribute'):
                process_attribute(child, class_uri, g, namespaces)
            elif tag.endswith('attributeGroup'):
                # Handle attributeGroup if needed
                pass

    # Serialize the graph to RDF/XML
    g.serialize(destination=rdf_output, format=format)
    print(f"RDF/XML file has been generated: {rdf_output}")

def get_type_uri(type_str, namespaces):
    if ':' in type_str:
        prefix, localname = type_str.split(':')
        ns_uri = namespaces.get(prefix)
        if ns_uri:
            return URIRef(ns_uri + '#' + localname)
        else:
            print(f"Unknown namespace prefix: {prefix}")
            return None
    else:
        # Default to SBVR namespace
        return URIRef(namespaces['sbvr'] + '#' + type_str)

def process_element(element, class_uri, graph, namespaces):
    elem_name = element.get('name')
    elem_type = element.get('type')
    elem_ref = element.get('ref')

    # Create a property
    if elem_ref:
        ref_uri = get_type_uri(elem_ref, namespaces)
        if ref_uri:
            prop_uri = ref_uri
            graph.add((prop_uri, RDF.type, RDF.Property))
            graph.add((prop_uri, RDFS.domain, class_uri))
            graph.add((prop_uri, RDFS.range, ref_uri))
    else:
        prop_uri = URIRef(namespaces['sbvr'] + '#' + elem_name)
        graph.add((prop_uri, RDF.type, RDF.Property))
        graph.add((prop_uri, RDFS.domain, class_uri))
        if elem_type:
            type_uri = get_type_uri(elem_type, namespaces)
            if type_uri:
                graph.add((prop_uri, RDFS.range, type_uri))
        else:
            graph.add((prop_uri, RDFS.range, XSD.string))

def process_attribute(attribute, class_uri, graph, namespaces):
    attr_name = attribute.get('name')
    attr_type = attribute.get('type')
    attr_ref = attribute.get('ref')

    # Create a property
    if attr_ref:
        ref_uri = get_type_uri(attr_ref, namespaces)
        if ref_uri:
            prop_uri = ref_uri
            graph.add((prop_uri, RDF.type, RDF.Property))
            graph.add((prop_uri, RDFS.domain, class_uri))
            graph.add((prop_uri, RDFS.range, ref_uri))
    else:
        prop_uri = URIRef(namespaces['sbvr'] + '#' + attr_name)
        graph.add((prop_uri, RDF.type, RDF.Property))
        graph.add((prop_uri, RDFS.domain, class_uri))
        if attr_type:
            type_uri = get_type_uri(attr_type, namespaces)
            if type_uri:
                graph.add((prop_uri, RDFS.range, type_uri))
        else:
            graph.add((prop_uri, RDFS.range, XSD.string))

if __name__ == '__main__':
    xsd_input_file = 'sbvr-dtc-19-05-32.xsd'  # Replace with your XSD file path
    rdf_output_file = 'sbvr-dtc-19-05-32.ttl'  # Output RDF/Turtle file
    xsd_to_rdf(xsd_input_file, rdf_output_file, "turtle")            