import unittest

from valuation_service import currency_all_same, compute_result


class ValuationServiceTestCase(unittest.TestCase):
    def test_currency_all_same(self):
        self.assertTrue(currency_all_same([
            (1, 2, 'EU', 4),
            (2, 4, 'EU', 1)
        ], 'EU'))
        self.assertFalse(currency_all_same([
            (1, 2, 'EU', 4),
            (2, 4, 'PLN', 1)
        ], 'EU'))
        self.assertFalse(currency_all_same([
            (1, 2, 'PLN', 4),
            (2, 4, 'PLN', 1)
        ], 'EU'))

    def test_compute_result(self):
        data = {
            1: [(1, 1, 'EU', 1),
                (2, 1, 'PLN', 2)],
            2: [(3, 2, 'GBP', 1)],
            3: [(4, 1, 'EU', 2),
                (5, 1, 'EU', 2),
                (6, 2, 'GBP', 2),
                (7, 2, 'PLN', 2)],
            4: [(8, 1, 'GBP', 1),
                (9, 1, 'GBP', 1)]
        }
        currencies = {
            'EU': 4.3,
            'GBP': 5.4,
            'PLN': 1
        }
        matchings = {
            1: 1,
            2: 1,
            3: 3,
            4: 2
        }
        self.assertEqual(compute_result(data, currencies, matchings),
                         {1: {'avg_price': 1.0,
                              'currency': 'EU',
                              'ignored_products_count': 1,
                              'matching_id': 1,
                              'total_price': 1},
                          2: {'avg_price': 2.0,
                              'currency': 'GBP',
                              'ignored_products_count': 0,
                              'matching_id': 2,
                              'total_price': 2},
                          3: {'avg_price': 1.33,
                              'currency': 'PLN',
                              'ignored_products_count': 1,
                              'matching_id': 3,
                              'total_price': 8},
                          4: {'avg_price': 1.0,
                              'currency': 'GBP',
                              'ignored_products_count': 0,
                              'matching_id': 4,
                              'total_price': 2}})


if __name__ == '__main__':
    unittest.main()
