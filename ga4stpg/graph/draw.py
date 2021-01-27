
import random
from collections import deque
from os import path

import networkx as nx
from matplotlib import pyplot as plt

from graph import Graph


def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def draw_common(graph,terminals, ggvermelho,ggazul):

    G = nx.Graph(graph.edges)

    # G.add_edges_from(E1)
    def node_color(node):
        if node in terminals :
            return 'orange'
        else :
            return 'white'

    def edge_color(v,u):
        if ggvermelho.has_edge(v,u) and ggazul.has_edge(v,u):
            return 'black'
        elif ggvermelho.has_edge(v,u) and not ggazul.has_edge(v,u):
            return 'red'
        elif not ggvermelho.has_edge(v,u) and ggazul.has_edge(v,u):
            return 'steelblue'
        else:
            return 'yellow'

    ed_colors = [edge_color(v,u) for v,u in G.edges() ]

    nd_colors = [node_color(i) for i in G.nodes() ]

    plt.subplot()

    # nx.draw(G, with_labels=True, font_weight='bold')
    # nx.draw_networkx(G,node_size=50,with_labels=False)
    nx.draw_kamada_kawai(G, with_labels=True,node_color=nd_colors,edge_color=ed_colors)
    # nx.draw_kamada_kawai(G, with_labels=False,node_size=50,node_color=nd_colors)

    # pos = nx.kamada_kawai_layout(G)
    # nx.draw_networkx_nodes(G,pos,with_labels=True,node_color=nd_colors)
    # labels = nx.draw_networkx_labels(G, pos=pos)

    # del labels

    plt.show()

    return G

    # G = nx.Graph(stp.graph)

    # plt.subplot()

    # nx.draw_networkx(G,node_size=50,with_labels=False)

    # plt.show()

def draw_tree(graph, root : int):

    if isinstance(graph,nx.Graph):
        G = graph
    elif isinstance(graph,Graph):
        G = nx.Graph(graph.edges)
    else:
        raise TypeError("Type graph not recognizable")

    pos = hierarchy_pos(G, root)

    nx.draw(G, pos=pos, with_labels=True)

    plt.show()
