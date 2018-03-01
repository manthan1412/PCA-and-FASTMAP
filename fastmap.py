import numpy as np
from math import sqrt
import pylab

class FastMap(object):

	def __init__(self, data=[], dim=2):

		if not data or len(data) == 0:
			raise ValueError('No data or data with length zero given')
			# raise Exception('This is the exception you expect to handle')

		if dim < 1:
			raise ValueError('Dimension can not be zero or negative')

		self.__data = data
		self.__preprocess()
		# print(self.__distance)
		# print(self.__s_distance)
		self.__N = len(self.__distance)
		# print(self.__N)
		self.__dim = dim
		self.__fastmap()


	def __preprocess(self):
		self.__distance = {}
		self.__s_distance = {}
		for d in self.__data:
			if d[0] not in self.__distance:
				self.__distance[d[0]] = {d[0] : 0}
				self.__s_distance[d[0]] = {d[0] : 0}
			if d[1] not in self.__distance:
				self.__distance[d[1]] = {d[1]: 0}
				self.__s_distance[d[1]] = {d[1]: 0}
			self.__distance[d[0]][d[1]] = d[2]
			self.__s_distance[d[0]][d[1]] = d[2]*d[2]
			self.__distance[d[1]][d[0]] = d[2]
			self.__s_distance[d[1]][d[0]] = self.__s_distance[d[0]][d[1]]


	def __furthest(self, point):
		max_dist = -1
		furthest_pt = -1
		distances = self.__distance[point]
		for pt in distances.keys():
			if (max_dist < distances[pt]) or (max_dist == distances[pt] and furthest_pt > pt):
				max_dist = distances[pt]
				furthest_pt = pt
		return furthest_pt

	def __get_furthest_pair(self):
		p1 = np.random.randint(0, self.__N)+1
		p2 = self.__furthest(p1)
		p3 = self.__furthest(p2)

		# print(p1, p2, p3)
		if p3 == p1:
			return p2, p3
		p1 = p3
		while True:
			p2 = self.__furthest(p1)
			p3 = self.__furthest(p2)
			if p1 == p3:
				break
			# print(p1, p2, p3)

		return p2, p3

	def __project(self, a, b, dim):
		dab = self.__distance[a][b]
		sq_dab = self.__s_distance[a][b]

		for i in self.__distance.keys():
			# print(self.__s_distance[i])
			sq_dia = self.__s_distance[i][a]
			sq_dib = self.__s_distance[i][b]

			self.__mapped[i][dim] = (sq_dia + sq_dab - sq_dib) / (2*dab)

	def __distance_updated(self, a, b):
		if (a,b) in self.__updated or (b,a) in self.__updated:
			return True
		return False


	def __update_distance(self, dim):
		self.__updated = {}
		for point in self.__distance.keys():
			for neighbour in self.__distance[point].keys():
				if not self.__distance_updated(point, neighbour):
					try:
						self.__s_distance[point][neighbour] -= (self.__mapped[point][dim] - self.__mapped[neighbour][dim])**2
						self.__s_distance[neighbour][point] = self.__s_distance[point][neighbour]

						self.__updated[(point, neighbour)] = True
						self.__distance[point][neighbour] = sqrt(self.__s_distance[point][neighbour])
						self.__distance[neighbour][point] = self.__distance[point][neighbour]
					except Exception as e:
						print("Some error occured: ", point, neighbour)


	def __fastmap(self):

		self.__mapped = [[0.0 for _ in range(0, self.__dim)] for _ in range(0, self.__N + 1)]
		self.__pivots = [[0 for _ in range(0, 2)] for _ in range(0, self.__dim)]

		for dimension in range(0, self.__dim):
			a, b = self.__get_furthest_pair()
			if a > b:
				a, b = b, a

			print(a, b)
			print(self.__distance[a][b])

			if self.__distance[a][b] == 0:
				print(self.__mapped)
				return
		
			self.__project(a, b, dimension)
			# print(self.__mapped)
			self.__update_distance(dimension)
			# print(self.__distance)
			# print(self.__s_distance)
		self.__mapped = self.__mapped[1:]

	def __repr__(self):
		return repr(self.__mapped)

	def plot(self, strings=None):

		if not strings:
			raise ValueError('No string is provided')

		if len(strings) != len(self.__mapped):
			raise ValueError('String length and data length is not matched')

		pylab.scatter([x[0] for x in self.__mapped], [x[1] for x in self.__mapped], c="r")
		for i,s in enumerate(strings):
			pylab.annotate(s,self.__mapped[i])
		pylab.show()
