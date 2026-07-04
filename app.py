from flask import Flask, render_template
import folium
from folium.plugins import MiniMap, Fullscreen, MousePosition

app = Flask(__name__)

# -----------------------------
# ข้อมูลสถานที่ (เพิ่มรูปภาพ และ คำบรรยาย เพื่อส่งไปให้หน้าเว็บดีไซน์ใหม่)
# -----------------------------
locations = [
    {
        "name": "White Wall Riverfront Café and Hotel",
        "type": "จุดที่ 1 : ที่พัก",
        "lat": 16.4513106,
        "lon": 99.5187622,
        "color": "blue",
        "desc": "เริ่มต้นทริปด้วยที่พักและคาเฟ่ริมแม่น้ำปิง บรรยากาศสุดชิล ตกแต่งสไตล์มินิมอล จิบกาแฟยามเช้าเตรียมพร้อมก่อนออกเดินทาง",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80"
    },
    {
        "name": "Banyakad Cafe' & Restaurant",
        "type": "จุดที่ 2 : คาเฟ่",
        "lat": 16.4555854,
        "lon": 99.5245269,
        "color": "green",
        "desc": "แวะพักทานอาหารและเครื่องดื่มในร้านบรรยากาศดี พื้นที่กว้างขวาง มีมุมถ่ายรูปสวยๆ เพียบ เติมพลังก่อนลุยต่อ",
        "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&q=80"
    },
    {
        "name": "ศาลหลักเมืองกำแพงเพชร",
        "type": "จุดที่ 3 : จุดเช็คอินศักดิ์สิทธิ์",
        "lat": 16.4898988,
        "lon": 99.5160818,
        "color": "red",
        "desc": "สักการะสิ่งศักดิ์สิทธิ์คู่บ้านคู่เมืองกำแพงเพชรเพื่อความเป็นสิริมงคล ศูนย์รวมจิตใจของชาวเมืองที่ใครมาเยือนก็ต้องแวะ",
        "image": "https://temple-thai.com/wp-content/uploads/2021/10/kamphaeng-phet-city-pillar-shrine-2.jpg" 
    },
    {
        "name": "พิพิธภัณฑสถานแห่งชาติ",
        "type": "จุดที่ 4 : ชมประวัติศาสตร์",
        "lat": 16.4884142,
        "lon": 99.5222863,
        "color": "purple",
        "desc": "เดินชมโบราณวัตถุและศิลปวัตถุชิ้นสำคัญ ที่บอกเล่าเรื่องราวประวัติศาสตร์อันยาวนานและความรุ่งเรืองของเมืองชากังราว",
        "image": "https://images.unsplash.com/photo-1574359411659-15573a27fd0c?w=800&q=80"
    },
    {
        "name": "วัดพระบรมธาตุนครชุม",
        "type": "จุดที่ 5 : ไหว้พระ",
        "lat": 16.4797717,
        "lon": 99.5104020,
        "color": "orange",
        "desc": "ข้ามฝั่งแม่น้ำมาไหว้พระบรมธาตุเจดีย์สีทองอร่าม ศิลปะพม่า สวยงามตระการตา เป็นวัดเก่าแก่คู่เมืองในย่านนครชุม",
        "image": "https://cms.dmpcdn.com/travel/2022/12/28/c790f8f0-8661-11ed-be11-c1ffa20b773e_webp_original.jpg"
    },
    {
        "name": "ตลาดย้อนยุคนครชุม",
        "type": "จุดที่ 6 : ตลาดเย็น",
        "lat": 16.4832914,
        "lon": 99.4939192,
        "color": "cadetblue",
        "desc": "ปิดท้ายทริปด้วยการเดินเล่นชิมอาหารพื้นบ้าน ซื้อของฝาก ในบรรยากาศตลาดย้อนยุคสุดคลาสสิกที่ยังคงเสน่ห์วิถีชีวิตดั้งเดิม",
        "image": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=800&q=80"
    }
]

@app.route('/')
def index():
    # 1. สร้างแผนที่ตั้งต้น
    center = [16.475, 99.515]
    m = folium.Map(location=center, zoom_start=14, tiles="CartoDB positron", control_scale=True)

    # ใส่เครื่องมือเสริม
    Fullscreen().add_to(m)
    MiniMap(toggle_display=True).add_to(m)
    MousePosition().add_to(m)

    points = []
    
    # 2. วนลูปปักหมุด
    for place in locations:
        points.append([place["lat"], place["lon"]])
        
        # ปรับสีฟอนต์ในป๊อปอัปให้เข้ากับธีมวินเทจ
        popup_html = f'''
        <div style="width:200px; font-family: 'Sarabun', sans-serif;">
            <h5 style="color: #E65100; font-weight: bold; font-size: 16px;">{place["name"]}</h5>
            <span style="color: #004D40; font-size: 14px;">{place["type"]}</span>
        </div>
        '''

        folium.Marker(
            [place["lat"], place["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=place["name"],
            icon=folium.Icon(color=place["color"], icon="info-sign")
        ).add_to(m)

    # 3. วาดเส้นเชื่อมต่อ (เปลี่ยนเป็นสีเขียวเข้มให้เข้ากับธีมเว็บ)
    folium.PolyLine(
        points, 
        color="#004D40", 
        weight=4, 
        opacity=0.8,
        dash_array="5, 10" # ทำให้เป็นเส้นประสวยๆ
    ).add_to(m)

    map_html = m._repr_html_()

    # 4. ส่งข้อมูลทั้งแผนที่ (map) และข้อมูลสถานที่ (locations) ไปยังหน้า index.html
    return render_template("index.html", map=map_html, locations=locations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)