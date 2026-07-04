from flask import Flask, render_template
import folium
from folium.plugins import MiniMap, Fullscreen, MousePosition
app = Flask(__name__)

# -----------------------------
# ข้อมูลสถานที่
# -----------------------------
locations = [
    {
        "name": "🏨 White Wall Riverfront Café and Hotel",
        "type": "จุดที่ 1 : ที่พัก",
        "lat": 16.4513106,
        "lon": 99.5187622,
        "color": "blue"
    },
    {
        "name": "☕ Banyakad Cafe' & Restaurant",
        "type": "จุดที่ 2 : คาเฟ่",
        "lat": 16.4555854,
        "lon": 99.5245269,
        "color": "green"
    },
    {
        "name": "🙏 ศาลหลักเมืองกำแพงเพชร",
        "type": "จุดที่ 3 : จุดเช็คอินศักดิ์สิทธิ์",
        "lat": 16.4898988,
        "lon": 99.5160818,
        "color": "red"
    },
    {
        "name": "🏛 พิพิธภัณฑสถานแห่งชาติ",
        "type": "จุดที่ 4 : ชมประวัติศาสตร์",
        "lat": 16.4884142,
        "lon": 99.5222863,
        "color": "purple"
    },
    {
        "name": "🛕 วัดพระบรมธาตุนครชุม",
        "type": "จุดที่ 5 : ไหว้พระ",
        "lat": 16.4797717,
        "lon": 99.5104020,
        "color": "orange"
    },
    {
        "name": "🛍 ตลาดย้อนยุคนครชุม",
        "type": "จุดที่ 6 : ตลาดเย็น",
        "lat": 16.4832914,
        "lon": 99.4939192,
        "color": "cadetblue"
    }
]

@app.route('/')
def index():

    center = [16.475, 99.515]

    m = folium.Map(
        location=center,
        zoom_start=14,
        tiles="CartoDB positron",
        control_scale=True
    )

    # Full Screen
    Fullscreen().add_to(m)

    # Mini Map
    MiniMap(toggle_display=True).add_to(m)

    # Mouse Position
    MousePosition().add_to(m)

    points = []

    for place in locations:

        points.append([place["lat"], place["lon"]])

        html = f"""
        <div style="width:220px">
            <h4>{place["name"]}</h4>
            <b>{place["type"]}</b><br><br>
            Latitude : {place["lat"]}<br>
            Longitude : {place["lon"]}
        </div>
        """

        folium.Marker(
            [place["lat"], place["lon"]],
            popup=folium.Popup(html, max_width=300),
            tooltip=place["name"],
            icon=folium.Icon(
                color=place["color"],
                icon="info-sign"
            )
        ).add_to(m)

    # เส้นทางเชื่อมแต่ละจุด
    folium.PolyLine(
        points,
        color="#007BFF",
        weight=5,
        opacity=0.8
    ).add_to(m)

    map_html = m._repr_html_()

    return render_template(
        "index.html",
        map=map_html
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)