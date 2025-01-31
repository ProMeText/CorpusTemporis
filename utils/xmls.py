from xml.dom.minidom import parseString


def prittify_xml(xml_content):
    dom = parseString(xml_content)
    return dom.toprettyxml(indent="  ")
