# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:14:38 2017

@author: Vaiva
"""

from utilities import *

def dag_closeness_centrality(graph,centrality_type, normalised = False,future_past="future"):

  """
  centrality_type : shortest path (fsp)
                    longest path (flp)
                    harmonic shortest path (hsp)
                    harmonic longest path (hlp)
  normalised:
                    True
                    False
  future_past:
                    future
                    past
  """
  if future_past =="past":
      graph = graph.reverse(copy= True)
      
  if centrality_type == "sp":
      if normalised = True:
        return nx.closeness_centrality(graph,normalised = True)
      else:
        return nx.closeness_centrality(graph,normalised = False)

  if centrality_type == "hsp":
      centrality = {}
      if normalised == True:
        for n in graph:
            sp = [len(a) for a in nx.shortest_path(graph,target= n).values()]
            inverse_totsp = sum([1/a for a in sp if a != 0])
            if inverse_totsp >1 :
                centrality[n] = inverse_totsp/(len(sp)-1)
            else:
                centrality[n] = 0
      else:
        for n in graph:
            sp = [len(a) for a in nx.shortest_path(graph,target= n).values()]
            inverse_totsp = sum([1/a for a in sp if a != 0])
            centrality[n] = inverse_totsp
     return centrality
     
     if centrality_type == "lp" :
     
     
        centrality = {}
        distances = BFS(G)
        for n in G:
          lp = distances[n]
          totlp = sum(lp)
          if totlp >0
        
          def longest_path_future_harmonic_closeness_normalised(G):
    closeness_centrality = {}
    breadth_first_search = BFS(G)
    T = list(nx.topological_sort(G))
    for n in G:
        lp = breadth_first_search[n]
        totlp_inverse = sum([1/a for a in lp.values() if a != 0])
        normalisation = len(G) - T.index(n)
        if totlp_inverse > 0.0 and len(G) > 1:
            closeness_centrality[n] = totlp_inverse/normalisation
        else:
            closeness_centrality[n] = 0.0
    return closeness_centrality
