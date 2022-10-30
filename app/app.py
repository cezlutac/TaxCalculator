from flask import Flask, jsonify, request
from flask_cors import CORS
from tax_calculator import calculate_all

app = Flask(__name__)
CORS(app)

app = Flask(__name__)


@app.errorhandler(404)
def not_found_handler(e):
    return jsonify(str(e)), 404


@app.errorhandler(Exception)
def exception_handler(e):
    return jsonify(str(e)), 500


@app.route('/sanity')
def sanity_test():
    return jsonify('Success')


@app.route('/calculate', methods=['GET'])
def calculate():
    year = request.args.get('year')
    income = request.args.get('income')
    type = request.args.get('type') if request.args.get(
        'type') is not None else 'tax'

    if not year or not income:
        raise Exception(
            'Year or income not provided. year: {} | income: {}'.format(year, income))

    if not(type == 'all' or type == 'tax'):
        raise Exception('Invalid type request: {}'.format(type))

    try:
        year = int(year)
    except ValueError:
        raise Exception(
            'Invalid year entered. Please input a positive integer. year: {}'.format(year))

    if year < 0:
        raise Exception(
            'Year must be a positive integer. year: {}'.format(year))

    try:
        income = float(income)
    except ValueError:
        raise Exception(
            'Invalid income entered. Please input a positive float. income: {}'.format(income))

    if income < 0:
        raise Exception(
            'Income must be a positive integer. income: {}'.format(income))

    all_results = calculate_all(year=year, income=income)

    if type == 'all':
        return jsonify(all_results)
    elif type == 'tax':
        return jsonify({'total_tax': all_results['total_tax']})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
