import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# NLTK için gerekli verilerin indirilmesi
nltk.download('punkt')
nltk.download('stopwords')

# Ses Tanıma Fonksiyonu
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Konuşun...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='tr-TR')
        print(f"Siz: {text}")
        return text
    except sr.UnknownValueError:
        print("Anlaşılamadı")
        return ""
    except sr.RequestError:
        print("API servisine ulaşılamadı")
        return ""

# Ses Sentezleme Fonksiyonu
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Doğal Dil İşleme Fonksiyonu
def process_text(text):
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if word not in stopwords.words('turkish')]
    return words

# Hava Durumu Fonksiyonu
def get_weather():
    api_key = "YOUR_API_KEY"
    city = "Istanbul"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=tr"
    response = requests.get(url)
    data = response.json()
    weather = data["weather"][0]["description"]
    return f"Bugün İstanbul'da hava {weather}"

# Kivy Uygulaması
class VoiceAssistantApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Merhaba, nasıl yardımcı olabilirim?")
        layout.add_widget(self.label)
        button = Button(text="Konuş")
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)
        return layout

    def on_button_press(self, instance):
        text = recognize_speech()
        self.label.text = text
        if "hava" in text.lower():
            response = get_weather()
        else:
            response = "Bu komutu anlayamadım."
        self.label.text += "\n" + response
        speak(response)

if __name__ == '__main__':
    VoiceAssistantApp().run()
