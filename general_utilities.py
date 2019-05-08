# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:14:38 2017

@author: Vaiva
"""

def trophic_level(A, eps=1.0e-8):
    #calculate trophic levels, as average trophic levels of predator's prey+1
    M= A/A.sum(axis=1)
    N = M.shape[1]
    v = np.random.rand(N,1)
    last_v = np.random.rand(N, 1)
    
    while np.linalg.norm(v - last_v, 2) > eps:
        last_v = v
        mul =np.matmul(M, v)
        for i in range(N):
            val = mul[i] +1
            if np.isnan(val)==True:
                v[i] =last_v[i]
            else:
                v[i] = val 
    return v

def BFS(G):    
    bfs = defaultdict(dict)
    graph = list(reversed(list(nx.topological_sort(G))))
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
    
    

def calc_diversity(sample, label_dictionary):
    """
    Diversity score, based on Shannon entropy
    """
    denom = len(sample)
    H = 0
    if denom != 0:
        p_dict = {}
        for item in sample:
            label_item = label_dictionary[item]
            try:
                p_dict[label_item] += 1
            except:
                p_dict[label_item] = 1
        
        for key,val in p_dict.items():
            p_dict[key] = p_dict[key]/denom
        for p in p_dict.values():
            H += (-p*np.log(p))
        
    return np.exp(H)
    
    
 def calc_richness(sample, label_dictionary):
    p = set()
    if len(sample) > 0:
        for item in sample:
            label_item = label_dictionary[item]
            p.add(label_item)
    return len(p)


def cos_sim(a, b):
    
	"""Takes 2 vectors a, b and returns the cosine similarity according 
	to the definition of the dot product
	"""
    dot_product = np.dot(a, b.transpose())
    norm_a = a.data.sum()
    norm_b = b.data.sum()
    try:
        return (dot_product / (norm_a * norm_b)).data[0]
    except:
        return 0
        
        
 

def summary(dataPoints):
    if not dataPoints:
        raise StatsError('no data points passed')
    return [min(dataPoints), quartiles(dataPoints)[0], median(dataPoints), mean(dataPoints), quartiles(dataPoints)[1], max(dataPoints) ]





def quartiles(dataPoints):
   # check the input is not empty
   if not dataPoints:
       raise StatsError('no data points passed')
   # 1. order the data set
   sortedPoints = sorted(dataPoints)
   # 2. divide the data set in two halves
   mid = math.floor(len(sortedPoints) / 2)
  
  
   if (len(sortedPoints) % 2 == 0):
      # mid =int(mid)
   # even
       lowerQ = median(sortedPoints[:mid])
       upperQ = median(sortedPoints[mid:])
   else:
   # odd
       lowerQ = median(sortedPoints[:mid])  # same as even
       upperQ = median(sortedPoints[mid+1:])

   return (lowerQ, upperQ)
    

def median(dataPoints):
    """
    the median of given data
    Arguments:
        dataPoints: a list of data points, int or float
    Returns:
        the middle number in the sorted list, a float or an int
    """
    if not dataPoints:
        raise StatsError('no data points passed')
        
    sortedPoints = sorted(dataPoints)
    mid = len(sortedPoints) // 2  # uses the floor division to have integer returned
    if (len(sortedPoints) % 2 == 0):
        # even
        return (sortedPoints[mid-1] + sortedPoints[mid]) / 2.0
    else:
        # odd
        return sortedPoints[mid]
    
def mean(dataPoints, precision=3):
    """
    the arithmetic average of given data
    Arguments:
        dataPoints: a list of data points, int or float
        precision (optional): digits precision after the comma, default=3
    Returns:
        float, the mean of the input
        or StatsError if X is empty.
    """
    try:
        return round(sum(dataPoints) / float(len(dataPoints)), precision)
    except ZeroDivisionError:
        raise StatsError('no data points passed')
        
        
 
def tr(DAG, output=False):
    # for printing progress
    E = DAG.number_of_edges()
    i = 0
    print_limit = 10
    print_counter = print_limit
    edges = list(DAG.edges())
    #########################
    for edge in edges:
        # check edge is necessary for causal structure
        [a, b] = edge
        DAG.remove_edge(a, b)
        if not nx.has_path(DAG, a, b):
            DAG.add_edge(a, b)
        
        if output:
            i += 1
            pc = (i/float(E))*100
            if pc > print_counter:
                print ('Finished %s percent' % int(math.floor(pc)))
                print_counter += print_limit
                
    return DAG

def dag_rewire(DAG,percentage,cutoff = 1000000):
    edges = list(DAG.edges())
    
    N = round(len(edges)*percentage)
    rewired = 0
    attempts = 0
    
    while rewired < N:
        print(attempts)
        e1,e2 = random.sample(edges,2)
        a,b,c,d = e1[0],e1[1], e2[0],e2[1]
        if int(d)>int(b) and int(c) > int(a):
            e3,e4 = (c,a),(d,b)
            edges.remove(e1)
            edges.remove(e2)
            edges.append(e3)
            edges.append(e4)
            rewired += 1
        attempts += 1
        if attempts > cutoff:
            break
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G
            
    
    
    
