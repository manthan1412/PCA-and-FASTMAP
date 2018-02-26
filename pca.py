import numpy as np
import numpy.linalg as linalg

class PCA(object):


    def __init__(self, data=[], dim=2):
        
        if len(data) == 0:
            raise ValueError('No data or data with length zero given')
            raise Exception('This is the exception you expect to handle')


        self.__load_data(data)
        # self.__data = np.array(data)
        # print(self.__data)
        self.__N = len(self.__data)
        # print(self.__N)
        if self.__dim < dim:
            raise ValueError('Dimension to reduced can not be greater the current dimension')
            raise Exception('This is the exception you expect to handle')

        self.__to_dim = dim
        # print(self.__to_dim)
        self.__compute_mu()
        # print(self.__mu)
        # print(self.__data)
        self.__normalize()
        # print(self.__data)
        self.__compute_covarince()

        self.__compute_eigens()
        # print(self.__eigenVectors)
        # print(self.__eigenValues)

        self.__reduce()


    def __load_data(self, data):
        N = len(data)
        self.__data = []
        dim = len(data[0])
        self.__dim = dim
        # print(dim)
        for i in range(0, N):

            if dim == len(data[i]):
                self.__data.append(np.array(data[i]).reshape(dim, 1))
            else:
                raise ValueError('Check dimensions of data')
                raise Exception('This is the exception you expect to handle')
            
        self.__data = np.array(self.__data)

    def __compute_mu(self):

        N = self.__N
        mu = [0.0 for _ in range(0, self.__dim)]
        for i in range(0, N):
            for j in range(0, self.__dim):
                mu[j] += self.__data[i][j]
        self.__mu = np.array(mu) / N

    def __normalize(self):
        N = self.__N
        # for i in range(0, N):
        self.__data -= self.__mu

    def __compute_covarince(self):

        N = self.__N
        dim = self.__dim
        self.__covarince = [[0.0 for _ in range(0, dim)] for _ in range(0, dim)]
        for i in range(0, N):
            self.__covarince += self.__data[i].dot(self.__data[i].T)
        # print(self.__covarince)
        self.__covarince /= N
        # print(self.__covarince)

    def __compute_eigens(self):

        eigenValues, eigenVectors = linalg.eig(self.__covarince)
        # print(eigenVectors)
        # print(eigenValues)
        index = eigenValues.argsort()[::-1]   
        self.__eigenValues = eigenValues[index]
        self.__eigenVectors = eigenVectors[:,index]

    def __reduce(self):

        truncated = self.__eigenVectors[:, :self.__to_dim]
        # print(truncated)
        self.__reduced = []
        N = self.__N
        for i in range(0, N):
            self.__reduced.append(truncated.T.dot(self.__data[i]))
        self.__reduced = np.array(self.__reduced)
        # print(self.__reduced)

    def __repr__(self):
        return repr(self.__reduced.tolist())
