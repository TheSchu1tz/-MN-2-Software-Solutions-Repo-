import numpy as np
points = np.loadtxt('test/pecan1212.txt')
centers = np.array([[25, 70], [55, 25], [56, 36], [80, 68]])
files=[
    'test/pecan1212_1_SOLUTION_420.txt',
    'test/pecan1212_2_SOLUTION_325.txt',
    'test/pecan1212_3_SOLUTION_330.txt',
    'test/pecan1212_4_SOLUTION_630.txt',
]

cluster_sse=[]
for k,f in enumerate(files):
    idxs = np.loadtxt(f, dtype=int) - 1    # convert from 1-based to 0-based indices
    pts = points[idxs]
    dif = pts - centers[k]
    cluster_sse.append(np.sum(np.sum(dif**2, axis=1)))

print("Cluster SSE:", cluster_sse)
print("TOTAL SSE:", sum(cluster_sse))