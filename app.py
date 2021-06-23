from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/home', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    weather_data = []

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=263d3683d07ad20b4a7827fe76482ac9'

    for city in cities:

        res = requests.get(url.format(city.name)).json()

        weather = {
            'city' : city.name,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'icon' : res['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
