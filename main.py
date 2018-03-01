from pca import PCA
from fastmap import FastMap


if __name__ == '__main__':
	# pca
	pca_data = []
	with open('pca-data.txt') as f:
		for line in f:
			if line:
				pca_data.append(list(map(float, line.strip().split("\t"))))
	# print(pca_data)

	reduced = PCA(data=pca_data, dim=2)

	# fast map
	fastmap_data = []
	with open('fastmap-data.txt') as f:
		for line in f:
			if line:
				fastmap_data.append(list(map(int, line.strip().split("\t"))))
	# print(fastmap_data)

	fastmap = FastMap(fastmap_data, 2)
	print(fastmap)

	fastmap_wordlist = []
	with open('fastmap-wordlist.txt') as f:
		for line in f:
			if line:
				fastmap_wordlist.append(line.strip())

	fastmap.plot(fastmap_wordlist)

