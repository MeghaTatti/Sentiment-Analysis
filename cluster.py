#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Cluster data.
"""
from collections import Counter, defaultdict, deque
import matplotlib.pyplot as plt
import networkx as nx
import sys
import pickle
import math
from itertools import chain, combinations

def get_twitter_user(name):
    
    with open(name + '.pkl', 'rb') as val:
        return pickle.load(val)
    print("User data Collected.")


# In[2]:


def print_num_friends(users):
    """
    Print the number of friends of each user, sorted by candidate name.
    
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    for i in users:
        print(i['screen_name'], str(len(i['friends_id'])))
    pass

#     for usern in users:
#         num_friends = str(len(usern['friends_id']))
#         print (usern['screen_name'] + ' ' + num_friends)


# In[3]:


def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    
    c = Counter()
    for i in users:
        c.update(i['friends_id'])
    return c
        
pass


# In[4]:


def friend_overlap(users):
    """
    Compute the number of common friends of each pair of users.

    Args:
        users...The list of user dicts.

    Return:
        A list of tuples containing (user1, user2, N), where N is the
        number of friends that both user1 and user2 follow.
        This list shouldbe sorted in descending order of N.
        Ties are broken first by user1's screen_name, then by
        user2's screen_name (sorted in ascending alphabetical order).
    """

    pointer = 0
    friend_overlap = []
    overlap = tuple()
    
    for i in range(0, len(users)):
        for j in range(i+1, len(users)):
            for m in range(0, len(users[i]['friends_id'])):
                for n in range(0, len(users[j]['friends_id'])):
                    if users[i]['friends_id'][m] == users[j]['friends_id'][n]:
                        pointer += 1
            overlap = (users[i]['screen_name'], users[j]['screen_name'], pointer)
            friend_overlap.append(overlap)
            pointer = 0

    friend_overlap = sorted(friend_overlap, key=lambda tup: (-tup[2], tup[0], tup[1]))

    return friend_overlap


# In[5]:


def create_graph(users, friend_counts, min_common):
    """
    Create a networkx undirected Graph, adding each user and their friends
    as a node.
    Note: while all users should be added to the graph,
    Each user in the Graph will be represented by their screen_name,
    while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
      min_common......Add friends to the graph if they are followed by more than min_common users.
    Returns:
      A networkx Graph
    """
    follow = [x for x in friend_counts if friend_counts[x] > min_common]
    graph = nx.Graph()
    for x in follow:
        graph.add_node(x)
    for user in users:
        graph.add_node(user['id'])
        fndlst = set(user['friends_id']) & set(follow)
        for fnd in fndlst:
            graph.add_edge(fnd, user['id'])
    nx.draw_networkx(graph, with_labels=True)    
    return graph
pass


# In[6]:


def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    labels={}
    for n in graph.nodes():
        for u in users:
            if n in u['id']:
                labels[n] = u['screen_name']
            #labels[u['screen_name']]=u['screen_name']
    plt.figure(figsize=(15,15))
    nx.draw_networkx(graph,labels=labels,with_labels=True,alpha=0.5, width=0.5, node_size=100)
    plt.axis('off')
    plt.savefig(filename)
    plt.show()
    pass


# In[7]:


def get_subgraph(graph, min_degree):
    """
    Return a subgraph containing nodes whose degree is
    greater than or equal to min_degree.
    To prune the original graph.

    Params:
      graph........a networkx graph
      min_degree...degree threshold
    Returns:
      a networkx graph, filtered as defined above.
    """   
    s_n = []
    for n in graph.nodes():
        if (graph.degree(n) >= min_degree):
            s_n.append(n)
    return graph.subgraph(s_n)
pass


# In[8]:


def bfs(graph, root, max_depth):

    node2parents = {}
    node2distances = {}
    node2num_paths = {}
    visiting = deque()
    visited = deque()    
    nodes = graph.nodes()
    visited={x:"No" for x in nodes}
    visiting.append(root)
    distance= {x:float("inf") for x in nodes}
    distance[root] = 0
    parents = {x:[] for x in nodes} 
    parents[root] = root  
    while(len(visiting) > 0):
        c = visiting.popleft()
        child = graph.neighbors(c)            
        for node in child:
            if(distance[c] > max_depth):
                break
            if(visited[node] == "No"):
                if(distance[node] < distance[c]):
                    break
                elif(distance[node] > distance[c] ):
                    distance[node] = distance[c] + 1
                    parents[node].append(c)
                    visiting.append(node)
        visited[c] = "Yes"        
    for node in visited:
        if(visited[node] == "Yes"):
            node2distances[node] = distance[node]
            node2num_paths[node] = len(parents[node])
            if(node != root):
                node2parents[node] = parents[node]
    return node2distances, node2num_paths, node2parents
