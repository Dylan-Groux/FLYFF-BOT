import win32gui  # Importation des bibliothèques nécessaires
import win32api
import win32con
import pyautogui
import time
import keyboard  # Pour la gestion des touches du clavier

# Constantes utilisées dans le script
WINDOW_TITLE = "{launcher flyff} - {player-name}"  # Titre de la fenêtre à rechercher
IMAGE_PATHS = [  # Chemins vers les images à détecter
    r".\flyffbot\src\picture\captain-tower4.JPG",
    r".\flyffbot\src\picture\captain-tower3.JPG",
    r".\flyffbot\src\picture\captain-tower2.JPG",
]
DETECTION_CONFIDENCE = 0.7  # Seuil de confiance pour la détection d'image
DELAY_BETWEEN_ATTEMPTS = 1  # Délai entre chaque tentative de recherche d'image
MAX_FAILED_ATTEMPTS = 3  # Nombre maximum de tentatives infructueuses avant d'agir
RIGHT_KEY_DURATION = 0.8  # Durée pendant laquelle la touche droite est enfoncée

def find_window(window_title):
    """ Fonction pour trouver la fenêtre par son titre """
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        return hwnd
    else:
        return None

def activate_window(hwnd):
    """ Fonction pour activer la fenêtre spécifiée """
    win32gui.SetForegroundWindow(hwnd)

def locate_image(image_path):
    """ Fonction pour localiser une image à l'écran """
    try:
        return pyautogui.locateCenterOnScreen(image_path, confidence=DETECTION_CONFIDENCE)
    except pyautogui.ImageNotFoundException:
        return None

def click_image(target_pos, image_path):
    """ Fonction pour cliquer sur une image trouvée """
    if target_pos:
        target_x, target_y = target_pos
        target_y += 30  # Décalage de 30 pixels vers le bas par rapport à l'image détectée
        win32api.SetCursorPos((target_x, target_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, target_x, target_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, target_x, target_y, 0, 0)
        time.sleep(1)
        keyboard.press_and_release('c')  # Simuler l'appui sur la touche 'c'
        print("Happyfarm")  # Message de confirmation de clic

def press_right_key():
    """ Fonction pour simuler l'appui sur la touche droite """
    win32api.keybd_event(win32con.VK_RIGHT, 0, 0, 0)
    time.sleep(RIGHT_KEY_DURATION)
    win32api.keybd_event(win32con.VK_RIGHT, 0, win32con.KEYEVENTF_KEYUP, 0)

def main():
    """ Fonction principale du script """
    unsuccessful_attempts = 0  # Initialisation du compteur de tentatives infructueuses
    while True:
        hwnd = find_window(WINDOW_TITLE)
        if hwnd:
            activate_window(hwnd)  # Activer la fenêtre trouvée
            for image_path in IMAGE_PATHS:
                target_pos = locate_image(image_path)
                if target_pos:
                    click_image(target_pos, image_path)
                    time.sleep(3.2)  # Attendre un peu après avoir cliqué sur l'image
                    unsuccessful_attempts = 0  # Réinitialiser les tentatives infructueuses
                    break  # Sortir de la boucle une fois une image trouvée
            else:
                print("Aucune des images n'a été trouvée.")
                time.sleep(DELAY_BETWEEN_ATTEMPTS)
                unsuccessful_attempts += 1
                if unsuccessful_attempts == MAX_FAILED_ATTEMPTS:
                    print("Appuyer sur la touche de droite pendant 1.5 seconde.")
                    press_right_key()  # Appuyer sur la touche droite en cas d'échecs répétés
                    unsuccessful_attempts = 0
        else:
            print("Fenêtre introuvable!")
            break  # Sortir de la boucle si la fenêtre n'est pas trouvée

        if keyboard.is_pressed('esc'):
            print("Boucle terminée.")
            break  # Sortir de la boucle si la touche 'esc' est pressée

if __name__ == "__main__":
    main()  # Exécuter la fonction principale si ce fichier est exécuté en tant que script
