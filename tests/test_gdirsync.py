import unittest


class GdirsyncTest(unittest.TestCase):
    """Unittests for gdirsync"""

    def test_sample(self):
        """sample test"""
        a = 5
        self.assertEqual(a, 5)


if __name__ == "__main__":
    unittest.main()
