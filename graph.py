"""
Graph module for directed graph.

Includes the functions implemented in the Jan 21/22
lectures with one key difference.

The way the nodes and edges are stored has already
been converted to the "adjacency list" representation
we will discuss next lecture.

More specifically, _alist is a dictionary that maps
a node u to the list of neighbours of u. You can call
the methods of the graph in exactly the same way as before,
these changes simply improve the running time.

All running time statements are under the assumption that it takes
O(1) time to index a dictionary.

We will add more to this file in the next lecture, but this
is enough to do the next exercise.
"""


class Graph:
    def __init__(self, V=set(), E=[]):
        """
        Create a graph with a given set of
        vertices and list of edges.
        For the purpose of this class
        We want E to be a list of tuples.

        If no arguements are passed in,
        the graph is an empty graph with
        no vertices and edges.

        Running time: O(len(V) + len(E))

        >>> g = Graph()
        >>> g._alist == {}
        True
        >>> g = Graph({1,2,3}, {(1,2), (2,3)})
        >>> g._alist.keys() == set({1,2,3})
        True
        >>> g._alist[1]
        [2]
        >>> g._alist[3]
        []
        """

        # _alist is a dictionary that maps vertices to a list of vertices
        # i.e. _alist[v] is the list of neighbours of v
        # This also means _alist.keys() is the set of nodes in the graph
        self._alist = {}

        for v in V:
            self.add_vertex(v)

        for e in E:
            self.add_edge(e)

    def add_vertex(self, v):
        """
        Adds a vertex to our graph.

        Running time: O(1)
        
        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> 1 in g._alist.keys()
        True
        >>> g.add_vertex(1)
        >>> len(g._alist) == 1
        True
        """
        if v not in self._alist.keys():
            self._alist[v] = []

    def add_edge(self, e):
        """
        Adds an edge to our graph.
        Do not add edge if the vertices
        for it do not exist. 
        Can add more than one copy of an edge.

        Running time: O(1)

        >>> g = Graph({1,2})
        >>> 2 in g._alist[1]
        False
        >>> g.add_edge((1,2))
        >>> 2 in g._alist[1]
        True
        >>> g.add_edge((1,2))
        >>> len(g._alist[1]) == 2
        True
        """
        if e[0] in self._alist.keys() and e[1] in self._alist.keys():
            self._alist[e[0]].append(e[1])

    def neighbours(self, v):
        """
        Given a vertex v, return a copy of the list
        of neighbours of v in the graph.
        
        >>> g = Graph()
        >>> g.neighbours(1)
        []
        >>> g = Graph({1,2,3}, [(1,2), (1,3)])
        >>> g.neighbours(1)
        [2, 3]

        Running time: O(len(self._alist[v]))
        (linear in the number of neighbours of v)
        """

        if v not in self._alist.keys():
            return []
        else:
            return list(self._alist[v])

    def vertices(self):
        """
        Returns a copy of the set of vertices in the graph.

        Running time: O(# vertices)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g.vertices() == {1,2,3}
        True
        """

        return list(self._alist.keys())

    def edges(self):
        """
        Create and return a list of the edges in the graph.

        Running time: O(# nodes + # edges)

        >>> g = Graph({1,2,3}, [(1,2), (2,3)])
        >>> g.edges()
        [(1, 2), (2, 3)]
        """

        edges = []
        for v, adj in self._alist.items():
            for u in adj:
                edges.append((v, u))

        return edges

    def is_vertex(self, v):
        """
        Returns true if and only if v is a vertex in the graph.
        This is more efficient then checking v in g.vertices().

        Running time: O(1)

        >>> g = Graph({1,2})
        >>> g.is_vertex(1)
        True
        >>> g.is_vertex(3)
        False
        """

        return v in self._alist.keys()

    def is_edge(self, e):
        """
        Returns true if and only if e is an edge in the graph.
        
        Running time: O(len(self._alist[e[0]]))
        linear in the number neighbours of e[0]

        >>> g = Graph({1,2}, [(1,2)])
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        False
        >>> g.is_edge((3,1))
        False
        """

        if not self.is_vertex(e[0]):
            return False
        return e[1] in self._alist[e[0]]


def is_walk(g, walk):
    """
    g is a graph and w is a list of nodes.
    Returns true if and only if w is a walk in g.

    Running time - O(d * m) where:
      - k = len(walk)
      - d = maximum size of a neighbourhood of a node
    In particular, if the graph has no repeated edges, then d <= # nodes.
    
    >>> g = Graph({1,2,3,4}, [(1,2), (2,3), (2,4), (4,3), (3,1)])
    >>> is_walk(g, [1,2,3,1,2,4])
    True
    >>> is_walk(g, [1,2,3,2])
    False
    >>> is_walk(g, [])
    False
    >>> is_walk(g, [1])
    True
    >>> is_walk(g, [5])
    False
    """

    for v in walk:  # O(k)
        if not g.is_vertex(v):  # O(1)
            return False

    if len(walk) == 0:
        return False

    # Note, can reduce the running time of the entire function
    # to O(k) if we implement the method is_edge to run in O(1) time.
    # This is a good exercise to think about.
    for node in range(0, len(walk) - 1):  # O(k)
        if not g.is_edge((walk[node], walk[node + 1])):  # O(d)
            return False

    return True


