class DirectedGraph:

	splitSign = '-->' 

	def __init__(self, vertices, arrows):
		self._V = vertices
		self._A = arrows

	@property
	def vertices(self):
	    return self._V

	@vertices.setter
	def vertices(self, values):
		temp = {}
		for arrow, val in self.arrows.items():
			head, tail = arrow.split(self.splitSign)
			if head in values and tail in values:
				temp[self._makeEdge(head, tail)] = val
		self._A = temp
		self._V = values

	@property
	def arrows(self):
		return self._A

	@arrows.setter
	def arrows(self, values):
		temp = {}
		for arrow, val in self.arrows.items():
			head, tail = arrow.split(self.splitSign)
			if head in self.vertices and tail in self.vertices:
				temp[self._makeEdge(head, tail)] = val
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

	def arrowFromTo(self, start, end):
		return self._makeEdge(start, end) in self.arrows

	def _makeEdge(self, start, end):
		return self.splitSign.join([start, end])

	def __repr__(self):
		return '{} with vertices {} and arrows {}'.format(self.__class__.__name__, ', '.join(self.vertices), ', '.join(self.arrows))

a = DirectedGraph(['A', 'B', 'C', 'D', 'E'], {'A-->B':1, 'C-->D':1, 'A-->E':1, 'A-->D':1, 'B-->A':1, 'B-->B':2, 'B-->E':4, 'D-->C':2, 'E-->B':2})
a.vertices = ['A', 'B', 'C']
a.arrows = {'A-->D':3, 'A-->A':10, 'B-->C':4, 'A-->B': 1}
for row in a.adjacencyMatrix:
	print(str(row))
print(a)
print(a.vertices, a.arrows)