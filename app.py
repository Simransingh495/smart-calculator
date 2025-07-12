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
           <option value="cm_to_inch">cm → inch</option>
            <option value="inch_to_cm">inch → cm</option>
            <option value="kg_to_lb">kg → lb</option>
            <option value="lb_to_kg">lb → kg</option>
            <option value="km_to_mi">km → miles</option>
            <option value="mi_to_km">miles → km</option>
            <option value="c_to_f">°C → °F</option>
            <option value="f_to_c">°F → °C</option>
            <option value="m_to_ft">meters → feet</option>
            <option value="ft_to_m">feet → meters</option>
            <option value="l_to_gal">liters → gallons</option>
            <option value="gal_to_l">gallons → liters</option>
        }
        converted = conversions.get(conversion_type, "Invalid")
        return jsonify({"converted": round(converted, 4)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
