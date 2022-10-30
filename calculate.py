import requests
import argparse
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(
        description = 'simple command line script to request results from the api'
    )
    parser.add_argument('-year', help='year', required=True)
    parser.add_argument('-income', help='income', required=True)
    parser.add_argument('-type', help='type: either tax or all', required=False, default='tax')

    args = parser.parse_args()

    full_url = 'http://localhost:4000/calculate?year={}&income={}&type={}'.format(args.year,args.income,args.type)
    r = requests.get(full_url)

    pprint(r.json())

if __name__ == '__main__':
    main()