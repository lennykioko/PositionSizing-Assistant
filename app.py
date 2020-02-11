"""contains backend logic for the web app"""
import locale

from flask import Flask, render_template, request

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)


def calculate_scalp(pip_value, max_risk, breather, target):
    try:
        breather_value = breather * pip_value
        raw_volume = max_risk / breather_value
        volume = round(raw_volume, 2)
        pot_win = target * pip_value * volume

        results = {"risk": f"{round(max_risk * 100, 2):n}", "volume": volume, "raw_volume": raw_volume, "pot_win": f"{round(pot_win * 100, 2):n}"}  # noqa E501
    except Exception as e:
        print(e)

    return results


def calculate_swing(pip_value, max_risk, sl_pips, tp_pips):
    try:
        risk_reward = round(tp_pips / sl_pips, 2)
        raw_volume = max_risk / (sl_pips * pip_value)
        volume = round(raw_volume, 2)
        results = {"risk_reward": risk_reward, "max_risk": f"{max_risk * 100 :n}", "max_win": f"{(max_risk * risk_reward) * 100 :n}", "volume": volume, "raw_volume": raw_volume}  # noqa E501
    except Exception as e:
        print(e)

    return results


@app.route('/')
def scalping():
    """displays the scalping page"""
    return render_template('scalping.html')


@app.route('/calcScalp', methods=['POST'])
def calcScalp():
    """calculates the scalping values"""
    pip_value = request.form['pipValue']
    max_risk = request.form['maxRisk']
    breather_pips = request.form['breatherPips']
    target_pips = request.form['targetPips']

    try:
        results = calculate_scalp(float(pip_value), float(max_risk), float(breather_pips), float(target_pips))  # noqa E501
    except Exception as e:
        print(e)
        results = {}

    return render_template('scalping.html', results=results)


@app.route('/swings')
def swings():
    """displays the swings page"""
    return render_template('swings.html')


@app.route('/calcSwings', methods=['POST'])
def calcSwings():
    """calculates the swings values"""
    pip_value = request.form['pipValue']
    max_risk = request.form['maxRisk']
    sl_pips = request.form['SLPips']
    tp_pips = request.form['TPPips']

    try:
        results = calculate_swing(float(pip_value), float(max_risk), float(sl_pips), float(tp_pips))  # noqa E501
    except Exception as e:
        print(e)
        results = {}

    return render_template('swings.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
