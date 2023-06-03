from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""https://datos.gob.cl/dataset/gtfs-talca/resource/f4526a2f-dd8e-4943-ab12-be997ce04fbb
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
import numpy as np
from heapq import heappush,heappop

class abstract_graph:
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges} | {v for u,v in self.edges}
        
    def adjacency_matrix(self):
        pass
    
    def adjacency_list(self):
        pass

    
class simple_graph(abstract_graph):
    
    def adjacency_list(self):
        adjacent=lambda n : {v for u,v in self.edges if u==n } | {u for u,v in self.edges if v==n}
        return {v:adjacent(v) for v in self.nodes}
   
class weighted_graph(abstract_graph):
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        
    def adjacency_matrix(self):
        n=len(self.nodes)
        mat=np.zeros((n,n))
        adjacent=lambda x : [1 if x==v else 0 for (u,v) in enumerate(sorted(list(G.nodes))) ]
        L=self.adjacency_list()
        i=0
        for v in sorted(list(G.nodes)):
            for l in L[v]:
                mat[i,]+=adjacent(l)
            i=i+1
        return mat
    
    def adjacency_list(self):
        adjacent=lambda n : {v for u,v in self.edges.keys() if u==n } | {u for u,v in self.edges if v==n}
        return {v:adjacent(v) for v in self.nodes}

class weighted_digraph(abstract_graph):
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        
    
    def adjacency_list(self):
        adjacent=lambda n : {v for u,v in self.edges.keys() if u==n } 
        return {v:adjacent(v) for v in self.nodes}    
    
    
def prim_mst(graph,start):
    frontier, visited = [], set()
    tree=[]
    heappush(frontier, (0, (None,start)))
    adjacency=graph.adjacency_list()
    while frontier:
        weight,(u,v)=heappop(frontier)
        if v in visited:
            continue
        print('Vertice padre: {0}, Prioridad {1}'.format(v,weight))
        visited.update({v})
        tree.append((u,v,{'weight':weight}))
        for neighbor in adjacency[v]:
            #print('Vertice vecino : {0}'.format(neighbor))
            if neighbor not in visited:
                if (v,neighbor) in graph.edges:
                    new_edge=(v,neighbor)
                else:
                    new_edge=(neighbor,v)
                heappush(frontier, (graph.edges[new_edge], (v,neighbor)))
                
df=pd.read_csv('https://github.com/iZpasito/taller2/blob/main/stops.txt', encoding = 'utf-8',dtype={'WKT':str,'InputID':str,'TargetID':str,'Distance':float}) 
df.loc[df['InputID']=='TALCA'].head()
df['WKT'] = df['WKT'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
df['InputID'] = df['InputID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
df['TargetID'] = df['TargetID'].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))
df['InputID'].unique()
T=prim_mst(G,'TALCA')
cost=np.sum([d['weight'] for (u,v,d) in T])
print('El costo del arbol recubridor es : {}'.format(cost))
