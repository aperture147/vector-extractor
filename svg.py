from lxml import etree
from time import time
import os

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
NSMAP = {None: SVG_NAMESPACE}

def extract_elements(file_path):
    tree = etree.parse(file_path, parser=etree.XMLParser())
    root = tree.getroot()
    parent_dir, _ = os.path.splitext(file_path)
    part_dir = f"{parent_dir}/part"
    os.makedirs(part_dir, exist_ok=True)
    new_root = etree.Element("svg", attrib=root.attrib, nsmap=NSMAP)
    def node_travel(node, new_node, group_node):
        for child in node:
            if child.tag.endswith("{http://www.w3.org/2000/svg}g"):
                new_group_node = etree.Element('g', attrib=child.attrib)
                group_node.append(new_group_node)
                node_travel(child, new_node, new_group_node)
                group_node.remove(new_group_node)
            else:
                if not child.tag.endswith("{http://www.w3.org/2000/svg}defs"):
                    group_node.append(child)
                    part_file_path = f"{part_dir}/{time()}.svg"
                    with open(part_file_path, 'wb') as f:
                        f.write(etree.tostring(
                            etree.ElementTree(new_root),
                            xml_declaration=True,
                            encoding='utf-8',
                            standalone=False,
                        ))
                    group_node.remove(child)
                else:
                    new_node.append(child)
    node_travel(root, new_root, new_root)