def is_path(g, path):
    """
    Returns true if and only if path is a path in g

    Running time: O(k*d)
    Specifically, is O(k) + running time of is_walk.

    >>> g = Graph({1,2,3,4}, [(1,2), (2,3), (2,4), (4,3), (3,1)])
    >>> is_path(g, [1,2,3,1,2,4])
    False
    >>> is_path(g, [1,2,3])
    True
    """

    return is_walk(g, path) and len(path) == len(set(path))


def search(g, v):
    """
    Find all nodes that can be reached from v in the graph g.

    Returns a dictionary 'reached' such that reached.keys()
    are all nodes that can be reached from v and reached[u]
    is the predecessor of u in the search.

    Running time: O(# nodes + # edges)
    More specifically, O(# edges (u,w) with u reachable from v)

    >>> g = Graph({1,2,3,4,5,6}, [(1,2), (1,3), (2,5), (3,2), (4,3), (4,5), (4,6), (5,2), (5,6)])
    >>> reached = search(g, 1)
    >>> reached.keys() == {1,2,3,5,6}
    True
    >>> g.is_edge((reached[6], 6))
    True
    """

    reached = {}
    stack = [(v, v)]
    # brief running time analysis:
    # each edge (u,v) will be added and removed from the stack at most once
    while stack:
        u, w = stack.pop()

        # the block under the if statement will be run at
        # most once per node u and the
        # inner loop takes time O(# neighbours of u)
        # the sum of (# neighbours of u) over all u is just # edges.
        if u not in reached.keys():
            reached[u] = w

            for x in g.neighbours(u):
                stack.append((x, u))

    # so, even though there are nested loops the running
    # time will still be linear

    return reached


# from eClass
def least_cost_path(graph, start, dest, cost):
    """
    Using Dijkstra's algorithm to solve for the least
    cost path in graph from start vertex to dest vertex.
    Input variable cost is a function with method signature
    c = cost(e) where e is an edge from graph.

    >>> graph = Graph({1,2,3,4,5,6}, [(1,2), (1,3), (1,6), (2,1), (2,3), (2,4), (3,1), (3,2), \
            (3,4), (3,6), (4,2), (4,3), (4,5), (5,4), (5,6), (6,1), (6,3), (6,5)])
    >>> weights = {(1,2): 7, (1,3):9, (1,6):14, (2,1):7, (2,3):10, (2,4):15, (3,1):9, \
            (3,2):10, (3,4):11, (3,6):2, (4,2):15, (4,3):11, (4,5):6, (5,4):6, (5,6):9, (6,1):14,\
            (6,3):2, (6,5):9}
    >>> cost = lambda e: weights.get(e, float("inf"))
    >>> least_cost_path(graph, 1,5, cost)
    [1, 3, 6, 5]
    """
    # est_min_cost[v] is our estimate of the lowest cost
    # from vertex start to vertex v
    est_min_cost = {}

    # parents[v] is the parent of v in our current
    # shorest path from start to v
    parents = {}

    # todo is the set of vertices in our graph which
    # we have seen but haven't processed yet. This is
    # the list of vertices we have left "to do"
    todo = {start}

    est_min_cost[start] = 0

    while todo:
        current = min(todo, key=lambda x: est_min_cost[x])

        if current == dest:
            return reconstruct_path(start, dest, parents)

        todo.remove(current)

        for neighbour in graph.neighbours(current):
            #if neighbour isn't in est_min_cost, that means I haven't seen it before,
            #which means I should add it to my todo list and initialize my lowest
            #estimated cost and set it's parent
            if not neighbour in est_min_cost:
                todo.add(neighbour)
                est_min_cost[neighbour] = (est_min_cost[current] + cost((current, neighbour)))
                parents[neighbour] = current
            elif est_min_cost[neighbour] > (est_min_cost[current] + cost((current, neighbour))):
                #If my neighbour isn't new, then I should check if my previous lowest cost path
                #is worse than a path going through vertex current. If it is, I will update
                #my cost and record current as my new parent.
                est_min_cost[neighbour] = (est_min_cost[current] + cost((current, neighbour)))
                parents[neighbour] = current

    return []


# from eClass
def reconstruct_path(start, dest, parents):
    """
    reconstruct_path reconstructs the shortest path from vertex
    start to vertex dest.

    "parents" is a dictionary which maps each vertex to their
    respective parent in the lowest cost path from start to that
    vertex.

    >>> parents = {'l': ' ', 'e': 'l', 'a': 'e', 'h':'a'}
    >>> reconstruct_path('l', 'h', parents)
    ['l', 'e', 'a', 'h']

    """
    current = dest
    path = [dest]

    while current != start:
        path.append(parents[current])
        current = parents[current]

    path.reverse()
    return path