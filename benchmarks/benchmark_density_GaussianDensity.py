import numpy as np
import freud
from benchmark import Benchmark
from benchmarker import run_benchmarks


class BenchmarkDensityGaussianDensity(Benchmark):
    def __init__(self, width, rcut, sigma):
        self.width = width
        self.rcut = rcut
        self.sigma = sigma

    def bench_setup(self, N):
        self.box_size = self.rcut*3.1
        self.box = freud.box.Box.square(self.box_size)
        np.random.seed(0)
        self.points = np.random.random_sample((N, 3)).astype(np.float32) \
            * self.box_size - self.box_size/2
        self.points[:, 2] = 0
        self.gd = freud.density.GaussianDensity(self.width, self.rcut,
                                                self.sigma)

    def bench_run(self, N):
        self.gd.compute(self.box, self.points)


def run():
    Ns = [1000, 10000]
    width = 100
    rcut = 10
    sigma = 0.1
    name = 'freud.density.GaussianDensity'
    classobj = BenchmarkDensityGaussianDensity
    number = 100

    return run_benchmarks(name, Ns, number, classobj,
                          width=width, rcut=rcut, sigma=sigma)


if __name__ == '__main__':
    run()
