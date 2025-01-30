from xml.etree import ElementTree as ET
# def xml_to_txt(xml_conent):
#     return xml_conent#.replace('<', '').replace('>', '')

# def xml_to_txt(xml_conent):
#     tree = ET.fromstring(xml_conent)
#     return "".join([i for i in tree.itertext()])
namespaces = {
    'tei': "http://www.tei-c.org/ns/1.0",
    'amc': "http://www.amc.ed.ac.uk",
    'txm': "http://textometrie.org/1.0"
}


def xml_to_txt(xml_conent, token_tag='tok'):
    tree = ET.fromstring(xml_conent)
    #print(list(tree.findall(f'.//{token_tag}')))le
    return " ".join([i.text or '' for i in tree.findall(f'.//{token_tag}', namespaces=namespaces)])
