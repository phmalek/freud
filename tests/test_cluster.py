import numpy as np
import freud
import unittest
import util


class TestCluster(unittest.TestCase):
    def test_cluster_props(self):
        Nlattice = 4
        Nrep = 5

        np.random.seed(0)
        positions = []
        for _ in range(Nrep):
            (box, pos) = util.make_fcc(Nlattice, Nlattice, Nlattice,
                                       noise=1e-2)
            positions.append(pos)

        # number of grid points (N = Nrep*Ngrid)
        Ngrid = positions[-1].shape[0]
        positions = np.array(positions).reshape((-1, 3))

        # Test box access
        clust = freud.cluster.Cluster(box, 0.5)
        self.assertEqual(clust.box, box)

        # Test protected attribute access
        with self.assertRaises(AttributeError):
            clust.num_clusters
        with self.assertRaises(AttributeError):
            clust.num_particles
        with self.assertRaises(AttributeError):
            clust.cluster_idx

        # Test with explicit box provided
        clust.computeClusters(positions, box=box)

        # Test if attributes are accessible now
        clust.num_clusters
        clust.num_particles
        clust.cluster_idx

        # Test all property APIs
        props = freud.cluster.ClusterProperties(box)

        # Test protected attribute access
        with self.assertRaises(AttributeError):
            props.num_clusters
        with self.assertRaises(AttributeError):
            props.cluster_COM
        with self.assertRaises(AttributeError):
            props.cluster_G
        with self.assertRaises(AttributeError):
            props.cluster_sizes

        props.computeProperties(positions, clust.cluster_idx, box=box)

        # Test if attributes are accessible now
        props.num_clusters
        props.cluster_COM
        props.cluster_G
        props.cluster_sizes

        self.assertEqual(props.num_clusters, Ngrid)
        self.assertTrue(np.all(props.cluster_sizes == Nrep))

        # Test without explicit box provided
        clust.computeClusters(positions)

        props = freud.cluster.ClusterProperties(box)
        props.computeProperties(positions, clust.cluster_idx, box=box)
        self.assertEqual(props.num_clusters, Ngrid)
        self.assertTrue(np.all(props.cluster_sizes == Nrep))

    def test_cluster_props_advanced(self):
        """Test radius of gyration and COM calculations"""
        box = freud.box.Box.square(L=5)
        positions = np.array([[0, -2, 0],
                              [0, -2, 0],
                              [0, 2, 0],
                              [-0.1, 1.9, 0]])
        clust = freud.cluster.Cluster(box, 0.5)
        clust.computeClusters(positions, box=box)

        props = freud.cluster.ClusterProperties(box)
        props.computeProperties(positions, clust.cluster_idx, box=box)

        com_1 = np.array([[0, -2, 0]])
        com_2 = np.array([[-0.05, 1.95, 0]])
        g_tensor_2 = np.array([[0.0025, 0.0025, 0],
                               [0.0025, 0.0025, 0],
                               [0, 0, 0]])
        self.assertTrue(np.all(props.cluster_COM[0, :] == com_1))
        self.assertTrue(np.allclose(props.cluster_COM[1, :], com_2))
        self.assertTrue(np.all(props.cluster_G[0] == 0))
        self.assertTrue(np.allclose(props.cluster_G[1], g_tensor_2))

    def test_cluster_keys(self):
        Nlattice = 4
        Nrep = 5

        np.random.seed(0)
        positions = []
        for _ in range(Nrep):
            (box, pos) = util.make_fcc(Nlattice, Nlattice, Nlattice,
                                       noise=1e-2)
            positions.append(pos)

        # number of grid points (N = Nrep*Ngrid)
        Ngrid = positions[-1].shape[0]
        positions = np.array(positions).reshape((-1, 3))

        clust = freud.cluster.Cluster(box, 0.5)
        clust.computeClusters(positions, box=box)

        # Test protected attribute access
        with self.assertRaises(AttributeError):
            clust.cluster_keys

        clust.computeClusterMembership(np.array(range(Nrep*Ngrid)))

        # Test if attributes are accessible now
        clust.cluster_keys

        self.assertEqual(len(clust.cluster_keys), Ngrid)

        ckeys = np.array(clust.cluster_keys) % Ngrid
        check_values = np.arange(Ngrid)[:, np.newaxis].repeat(Nrep, axis=1)

        self.assertTrue(np.all(ckeys == check_values))

    def test_repr(self):
        box = freud.box.Box(Lx=2, Ly=2, Lz=2, xy=1, xz=0, yz=1)
        clust = freud.cluster.Cluster(box, 0.5)
        self.assertEqual(str(clust), str(eval(repr(clust))))
        props = freud.cluster.ClusterProperties(box)
        self.assertEqual(str(props), str(eval(repr(props))))

    def test_repr_png(self):
        box = freud.box.Box.square(L=5)
        positions = np.array([[0, -2, 0],
                              [0, -2, 0],
                              [0, 2, 0],
                              [-0.1, 1.9, 0]])
        clust = freud.cluster.Cluster(box, 0.5)

        with self.assertRaises(AttributeError):
            clust.plot()
        self.assertEqual(clust._repr_png_(), None)

        clust.computeClusters(positions, box=box)
        clust._repr_png_()


if __name__ == '__main__':
    unittest.main()
