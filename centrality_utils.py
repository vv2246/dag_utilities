# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:55:33 2017

@author: VV1615
"""
import datetime 
from collections import defaultdict
import numpy as np
import networkx as nx
import random
import math

def extend_shortest_paths(graph,source,target):
    neighbors = graph.neighbors(source)
    paths = []
    for neighbor in neighbors:
        if target in neighbors:
            paths.append([source,neighbor,target])    
    return paths


def kdd_citation_dag(location = "C://Users/VV1615/OneDrive - Imperial College London/DAG/Data/hep-ph-citations.tar/hep-th-citations.txt"):
    """
    Retrieve hep-ph/hep-th citation dag from the edge list
    
    Returns
    -------
    graph - networkx directed acyclic graph
    """
    
    graph= nx.DiGraph()
    day=1
    with open(location) as data_file:
        for line in data_file:  
            if len(line.split())==2:
                paper,citation = line.split(" ") 
                paper_year = paper[0:2]
                if paper_year[0] == "0":
                    paper_year = "20" + paper_year
                else:
                    paper_year = "19" + paper_year
                date_paper = datetime.datetime(year = int(paper_year),month = int(paper[2:4]),day = day,microsecond =int(paper[4:7])) 
                citation_year = citation[0:2]
                if citation_year[0] == "0":
                    citation_year = "20" + citation_year
                else:
                    citation_year = "19" + citation_year
                date_citation = datetime.datetime(year = int(citation_year),month = int(citation[2:4]),day = day,microsecond =int(citation[4:7])) 
                if date_citation < date_paper:# and date_citation.year > yearzero and date_paper.year>yearzero and date_citation.year < yearinf and date_paper.year < yearinf:# and random.random()<0.05:
                    graph.add_edge(date_citation,date_paper)
    return graph
 

def reverse_and_enumerate_dag(graph):
    # flips edge direction in a dag and enumerates nodes
    node_ids = {}

    i = 0
    for n in sorted(graph.nodes()):
        node_ids[n] = i
        i += 1
        
    edges = graph.edges()
    reverse_edges = []

    for (i,j) in edges:
        reverse_edges.append((node_ids[j],node_ids[i]))
    
    reverse_dag = nx.DiGraph()
    reverse_dag.add_edges_from(reverse_edges)
    
    return node_ids,reverse_dag
    
    
def reverse_dag(graph):
    # flips edge direction in a dag 
    reverse_dag = nx.DiGraph()
    edges = graph.edges()
    for i,j in edges:
        reverse_dag.add_edge(j,i)
        
    return reverse_dag

def find_interval(DAG, start, end):
    # start is a higher integer than end
                       
    ################################################################################
    # find_interval
    # input: DAG - networkx DAG object
    #      start - start node of the interval
    #        end - end node fo the interval
    # return: interval_DAG - networkx DAG object of the interval between the start and end
    ################################################################################
    interval_nodes = interval_list(DAG, start, end)
    if not interval_nodes:
        return None
    interval_DAG = DAG.copy()
    for node in interval_DAG.nodes():
        if node not in interval_nodes:
            if node != start:
                if node != end:
                    interval_DAG.remove_node(node)
    return interval_DAG
    
def interval_list(DAG, start, end):
    node_list = []
    start_lightcone = lightcone_list(DAG, start, end, 'forward', [])
    end_lightcone = lightcone_list(DAG, start, end, 'backward', [])
    for node in start_lightcone:
        if node in end_lightcone:
            node_list.append(node)
    return node_list
    
def lightcone_list(DAG, start, end, direction, already_visited=[]):
    l=[]
    if direction=='forward':
        l += [start]
        already_visited.append(start)
        if start<=end:
            return l
        else:
            for node in DAG.successors(start):
                if node not in already_visited:
                    l += lightcone_list(DAG, node, end, direction, already_visited)
    elif direction=='backward':
        l += [end]
        already_visited.append(end)
        if end>=start:
            return l
        else:
            for node in DAG.predecessors(end):
                if node not in already_visited:
                    l += lightcone_list(DAG, start, node, direction, already_visited)
    return l

def interval_nodes_dict(D_in, D_out, start, end):
    
    
    ################################################################################
    # interval_nodes_dict
    # input: D_in - dictionary of in edges
    #       D_out - dictionary of out edges
    #       start - start node
    #         end - end node
    # 
    # return - node_list - list of nodes in the interval
    ################################################################################
    node_list = []
    start_lightcone = lightcone_list_dict(D_in, start, end, 'forward', [])
    end_lightcone = lightcone_list_dict(D_out, start, end, 'backward', [])
    for node in start_lightcone:
        if node in end_lightcone:
            node_list.append(node)
    return node_list
            
def lightcone_list_dict(DAG, start, end, direction, already_visited=[]):
    l = []   
    if direction=='forward':
        l += [start]
        already_visited.append(start)
        if start<=end:
            return l
        else:
            # D_in does not contain nodes which have no successors so avoid key error
            if start in DAG:
                for node in DAG[start]:
                    if node not in already_visited:
                        l += lightcone_list_dict(DAG, node, end, direction, already_visited)                        
    elif direction=='backward':
        l += [end]
        already_visited.append(end)
        if end>=start:
            return l
        else:
            if end in DAG:
                for node in DAG[end]:
                    if node not in already_visited:
                        l += lightcone_list_dict(DAG, start, node, direction, already_visited)        
    return l
                    
def path_preference(graph,path, type_of_preference = "bibliographic coupling"):
    path_pref = 0
    for i in range(len(path)-1):
        a,b = path[i],path[i+1]
        if type_of_preference == "bibliographic coupling":
            JI = compute_jaccard_index(set(graph.successors(a)),set(graph.successors(b)))
 
        elif type_of_preference == "co-citation":
            JI = compute_jaccard_index(set(graph.predecessors(a)),set(graph.predecessors(b)))
        path_pref += JI

    return path_pref/len(path)


def compute_jaccard_index(set1,set2):
    return len(set1.intersection(set2))/len(set1.union(set2))
    
def BFS(G):    
    bfs = defaultdict(dict)
    root = list(reversed(nx.topological_sort(G)))[0]
    roots = [root]
    graph = list(reversed(nx.topological_sort(G)))
    while graph:
        root = graph.pop(0)
        bfs[root][root] = 0
        for i in G.predecessors(root):
            for pred,val in bfs[root].items():
                if pred in bfs[i].keys():
                    bfs[i][pred] = max((val+1),bfs[i][pred])
                else:
                    bfs[i][pred] = val+1
    return bfs    
    
def rewire(edge_list, N):
    # this doesn't require us to actually make a graph - just use an edge list
    # we will do N successful rewirings
    # edge list is a list of 2-lists which all have [high_int, low_int] or reverse as per Vaiva's convention
    E = len(edge_list)
    if E < 3:
        #print 'edge list is not long enough'
        exit(0)
    n = 0
    while n < N:
        r1 = random.randrange(E)
        e1 = edge_list.pop(r1)
        r2 = random.randrange(E-1)
        e2 = edge_list.pop(r2)
        
        a, b = e1
        c, d = e2
        if (a<d and c<b): #Vaiva's convention
            # then we can swap
            new_e1 = [a, d]
            new_e2 = [c, b]
            edge_list.append(new_e1)
            edge_list.append(new_e2)
            n += 1
            if not n%1000:
                print (n)
        else:
            # we can't swap
            edge_list.append(e1)
            edge_list.append(e2)
            
    return edge_list
    

def cube_space_graph(N, D, p=1.0):
    """
    Create a cube space DAG


    Parameters
    ----------

    N - number of vertices in DAG
    D - dimension of box space
    p - probability with which allowed edges appear

    Notes
    -----

    In the cube space model, point a connects to point b iff a has smaller
    coordinates than b in every dimension.
    D=1 is a random DAG
    D=2 is equivalent to Minkowski space with D=2.
    """
    R = np.random.random((N, D))
    G = nx.DiGraph()
    edge_list = []
    for i in range(N):
        G.add_node(i, position=tuple(R[i]))
        for j in range(N):
            if (R[i] > R[j]).all():
                if p == 1. or p > np.random.random():
                    edge_list.append([j,i])
    G.add_edges_from(edge_list)
    return G    
    
    
    

def dag_closeness_centrality(graph,centrality_type, normalised = False,path_type="in"):
    
      """
      centrality_type : shortest path (sp)
                        longest path (lp)
                        harmonic shortest path (hsp)
                        harmonic longest path (hlp)
      normalised:
                        True
                        False
      future_past:
                        future
                        past
      """
      
      centrality = {}
      if path_type == "in" and  centrality_type == "sp":
          if normalised == True:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,target= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0
          
          else:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,target= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0
          return centrality
      
      if path_type == "out" and  centrality_type == "sp":
          if normalised == True:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,source= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0
          
          else:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,source= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0
          return centrality
      if path_type == "in" and  centrality_type == "hsp":
          if normalised == True:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,target= n).values()]
                  inverse_totsp = sum([1/a for a in sp if a != 0])
                  if inverse_totsp >1 :
                      centrality[n] = inverse_totsp/(len(sp)-1)
                  else:
                      centrality[n] = 0

          else:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,target= n).values()]
                  inverse_totsp = sum([1/a for a in sp if a != 0])
                  centrality[n] = inverse_totsp

          return centrality
      
      if path_type == "out" and  centrality_type == "hsp":
          if normalised == True:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,source= n).values()]
                  inverse_totsp = sum([1/a for a in sp if a != 0])
                  if inverse_totsp >1 :
                      centrality[n] = inverse_totsp/(len(sp)-1)
                  else:
                      centrality[n] = 0

          else:
              for n in graph:
                  sp = [len(a)-1 for a in nx.shortest_path(graph,source= n).values()]
                  inverse_totsp = sum([1/a for a in sp if a != 0])
                  centrality[n] = inverse_totsp

          return centrality
      
      if path_type=="in":
          
          graph = graph.reverse(copy=True)
          
     
      if centrality_type == "lp" :
          distances = BFS(graph)
          if normalised == True:
              for n in graph:
                  lp = list(distances[n].values())
                  totlp = sum(lp)
                  if totlp >0:
                      centrality[n] = (len(lp)-1)/totlp
                  else:
                      centrality[n] = 0
          else:
              for n in graph:
                  lp = list(distances[n].values())
                  totlp = sum(lp)
                  if totlp >0:
                      centrality[n] = 1/totlp
                  else:
                      centrality[n] = 0
          return centrality      
           
      if centrality_type == "hlp":
         distances = BFS(graph)
         if normalised == True:
             for n in graph:
                 lp = list(distances[n].values())
                 inverse_totlp = sum([1/a for a in lp if a != 0])
                 if inverse_totlp >1 :
                     centrality[n] = inverse_totlp/(len(lp)-1)
                 else:
                     centrality[n] = 0
         else:
            for n in graph:
                lp = list(distances[n].values())
                inverse_totlp = sum([1/a for a in lp if a != 0])
                centrality[n] = inverse_totlp
         return centrality

    
    
