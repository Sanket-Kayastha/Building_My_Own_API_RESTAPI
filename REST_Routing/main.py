from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        return {
                "id": self.id,
                "name" : self.name,
                "map_url" : self.map_url,
                "img_url" : self.img_url,
                "location" : self.location,
                "seats" : self.seats,
                "has_toilet" : self.has_toilet,
                "has_wifi" : self.has_wifi,
                "has_sockets": self.has_sockets,
                "can_take_calls": self.can_take_calls,
                "coffee_price": self.coffee_price
        }

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def all_result():
    result = db.session.execute(db.select(Cafe)).scalars().all()
    all_result = random.choice(result)
    # print(all_result.name)
    return jsonify(name = all_result.name,
                   map_url = all_result.map_url,
                   img_url = all_result.img_url,
                   location = all_result.location,
                   seats = all_result.seats,
                   has_toilet = all_result.has_toilet,
                   has_wifi = all_result.has_wifi,
                   has_sockets = all_result.has_sockets,
                   can_take_calls = all_result.can_take_calls,
                   coffee_price = all_result.coffee_price
                   )


@app.route("/all")
def all():
    result = db.session.execute(db.select(Cafe))
    all_result = result.scalars().all()
    #for all_result in all_result:
    all_cafe = [cafe.to_dict() for cafe in all_result]
    return jsonify(all_cafe)

@app.route("/search")
#http://127.0.0.1:5000/search?loc=lucknow "formate to search in browser"
def search():
    q_location=request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location==q_location)).scalars().all()
    if result:
        return jsonify(cafes = [cafe.to_dict() for cafe in result])
    else:
        return jsonify(error = {"Not Found": "Sorry, we don't have a cafe at that location."})
# HTTP POST - Create Record
@app.route("/add", methods=["POST","GET"])
def add():
    # all_data = Cafe(
    #     name =  "Sanket Srivastav",
    #     map_url = "kalikha",
    #     seats = "3",
    #     img_url= "koplimg",
    #     location= "lucknow",
    #     has_toilet = True,
    #     has_wifi = False,
    #     has_sockets = True,
    #     can_take_calls = True,
    #     coffee_price = "$3.5"


    # )
    # db.session.add(all_data)
    # db.session.commit()
    
    return f"Data Added Successfully"

# HTTP PUT/PATCH - Update Record0
@app.route("/update-price/<int:cafe_id>", methods=["PATCH","GET"])
def update(cafe_id):
    #http://127.0.0.1:5000/update-price/2?new_price=$4.5
    cafe_no = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one_or_none()
    # if cafe_no:
    #     return jsonify({
    #         "Coffee-Price" : cafe_no.coffee_price
    #     })
    # else:
    #     return jsonify("Sorry, No data found")
    new_price = request.args.get("new_price")
    cafe_no.coffee_price = new_price
    db.session.commit()
    return f"{cafe_no.coffee_price}"

# HTTP DELETE - Delete Record
@app.route("/remove-cafe/<int:cafe_id>", methods=["DELETE","GET"])
def remove(cafe_id):
    cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one_or_none()
    secret = "secretapikey"
    apikey = request.args.get("API_KEY")
    if secret == apikey:
        db.session.delete(cafe)
        db.session.commit()
        return f"Data Remove Successfully"
    else:
        return f"Unauthorised Access, Please provide correct Api_key"


if __name__ == '__main__':
    app.run(debug=False)
