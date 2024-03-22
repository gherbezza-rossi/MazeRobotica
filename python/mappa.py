import pygame

# Definisci la mappa
mappa = [[0 for x in range(20)] for y in range(20)]
mappa[10][10] = 1

# Inizializza il robot
robot = {"x": 10, "y": 10, "direzione": "su"}

# Inizializza Pygame
pygame.init()

def muovi_avanti(robot):
    robot["x"] += 1 if robot["direzione"] == "destra" else -1
    robot["y"] += 1 if robot["direzione"] == "giù" else -1

def muovi_indietro(robot):
    robot["x"] -= 1 if robot["direzione"] == "destra" else 1
    robot["y"] -= 1 if robot["direzione"] == "giù" else 1

def muovi_a_sinistra(robot):
    robot["direzione"] = "sinistra" if robot["direzione"] == "su" else "su"
    robot["direzione"] = "giù" if robot["direzione"] == "destra" else "destra"

def muovi_a_destra(robot):
    robot["direzione"] = "destra" if robot["direzione"] == "su" else "su"
    robot["direzione"] = "giù" if robot["direzione"] == "sinistra" else "destra"
    
# Crea una finestra
finestra = pygame.display.set_mode((400, 400))

# Stampa la mappa
for y in range(len(mappa)):
    for x in range(len(mappa[0])):
        if mappa[y][x] == 1:
            pygame.draw.rect(finestra, (255, 0, 0), (x * 20, y * 20, 20, 20))
        else:
            pygame.draw.rect(finestra, (0, 0, 0), (x * 20, y * 20, 20, 20))

# Stampa il robot
pygame.draw.rect(finestra, (255, 255, 0), (robot["x"] * 20, robot["y"] * 20, 20, 20))

# Aggiorna la finestra
pygame.display.update()

# Ciclo principale
while True:
    # Leggi l'input dell'utente
    input_utente = input("Inserisci un comando (w, a, s, d, q, e): ")

    # Esegui il comando
    if input_utente == "w":
        if robot["y"] > 0:
            muovi_avanti(robot)
    elif input_utente == "a":
        if robot["x"] > 0:
            muovi_a_sinistra(robot)
    elif input_utente == "s":
        if robot["y"] < len(mappa) - 1:
            muovi_indietro(robot)
    elif input_utente == "d":
        if robot["x"] < len(mappa[0]) - 1:
            muovi_a_destra(robot)
    # Stampa la mappa
    for y in range(len(mappa)):
        for x in range(len(mappa[0])):
            if mappa[y][x] == 1:
                pygame.draw.rect(finestra, (255, 0, 0), (x * 20, y * 20, 20, 20))
            else:
                pygame.draw.rect(finestra, (0, 0, 0), (x * 20, y * 20, 20, 20))

    # Stampa il robot
    pygame.draw.rect(finestra, (255, 255, 0), (robot["x"] * 20, robot["y"] * 20, 20, 20))
    print("Direzione:", robot["direzione"])

    # Aggiorna la finestra
    pygame.display.update()