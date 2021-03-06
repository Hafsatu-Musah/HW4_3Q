from flask import Flask, render_template, request, url_for
import datetime
from io import StringIO
import requests
import datetime
import csv


app = Flask(__name__)

url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/"
countries = ["Benin", "Burkina Faso", "Cape Verde", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Cote d'Ivoire", "Liberia", "Mali", "Mauritania", "Niger", "Nigeria", "Senegal", "Sierra Leone","Togo"]

def fetch_data(url, date=None):
    data = []
    cdate = datetime.date.today() - datetime.timedelta(1)
    if date:
        raw_data = requests.get(url+date+".csv").content.decode("ascii")
    else: 
        raw_data = requests.get(url+cdate.strftime('%m-%d-%Y')+".csv").content.decode("utf-8")

    decoded_data = StringIO(raw_data)
    actual_data = csv.reader(decoded_data)
    
    for items in actual_data:
        if items[3] in countries:
            data.append({"id": len(data)+1,"Country" : items[3], "Confirmed" : items[7], "Deaths": items[8], "Recovered": items[9], "Active": items[10]})
    return data


@app.route('/', methods=['GET', 'POST'])
def home():
    data = fetch_data(url)
    res = {}
    if request.method == 'POST':
        dform = request.form.get('west_africa')
        for item in data:
            if item['Country'] == str(dform):
                res.update(item)
                print(res)
            return render_template('HW4_3QN6CQ5TR5.html', data=res)
    elif request.method == 'GET':
        for item in data:
            if item['Country'] == 'Benin':
                res.update(item)
            return render_template('HW4_3QN6CQ5TR5.html', data=res, country=countries)


if __name__ == "__main__":
    app.run(debug=True)