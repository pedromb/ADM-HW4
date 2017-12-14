from graph import Graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def viz_centralities(conf_id:int, reduced: bool = False):
    g = Graph(reduced)
    sub = g.get_subgraph_conf(conf_id, reduced)
    d, c, b = g.get_centralities(reduced, sub)

def viz_subgraph_author(author_id: int, d: int, reduced: bool = False):
    g = Graph(reduced)
    sub, node_list = g.get_subgraph_author(author_id, d, reduced)
    pos = nx.fruchterman_reingold_layout(sub)
    legend_handles = []
    plt.figure(figsize=(16,12))
    for index, value in enumerate(node_list):
        color = np.random.rand(3,)
        if index == 0:
            label = "Root"
        else:
            label = 'Distance {}'.format(str(index))
        patch = mpatches.Patch(color=color, label=label)
        legend_handles.append(patch)
        nx.draw_networkx(sub, pos = pos, nodelist=value, node_color=color, with_labels=False, node_size=100)
    plt.legend(handles=legend_handles)
    plt.show()

viz_subgraph_author(1, 3, reduced = False)
