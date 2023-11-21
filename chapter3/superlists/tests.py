import unittest


class SmokeTest(unittest.TestCase):
    """Тест на токсичность"""
    def test_bad_math(self):
        self.assertEqual(1 + 1, 3)
