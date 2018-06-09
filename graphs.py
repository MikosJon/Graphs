from collections import namedtuple, defaultdict
import heapq

Arrow = namedtuple('Arrow', 'head tail weight')
Arrow.__new__.__defaults__ = (1,)

class DirectedGraph:
    def __init__(self, *, vertices=set(), arrows=set()):
        self._V, self._A = set(), set()
        self.vertices = set(str(vertex) for vertex in vertices)
        for head, tail, *weight in arrows:
            if weight:
                weight = weight[0]
            else:
                weight = 1
            self.arrows |= {Arrow(str(head), str(tail), weight)}

    @classmethod
    def fromAdjacencyList(cls, dic):
        vertices = set()
        arrows = set()
        for vertex, vals in dic.items():
            vertices.add(vertex)
            try:
                arrows ^= set((vertex, *arrow) for arrow in vals)
            except TypeError:
                arrows ^= set((vertex, node) for node in vals)

        return cls(vertices=vertices, arrows=arrows)

    @classmethod
    def fromAdjacencyMatrix(cls, mat):
        vertices = set()
        arrows = set()
        for i, row in enumerate(mat):
            vertices.add(i+1)
            for j, val in enumerate(row):
                if not val:
                    continue
                arrows.add((i+1, j+1, val))

        return cls(vertices=vertices, arrows=arrows)

    def __repr__(self):
        return '{}(vertices={}, arrows={})'.format(self.__class__.__name__,
                                                  '{' + ', '.join("'{}'".format(vertex) for vertex in self.vertices) + '}',
                                                  '{' + ', '.join("Arrow('{}', '{}', {})".format(*arrow) for arrow in self.arrows) + '}')

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
        self._A = set(Arrow(*arrow) for arrow in values)
        self._V = set(arrow.head for arrow in self._A) | set(arrow.tail for arrow in self._A)

    @property
    def size(self):
        return len(self.vertices)

    @property
    def adjacencyList(self):
        dic = defaultdict(list)
        for arrow in self.arrows:
            dic[arrow.head].append((arrow.tail, arrow.weight))
        return dic

    def addVertex(self, vertex):
        self.vertices |= {vertex}

    def removeVertex(self, vertex):
        self.vertices -= {vertex}

    def hasVertex(self, vertex):
        return vertex in self.vertices

    def addArrow(self, arrow):
        self.arrows |= {Arrow(*arrow)}

    def removeArrow(self, arrow):
        self.arrows -= {Arrow(*arrow)}

    def hasArrow(self, arrow):
        return Arrow(*arrow) in self.arrows

    def isolatedVertices(self):
        return set(vertex for vertex in self.vertices if self.indegree(vertex) == 0 and self.outdegree(vertex) == 0)

    def existsPath(self, node, end, *, visited=set()):
        if node == end:
            return True
        visited.add(node)
        for neighbour in self.neighbours(node):
            if neighbour not in visited and self.existsPath(neighbour, end):
                return True
        return False

    def shortestPath(self, start, end, *, returnWeight=False):
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, [], start))
        visited = set()
        while priorityQueue:
            sum_weights, all_prev, curr = heapq.heappop(priorityQueue)
            if curr in visited:
                continue
            visited.add(curr)
            new_path = all_prev + [curr]
            if curr == end:
                if returnWeight:
                    return new_path, sum_weights
                else:
                    return new_path
            for neighbour_arrow in [arrow for arrow in self.arrows if arrow.head == curr]:
                heapq.heappush(priorityQueue, (sum_weights+neighbour_arrow.weight, new_path, neighbour_arrow.tail))
        if returnWeight:
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
                self.cyclesFrom(neighbour, search=search, visited=visited, prefix=prefix+(neighbour,), cycles=cycles)
            visited.remove(node)
        return cycles

    def stronglyConnected(self):
        out = []
        indicies = {}
        for vertex in self.vertices:
            if vertex not in indicies:
                self._strongConnect(vertex, index=0, indicies=indicies, lowLinks={}, S=[], components=out)
        return out

    def _strongConnect(self, v, *, index=0, indicies={}, lowLinks={}, S=[], components=[]):
        indicies[v] = index
        lowLinks[v] = index
        index += 1
        S.append(v)

        for w in self.neighbours(v):
            if w not in indicies:
                self._strongConnect(w, index=index, indicies=indicies, lowLinks=lowLinks, S=S, components=components)
                lowLinks[v] = min(lowLinks[v], lowLinks[w])
            elif w in S:
                lowLinks[v] = min(lowLinks[v], indicies[w])

        if lowLinks[v] == indicies[v]:
            new_component = set()
            while True:
                w = S.pop()
                new_component.add(w)
                if w == v:
                    components.append(new_component)
                    break

    def neighbours(self, vertex):
        return set(arrow.tail for arrow in self.arrows if arrow.head == vertex)

    def indegree(self, vertex):
        return [arrow.tail for arrow in self.arrows].count(vertex)

    def outdegree(self, vertex):
        return [arrow.head for arrow in self.arrows].count(vertex)

    def isBalanced(self):
        return all([self.indegree(vertex) == self.outdegree(vertex) for vertex in self.vertices])

    def isSource(self, vertex):
        return self.indegree(vertex) == 0 and self.outdegree(vertex) != 0

    def isSink(self, vertex):
        return self.outdegree(vertex) == 0 and self.indegree(vertex) != 0

    def isInternal(self, vertex):
        return not self.isSource(vertex) and not self.isSink(vertex)