import numpy as np
import freud
import unittest
import util


class TestInterface(unittest.TestCase):
    def test_take_one(self):
        """Test that there is exactly 1 or 12 particles at the interface when
        one particle is removed from an FCC structure"""
        np.random.seed(0)
        (box, positions) = util.make_fcc(4, 4, 4, noise=1e-2)
        positions.flags['WRITEABLE'] = False

        index = np.random.randint(0, len(positions))

        point = positions[index].reshape((1, 3))
        others = np.concatenate([positions[:index], positions[index + 1:]])

        inter = freud.interface.InterfaceMeasure(1.5)

        # Test attribute access
        with self.assertRaises(AttributeError):
            inter.ref_point_count
        with self.assertRaises(AttributeError):
            inter.ref_point_ids
        with self.assertRaises(AttributeError):
            inter.point_count
        with self.assertRaises(AttributeError):
            inter.point_ids

        test_one = inter.compute(box, point, others)

        # Test attribute access
        inter.ref_point_count
        inter.ref_point_ids
        inter.point_count
        inter.point_ids

        self.assertEqual(test_one.ref_point_count, 1)
        self.assertEqual(len(test_one.ref_point_ids), 1)

        test_twelve = inter.compute(box, others, point)
        self.assertEqual(test_twelve.ref_point_count, 12)
        self.assertEqual(len(test_twelve.ref_point_ids), 12)

    def test_filter_r(self):
        """Test that nlists are filtered to the correct rmax."""
        np.random.seed(0)
        (box, positions) = util.make_fcc(4, 4, 4, noise=1e-2)

        index = np.random.randint(0, len(positions))

        point = positions[index].reshape((1, 3))
        others = np.concatenate([positions[:index], positions[index + 1:]])

        # Creates a neighborlist with rmax larger than the interface rmax
        lc = freud.locality.LinkCell(box, 3.0).compute(box, others, point)

        inter = freud.interface.InterfaceMeasure(1.5)

        test_twelve = inter.compute(box, others, point, lc.nlist)
        self.assertEqual(test_twelve.ref_point_count, 12)
        self.assertEqual(len(test_twelve.ref_point_ids), 12)

    def test_repr(self):
        inter = freud.interface.InterfaceMeasure(1.5)
        self.assertEqual(str(inter), str(eval(repr(inter))))


if __name__ == '__main__':
    unittest.main()
