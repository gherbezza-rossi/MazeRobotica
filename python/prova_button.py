from gpiozero import Button


pulsante = Button(17)
while True:
    
    if pulsante.is_pressed:                # linea  8
        print("Pulsante Premuto!")         # linea  9
    else:                                  # linea 10 
        print("Pulsante non Premuto!")     # linea 11