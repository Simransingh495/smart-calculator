from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expression = data.get("expression", "")
    try:
        result = eval(expression, {"__builtins__": None, "math": math})
        entry = f"{expression} = {result}"
        history.append(entry)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(history[-10:])  

@app.route("/convert", methods=["POST"])
def convert_units():
    data = request.get_json()
    value = float(data.get("value"))
    conversion = data.get("type")
    try:
        conversions = {
            "cm_to_inch": value / 2.54,
            "inch_to_cm": value * 2.54,
            "kg_to_lb": value * 2.20462,
            "lb_to_kg": value / 2.20462
        }
        result = conversions[conversion]
        return jsonify({"converted": round(result, 4)})
    except:
        return jsonify({"error": "Conversion failed"})
    
if __name__ == "__main__":
    app.run(debug=True)