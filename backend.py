from flask import Flask, request, jsonify
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = Flask(__name__)

@app.route('/kundali', methods=['POST'])
def kundali():
    data = request.json
    dob = data.get('dob')
    tob = data.get('tob')
    lat = float(data.get('lat'))
    lon = float(data.get('lon'))
    name = data.get('name', 'Unknown')

    dt = Datetime(dob, tob, '+05:30')  # IST
    geo = GeoPos(lat, lon)
    chart = Chart(dt, geo, hsys='Placidus')

    planets = ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu','Asc']
    kundali = {}
    for p in planets:
        try:
            obj = chart.get(p)
            kundali[p] = f"{obj.sign} {obj.lon:.2f}"
        except:
            kundali[p] = "NA"

    return jsonify({
        'name': name,
        'dob': dob,
        'tob': tob,
        'place': f"{lat},{lon}",
        'kundali': kundali
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
