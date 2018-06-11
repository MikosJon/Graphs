from collections import namedtuple, defaultdict, deque
from heapq import heappush, heappop

class DirectedGraph:
    Arrow = namedtuple('Arrow', 'head tail weight')
    Arrow.__new__.__defaults__ = (1,)


    def __init__(self, *, vertices=set(), arrows=set(), vertexFill=False):
        self._V, self._A = set(), set()
        for head, tail, *value in arrows:
            if value:
                self.arrows |= {self.Arrow(head, tail, value[0])}
            else:
                self.arrows |= {self.Arrow(head, tail)}

        if not vertexFill:
            self.vertices = set(vertex for vertex in vertices)

    @classmethod
    def fromAdjacencyList(cls, dic):
        vertices = set()
        arrows = set()
        for vertex, values in dic.items():
            vertices.add(vertex)
            for value in values:
                try:
                    arrows |= {(vertex, *value)}
                    vertices.add(value[0])
                except TypeError:
                    arrows |= {(vertex, value)}
                    vertices.add(value)

        return cls(vertices=vertices, arrows=arrows)

    @classmethod
    def fromAdjacencyMatrix(cls, mat):
        vertices = set()
        arrows = set()
        for i, row in enumerate(mat):
            vertices.add(i+1)
            for j, value in enumerate(row):
                if value == 0:
                    continue
                arrows.add((i+1, j+1, value))

        return cls(vertices=vertices, arrows=arrows)

    def __repr__(self):
        return '{}(vertices={}, arrows={})'.format(self.__class__.__name__,
                                                  '{' + ', '.join("{}".format(vertex) for vertex in self.vertices) + '}',
                                                  '{' + ', '.join("self.Arrow({}, {}, {})".format(*arrow) for arrow in self.arrows) + '}')

    def __getitem__(self, values):
        new_vertices = set(values)
        new_arrows = set(arrow for arrow in self.arrows if arrow.head in new_vertices and arrow.tail in new_vertices)
        return DirectedGraph(vertices=new_vertices, arrows=new_arrows)

    @property
    def vertices(self):
        return self._V

    @vertices.setter
    def vertices(self, values):
        self._V = set(values)
        self._A = set(arrow for arrow in self.arrows if arrow.head in values and arrow.tail in values)

    @property
    def arrows(self):
        return self._A

    @arrows.setter
    def arrows(self, values):
        self._A = set(self.Arrow(*arrow) for arrow in values)

    @property
    def size(self):
        return len(self.arrows)

    @property
    def order(self):
        return len(self.vertices)

    @property
    def adjacencyList(self):
        dic = defaultdict(list)
        for arrow in self.arrows:
            dic[arrow.head].append((arrow.tail, arrow.weight))
        return dic

    @property
    def delta(self):
        return min(self.degree(vertex) for vertex in self.vertices)

    @property
    def Delta(self):
        return max(self.degree(vertex) for vertex in self.vertices)

    @property
    def balanced(self):
        return all([self.indegree(vertex) == self.outdegree(vertex) for vertex in self.vertices])

    @property
    def radius(self):
        return min(self.eccentricity(vertex) for vertex in self.vertices)

    @property
    def girth(self):
        done = set()
        minSeen = None
        for vertex in self.vertices:
            if vertex in done:
                continue
            for cycle in self.cyclesFrom(vertex):
                done |= set(cycle)
                if minSeen:
                    minSeen = min([minSeen, len(cycle)-1])
                else:
                    minSeen = len(cycle)-1
        return minSeen

    @property
    def circumference(self):
        done = set()
        maxSeen = None
        for vertex in self.vertices:
            if vertex in done:
                continue
            for cycle in self.cyclesFrom(vertex):
                done |= set(cycle)
                if maxSeen:
                    maxSeen = max([maxSeen, len(cycle)-1])
                else:
                    maxSeen = len(cycle)-1
        return maxSeen

    @property
    def weaklyConnected(self):
        temp_arrows = self.arrows | set(self.flipArrow(arrow) for arrow in self.arrows)
        temp_graph = DirectedGraph(vertices=self.vertices, arrows=temp_arrows)
        return len(temp_graph.isolatedVertices()) == 0

    @property
    def stronglyConnected(self):
        return len(list(self.stronglyConnectedComponents())) == 1

    def addVertex(self, vertex):
        self.vertices |= {vertex}

    def removeVertex(self, vertex):
        self.vertices -= {vertex}

    def hasVertex(self, vertex):
        return vertex in self.vertices

    def addArrow(self, arrow):
        self.arrows |= {self.Arrow(*arrow)}

    def removeArrow(self, arrow):
        self.arrows -= {self.Arrow(*arrow)}

    def hasArrow(self, arrow):
        return self.Arrow(*arrow) in self.arrows

    def flipArrow(self, arrow):
        return self.Arrow(arrow.tail, arrow.head, arrow.weight)

    def isolatedVertices(self):
        return set(vertex for vertex in self.vertices if self.degree(vertex) == 0)

    def removeIsolated(self):
        self.vertices = set(vertex for vertex in self.vertices if self.degree(vertex) != 0)

    def neighbours(self, vertex):
        return set(arrow.tail for arrow in self.arrows if arrow.head == vertex)

    successors = neighbours

    def predecessors(self, vertex):
        return set(arrow.head for arrow in self.arrows if arrow.tail == vertex)

    def indegree(self, vertex):
        return [arrow.tail for arrow in self.arrows].count(vertex)

    def outdegree(self, vertex):
        return [arrow.head for arrow in self.arrows].count(vertex)

    def degree(self, vertex):
        return self.indegree(vertex) + self.outdegree(vertex)

    def isSource(self, vertex):
        return self.indegree(vertex) == 0 and self.outdegree(vertex) != 0

    def isSink(self, vertex):
        return self.outdegree(vertex) == 0 and self.indegree(vertex) != 0

    def isInternal(self, vertex):
        return not self.isSource(vertex) and not self.isSink(vertex)

    def eccentricity(self, vertex):
        max_dist = 0
        visited = set()
        Q = deque([(vertex, 0)])
        while Q:
            curr, eccentricity = Q.popleft()
            max_dist = max(max_dist, eccentricity)
            visited.add(curr)
            for neighbour in self.neighbours(curr):
                if neighbour not in visited:
                    Q.append((neighbour, eccentricity+1))
        return max_dist

    def existsPath(self, node, end, *, visited=set()):
        if node == end:
            return True
        visited.add(node)
        for neighbour in self.neighbours(node):
            if neighbour not in visited and self.existsPath(neighbour, end):
                return True
        return False

    def shortestPath(self, start, end, *, distance=False):
        priorityQueue = []
        heappush(priorityQueue, (0, [], start))
        visited = set()
        while priorityQueue:
            sum_weights, all_prev, curr = heappop(priorityQueue)
            if curr in visited:
                continue
            visited.add(curr)
            new_path = all_prev + [curr]
            if curr == end:
                if distance:
                    return new_path, sum_weights
                else:
                    return new_path
            for neighbour_arrow in [arrow for arrow in self.arrows if arrow.head == curr]:
                heappush(priorityQueue, (sum_weights+neighbour_arrow.weight, new_path, neighbour_arrow.tail))
        if distance:
            return None, None
        else:
            return None

    def cyclesFrom(self, node, *, search=None, visited=set(), prefix=None, cycles=set()):
        if search is None:
            search = node

        if prefix is None:
            prefix = (search,)

        if node in visited:
            if node == search:
                cycles.add(prefix)
        else:
            visited.add(node)
            for neighbour in self.neighbours(node):
                self.cyclesFrom(neighbour, search=search, prefix=prefix+(neighbour,))
            visited.remove(node)
        return cycles

    def stronglyConnectedComponents(self):
        done = set()
        for vertex in self.vertices:
            if vertex in done:
                continue
            component = self._trajan(vertex)
            done |= set(component)
            yield component

    def stronglyConnectedTo(self, vertex):
        component = self._trajan(vertex)
        if vertex in component:
            return component

    def _trajan(self, v, *, index=0, indicies={}, low_links={}, S=[], components=[]):
        indicies[v] = index
        low_links[v] = index
        index += 1
        S.append(v)

        for w in self.neighbours(v):
            if w not in indicies:
                self._trajan(w, index=index, indicies=indicies, low_links=low_links, S=S, components=components)
                low_links[v] = min(low_links[v], low_links[w])
            elif w in S:
                low_links[v] = min(low_links[v], indicies[w])

        if low_links[v] == indicies[v]:
            new_component = set()
            while True:
                w = S.pop()
                new_component.add(w)
                if w == v:
                    return new_component