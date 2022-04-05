
from flask import Flask, render_template,request
import requests
from flask_sqlalchemy import SQLAlchemy
import psycopg2


# Connect database

conn = psycopg2.connect(user = "postgres", password = "1092",
        host = "localhost", port = "5432", database = "weather")
cur = conn.cursor()





app = Flask(__name__)
app.config["DEBUG"]=True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


@app.route('/', methods= ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        cityname = request.form.get('city')
        # print(cityname)
        cur.execute("""insert into city(name) values(%(cityname)s)""",{'cityname':cityname})
    
    cur.execute("select * from city")
    cities = cur.fetchall()
    print(cities)
    

   
    
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=85d491b0e478fe94addfd742315183d8"

    data = []

    for city in cities:
        r = requests.get(url.format(city[1])).json()
        # print(r)
        
    weather ={
        'city': city[1],
        'temperature':r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'],
    }

   
    data.append(weather)
  

    return render_template ('weather.html', data=data)
    


if __name__ == "__main__":
    app.run(debug=True)

# Installing env
    #pip install python-dotenv