import requests

DEFAULT_API_URL = 'http://localhost:5000/tax-calculator/brackets/'
MAX_RETRIES = 5


def fetch_with_retries(full_url, max_retries):
    retries = max_retries
    while retries > 0:
        retries -= 1
        r = requests.get(full_url)

        if r.status_code == 200:
            return r.json()
    raise Exception(
        'Could not get an OK answer within {} retries. Last known response: {}'.format(max_retries, r.json()))


def verify_brackets(results):
    if 'tax_brackets' not in results:
        return False

    sorted_brackets = sorted(results['tax_brackets'], key=lambda x: x['min'])

    if sorted_brackets[0]['min'] != 0:
        return False

    if 'max' in sorted_brackets[-1]:
        return False

    for i in range(len(sorted_brackets)-1):
        if sorted_brackets[i]['max'] != sorted_brackets[i+1]['min']:
            return False
        this_rate = sorted_brackets[i]['rate']
        if type(this_rate) is not float or this_rate < 0:
            return False

    return True


def fetch_brackets(year):
    full_url = '{}/{}'.format(DEFAULT_API_URL, year)
    brackets = fetch_with_retries(full_url, MAX_RETRIES)

    if not verify_brackets(brackets):
        raise Exception(
            'Brackets returned are of unexpected format {}'.format(brackets))

    return brackets['tax_brackets']


def calculate_all(year, income):
    brackets = fetch_brackets(year)

    results = {}
    results['total_tax'] = 0.0
    results['marginal'] = 0.0

    for bracket in brackets:
        bracket['taxable'] = 0.0

        if 'max' not in bracket:
            if income > bracket['min']:
                bracket['taxable'] = income - bracket['min']
        else:
            if income > bracket['max']:
                bracket['taxable'] = bracket['max'] - bracket['min']
            elif income > bracket['min']:
                bracket['taxable'] = income - bracket['min']

        if income >= bracket['min']:
            results['marginal'] = max(bracket['rate'], results['marginal'])

        bracket['tax_amount'] = round(bracket['taxable'] * bracket['rate'], 2)
        results['total_tax'] += bracket['tax_amount']

    results['effective_tax'] = round(results['total_tax'] / income, 2)
    results['total_tax'] = round(results['total_tax'], 2)
    results['brackets'] = brackets

    return results
