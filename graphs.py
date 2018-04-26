class DirectedGraph:
	def __init__(self, vertices, arrows):
		self._V = vertices
		self._A = arrows

	@property
	def vertices(self):
	    return self._V

	@vertices.setter
	def vertices(self, values):
		self.arrows = [arrow for arrow in self.arrows if arrow[0] in values and arrow[1] in values]
		self._V = values

	@property
	def arrows(self):
		return self._A

	@arrows.setter
	def arrows(self, values):
		self._A = values

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
		return ''.join([start, end])

	def __repr__(self):
		return '{} with vertices {} and edges {}'.format(self.__class__.__name__, ', '.join(self.vertices), ', '.join(self.arrows))

a = DirectedGraph(['A', 'B', 'C', 'D', 'E'], {'AB':1, 'CD':1, 'AE':1, 'AD':1, 'BA':1, 'BB':2, 'BE':4, 'DC':2, 'EB':2})
a.vertices = ['A', 'B', 'C']
for row in a.adjacencyMatrix:
	print(str(row))
print(a, a.vertices)