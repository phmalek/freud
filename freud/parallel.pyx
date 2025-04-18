# Copyright (c) 2010-2019 The Regents of the University of Michigan
# This file is from the freud project, released under the BSD 3-Clause License.

R"""
The :class:`freud.parallel` module controls the parallelization behavior of
freud, determining how many threads the TBB-enabled parts of freud will use.
freud uses all available threads for parallelization unless directed otherwise.
"""

cimport freud._parallel

_numThreads = 0


def getNumThreads():
    R"""Get the number of threads for parallel computation.

    .. moduleauthor:: Bradley Dice <bdice@bradleydice.com>

    Returns:
        int: Number of threads.
    """
    global _numThreads
    return _numThreads


def setNumThreads(nthreads=None):
    R"""Set the number of threads for parallel computation.

    .. moduleauthor:: Joshua Anderson <joaander@umich.edu>

    Args:
        nthreads(int, optional):
            Number of threads to use. If None (default), use all threads
            available.
    """
    global _numThreads
    if nthreads is None or nthreads < 0:
        nthreads = 0

    _numThreads = nthreads

    cdef unsigned int cNthreads = nthreads
    freud._parallel.setNumThreads(cNthreads)


class NumThreads:
    R"""Context manager for managing the number of threads to use.

    .. moduleauthor:: Joshua Anderson <joaander@umich.edu>

    Args:
        N (int, optional): Number of threads to use in this context. Defaults
            to None, which will use all available threads.
    """

    def __init__(self, N=None):
        global _numThreads
        self.restore_N = _numThreads
        self.N = N

    def __enter__(self):
        setNumThreads(self.N)
        return self

    def __exit__(self, *args):
        setNumThreads(self.restore_N)


# Override TBB's default autoselection. This is necessary because once the
# automatic selection runs, the user cannot change it.
setNumThreads(0)
