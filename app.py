from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import math
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get("expression")
    try:
        result = str(eval(expression, {"__builtins__": None}, {"math": math}))

        # Store history in session
        if 'history' not in session:
            session['history'] = []
        session['history'].append(f"{expression} = {result}")
        session.modified = True

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/history')
def history():
    return jsonify(session.get('history', []))

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    value = float(data.get("value"))
    conversion_type = data.get("type")

    try:
        conversions = {
    "cm_to_inch": value / 2.54,
    "inch_to_cm": value * 2.54,
    "kg_to_lb": value * 2.20462,
    "lb_to_kg": value / 2.20462,
    "km_to_mi": value * 0.621371,
    "mi_to_km": value / 0.621371,
    "c_to_f": (value * 9/5) + 32,
    "f_to_c": (value - 32) * 5/9,
    "m_to_ft": value * 3.28084,
    "ft_to_m": value / 3.28084,
    "l_to_gal": value * 0.264172,
    "gal_to_l": value / 0.264172
}
        converted = conversions.get(conversion_type, "Invalid")
        return jsonify({"converted": round(converted, 4)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
