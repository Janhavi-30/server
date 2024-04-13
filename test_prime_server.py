import unittest
from unittest.mock import patch
from script import generate_primes_range

class TestPrimeGenerator(unittest.TestCase):
    def test_generate_primes_naive(self):
        result = generate_primes_range(1, 10, 'naive')
        self.assertEqual(result, [2, 3, 5, 7])

    def test_generate_primes_sieve(self):
        result = generate_primes_range(1, 10, 'sieve')
        self.assertEqual(result, [2, 3, 5, 7])

    def test_generate_primes_invalid_strategy(self):
        with self.assertRaises(ValueError):
            generate_primes_range(1, 10, 'invalid')

if __name__ == '__main__':
    unittest.main()
