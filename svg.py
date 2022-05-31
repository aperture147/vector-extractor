from lxml import etree
from time import time
import os

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
NSMAP = {None: SVG_NAMESPACE}

def extract_elements(file_path):

    tree = etree.parse(file_path, parser=etree.XMLParser())
    root = tree.getroot()
    
    parent_dir, _ = os.path.splitext(file_path)
    part_dir = f"{parent_dir}/"
    os.makedirs(part_dir, exist_ok=True)
    text_root = etree.Element("svg", attrib=root.attrib, nsmap=NSMAP)
    shape_root = etree.Element("svg", attrib=root.attrib, nsmap=NSMAP)
    def node_travel(original_node, text_node, shape_node):
        child_shape_node_list = []
        for child_node in original_node:
            if child_node.tag.endswith("{http://www.w3.org/2000/svg}g"):
                new_text_node = etree.Element('g', attrib=child_node.attrib)
                new_shape_node = etree.Element('g', attrib=child_node.attrib)
                text_node.append(new_text_node)
                shape_node.append(new_shape_node)
                node_travel(child_node, new_text_node, new_shape_node)
                shape_node.remove(new_shape_node)
            elif child_node.tag.endswith("{http://www.w3.org/2000/svg}text"):
                text_node.append(child_node)
            elif child_node.tag.endswith("{http://www.w3.org/2000/svg}defs"):
                shape_node.append(child_node)
            else:
                child_shape_node_list.append(child_node)
        if child_shape_node_list:
            for child_shape_node in child_shape_node_list:
                shape_node.append(child_shape_node)
            part_file_path = f"{part_dir}/{time()}.svg"
            with open(part_file_path, 'wb') as f:
                f.write(etree.tostring(
                    etree.ElementTree(shape_root),
                    xml_declaration=True,
                    encoding='utf-8',
                    standalone=False,
                ))
    node_travel(root, text_root, shape_root)

    part_file_path = f"{part_dir}/{time()}.svg"
    with open(part_file_path, 'wb') as f:
        f.write(etree.tostring(
            etree.ElementTree(text_root),
            xml_declaration=True,
            encoding='utf-8',
            standalone=False,
        ))