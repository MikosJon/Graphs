from collections import namedtuple
import heapq

Arrow = namedtuple('Arrow', 'head tail weight')

class DirectedGraph:
    def __init__(self, *, vertices=[], arrows=[]):
        self._V = set(vertices)
        self._A = set(Arrow(*arrow) for arrow in arrows)

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
        self._A = set(arrow for arrow in self.arrows if arrow.head in self.vertices and arrow.tail in self.vertices)

    @property
    def size(self):
        return len(self.vertices)

    @property
    def adjacencyMatrix(self):
        mat = [[0] * self.size for _ in range(self.size)]
        for i, vertex in enumerate(self.vertices):
            for j, other in enumerate(self.vertices):
                if self.arrowFromTo(vertex, other):
                    mat[i][j] = 1
        return mat

    def pathFromTo(self, start, end):
        priorityQueue = []
        heapq.heappush(priorityQueue, (0, [], start))
        visited = set()
        while priorityQueue:
            sum_weights, all_prev, curr = heapq.heappop(priorityQueue)
            if curr in visited:
                continue
            new_path = all_prev + [curr]
            visited.add(curr)
            if curr == end:
                return new_path, sum_weights
            for neighbour_arrow in [arrow for arrow in self.arrows if arrow.head == curr]:
                heapq.heappush(priorityQueue, (sum_weights+neighbour_arrow.weight, new_path, neighbour_arrow.tail))
        return None, None
    
    def neighbours(self, vertex):
        return set(arrow.tail for arrow in self.arrows if arrow.head == vertex)

    def isArrowFromTo(self, start, end):
        return any([start == arrow.head and end == arrow.tail for arrow in self.arrows])

    def isBalanced(self):
        return all([self.indegree(vertex) == self.outdegree(vertex) for vertex in self.vertices])

    def indegree(self, vertex):            
        return [arrow.tail for arrow in self.arrows].count(vertex)

    def outdegree(self, vertex):
        return [arrow.head for arrow in self.arrows].count(vertex)

    def isSource(self, vertex):
        return self.indegree(vertex) == 0 and self.outdegree(vertex) != 0

    def isSink(self, vertex):
        return self.outdegree(vertex) == 0 and self.indegree(vertex) != 0

    def isInternal(self, vertex):
        return not self.isSource(vertex) and not self.isSink(vertex)

    def __repr__(self):
        return '{}(vertices={}, edges={})'.format(self.__class__.__name__,
                                                  '{' + ', '.join("'{}'".format(vertex) for vertex in self.vertices) + '}',
                                                  '{' + ', '.join("('{}', '{}', {})".format(*arrow) for arrow in self.arrows) + '}')


a = DirectedGraph(vertices=['A', 'B', 'C', 'D', 'E'], arrows=[('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 5), ('C', 'B', 1), ('B', 'A', 2), ('A', 'D', 1), ('D', 'E', 4), ('E', 'A', 2)])
print(a)
print(a.pathFromTo('B', 'E'))