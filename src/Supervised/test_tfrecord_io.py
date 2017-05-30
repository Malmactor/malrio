"""Unittest suit cases for TFRecord IO
"""

__author__ = "Liyan Chen"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

import unittest

import numpy as np


class TestTFRecordIO(unittest.TestCase):
    def test_IO(self):
        batch = np.random.rand(32, 60, 60, 4)

        # Write numpy batch into TFRecord

        # Read it out from TFRecord again

        # Compare them
        self.assertTrue(np.allclose(batch, batch))


if __name__ == "__main__":
    unittest.main()
