from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/convert', methods=['GET'])
def convert_currency():

    euro_amount = request.args.get('euro')
    type_of_currency = request.args.get('type_of_currency')

    if not type_of_currency :
        return jsonify({'error': 'Parameter Type of Currency is required'}), 400

    # Validation
    if not euro_amount:
        return jsonify({'error': 'Parameter euro is required'}), 400
    if not type_of_currency:
        return jsonify({'error': 'Parameter type_of_currency is required'}), 400

    try:
        euro_amount = float(euro_amount)
    except ValueError:
        return jsonify({'error': 'Invalid euro amount'}), 400

    conversion_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur/{type_of_currency}.json"

    # Get Request to 3rd Party Url to get crreny rates
    try:
        response = requests.get(conversion_url)
        response.raise_for_status()
        conversion_data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch conversion data'}), 500
    except ValueError:
        return jsonify({'error': 'Invalid conversion data'}), 500

    conversion_rate = conversion_data.get(type_of_currency)

    if not conversion_rate:
        return jsonify({'error': f'Conversion rate for {type_of_currency} not found'}), 400

    #Convert
    converted_amount = euro_amount * conversion_rate

    response_data = {
        'date': conversion_data.get('date'),
        'euro_amount': euro_amount,
        f'{type_of_currency}_amount': converted_amount
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run()
