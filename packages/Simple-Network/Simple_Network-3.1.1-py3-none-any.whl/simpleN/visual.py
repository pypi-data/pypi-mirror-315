#                                 #          In the Name of GOD   # #
#
import plotly.graph_objects as go
import scipy.sparse as sp
import numpy as np
import math
from itertools import cycle



class Visualize:
    """
    A class to visualize the MultilayerNetwork.
    """
    
    def __init__(self, network):
        """
        Initialize the Visualize class.
        
        Args:
            network (MultilayerNetwork): The network to visualize.
        """
        self.network = network
        self.layer_colors = self._assign_layer_colors()
    
    
    def _assign_layer_colors(self):
        """
        Assign distinct colors to each layer using Plotly's qualitative color scales.
        
        Returns:
            dict: Mapping of layer names to colors.
        """
        color_cycle = cycle(['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                             '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                             '#bcbd22', '#17becf'])
        return {layer: next(color_cycle) for layer in self.network.layers}
    
    
    def _circular_layout(self, num_nodes, radius=1):
        """
        Generate circular layout positions for nodes.
        
        Args:
            num_nodes (int): Number of nodes in the layer.
            radius (float): Radius of the circle.
        
        Returns:
            list of tuples: (x, y) positions for each node.
        """
        angles = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
        return [(radius * math.cos(angle), radius * math.sin(angle)) for angle in angles]
    
    
    def show_graph(
        self,
        space_between_layers: int = 5,
        edge_visibility_threshold: float = 0.1,
        marker_size: int = 8,
        line_width: float = 2,
        colorscale='Viridis',
        title='Network Visualization',
    ):
        """
        Visualize the network in 3D.
        
        Args:
            space_between_layers (int): Space between layers on the z-axis.
            edge_visibility_threshold (float): Threshold for edge visibility.
            marker_size (int): Size of the node markers.
            line_width (float): Width of the edges.
            colorscale (str): Color scale for nodes.
            title (str): Title of the visualization.
        """
        edge_x = []
        edge_y = []
        edge_z = []
        edge_colors = []
        node_x = []
        node_y = []
        node_z = []
        node_text = []
        label_x = []
        label_y = []
        label_z = []
        labels = []
        layer_positions = {layer_name: idx * space_between_layers for idx, layer_name in enumerate(self.network.layers)}
        node_positions = {}
        
        for layer_name, nodes in self.network.nodes.items():
            z_pos = layer_positions[layer_name]
            num_nodes = len(nodes)
            x_layout, y_layout = zip(*self._circular_layout(num_nodes, radius=math.sqrt(num_nodes)))
            node_positions[layer_name] = {}
            for i, node in enumerate(nodes):
                x = x_layout[i] + np.random.uniform(-0.1, 0.1)
                y = y_layout[i] + np.random.uniform(-0.1, 0.1)
                node_positions[layer_name][node] = (x, y, z_pos)
                node_x.append(x)
                node_y.append(y)
                node_z.append(z_pos)
                node_text.append(f'{node} ({layer_name})')
                label_x.append(x)
                label_y.append(y)
                label_z.append(z_pos)
                labels.append(node)
        
        for layer_name, adjacency_matrix in self.network.edges.items():
            if layer_name not in node_positions:
                continue
            if sp.issparse(adjacency_matrix):
                adjacency_matrix = adjacency_matrix.toarray()
            nodes = list(self.network.nodes[layer_name])
            for i, node_i in enumerate(nodes):
                for j, node_j in enumerate(nodes):
                    if i < j and adjacency_matrix[i, j] > edge_visibility_threshold:
                        x1, y1, z1 = node_positions[layer_name][node_i]
                        x2, y2, z2 = node_positions[layer_name][node_j]
                        edge_x.extend([x1, x2, None])
                        edge_y.extend([y1, y2, None])
                        edge_z.extend([z1, z2, None])
                        edge_colors.append(adjacency_matrix[i, j])
        
        for edge in self.network.inter_layer_edges:
            (node1, layer1), (node2, layer2), weight = edge
            if weight > edge_visibility_threshold:
                if layer1 in node_positions and layer2 in node_positions:
                    if node1 in node_positions[layer1] and node2 in node_positions[layer2]:
                        x1, y1, z1 = node_positions[layer1][node1]
                        x2, y2, z2 = node_positions[layer2][node2]
                        edge_x.extend([x1, x2, None])
                        edge_y.extend([y1, y2, None])
                        edge_z.extend([z1, z2, None])
                        edge_colors.append(weight)
        
        if edge_colors:
            edge_colors = np.array(edge_colors)
            edge_colors_normalized = (edge_colors - edge_colors.min()) / (edge_colors.max() - edge_colors.min() + 1e-9)
        else:
            edge_colors_normalized = []
        
        edge_trace = go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(
                width=line_width,
                color='rgba(200,200,200,0.5)',
                colorscale='Greys',
                colorbar=dict(title='Edge Weight'),
                cmin=0,
                cmax=1,
            ) if edge_colors_normalized.size else dict(width=line_width, color='rgba(200,200,200,0.5)'),
            hoverinfo='none',
        )
        
        if edge_colors_normalized.size:
            edge_trace.line.color = edge_colors_normalized
            edge_trace.line.colorscale = 'Viridis'
            edge_trace.line.colorbar = dict(title='Edge Weight')
            edge_trace.line.showscale = True
        
        node_trace = go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode='markers',
            marker=dict(
                size=marker_size,
                color=[self.layer_colors[layer] for layer in self.network.nodes.keys() for _ in self.network.nodes[layer]],
                #colorscale=colorscale,
                opacity=0.8,
            ),
            text=node_text,
            hoverinfo='text',
        )
        
        label_trace = go.Scatter3d(
            x=label_x,
            y=label_y,
            z=label_z,
            mode='text',
            text=labels,
            textposition="middle right",
            textfont=dict(
                size=10,
                color='black'
            ),
            hoverinfo='none',
        )
        
        layout = go.Layout(
            title=title,
            showlegend=False,
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                bgcolor='white',
            ),
            margin=dict(l=0, r=0, b=0, t=50),
        )
        
        fig = go.Figure(data=[edge_trace, node_trace, label_trace], layout=layout)
        fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
        fig.show()
    
#end#