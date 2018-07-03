from collections import defaultdict

from flask import (
    Flask,
    render_template,
    jsonify)
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy import create_engine, inspect, func

Base = automap_base()


class Incident(Base):
    __tablename__ = 'incident'
    index = sqlalchemy.Column('index', sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column('name', sqlalchemy.String)
    latitude = sqlalchemy.Column('latitude', sqlalchemy.Float)
    longitude = sqlalchemy.Column('longitude', sqlalchemy.Float)
    item = sqlalchemy.Column('item', sqlalchemy.String)
    date = sqlalchemy.Column('date', sqlalchemy.Date)


engine = create_engine("sqlite:///db/mergemap.sqlite", echo=False)
Base.prepare(engine, reflect=True)
session = Session(engine)

app = Flask(__name__)


@app.route("/data")
def data():
    sel = [Incident.name, Incident.latitude,
           Incident.longitude, Incident.item, func.count(Incident.item)]
    records = session.query(*sel).group_by(Incident.name, Incident.item).all()
    results = {}
    for record in records:
        name, lat, long, item, count = record
        if name not in results:
            results[name] = {
                "name": name,
                "lat": lat,
                "long": long,
                "items": defaultdict(int)
            }
        results[name]["items"][item] += 1
    return jsonify(list(results.values()))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
