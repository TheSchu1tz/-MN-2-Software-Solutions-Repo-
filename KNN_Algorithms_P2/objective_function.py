import numpy as np
points = np.loadtxt('test/Almond9832.txt')
centers = np.array([[50, 116], [50, -117], [51, -4]])
files=[
    'test/Almond9832_1_SOLUTION_2951.txt',
    'test/Almond9832_2_SOLUTION_2581.txt',
    'test/Almond9832_3_SOLUTION_2803.txt'
]

cluster_sse=[]
for k,f in enumerate(files):
    idxs = np.loadtxt(f, dtype=int) - 1    # convert from 1-based to 0-based indices
    pts = points[idxs]
    dif = pts - centers[k]
    cluster_sse.append(np.sum(np.sum(dif**2, axis=1)))

print("Cluster SSE:", cluster_sse)
print("TOTAL SSE:", sum(cluster_sse))
