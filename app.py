from flask import Flask, Response,jsonify, request

app = Flask(__name__)



# Tabla de datos de saturación (extraída del diagrama)
saturation_data = [
    {"pressure": 0.05, "specific_volume_liquid": 0.00105, "specific_volume_vapor": 30.00},
    {"pressure": 1, "specific_volume_liquid": 0.00112, "specific_volume_vapor": 1.694},
    {"pressure": 3, "specific_volume_liquid": 0.00143, "specific_volume_vapor": 0.272},
    {"pressure": 5, "specific_volume_liquid": 0.00158, "specific_volume_vapor": 0.127},
    {"pressure": 7, "specific_volume_liquid": 0.00174, "specific_volume_vapor": 0.0615},
    {"pressure": 10, "specific_volume_liquid": 0.0035, "specific_volume_vapor": 0.0035},
]

def interpolate(pressure, key):
    """ Interpola un valor basado en la tabla de datos. """
    for i in range(len(saturation_data) - 1):
        p1, p2 = saturation_data[i]["pressure"], saturation_data[i+1]["pressure"]
        if p1 <= pressure <= p2:
            v1, v2 = saturation_data[i][key], saturation_data[i+1][key]
            return v1 + ((pressure - p1) / (p2 - p1)) * (v2 - v1)
    return None  # Si la presión está fuera del rango

@app.route('/phase-change-diagram', methods=['GET'])
def phase_change_diagram():
    try:
        pressure = float(request.args.get('pressure'))

        # Buscar si la presión está en los datos directos
        for data in saturation_data:
            if data["pressure"] == pressure:
                return jsonify({
                    "specific_volume_liquid": data["specific_volume_liquid"],
                    "specific_volume_vapor": data["specific_volume_vapor"]
                })

        # Si no está, interpolar valores
        v_f = interpolate(pressure, "specific_volume_liquid")
        v_g = interpolate(pressure, "specific_volume_vapor")

        if v_f is not None and v_g is not None:
            return jsonify({
                "specific_volume_liquid": v_f,
                "specific_volume_vapor": v_g
            })
        else:
            return jsonify({"error": "Pressure out of range"}), 400
    except ValueError:
        return jsonify({"error": "Invalid pressure value"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)