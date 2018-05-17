from collections import namedtuple

Arrow = namedtuple('Arrow', 'head tail weight')

class DirectedGraph:
    def __init__(self, vertices, arrows):
        self._V = vertices
        self._A = set(arrows)

    @property
    def vertices(self):
        return self._V

    @vertices.setter
    def vertices(self, values):
        self._V = values
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
        priorityQueue = [([], start, 0)]
        while priorityQueue:
            priorityQueue.sort(key=lambda x: -x[2])
            all_prev, curr, sum_weights = priorityQueue.pop()
            if curr == end:
                return (all_prev + [end], sum_weights)
            for neighbour in [arrow for arrow in self.arrows if arrow.head == curr and arrow.tail not in all_prev]:
                priorityQueue.append((all_prev+[curr], neighbour.tail, sum_weights+neighbour.weight))
            


    def arrowFromTo(self, start, end):
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
        return '{} with vertices {} and arrows {}.'.format(self.__class__.__name__, ', '.join(self.vertices), ', '.join('{}-->{} with weight {}'.format(*arrow) for arrow in self.arrows))


a = DirectedGraph(['A', 'B', 'C', 'D', 'E'], set([Arrow('A', 'B', 4), Arrow('A', 'C', 2), Arrow('B', 'C', 5), Arrow('C', 'B', 1), Arrow('B', 'A', 2), Arrow('A', 'D', 1), Arrow('D', 'E', 4), Arrow('E', 'A', 2)]))
print(a.pathFromTo('B', 'E'))
