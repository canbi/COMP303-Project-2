import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

number_of_cities = 10
source = 0
destination = 5
constant_diff = 3
fromNode=[] #[0, 1, 2]
toNode=[] #[2, 2, 3]
edgeWeights=[] #[3, 4, 5]
edges_list={}
shortest_path=[]
number_of_edges=0;
# initialize edges
for i in range(1,number_of_cities+1):
    for j in range(1,number_of_cities+1):
        if i != j and j>i and abs(i-j) <= constant_diff:
            fromNode.append(i)
            toNode.append(j)
            edgeWeights.append(i+j)
            edges_list[str(i)+"-"+str(j)]= number_of_edges
            number_of_edges+=1
colorValues=["black" for i in range(number_of_edges)]
"""
print(len(fromNode))
print(len(toNode))
print(len(edgeWeights))
print(edges_list)
"""


# Simple integer weights on edges:
pd.options.display.max_columns = 20
edges = pd.DataFrame({"source": fromNode, "target": toNode, "weight": edgeWeights, "color": colorValues})
G = nx.from_pandas_edgelist(edges, edge_attr=True)
pos=nx.circular_layout(G)
print(G[2][1]["color"])
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw(G, pos= pos, with_labels=True, node_color='skyblue', node_size=500, edge_color=edges['color'], width=2.0, edge_cmap=plt.cm.Blues)
plt.show()

# Coloring specific edge
i=1
j=2
shortest_path.append(j if i>j else i)
shortest_path.append(i if i>j else j)
colorValues[edges_list.get(str(j if i>j else i)+"-"+str(i if i>j else j))] ="red"
edges = pd.DataFrame({"source": fromNode, "target": toNode, "weight": edgeWeights, "color": colorValues})
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw_networkx_nodes(G,pos=pos,nodelist=shortest_path,node_color="red", node_size=600)
nx.draw(G, pos= pos, with_labels=True , node_color='skyblue', node_size=500, edge_color=edges['color'], width=2.0, edge_cmap=plt.cm.Blues)
plt.show()


