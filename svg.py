import json
import os
from lxml import etree
from time import time
from transformation import get_transformation_matrix, make_coordinate_vector, IDENTITY_MATRIX
import numpy as np

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
    element_locations = {}

    def node_travel(original_node, text_node, shape_node, trans_matrix):
        child_shape_node_list = []
        for child_node in original_node:
            if 'transform' in child_node.attrib:
                child_trans_matrix = get_transformation_matrix(child_node.get('transform'))
                # current transformation matrix 
                ctw = np.matmul(trans_matrix, child_trans_matrix)
            else:
                ctw = trans_matrix
            if child_node.tag.endswith("{http://www.w3.org/2000/svg}g"):
                new_text_node = etree.Element('g', attrib=child_node.attrib)
                new_shape_node = etree.Element('g', attrib=child_node.attrib)
                text_node.append(new_text_node)
                shape_node.append(new_shape_node)
                node_travel(child_node, new_text_node, new_shape_node, ctw)
                shape_node.remove(new_shape_node)
            elif child_node.tag.endswith("{http://www.w3.org/2000/svg}defs"):
                shape_node.append(child_node)
            else:
                child_node_coord_vector = make_coordinate_vector(child_node)
                trans_child_node_coord_vector = np.dot(ctw, child_node_coord_vector)

                element_locations[child_node.get('id')] = {
                    'x': trans_child_node_coord_vector[0],
                    'y': trans_child_node_coord_vector[1]
                }
                if child_node.tag.endswith("{http://www.w3.org/2000/svg}text"):
                    text_node.append(child_node)
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
    node_travel(root, text_root, shape_root, IDENTITY_MATRIX)

    part_file_path = f"{part_dir}/{time()}.svg"
    with open(part_file_path, 'wb') as f:
        f.write(etree.tostring(
            etree.ElementTree(text_root),
            xml_declaration=True,
            encoding='utf-8',
            standalone=False,
        ))
    with open(part_file_path + '.json', 'w') as f:
        json.dump(element_locations, f)