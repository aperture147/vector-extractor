import json
import os
from lxml.etree import Element, XMLParser
from lxml import etree
from transformation import get_transformation_matrix, calculate_node_coodination, IDENTITY_MATRIX
import numpy as np

SVG_NAMESPACE = "http://www.w3.org/2000/svg"

SVG_NSMAP = {None: SVG_NAMESPACE}

SVG_GROUP_TAG = f"{{{SVG_NAMESPACE}}}g"
SVG_DEFS_TAG = f"{{{SVG_NAMESPACE}}}defs"
SVG_TEXT_TAG = f"{{{SVG_NAMESPACE}}}text"

def extract_elements(file_path):
    tree = etree.parse(file_path, parser=XMLParser())
    root = tree.getroot()

    part_path, _ = os.path.splitext(file_path)
    os.makedirs(part_path)

    element_locations = {}
    
    text_root  = Element("svg", attrib=root.attrib, nsmap=SVG_NSMAP)
    shape_root = Element("svg", attrib=root.attrib, nsmap=SVG_NSMAP)

    def _node_travel(
            original_node: Element,
            text_node: Element,
            shape_node: Element,
            trans_matrix: np.ndarray):
        child_shape_node_list = []

        for child_node in original_node:
            if 'transform' in child_node.attrib:
                child_trans_matrix = get_transformation_matrix(child_node.get('transform'))
                # current transformation matrix 
                ctw = np.matmul(trans_matrix, child_trans_matrix)
            else:
                ctw = trans_matrix
            if child_node.tag.endswith(SVG_GROUP_TAG):
                new_text_node  = Element('g', attrib=child_node.attrib)
                new_shape_node = Element('g', attrib=child_node.attrib)
                text_node.append(new_text_node)
                shape_node.append(new_shape_node)
                _node_travel(child_node, new_text_node, new_shape_node, ctw)
                shape_node.remove(new_shape_node)
            elif child_node.tag.endswith(SVG_DEFS_TAG):
                shape_node.append(child_node)
            else:
                x, y = calculate_node_coodination(child_node, ctw)

                element_locations[child_node.get('id')] = {
                    'x': x,
                    'y': y
                }

                if child_node.tag.endswith(SVG_TEXT_TAG):
                    text_node.append(child_node)
                else:
                    child_shape_node_list.append(child_node)
        if child_shape_node_list:
            for child_shape_node in child_shape_node_list:
                shape_node.append(child_shape_node)
            with open(f"{part_path}/{shape_node.get('id')}.svg", 'wb') as f:
                f.write(etree.tostring(
                    shape_root,
                    xml_declaration=True,
                    encoding='utf-8',
                    standalone=False,
                ))
    
    _node_travel(root, text_root, shape_root, IDENTITY_MATRIX)

    with open(f"{part_path}/text.svg", 'wb') as f:
        f.write(etree.tostring(
            text_root,
            xml_declaration=True,
            encoding='utf-8',
            standalone=False,
        ))
    with open(f'{part_path}/location.json', 'w') as f:
        json.dump(element_locations, f)