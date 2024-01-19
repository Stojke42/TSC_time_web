import time
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
counting= False

@app.route('/')
def main_function():
    return render_template('index.html')


@app.route('/ftime', methods=['POST'])
def ftime():
    global counting
    data = request.get_json()
    counting = data['status']

    if not counting:
        return jsonify({'status': 'sikeres'})
    start_time = datetime.now()
    while counting:
        time.sleep(0.5)
        minutes, seconds = convert_seconds_to_minutes_and_seconds((datetime.now() - start_time).seconds)
        file = open('data.txt', 'w')
        file.write(format_time(minutes, seconds))
        file.close()
    file = open('data.txt', 'w')
    file.write(format_time(0, 0))
    file.close()
    return jsonify({'status': 'sikeres'})


@app.route('/htime', methods=['POST'])
def htime():
    global counting
    data = request.get_json()
    counting = data['status']

    if not counting:
        return jsonify({'status': 'sikeres'})
    start_time = datetime.now()-timedelta(minutes=45)

    while counting:
        time.sleep(0.5)
        minutes, seconds = convert_seconds_to_minutes_and_seconds((datetime.now() - start_time).seconds)
        file = open('data.txt', 'w')
        file.write(format_time(minutes, seconds))
        file.close()
    file = open('data.txt', 'w')
    file.write(format_time(0, 0))
    file.close()
    return jsonify({'status': 'sikeres'})


def get_data():
    with open('data.txt', 'r') as file:
        data = file.read()
    return data


@app.route('/get_data')
def get_data_route():
    return jsonify(data=get_data())


def convert_seconds_to_minutes_and_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds


def format_time(minutes=0, seconds=0):
    return "{:02}:{:02}".format(int(minutes), int(seconds))


if __name__ == '__main__':
    app.run()
