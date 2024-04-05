import json
import os

import networkx as nx
from matplotlib import pyplot as plt
from pyvis.network import Network


def build_graph(graph, node):
    title = node['title']
    if title not in graph:
        graph.add_node(title)
    for link in node.get('links', []):
        link_title = link['title']
        graph.add_node(link_title)
        graph.add_edge(title, link_title)
        build_graph(graph, link)


def export(data):
    graph = nx.DiGraph()
    build_graph(graph, data)
    node_size = [len(list(graph.predecessors(node))) for node in graph]
    nx.draw_spring(graph, with_labels=True, node_size=node_size, node_color='red', font_size=1, alpha=0.8, arrows=True)

    nt = Network(width='1920px', height='1080px')
    nt.from_nx(graph)
    nt.show('wiki_graph.html', notebook=False)

    plt.savefig('wiki_graph.png', dpi=700)


if __name__ == '__main__':
    path = os.getenv("WIKI_FILE", "NOT SET")
    with open(path, 'r') as f:
        data = json.load(f)
        export(data)
