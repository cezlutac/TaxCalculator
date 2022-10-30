import unittest
import requests
import sys
sys.path.append('./app')
from tax_calculator import verify_brackets


class TaxBracketTests(unittest.TestCase):
    tax_bracket_api = 'http://localhost:5000/tax-calculator/brackets'

    def test_remote_api_running(self):
        try:
            r = requests.get(self.tax_bracket_api)
        except requests.exceptions.RequestException as e:
            self.fail(
                'Unable to tax bracket API. Is the tax brakcet app running?')
        except Exception as e:
            self.fail('Unexpected error occured: {}'.format(e))

    def test_remote_behaving_well(self):
        year = 2020
        full_url = '{}/{}'.format(self.tax_bracket_api, year)
        max_retries = 5
        retries = max_retries
        gotBrackets = False

        while retries > 0:
            retries -= 1
            r = requests.get(full_url)

            if r.status_code == 200:
                expected_success = {
                    'tax_brackets': [
                        {'max': 48535, 'min': 0, 'rate': 0.15},
                        {'max': 97069, 'min': 48535, 'rate': 0.205},
                        {'max': 150473, 'min': 97069, 'rate': 0.26},
                        {'max': 214368, 'min': 150473, 'rate': 0.29},
                        {'min': 214368, 'rate': 0.33},
                    ]
                }
                self.assertEqual(r.json(), expected_success)
                self.assertEqual(True, verify_brackets(expected_success))
                self.assertEqual(True, verify_brackets(r.json()))
                gotBrackets = True
                break
            elif r.status_code == 500:
                expected_error = {
                    'errors': [{
                        'code': 'INTERNAL_SERVER_ERROR',
                        'field': '',
                        'message': 'Database not found!',
                    }]
                }
                self.assertEqual(r.json(), expected_error)
            else:
                self.fail('Unexpected return: {}'.format(r.json()))

        self.assertEqual(
            True, gotBrackets, 'Could not fetch a response within retry window of {}'.format(max_retries))


class EndpointTests(unittest.TestCase):
    calculator_api = 'http://localhost:4000'

    def test_calculator_api_running(self):
        try:
            r = requests.get(self.calculator_api)
        except requests.exceptions.RequestException as e:
            self.fail(
                'Unable to reach calculator API. Is the calculator app running?')
        except Exception as e:
            self.fail('Unexpected error occured: {}'.format(e))

    def test_calculator_api_not_found(self):
        r = requests.get(self.calculator_api)

        expected_error = '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'

        self.assertEqual(r.json(), expected_error)

    def test_calculator_api_sanity(self):
        full_url = '{}/sanity'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = 'Success'

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_missing_year(self):
        full_url = '{}/calculate?income=0'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = 'Year or income not provided. year: None | income: 0'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_missing_income(self):
        full_url = '{}/calculate?year=0'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = "Year or income not provided. year: 0 | income: None"

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_year_negative(self):
        full_url = '{}/calculate?year=-1&income=0'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = 'Year must be a positive integer. year: -1'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_year_string(self):
        full_url = '{}/calculate?year=onehundred&income=0'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = 'Invalid year entered. Please input a positive integer. year: onehundred'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_year_float(self):
        full_url = '{}/calculate?year=1.1&income=0'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = 'Invalid year entered. Please input a positive integer. year: 1.1'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_income_negative(self):
        full_url = '{}/calculate?year=0&income=-1'.format(self.calculator_api)
        r = requests.get(full_url)

        expected = 'Income must be a positive integer. income: -1.0'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_income_string(self):
        full_url = '{}/calculate?year=0&income=onehundred'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = 'Invalid income entered. Please input a positive float. income: onehundred'

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)

    def test_calculator_api_invalid_type(self):
        full_url = '{}/calculate?year=0&income=0&type=other'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = "Invalid type request: other"

        self.assertEqual(r.status_code, 500)
        self.assertEqual(r.json(), expected)


class FunctionalTests(unittest.TestCase):
    calculator_api = 'http://localhost:4000'

    def test_calculator_default(self):
        full_url = '{}/calculate?year=2020&income=100000'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = {"total_tax": 17991.78}

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), expected)

    def test_calculator_default_with_type(self):
        full_url = '{}/calculate?year=2020&income=100000&type=tax'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = {"total_tax": 17991.78}

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), expected)

    def test_calculator_default_with_type(self):
        full_url = '{}/calculate?year=2020&income=100000&type=all'.format(
            self.calculator_api)
        r = requests.get(full_url)

        expected = {"brackets": [
            {
                "max": 48535,
                "min": 0,
                "rate": 0.15,
                "tax_amount": 7280.25,
                "taxable": 48535
            },
            {
                "max": 97069,
                "min": 48535,
                "rate": 0.205,
                "tax_amount": 9949.47,
                "taxable": 48534
            },
            {
                "max": 150473,
                "min": 97069,
                "rate": 0.26,
                "tax_amount": 762.06,
                "taxable": 2931.0
            },
            {
                "max": 214368,
                "min": 150473,
                "rate": 0.29,
                "tax_amount": 0.0,
                "taxable": 0.0
            },
            {
                "min": 214368,
                "rate": 0.33,
                "tax_amount": 0.0,
                "taxable": 0.0
            }
        ],
            "effective_tax": 0.18,
            "marginal": 0.26,
            "total_tax": 17991.78
        }

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), expected)


if __name__ == '__main__':
    unittest.main()
