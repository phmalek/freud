import numpy as np
from freud import locality, box
from benchmark import benchmark


class benchmark_locality_AABBQuery(benchmark):
    def __init__(self, L, rcut):
        self.L = L
        self.rcut = rcut

    def setup(self, N):
        self.fbox = box.Box.cube(self.L)
        seed = 0
        np.random.seed(seed)
        self.points = np.random.uniform(-self.L/2, self.L/2, (N, 3))

    def run(self, N):
        self.aq = locality.AABBQuery()
        self.aq.compute(self.fbox, self.rcut, self.points, self.points,
                        exclude_ii=True)


if __name__ == '__main__':
    print('freud.locality.AABBQuery')
    b = benchmark_locality_AABBQuery(L=10, rcut=0.5)
    b.run_size_scaling_benchmark([1000, 10000, 100000], number=100)
    b.run_thread_scaling_benchmark([1000, 10000, 100000], number=100)
    b = benchmark_locality_AABBQuery(L=10, rcut=1.0)
    b.run_size_scaling_benchmark([1000, 10000, 100000], number=100)
    b.run_thread_scaling_benchmark([1000, 10000, 100000], number=100)
    print('\n ----------------')
