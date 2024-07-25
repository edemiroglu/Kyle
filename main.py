import  os

import eel

eel.init("www")

# eel.start("index.html", port=8080)

os.system('start chrome.exe -app="http://localhost:8000/index.html"')
eel.start('index.html',mode=None, host="localhost", block=True)

