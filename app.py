"""AMPHIBIA web UI: reuses the unchanged console simulator's evaluate() function."""
from datetime import datetime
from math import isfinite
from secrets import token_hex
from zoneinfo import ZoneInfo
from flask import Flask, jsonify, render_template, request, session
from amphibia_demo import evaluate

app = Flask(__name__)
app.secret_key = __import__('os').environ.get('AMPHIBIA_SECRET_KEY', token_hex(32))


def parse_value(data, key, low, high):
    value = data.get(key)
    if isinstance(value, bool) or value is None:
        raise ValueError(f'{key}: enter a number between {low} and {high}.')
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f'{key}: enter a valid number.') from None
    if not isfinite(number) or not low <= number <= high:
        raise ValueError(f'{key}: enter a number between {low} and {high}.')
    return number


@app.get('/')
def home():
    return render_template('index.html')


@app.post('/api/simulate')
def simulate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Invalid request format.'), 400
    try:
        temp = parse_value(data, 'temperature', -50, 100)
        humidity = parse_value(data, 'humidity', 0, 100)
        water = parse_value(data, 'water_level', 0, 1000)
        custom = data.get('hour')
        if custom is None or custom == '':
            hour = datetime.now(ZoneInfo('Asia/Seoul')).hour
        else:
            hour_value = parse_value(data, 'hour', 0, 23)
            if not hour_value.is_integer():
                raise ValueError('hour: enter a whole number between 0 and 23.')
            hour = int(hour_value)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    t, h, l, w = evaluate(temp, humidity, water, hour, session.get('low_warning', False))
    session['low_warning'] = w['low_warning']
    return jsonify(temperature=t, humidity=h, lighting=l, water=w,
                   hour=hour, inputs={'temperature': temp, 'humidity': humidity, 'water_level': water})


@app.post('/api/reset')
def reset():
    session.pop('low_warning', None)
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
