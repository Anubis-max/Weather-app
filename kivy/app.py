import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
import requests

class MyGrid(FloatLayout):
    locate = ObjectProperty(None)

    def btn(self):
        api_key="83e2142cb7dda473719513bc695cbbdf"
        city = self.ids.city.text
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            temp = int(temp - 273.15)
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            self.show_popup(temp, desc, humidity, wind, city)
        else:
            self.show_error()
            
    def show_popup(self, temp, desc, humidity, wind, city):
        show = P(temp, desc, humidity, wind, city)

        popupWindow = Popup(title="Weather", content=show, size_hint=(0.6, 0.8), auto_dismiss=False)

        popupWindow.open()

    def show_error(self):
        show = error()

        popupWindow = Popup(title="Error X_X", content=show, size_hint=(0.6, 0.8), auto_dismiss=False)

        popupWindow.open()

class P(FloatLayout):
    source = StringProperty("")
    def __init__(self, temp, desc, humidity, wind, city):

        self.desc = desc

        super().__init__()
        self.ids.temp.text = (str(temp) + " °C")
        self.ids.desc.text = str(desc)
        self.ids.humidity.text = (str(humidity) + "%")
        self.ids.wind.text = (str(wind) + " km/h")
        self.ids.city.text = (str(city))

    def close_popup(self):
        self.parent.parent.parent.dismiss()
        
    def chose_weather(self):
        if "thunderstorm" in self.desc:
            return "image/thunder2.png"
        elif "drizzle" in self.desc:
            return "image/drizzle.png"
        elif "rain" in self.desc:
            return "image/rain.png"
        elif "snow" in self.desc:
            return "image/snow.png"
        elif "clear" in self.desc:
            return "image/sun.png"
        elif "clouds" in self.desc:
            return "image/cloud.png"
        else:
            return "image/cloud.png"

class error(FloatLayout):
    def close_popup(self):
        self.parent.parent.parent.dismiss()

class MyApp(App):
    def build(self):
        self.title = "Weather app"
        self.icon = "image/icon.jpg"
        return MyGrid()
    
if __name__ == "__main__":
    MyApp().run()