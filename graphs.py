class DirectedGraph:

    _splitSign = '-->' 

    def __init__(self, vertices, arrows):
        self._V = vertices
        self._A = arrows

    @property
    def vertices(self):
        return self._V

    @vertices.setter
    def vertices(self, values):
        self._V = values
        temp = {}
        for arrow, val in self.arrows.items():
            head, tail = arrow.split(self._splitSign)
            if head in values and tail in values:
                temp[self._makeArrow(head, tail)] = val
        self._A = temp
        

    @property
    def arrows(self):
        return self._A

    @arrows.setter
    def arrows(self, values):
        temp = {}
        for arrow, val in values.items():
            head, tail = arrow.split(self._splitSign)
            if head in self.vertices and tail in self.vertices:
                temp[self._makeArrow(head, tail)] = val
        self._A = temp

    @property
    def size(self):
        return len(self.vertices)

    @property
    def adjacencyMatrix(self):
        mat = [[0] * self.size for _ in range(self.size)]
        for idx, vertex in enumerate(self.vertices):
            for j, other in enumerate(self.vertices):
                if self.arrowFromTo(vertex, other):
                    mat[idx][j] = 1
        return mat

    def pathFromTo(self, start, end):
        # Djikstra maybe?
        pass

    def arrowFromTo(self, start, end):
        return self._makeArrow(start, end) in self.arrows

    def isBalanced(self):
        return all([self.indegree(vertex) == self.outdegree(vertex) for vertex in self.vertices])

    def indegree(self, vertex):            
        return [end for start, *split, end in self.arrows].count(vertex)

    def outdegree(self, vertex):
        return [start for start, *split, end in self.arrows].count(vertex)

    def isSource(self, vertex):
        return self.indegree(vertex) == 0 and self.outdegree(vertex) != 0

    def isSink(self, vertex):
        return self.outdegree(vertex) == 0 and self.indegree(vertex) != 0

    def isInternal(self, vertex):
        return not self.isSource(vertex) and not self.isSink(vertex)

    def _makeArrow(self, start, end):
        return self._splitSign.join([start, end])

    def __repr__(self):
        return '{} with vertices {} and arrows {}.'.format(self.__class__.__name__, ', '.join(self.vertices), ', '.join('{} with weight {}'.format(arrow, val) for arrow, val in self.arrows.items()))


a = DirectedGraph(['A', 'B', 'C', 'D', 'E'], {'A-->B': 1, 'B-->A': 2, 'C-->A': 5})
a.vertices = ['A', 'B', 'C']
print(a, a.isBalanced())