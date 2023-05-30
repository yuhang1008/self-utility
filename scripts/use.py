import numpy as np

A = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
B = np.array([[-1, -1, 1], [1, -1, 1], [-1, 1, 1]])

R = np.dot(A, np.linalg.inv(B))

print(R)