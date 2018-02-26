import pca
import fastmap


if __name__ == '__main__':
	# pca
	pca_data = []
	with open('pca-data.txt') as f:
		for line in f:
			if line:
				pca_data.append(list(map(float, line.strip().split("\t"))))
	# print(pca_data)

	reduced = pca.PCA(data=pca_data, dim=2)
	print(reduced)


	# fast map