pass


# In[9]:


def bottom_up(root, node2distances, node2num_paths, node2parents):
   
    node2credit = defaultdict(lambda :0)
    credit = defaultdict(lambda:0)
    parents = [item for sublist in node2parents.values() for item in sublist]
    for n in node2distances:
        if n not in parents:
            node2credit[n] = 1
    levels = sorted(node2distances.items(), key=lambda x: -x[1])
    for c,_ in levels:
        if c is root:
            break
        ps = node2parents[c]
        if root in ps:
            l = sorted([c,root])
            credit[(l[0], l[1])] = node2credit[c]
        else:
            s = sum(node2num_paths[i] for i in ps)
            for p in ps:
                l = sorted([c,p])
                edge = (l[0], l[1])
                credit[edge]  = node2credit[c]*node2num_paths[p]/s
                node2credit[p]+= credit[edge]
                parents.remove(p)
                if p not in parents:
                    node2credit[p] += 1

    return dict(credit)
    pass


# In[10]:


def approximate_betweenness(graph, max_depth):
    """
    Compute the approximate betweenness of each edge, using max_depth to reduce
    computation time in breadth-first search.
    Only leave the original users nodes and corresponding edges and betweenness for future analysis.

    Params:
      graph.......A networkx Graph
      max_depth...An integer representing the maximum depth to search.

    Returns:
      A dict mapping edges to betweenness. Each key is a tuple of two strings
      representing an edge (e.g., ('A', 'B')). Make sure each of these tuples
      are sorted alphabetically (so, it's ('A', 'B'), not ('B', 'A')).
    """

    betweenness = dict()
    for node in graph.nodes():
        node2distances, node2num_paths, node2parents = bfs(graph, node, max_depth)
        bet = bottom_up(node, node2distances, node2num_paths, node2parents)
        for edge in bet:
            if edge in betweenness:
                betweenness[edge] = betweenness[edge] + bet[edge]
            else:
                betweenness[edge] = bet[edge]
    for a,b in betweenness.items():
        betweenness[a]=b/2

    return betweenness
    pass


# In[11]:


def partition_girvan_newman(graph, max_depth, num_clusters):
    """
    Use the approximate_betweenness implementation to partition a graph.
    Unlike in class, here you will not implement this recursively. Instead,
    just remove edges until more than one component is created, then return
    those components.
    That is, compute the approximate betweenness of all edges, and remove
    them until multiple comonents are created.

    Note: the original graph variable should not be modified. Instead,
    make a copy of the original graph prior to removing edges.

    Params:
      graph..........A networkx Graph created before
      max_depth......An integer representing the maximum depth to search.
      num_clusters...number of clusters want

    Returns:
      clusters...........A list of networkx Graph objects, one per partition.
      users_graph........the partitioned users graph.
    """
 
    clusters = []

    partition_edge = list(sorted(approximate_betweenness(graph, max_depth).items(), key=lambda x:(-x[1], x[0])))    
    for i in range(0, len(partition_edge)):
        graph.remove_edge(*partition_edge[i][0])
        clusters = list(nx.connected_component_subgraphs(graph))
        if len(clusters) >= num_clusters:
            break
    new_clusters = [cluster for cluster in clusters if len(cluster.nodes()) > 1]
    return new_clusters, graph


# In[12]:


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)


# In[13]:


def main():
    users = get_twitter_user('twitter_users')
    print('Number of friends of each user:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    graph = create_graph(users, friend_counts,0)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'UserNetwork.png')
    print('Successful drawing of network1')
    subgraph = create_graph(users, friend_counts, 1)
    print('subgraph has %s nodes and %s edges' % (len(subgraph.nodes()), len(subgraph.edges())))
    draw_network(subgraph, users, 'Subgraph.png')
    print('Successful drawing of subgraph')
    clusters, partitioned_graph = partition_girvan_newman(subgraph, 5, 100)
    save_obj(clusters, 'Clusters')
    print('Total number of clusters= %d'%len(clusters))
    print('cluster 1 has %d nodes, cluster 2 has %d nodes' %
          (len(clusters[0].nodes()), len(clusters[1].nodes())))
    draw_network(partitioned_graph, users, 'Partitionedgraph.png')
    print('Successful drawing of partitioned_graph')
    
if __name__ == '__main__':
    main()

