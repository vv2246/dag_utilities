# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:14:38 2017

@author: Vaiva
"""

from utilities import *



def dag_closeness_centrality(graph,centrality_type, normalised = False,future_past="future"):
    
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
      if future_past == "past":
          graph = graph.reverse(copy=True)
          
      if centrality_type == "sp":
          if normalised == True:
              for n in graph:
                  sp = [len(a) for a in nx.shortest_path(graph,target= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0

          else:
              for n in graph:
                  sp = [len(a) for a in nx.shortest_path(graph,target= n).values()]
                  totsp = sum([a for a in sp if a != 0])
                  if totsp >0 :
                      centrality[n] = (len(sp)-1)/totsp
                  else:
                      centrality[n] = 0
          return centrality
      if centrality_type == "hsp":
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
