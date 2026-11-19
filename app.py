from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("campus_review.db")


OUTLETS = [
    {"slug": "student-canteen", "name": "Student Canteen", "kind": "Food & drinks",
     "description": "The everyday campus food stop. Rate individual dishes and share your experience.",
     "emoji": "🍔", "cover": "canteen"},
    {"slug": "safal", "name": "Safal", "kind": "Juices, shakes & snacks",
     "description": "Fresh juices, shakes, chaat, sandwiches and quick bites.",
     "emoji": "🥤", "cover": "safal"},
    {"slug": "nescafe", "name": "Nescafé", "kind": "Coffee & quick bites",
     "description": "Hot classics, chilled drinks, Maggi and more.",
     "emoji": "☕", "cover": "nescafe"},
    {"slug": "gym", "name": "College Gym", "kind": "Fitness facility",
     "description": "Review equipment condition, availability and your overall gym experience.",
     "emoji": "🏋️", "cover": "gym"}
]

# item name, category, price (rupees), size/options note
MENU = {
"student-canteen": [
("Aloo Patty / Big Aloo Patty","Snacks",15,"Price shown as 11/15 "),
("Paneer Patty / Big Paneer Patty","Snacks",25,"Price shown as 15/25; confirm exact variants"),
("Grill Sandwich","Sandwiches",30,""),
("Cheese Grill Sandwich","Sandwiches",45,""),
("Vegetable Maggi","Maggi",30,""),
("Cheese Maggi","Maggi",35,""),
("Tomato Maggi","Maggi",40,""),
("French Fries","Snacks",35,""),
("Peri Peri Fries","Snacks",50,""),
("Chilli Potato","Snacks",60,""),
("Veg Chowmein","Chinese",50,""),
("Cheese Burger","Burgers",45,""),
("Club Cheese Burger","Burgers",60,""),
("Red Sauce Pasta","Pasta",50,"With cheese option"),
("White Sauce Pasta","Pasta",60,"With cheese option"),
("Mix Sauce Pasta","Pasta",65,"With cheese option"),
("Fried Rice","Chinese",50,""),
("Chilli Paneer","Chinese",60,""),
("Rajma Chawal","Meals",80,""),
("Chole Chawal","Meals",50,""),
("Chole Kulche","Meals",50,""),
("Chole Bhature","Meals",60,""),
("Pav Bhaji","Meals",40,""),
("Plain Dosa","South Indian",50,""),
("Masala Dosa","South Indian",50,""),
("Veg Masala Dosa","South Indian",50,""),
("Maharaja Masala Dosa","South Indian",70,""),
("Paneer Dosa","South Indian",70,""),
("Uttapam","South Indian",70,""),
("Pizza Uttapam","South Indian",70,""),
("Idli Sambar","South Indian",40,""),
("Veg Kathi Roll","Rolls",50,""),
("Aloo Tikki Kathi Roll","Rolls",60,""),
("Paneer Kathi Roll","Rolls",70,""),
("Peri Peri Cheese Kathi Roll","Rolls",80,""),
("Chilli Paneer Kathi Roll","Rolls",80,""),
("Soya Kathi Roll","Rolls",70,""),
("Chilli Chowmein Kathi Roll","Rolls",70,""),
("Lachha Paratha","Paratha",25,""),
("Malabar Paratha","Paratha",25,""),
("Aloo Paratha","Paratha",25,""),
("Gobi Paratha","Paratha",30,""),
("Mix Veg Paratha","Paratha",40,""),
("Paneer Paratha","Paratha",40,""),
("Pizza Pocket","Pizza & sides",40,""),
("Pizza Puff","Pizza & sides",40,""),
("Garlic Bread","Pizza & sides",40,""),
("Margherita Pizza","Pizza & sides",80,""),
("Vegetable Pizza","Pizza & sides",90,""),
("Coke","Beverages",25,"Price not confirmed"),
("Thums Up","Beverages",25,"Price not confirmed"),
("Sprite","Beverages",25,"Price not confirmed")
],
"safal": [
("Ganna Juice","Juices",30,"S / M / L / E.L.: ₹30 / ₹40 / ₹50 / ₹60"),
("Mausami Juice","Juices",40,"S / M / L / E.L.: ₹40 / ₹50 / ₹60 / ₹70"),
("Orange Juice","Juices",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Pineapple Juice","Juices",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Mix Juice","Juices",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Watermelon Juice","Juices",60,"S / M / L / E.L.: ₹60 / ₹70 / ₹80 / ₹100"),
("Anaar Juice","Juices",80,"S / M / L / E.L.: ₹80 / ₹100 / ₹120 / ₹140"),
("Apple Juice","Juices",80,"S / M / L / E.L.: ₹80 / ₹100 / ₹120 / ₹150"),
("Vegetable Juice","Juices",40,"S / M / L / E.L.: ₹40 / ₹50 / ₹60 / ₹70"),
("Mango Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Banana Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Strawberry Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Butterscotch Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Vanilla Shake","Shakes",60,"S / M / L / E.L.: ₹60 / ₹80 / ₹100 / ₹120"),
("Pineapple Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Oreo Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Blueberry Shake","Shakes",50,"S / M / L / E.L.: ₹50 / ₹60 / ₹70 / ₹80"),
("Paan Shake","Shakes",70,"S / M / L / E.L.: ₹70 / ₹80 / ₹90 / ₹100"),
("Litchi Shake","Shakes",60,"S / M / L / E.L.: ₹60 / ₹70 / ₹80 / ₹100"),
("Chocolate Shake","Shakes",60,"S / M / L / E.L.: ₹60 / ₹80 / ₹100 / ₹120"),
("Khajur Shake","Shakes",60,"S / M / L / E.L.: ₹60 / ₹80 / ₹100 / ₹120"),
("Kesar Pista Shake","Shakes",80,"S / M / L / E.L.: ₹80 / ₹100 / ₹140 / ₹150"),
("Lemon Soda with Mint","Mojitos",50,"S / M / L: ₹50 / ₹60 / ₹70"),
("Virgin Mojito","Mojitos",40,"S / M / L: ₹40 / ₹50 / ₹60"),
("Lychee Mojito","Mojitos",50,"S / M / L: ₹50 / ₹60 / ₹70"),
("Dark Grape Mojito","Mojitos",60,"S / M / L: ₹60 / ₹70 / ₹80"),
("Guava Mojito","Mojitos",50,"S / M / L: ₹50 / ₹60 / ₹70"),
("Kiwi Mint Mojito","Mojitos",60,"S / M / L: ₹60 / ₹70 / ₹80"),
("Orange Mojito","Mojitos",50,"S / M / L: ₹50 / ₹60 / ₹70"),
("Watermelon Mojito","Mojitos",50,"S / M / L: ₹50 / ₹60 / ₹70"),
("Boiled Corn Chaat","Snacks",60,"Handwritten menu"),
("Tikki Chaat","Snacks",70,"Handwritten menu"),
("Veg Sandwich","Sandwiches",60,"Handwritten menu"),
("Bhel Puri","Snacks",50,"Handwritten menu"),
("Cold Coffee","Beverages",50,"Handwritten menu"),
("Poha","Snacks",50,"Handwritten menu"),
("Special Elaichi Tea","Beverages",15,"Handwritten menu"),
("Hot Coffee","Beverages",25,"Handwritten menu"),
("Mix Aloo Pyaz Pakoda","Snacks",60,"Handwritten menu"),
("Bread Pakoda","Snacks",50,"Handwritten menu; confirm price"),
("Bread Pakoda Paneer","Snacks",60,"Handwritten menu"),
("Egg Soup","Soups",100,"Handwritten menu"),
("Veg Manchow Soup","Soups",90,"Handwritten menu"),
("Sweet Corn Soup","Soups",100,"Handwritten menu"),
("Lemon Coriander Soup","Soups",90,"Handwritten menu"),
("Veg Hot & Sour Soup","Soups",120,"Handwritten menu"),
("Veg Momos","Momos",100,"8 pieces"),
("Paneer Momos","Momos",120,"8 pieces"),
("Veg Noodles","Chinese",80,"Handwritten menu"),
("Veg Paneer Noodles","Chinese",100,"Handwritten menu"),
("Chilli Garlic Noodles","Chinese",100,"Handwritten menu"),
("Singapuri Noodles","Chinese",100,"Handwritten menu"),
("Spring Rolls","Snacks",100,"2 pieces"),
("Chilli Mushroom","Chinese",150,"Special item; handwritten menu"),
("Kurkure Momos","Momos",150,"8 pieces"),
("Paneer Kurkure Momos","Momos",170,"8 pieces"),
("Veg Fry Momos","Momos",120,"Handwritten menu"),
("Paneer Veg Momos Fry","Momos",140,"8 pieces"),
("Mini Papdi","Chaat",10,"Handwritten menu; confirm price"),
("Mix Pakoda","Snacks",60,"Per plate"),
("Egg Roll","Rolls",100,""),
("Pizza","Pizza & sides",80,"Handwritten note; availability/price may change")
],
"nescafe": [
("Original Masala Maggi","Maggi",45,""),
("Green Chilli Maggi","Maggi",45,""),
("Double Masala Maggi","Maggi",55,""),
("Corn Maggi","Maggi",55,""),
("Spicy Garlic Maggi","Maggi",55,""),
("Oregano Maggi","Maggi",55,""),
("Special Masala Maggi","Maggi",55,""),
("Cheese Maggi","Maggi",65,""),
("Veg Maggi","Maggi",65,""),
("Butter Maggi","Maggi",65,""),
("Egg Maggi","Maggi",65,""),
("Atta Maggi","Maggi",65,""),
("Oats Maggi","Maggi",65,""),
("Butter Double Masala Maggi","Maggi",70,""),
("Oregano Cheese Maggi","Maggi",70,""),
("Cheese Pizza","Pizza",70,""),
("Mushroom Pizza","Pizza",70,""),
("Masala Pizza","Pizza",70,""),
("Tomato Pizza","Pizza",70,""),
("Regular Coffee","Hot Classics",25,""),
("Masala Tea","Hot Classics",25,""),
("Milk Tea Bag","Hot Classics",25,""),
("Cardamom Tea","Hot Classics",25,""),
("Green Tea","Hot Classics",25,""),
("Lemon Tea","Hot Classics",25,""),
("Espresso","Hot Classics",25,""),
("Espresso Macchiato","Hot Classics",40,""),
("Cafe Latte","Hot Classics",40,""),
("Tapri Coffee","Hot Classics",40,""),
("Cappuccino","Hot Classics",40,""),
("Cafe Mocha","Hot Classics",50,""),
("Hot Chocolate","Hot Classics",50,""),
("Chocochino","Hot Classics",50,""),
("Cappuccino Strong","Hot Classics",50,""),
("Irish Cappuccino","Hot Classics",60,""),
("Caramel Cappuccino","Hot Classics",60,""),
("Hazelnut Cappuccino","Hot Classics",60,""),
("Lemon Iced Tea","Chill Thrills",50,"Regular ₹50 / Large ₹80"),
("Masala Lemon Iced Tea","Chill Thrills",60,"Regular ₹60 / Large ₹90"),
("Watermelon Iced Tea","Chill Thrills",60,"Regular ₹60 / Large ₹100"),
("Mojito Iced Tea","Chill Thrills",60,"Regular ₹60 / Large ₹100"),
("Peach Iced Tea","Chill Thrills",60,"Regular ₹60 / Large ₹100"),
("Passion Fruit Iced Tea","Chill Thrills",60,"Regular ₹60 / Large ₹100"),
("Cafe Frappe (Cold Coffee)","Chill Thrills",60,"Regular ₹60 / Large ₹100"),
("Frappe Mocha","Chill Thrills",70,"Regular ₹70 / Large ₹110"),
("Cold Chocolate","Chill Thrills",70,"Regular ₹70 / Large ₹110"),
("Irish Frappe","Chill Thrills",70,"Regular ₹70 / Large ₹110"),
("Caramel Frappe","Chill Thrills",70,"Regular ₹70 / Large ₹110"),
("Hazelnut Frappe","Chill Thrills",70,"Regular ₹70 / Large ₹110")
]
}

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outlet TEXT NOT NULL, name TEXT NOT NULL, category TEXT,
            price INTEGER DEFAULT 0, note TEXT DEFAULT '',
            UNIQUE(outlet, name)
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )""")
        for outlet, rows in MENU.items():
            for name, category, price, note in rows:
                con.execute("INSERT OR IGNORE INTO items(outlet,name,category,price,note) VALUES(?,?,?,?,?)",
                            (outlet,name,category,price,note))
        # Gym is a placeholder until the actual equipment list is checked.
        gym_items = [
            ("Treadmill","Cardio",0,"Add the actual gym equipment and details after checking."),
            ("Exercise Cycle","Cardio",0,"Placeholder — confirm equipment availability."),
            ("Dumbbells","Free weights",0,"Placeholder — add weight range after checking."),
            ("Bench Press","Strength",0,"Placeholder — confirm equipment availability."),
            ("Cable Machine","Strength",0,"Placeholder — confirm equipment availability."),
            ("Leg Press","Strength",0,"Placeholder — confirm equipment availability.")
        ]
        for name, category, price, note in gym_items:
            con.execute("INSERT OR IGNORE INTO items(outlet,name,category,price,note) VALUES('gym',?,?,?,?)",
                        (name,category,price,note))
        con.commit()

@app.route("/")
def home():
    return render_template("index.html", outlets=OUTLETS)

@app.route("/outlet/<slug>")
def outlet_page(slug):
    outlet = next((o for o in OUTLETS if o["slug"] == slug), None)
    if not outlet:
        return "Outlet not found", 404
    return render_template("outlet.html", outlet=outlet)

@app.route("/api/outlets")
def get_outlets():
    return jsonify(OUTLETS)

@app.route("/api/items/<slug>")
def get_items(slug):
    if slug not in [o["slug"] for o in OUTLETS]:
        return jsonify({"error":"Unknown outlet"}), 404
    search = request.args.get("q","").strip()
    category = request.args.get("category","").strip()
    with connect() as con:
        query = """SELECT i.id,i.name,i.category,i.price,i.note,
                   ROUND(AVG(r.rating),1) AS average_rating,
                   COUNT(r.id) AS review_count
                   FROM items i LEFT JOIN reviews r ON i.id=r.item_id
                   WHERE i.outlet=?"""
        params = [slug]
        if search:
            query += " AND (i.name LIKE ? OR i.category LIKE ?)"
            params += [f"%{search}%",f"%{search}%"]
        if category:
            query += " AND i.category=?"
            params.append(category)
        query += " GROUP BY i.id ORDER BY i.category,i.name"
        rows = [dict(row) for row in con.execute(query,params).fetchall()]
        cats = [r[0] for r in con.execute("SELECT DISTINCT category FROM items WHERE outlet=? ORDER BY category",(slug,)).fetchall()]
    return jsonify({"items":rows,"categories":cats})

@app.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.get_json(silent=True) or {}
    name = str(data.get("student_name","")).strip()[:40]
    comment = str(data.get("comment","")).strip()[:500]
    rating = data.get("rating")
    item_id = data.get("item_id")
    if not name or not comment or not isinstance(rating,int) or rating < 1 or rating > 5 or not isinstance(item_id,int):
        return jsonify({"error":"Please enter your name, a comment and a rating from 1 to 5."}), 400
    with connect() as con:
        exists = con.execute("SELECT id FROM items WHERE id=?",(item_id,)).fetchone()
        if not exists:
            return jsonify({"error":"That menu item could not be found."}), 404
        con.execute("INSERT INTO reviews(item_id,student_name,rating,comment) VALUES(?,?,?,?)",
                    (item_id,name,rating,comment))
        con.commit()
        review_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    return jsonify({"message":"Review posted! Thanks for helping fellow NSUT students.","review_id":review_id}), 201

@app.route("/api/reviews/<int:item_id>")
def item_reviews(item_id):
    with connect() as con:
        rows = [dict(r) for r in con.execute(
            "SELECT student_name,rating,comment,created_at FROM reviews WHERE item_id=? ORDER BY id DESC LIMIT 30",
            (item_id,)).fetchall()]
    return jsonify(rows)

@app.route("/api/stats")
def stats():
    with connect() as con:
        count = con.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
        items = con.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        avg = con.execute("SELECT ROUND(AVG(rating),1) FROM reviews").fetchone()[0]
    return jsonify({"reviews":count,"items":items,"average":avg or 0})

def outlet_summary(con, slug):
    row = con.execute("""SELECT COUNT(r.id) AS total, ROUND(AVG(r.rating),1) AS average
                         FROM reviews r JOIN items i ON i.id = r.item_id
                         WHERE i.outlet=?""", (slug,)).fetchone()
    return row["total"], row["average"]

@app.route("/api/analytics")
def analytics_all():
    """Average stars + total reviews for every outlet (used on the homepage)."""
    with connect() as con:
        outlets = []
        for o in OUTLETS:
            total, avg = outlet_summary(con, o["slug"])
            outlets.append({"slug": o["slug"], "name": o["name"], "emoji": o["emoji"],
                            "cover": o["cover"], "reviews": total, "average": avg or 0})
        overall_total = con.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
        overall_avg = con.execute("SELECT ROUND(AVG(rating),1) FROM reviews").fetchone()[0]
    return jsonify({"overall": {"reviews": overall_total, "average": overall_avg or 0},
                    "outlets": outlets})

@app.route("/api/analytics/<slug>")
def analytics_outlet(slug):
    """Detailed analytics for one outlet: average, total, 1-5 star split, top items."""
    if slug not in [o["slug"] for o in OUTLETS]:
        return jsonify({"error": "Unknown outlet"}), 404
    with connect() as con:
        total, avg = outlet_summary(con, slug)
        distribution = {str(n): 0 for n in range(1, 6)}
        for row in con.execute("""SELECT r.rating AS rating, COUNT(*) AS c
                                  FROM reviews r JOIN items i ON i.id = r.item_id
                                  WHERE i.outlet=? GROUP BY r.rating""", (slug,)):
            distribution[str(row["rating"])] = row["c"]
        top_items = [dict(row) for row in con.execute("""
            SELECT i.id, i.name, ROUND(AVG(r.rating),1) AS average, COUNT(r.id) AS reviews
            FROM items i JOIN reviews r ON r.item_id = i.id
            WHERE i.outlet=?
            GROUP BY i.id
            ORDER BY AVG(r.rating) DESC, COUNT(r.id) DESC, i.name
            LIMIT 3""", (slug,))]
    return jsonify({"outlet": slug, "total_reviews": total, "average": avg or 0,
                    "distribution": distribution, "top_items": top_items})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)