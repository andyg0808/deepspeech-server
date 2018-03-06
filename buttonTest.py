from gpiozero import Button
from signal import pause

button = Button(17)

def pressed(button):
    print("button pressed")

button.when_pressed = pressed

pause()
