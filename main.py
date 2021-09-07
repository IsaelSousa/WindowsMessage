from win10toast import ToastNotifier
from dotenv import load_dotenv, find_dotenv
from dolarLib import dolarPriceValue, dolarAttValue
import requests
import random
import time
import os

load_dotenv(find_dotenv())
toaster = ToastNotifier()
API_KEY1 = os.environ.get("API_KEY1")

FirstMessage = random.choice(["Olá ", "Oie ", "Hello ", "Hey there "])
SecondMessage = random.choice(["Como vai você?", "eai?"])

##Weather
## The weather need a key, get your key in https://openweathermap.org/ .
api_key = API_KEY1
lat = "-23.5534"
lon = "-46.6365"
url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

## Weather response.
response = requests.get(url)
#with json format.
data = response.json()

temp = data['main']['temp']
tempValue = round(temp, 1)
city = data['name']
country = data['sys']['country']
q = data['weather'][0]['description']

##Translate description
translate = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=pt&dt=t&q=%s' % (q)
translateRes = requests.get(translate)
tempMessage = translateRes.json()[0][0][0]

##Message Notify
dolar = dolarPriceValue()
att = dolarAttValue()
cityRes = str('Cidade: ' + city + '-' + country)
TempRes = str('Temperatura: ' + str(tempValue) + '°C')
ClimateRes = str('Clima: ' + tempMessage)
PriceRes = str(dolar)
AttRes = att
space = ' '
breakRow = space * 50
AllMsg = cityRes + breakRow + TempRes + breakRow + ClimateRes + breakRow + PriceRes + '/' + AttRes

iconPath = './FILE.ico'
path = os.getlogin() + '! '

starttime=time.time()

def notification():
  time.sleep(1)
  toaster.show_toast(
  FirstMessage + path + SecondMessage,
  AllMsg,
  threaded=False,
  icon_path=iconPath,
  duration=10 
)


timer = float(60 * 60 * 2)##This code == 2hours
x = 0
while (x <= 1): 
  notification()
  time.sleep(timer)