#                                 #          In the Name of GOD   # #
#
import numpy as np
import scipy.sparse as sp
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict


class MultilayerNetwork:
    """
    A class to represent and manage a multilayer network.
    
    Attributes:
        directed (bool): Whether the network is directed.
        large_graph (bool): Whether the network is large (uses sparse matrices).
        node_set (set): Set of all nodes in the network.
        nodes (dict): Dictionary mapping layer names to lists of nodes.
        edges (dict): Dictionary mapping layer names to adjacency matrices (sparse or dense).
        layers (list): List of layer names.
        node_attributes (dict): Dictionary mapping nodes to their attributes.
        edge_attributes (dict): Dictionary mapping edges to their attributes.
        inter_layer_edges (list): List of inter-layer edges.
        bulk_updates (dict): Accumulates bulk updates for adjacency matrices.
        node_map (dict): Maps nodes to their indices and connections.
        index_node (int): Counter for assigning unique indices to nodes.
    """
    
    def __init__(self, directed: bool = False, large_graph: bool = False):
        """
        Initialize the MultilayerNetwork.
        
        Args:
            directed (bool): Whether the network is directed.
            large_graph (bool): Whether the network is large (uses sparse matrices).
        """
        self.directed = directed
        self.large_graph = large_graph
        self.node_set = set()
        self.nodes = {} 
        self.edges = {} 
        self.layers = []
        self.node_attributes = {}
        self.edge_attributes = {}
        self.inter_layer_edges = []
        self.extra_edges = []
        self.extra_attributes = []
        self.node_map = {}
        self.index_node = 0
        self.bulk_updates = defaultdict(lambda: {'rows': [], 'cols': [], 'data': []})
    
    def _update_node_map(
        self,
        node_,
        edge=None,
        layer_for_first_time: str = None,
        attributes=None,
        adjust_attributes_for_a_node=None,
        additional=None,
        directly_assign_additionals: bool = False,
        force_directly_assign_additionals: bool = False
    ):
        """
        Update the node_map with node information.
        
        Args:
            node_ (str): The node identifier.
            edge (str, optional): The connected node.
            layer_for_first_time (str, optional): The layer name if the node is added for the first time.
            attributes (int | float, optional): Attribute to add to the node.
            adjust_attributes_for_a_node (list, optional): List of attributes to adjust.
            additional (any, optional): Additional information to assign.
            directly_assign_additionals (bool): Whether to assign additional data directly.
            force_directly_assign_additionals (bool): Force assignment of additional data.
        """
        if node_ not in self.node_map:
            self.node_map[node_] = {}
        
        node_entry = self.node_map[node_]
        
        if 'index' not in node_entry:
            node_entry['index'] = self.index_node
            self.index_node += 1
        
        if 'edges' not in node_entry:
            node_entry['edges'] = {'node': [], 'index': []}
        
        if edge:
            if edge not in self.node_map:
                raise ValueError(f"Edge node '{edge}' does not exist in node_map.")
            node_entry['edges']['node'].append(edge)
            node_entry['edges']['index'].append(self.node_map[edge]['index'])
        
        if 'attributes' not in node_entry:
            node_entry['attributes'] = []
        
        if attributes is not None:
            if isinstance(attributes, (int, float)):
                node_entry['attributes'].append(attributes)
            else:
                raise ValueError("Attributes must be of type int or float.")
        
        if adjust_attributes_for_a_node:
            if not node_entry['attributes']:
                node_entry['attributes'] = adjust_attributes_for_a_node
            else:
                for attr in adjust_attributes_for_a_node:
                    if isinstance(attr, (int, float)):
                        node_entry['attributes'].append(attr)
                    else:
                        raise ValueError("Adjusted attributes must be int or float.")
        
        if 'layer' not in node_entry:
            if layer_for_first_time:
                node_entry['layer'] = layer_for_first_time
            else:
                for layer, nodes in self.nodes.items():
                    if node_ in nodes:
                        node_entry['layer'] = layer
                        break
                else:
                    raise ValueError(f"Layer not found for node '{node_}'.")
        
        if additional is not None:
            if 'additional' not in node_entry:
                node_entry['additional'] = additional if directly_assign_additionals else [additional]
            else:
                if directly_assign_additionals:
                    if isinstance(node_entry['additional'], list):
                        if not node_entry['additional']:
                            node_entry['additional'] = additional
                        elif force_directly_assign_additionals:
                            node_entry['additional'] = additional
                        else:
                            raise AssertionError(
                                f"Additional data for node '{node_}' already exists. "
                                "Use force_directly_assign_additionals=True to overwrite."
                            )
                    else:
                        if force_directly_assign_additionals:
                            node_entry['additional'] = additional
                        else:
                            raise AssertionError(
                                f"Additional data for node '{node_}' already exists. "
                                "Use force_directly_assign_additionals=True to overwrite."
                            )
                else:
                    node_entry['additional'].append(additional)
    
    def add_relevant_number_to_each_node(
        self, node, target: float | int | str = 'Any', force_directly_assign_additionals: bool = False
    ):
        """
        Add a relevant number or label to a node.
        
        Args:
            node (str): The node identifier.
            target (float | int | str): The target value or label.
            force_directly_assign_additionals (bool): Force assignment of additional data.
        """
        if node not in self.node_set:
            self.node_set.add(node)
        
        self._update_node_map(
            node_=node,
            additional=target,
            directly_assign_additionals=True,
            force_directly_assign_additionals=force_directly_assign_additionals
        )
    
    def get_target_of_each_node(self, node=None, give_them_all: bool = True):
        """
        Retrieve the additional data for nodes.
        
        Args:
            node (str, optional): Specific node to retrieve data for.
            give_them_all (bool): Whether to retrieve data for all nodes.
        
        Returns:
            dict or list: Dictionary of node data or data for a specific node.
        """
        if give_them_all:
            return {node: data.get('additional', None) for node, data in self.node_map.items()}
        else:
            if node:
                return self.node_map.get(node, {}).get('additional', None)
            else:
                raise ReferenceError(
                    "To retrieve data for a specific node, provide the node identifier."
                )
    
    def add_layer(self, layer_name: str = 'ALL'):
        """
        Add a new layer to the network.
        
        Args:
            layer_name (str): Name of the layer.
        """
        if layer_name not in self.layers:
            self.layers.append(layer_name)
            self.nodes[layer_name] = []
            if self.large_graph:
                self.edges[layer_name] = sp.lil_matrix((0, 0))
            else:
                self.edges[layer_name] = np.zeros((0, 0), dtype=int)
    
    def add_node(self, node, layer_name: str = 'ALL'):
        """
        Add a node to a specified layer.
        
        Args:
            node (str): The node identifier.
            layer_name (str): The layer to add the node to.
        """
        if layer_name not in self.layers:
            self.add_layer(layer_name)
        
        if node not in self.nodes[layer_name]:
            self.nodes[layer_name].append(node)
            self._update_node_map(node_=node, layer_for_first_time=layer_name)
            self.node_set.add(node)
            
            if self.large_graph:
                current_size = self.edges[layer_name].shape[0]
                self.edges[layer_name] = sp.lil_matrix((current_size + 1, current_size + 1))
            else:
                current_size = self.edges[layer_name].shape[0]
                new_size = current_size + 1
                new_matrix = np.zeros((new_size, new_size), dtype=int)
                if current_size > 0:
                    new_matrix[:current_size, :current_size] = self.edges[layer_name]
                self.edges[layer_name] = new_matrix
    
    def add_edge(
        self,
        node1,
        node2,
        layer_name1: str = 'ALL',
        layer_name2: str = None,
        weight: int | float = 1
    ):
        """
        Add an edge between two nodes, intra-layer or inter-layer.
        
        Args:
            node1 (str): The first node.
            node2 (str): The second node.
            layer_name1 (str): Layer of the first node.
            layer_name2 (str, optional): Layer of the second node. Defaults to None (intra-layer).
            weight (int | float): Weight of the edge.
        """
        self._update_node_map(node_=node1, edge=node2)
        self._update_node_map(node_=node2, edge=node1)
        
        if layer_name2 is None or layer_name1 == layer_name2:
            
            if layer_name1 not in self.layers:
                raise ValueError(f"Layer '{layer_name1}' does not exist.")
            
            if node1 not in self.nodes[layer_name1] or node2 not in self.nodes[layer_name1]:
                raise ValueError("One or both nodes do not exist in the specified layer.")
            
            self.extra_edges.append((node1, node2))
            self._ensure_correct_matrix_size(layer_name1, node1, node2)
            node1_index = self.nodes[layer_name1].index(node1)
            node2_index = self.nodes[layer_name1].index(node2)
            
            self.edges[layer_name1][node1_index, node2_index] = weight
            
            if not self.directed:
                self.edges[layer_name1][node2_index, node1_index] = weight
        
        else:
            
            self.add_inter_layer_edge(node1, node2, layer_name1, layer_name2, weight)
    
    def add_inter_layer_edge(
        self,
        node1,
        node2,
        layer_name1: str,
        layer_name2: str,
        weight: int | float = 1
    ):
        """
        Add an inter-layer edge between two nodes in different layers.
        
        Args:
            node1 (str): The first node.
            node2 (str): The second node.
            layer_name1 (str): Layer of the first node.
            layer_name2 (str): Layer of the second node.
            weight (int | float): Weight of the edge.
        """
        if layer_name1 not in self.layers or layer_name2 not in self.layers:
            raise ValueError(f"One or both specified layers ('{layer_name1}', '{layer_name2}') do not exist.")
        
        if node1 not in self.nodes.get(layer_name1, []) or node2 not in self.nodes.get(layer_name2, []):
            raise ValueError("One or both nodes do not exist in their specified layers.")
        
        self.inter_layer_edges.append(((node1, layer_name1), (node2, layer_name2), weight))
    
    def _ensure_correct_matrix_size(self, layer_name: str, node1, node2):
        """
        Ensure that the adjacency matrix for a layer is appropriately sized.
        
        Args:
            layer_name (str): The layer name.
            node1 (str): The first node.
            node2 (str): The second node.
        """
        node1_index = self.nodes[layer_name].index(node1)
        node2_index = self.nodes[layer_name].index(node2)
        
        if self.large_graph:
            self._ensure_matrix_initialized_and_resized(layer_name, node1_index, node2_index)
        else:
            self._ensure_dense_matrix_resized(layer_name, node1_index, node2_index)
    
    def _ensure_matrix_initialized_and_resized(self, layer_name: str, node1_index: int, node2_index: int):
        """
        Ensure that a sparse adjacency matrix is initialized and resized.
        
        Args:
            layer_name (str): The layer name.
            node1_index (int): Index of the first node.
            node2_index (int): Index of the second node.
        """
        current_matrix = self.edges[layer_name]
        max_index = max(node1_index, node2_index) + 1
        
        if max_index > current_matrix.shape[0]:
            new_matrix = sp.lil_matrix((max_index, max_index))
            new_matrix[:current_matrix.shape[0], :current_matrix.shape[1]] = current_matrix
            self.edges[layer_name] = new_matrix
    
    def _ensure_dense_matrix_resized(self, layer_name: str, node1_index: int, node2_index: int):
        """
        Ensure that a dense adjacency matrix is resized.
        
        Args:
            layer_name (str): The layer name.
            node1_index (int): Index of the first node.
            node2_index (int): Index of the second node.
        """
        current_matrix = self.edges[layer_name]
        max_index = max(node1_index, node2_index) + 1
        current_size = current_matrix.shape[0]
        
        if max_index > current_size:
            new_size = max_index
            new_matrix = np.zeros((new_size, new_size), dtype=int)
            if current_size > 0:
                new_matrix[:current_size, :current_size] = current_matrix
            self.edges[layer_name] = new_matrix
    
    def get_inter_layer_edges(self):
        """
        Retrieve all inter-layer edges.
        
        Returns:
            list: List of inter-layer edges.
        """
        return self.inter_layer_edges
    
    def find_inter_layer_edges(self, node, layer: str = None):
        """
        Find all inter-layer edges connected to a given node, optionally within a specific layer.
        
        Args:
            node (str): The node identifier.
            layer (str, optional): Specific layer to filter by.
        
        Returns:
            list: List of tuples representing inter-layer edges.
        """
        if layer:
            return [
                (n1, l1, n2, l2, w) for (n1, l1), (n2, l2), w in self.inter_layer_edges
                if (node == n1 and layer == l1) or (node == n2 and layer == l2)
            ]
        else:
            return [
                (n1, l1, n2, l2, w) for (n1, l1), (n2, l2), w in self.inter_layer_edges
                if node == n1 or node == n2
            ]
    
    def prepare_for_bulk_update(self, layer_name: str):
        """
        Prepare or reset the accumulator for bulk updates of a layer.
        
        Args:
            layer_name (str): The layer name.
        """
        self.bulk_updates[layer_name] = {'rows': [], 'cols': [], 'data': []}
    
    def accumulate_edge_update(self, node1, node2, layer_name: str, weight=1):
        """
        Accumulate an edge update for later bulk application.
        
        Args:
            node1 (str): The first node.
            node2 (str): The second node.
            layer_name (str): The layer name.
            weight (int | float): Weight of the edge.
        """
        if layer_name not in self.nodes:
            raise ValueError("Layer does not exist.")
        if node1 not in self.nodes[layer_name] or node2 not in self.nodes[layer_name]:
            raise ValueError("One or both nodes do not exist in the specified layer.")
        
        node1_index = self.nodes[layer_name].index(node1)
        node2_index = self.nodes[layer_name].index(node2)
        
        self.bulk_updates[layer_name]['rows'].append(node1_index)
        self.bulk_updates[layer_name]['cols'].append(node2_index)
        self.bulk_updates[layer_name]['data'].append(weight)
    
    def update_edge_weight(self, node1, node2, layer_name: str, new_weight: int | float):
        """
        Update the weight of an existing edge.
        
        Args:
            node1 (str): The first node.
            node2 (str): The second node.
            layer_name (str): The layer name.
            new_weight (int | float): The new weight to assign.
        """
        if layer_name not in self.layers:
            raise ValueError(f"Layer '{layer_name}' does not exist.")
        if node1 not in self.nodes[layer_name] or node2 not in self.nodes[layer_name]:
            raise ValueError("One or both nodes do not exist in the specified layer.")
        
        node1_index = self.nodes[layer_name].index(node1)
        node2_index = self.nodes[layer_name].index(node2)
        
        self.edges[layer_name][node1_index, node2_index] = new_weight
        
        if not self.directed:
            self.edges[layer_name][node2_index, node1_index] = new_weight
    
    def apply_bulk_updates(self, layer_name: str):
        """
        Apply accumulated updates in bulk to the adjacency matrix of a layer.
        
        Args:
            layer_name (str): The layer name.
        """
        if layer_name not in self.bulk_updates or not self.bulk_updates[layer_name]['data']:
            return
        
        update_data = self.bulk_updates[layer_name]
        rows = update_data['rows']
        cols = update_data['cols']
        data = update_data['data']
        
        if self.large_graph:
            
            update_matrix = sp.coo_matrix((data, (rows, cols)), shape=self.edges[layer_name].shape)
            self.edges[layer_name] += update_matrix.tocsr()
        else:
            
            for row, col, w in zip(rows, cols, data):
                self.edges[layer_name][row, col] = w
                if not self.directed:
                    self.edges[layer_name][col, row] = w
        
        self.prepare_for_bulk_update(layer_name)
    
    def set_node_attribute(self, node, attr_name: str, attr_value: int | float | list):
        """
        Set or update an attribute for a node.
        
        Args:
            node (str): The node identifier.
            attr_name (str): The name of the attribute.
            attr_value (int | float | list): The value of the attribute.
        """
        if node not in self.node_set:
            raise ValueError("Node does not exist.")
        
        if node not in self.node_attributes:
            self.node_attributes[node] = {}
        
        self.node_attributes[node][attr_name] = attr_value
        
        if isinstance(attr_value, list):
            self._update_node_map(node_=node, adjust_attributes_for_a_node=attr_value)
        else:
            self._update_node_map(node_=node, attributes=attr_value)
    
    def set_edge_attribute(self, node1, node2, layer_name: str, attr_name: str, attr_value: int | float):
        """
        Set or update an attribute for an edge.
        
        Args:
            node1 (str): The first node.
            node2 (str): The second node.
            layer_name (str): The layer name.
            attr_name (str): The name of the attribute.
            attr_value (int | float): The value of the attribute.
        """
        if node1 not in self.node_set or node2 not in self.node_set:
            raise ValueError("One or both nodes do not exist.")
        if layer_name not in self.layers:
            raise ValueError(f"Layer '{layer_name}' does not exist.")
        
        if self.large_graph:
            raise NotImplementedError("Edge attributes for large (sparse) graphs are not supported yet.")
        
        if self.directed:
            edge_key = (node1, node2, layer_name)
        else:
            edge_key = tuple(sorted((node1, node2)) + [layer_name])
        
        if edge_key not in self.edge_attributes:
            self.edge_attributes[edge_key] = {}
        
        self.edge_attributes[edge_key][attr_name] = attr_value
    
    def calculate_layer_degrees(self, layer_name: str, parallel_threshold: int = 10000):
        """
        Calculate degrees for nodes in a specific layer.
        
        Args:
            layer_name (str): The layer name.
            parallel_threshold (int): Threshold for parallel processing.
        
        Returns:
            tuple or np.ndarray: Degrees of nodes.
        """
        if layer_name not in self.layers:
            raise ValueError(f"Layer '{layer_name}' not found.")
        
        layer_matrix = self.edges[layer_name]
        node_count = layer_matrix.shape[0] if self.large_graph else len(layer_matrix)
        
        if self.large_graph and node_count > parallel_threshold:
            with ProcessPoolExecutor() as executor:
                func_args = [(self.large_graph, layer_matrix, i) for i in range(node_count)]
                degrees = list(executor.map(self._calculate_degree_of_node, func_args))
        else:
            degrees = self._calculate_layer_degrees_single_threaded(layer_name)
        
        return degrees
    
    def get_node_attributes(self):
        """
        Retrieve all node attributes sorted by node names.
        
        Returns:
            dict: Sorted dictionary of node attributes.
        """
        sorted_nodes = sorted(self.node_attributes.keys())
        return {node: self.node_attributes[node] for node in sorted_nodes}
    
    def get_index_map(self, sorted: bool = True, change_the_current_self_of_index_map: bool = False):
        """
        Get a mapping from indices to node names.
        
        Args:
            sorted (bool): Whether to sort the nodes.
            change_the_current_self_of_index_map (bool): Whether to update the internal index_map.

        Returns:
            dict: Mapping from indices to node names.
        """
        if not sorted:
            return {data['index']: node for node, data in self.node_map.items()}
        
        sorted_nodes = sorted(self.node_attributes.keys())
        temp_index_map = {idx: node for idx, node in enumerate(sorted_nodes)}
        
        if change_the_current_self_of_index_map:
            self.index_map = temp_index_map
        
        return temp_index_map
    
    def _calculate_layer_degrees_single_threaded(self, layer_name: str):
        """
        Calculate degrees for a layer in a single-threaded manner.
        
        Args:
            layer_name (str): The layer name.

        Returns:
            tuple or np.ndarray: Degrees of nodes.
        """
        layer_matrix = self.edges[layer_name]
        
        if self.large_graph:
            if self.directed:
                in_degrees = layer_matrix.sum(axis=0).A1
                out_degrees = layer_matrix.sum(axis=1).A1
                return in_degrees, out_degrees
            else:
                degrees = layer_matrix.sum(axis=1).A1 
                return degrees
        else:
            if self.directed:
                in_degrees = np.sum(layer_matrix > 0, axis=0)
                out_degrees = np.sum(layer_matrix > 0, axis=1)
                return in_degrees, out_degrees
            else:
                degrees = np.sum(layer_matrix > 0, axis=1)
                return degrees
    
    @staticmethod
    def _calculate_degree_of_node(args):
        """
        Static method to calculate the degree of a single node.
        
        Args:
            args (tuple): Tuple containing (large_graph, layer_matrix, node_index).
        
        Returns:
            int: Degree of the node.
        """
        large_graph, layer_matrix, node_index = args
        
        if large_graph:
            
            row = layer_matrix.getrow(node_index)
            return row.getnnz()
        else:
            
            return np.sum(layer_matrix[node_index] > 0)
    

#end#