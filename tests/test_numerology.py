import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from numerology_pyqt import NumerologyModel


class NumerologyModelTests(unittest.TestCase):
    def test_find_sum_and_term_sum(self):
        model = NumerologyModel()
        self.assertEqual(model.find_sum("Manian"), 17)
        self.assertEqual(model.find_term_sum(17), 8)

    def test_matching_name_search(self):
        model = NumerologyModel()
        names = model.generate_names(prefix="", max_length=1, desired_sum=3)
        self.assertEqual(names, ["c", "g", "l", "s"])


if __name__ == "__main__":
    unittest.main()
