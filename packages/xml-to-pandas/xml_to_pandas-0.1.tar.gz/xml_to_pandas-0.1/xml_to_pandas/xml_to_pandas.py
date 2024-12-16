import os
import logging
import xml.etree.ElementTree as ET
import pandas as pd
from typing import Optional
# The idea:
# If all child nodes are leaf nodes, then they will give a single record, i.e concat side by side
# Else if all child nodes are parent nodes (or even if there are leaf and parent nodes both (unbalanced tree structure)), 
# then flag them with parent tag and append them one below other

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def xml_to_pandas(
    file_path: str, 
    ignore_namespaces: bool = False, 
    preserve_root_tag: bool = True
) -> Optional[pd.DataFrame]:
    """
    Convert an XML file to a pandas DataFrame using XML tree traversal.

    This function reads an XML file and converts its contents to a pandas DataFrame 
    by leveraging the traverse_xml function for recursive parsing.

    Args:
        file_path (str): Path to the XML file
        ignore_namespaces (bool, optional): Remove XML namespaces. Defaults to False.
        preserve_root_tag (bool, optional): Keep root tag in DataFrame. Defaults to True.

    Returns:
        Optional[pd.DataFrame]: Parsed DataFrame or None if parsing fails

    Exceptions Handled:
        - xml.etree.ElementTree.ParseError: Raised for invalid XML formatting
        - FileNotFoundError: Raised when the specified file cannot be found

    Example:
        >>> df = xml_2_df('users.xml')
        >>> print(df)

    Note:
        - Requires xml.etree.ElementTree for XML parsing
        - Requires pandas for DataFrame creation
        - Depends on the traverse_xml() function for recursive parsing
    """
    # Validate file path
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    
    if not file_path.lower().endswith('.xml'):
        logger.warning(f"File {file_path} may not be an XML file")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Optional namespace removal
        if ignore_namespaces:
            for elem in root.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]
        
        return _traverse_xml(root, preserve_root_tag)
    
    except ET.ParseError as e:
        logger.error(f"XML Parsing Error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

def _traverse_xml(
    root: ET.Element, 
    preserve_root_tag: bool = True
) -> pd.DataFrame:
    """
    Recursively traverse an XML tree and convert it to a pandas DataFrame.

    This function handles different XML tree structures by:
    1. Converting leaf nodes to single-row DataFrames
    2. Handling nested structures with multiple child nodes
    3. Concatenating child nodes based on their type (leaf or parent)
    4. Preserving XML element attributes

    Args:
        root (ET.Element): XML element to parse
        preserve_root_tag (bool): Keep root tag in DataFrame

    Returns:
        pd.DataFrame: Parsed DataFrame representation of XML

    Behavior details:
    - Leaf nodes (no children) are converted to single-row DataFrames
    - Parent nodes with all leaf children are concatenated side by side
    - Parent nodes with all parent children are concatenated vertically
    - Mixed node types are handled by concatenating parent nodes and 
      exploding leaf node data across the result
    - XML element attributes are added as additional columns with 
      a prefix of "{attribute_name}_{element_tag}"

    Note:
        Requires pandas and xml.etree.ElementTree libraries
    """
    # Leaf node (no children)
    if len(root) == 0:
        record = {root.tag: [root.text or '']}
        df = pd.DataFrame(record)
        
        # Add attributes with prefixed column names
        for attr, value in root.attrib.items():
            df[f"{attr}_{root.tag}"] = value
        
        return df
    
    child_nodes_df = []
    leaf_nodes_check = []
    
    # Recursively process child nodes
    for child in root:
        leaf_nodes_check.append(1 if len(child) == 0 else 0)
        child_nodes_df.append(_traverse_xml(child, preserve_root_tag))
    
    # Determine how to combine child DataFrames
    all_leaf_nodes = sum(leaf_nodes_check) / len(root)
    
    if all_leaf_nodes == 1:
        # All child nodes are leaf nodes - concatenate side by side
        result = pd.concat(child_nodes_df, axis=1, ignore_index=False)
    elif all_leaf_nodes == 0:
        # All parent nodes - concatenate vertically
        result = pd.concat(child_nodes_df, axis=0, ignore_index=True)
    else:
        # Mixed node types
        # First, concatenate non-leaf node DataFrames vertically
        result = pd.concat(
            [df for df, is_leaf in zip(child_nodes_df, leaf_nodes_check) if is_leaf == 0], 
            axis=0, 
            ignore_index=True
        )

        # Then, add leaf node data across the result
        for df, is_leaf in zip(child_nodes_df, leaf_nodes_check):
            if is_leaf == 1:
                for key in df.columns:
                    result[key] = df.iloc[0][key]
    
    # Add attributes
    for attr, value in root.attrib.items():
        result[f"{attr}_{root.tag}"] = value
    
    # Optionally preserve or remove root tag
    if preserve_root_tag:
        result[root.tag] = root.tag
    return result
