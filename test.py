import unittest

from main import data_exists


class TestNycCabData(unittest.TestCase):

    def test_get_new_data(self):
        pass

    def test_data_exists(self):
        self.assertTrue(data_exists(2021, 1))
        self.assertFalse(data_exists(2020, 1))

    def test_get_data(self):
        pass

    def test_average_trip_length(self):
        pass

    def test_rolling_average(self):
        pass
