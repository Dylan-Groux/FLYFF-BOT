import cv2
import numpy as np
import mss
import time
import keyboard  # Pour la gestion des touches du clavier
import os

# Constantes utilisées dans le script
IMAGE_PATHS = [  # Chemins absolus vers les images à détecter
    r"c:\wamp64\www\testrest\flyffbot\FLYFF-BOT\src\picture\Aibatt.PNG",
    r"c:\wamp64\www\testrest\flyffbot\FLYFF-BOT\src\picture\AibattBody.PNG",
    r"c:\wamp64\www\testrest\flyffbot\FLYFF-BOT\src\picture\AibattBodyName.PNG",
]
DETECTION_CONFIDENCE = 0.7  # Seuil de confiance pour la détection d'image
DELAY_BETWEEN_ATTEMPTS = 0.1  # Délai entre chaque tentative de recherche d'image
MAX_FAILED_ATTEMPTS = 3  # Nombre maximum de tentatives infructueuses avant d'agir
RIGHT_KEY_DURATION = 0.8  # Durée pendant laquelle la touche droite est enfoncée


def capture_screen3():
    """Capture tout l'écran 3 et retourne l'image sous forme de tableau numpy BGR"""
    with mss.mss() as sct:
        if len(sct.monitors) < 4:
            print("L'écran 3 n'est pas disponible.")
            return None
        monitor = sct.monitors[2]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        return screenshot


def locate_image(image_path, screenshot):
    """Localise une image dans le screenshot donné (OpenCV)"""
    if not os.path.isfile(image_path):
        print(f"Fichier image introuvable ou chemin incorrect : {image_path}")
        return None
    template = cv2.imread(image_path)
    if template is None:
        print(f"Image non trouvée ou format non supporté : {image_path}")
        return None
    try:
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= DETECTION_CONFIDENCE:
            # Retourne le centre de la zone trouvée
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        else:
            print(f"Image non trouvée à l'écran : {image_path}")
            return None
    except Exception as e:
        print(f"Erreur lors de la détection de l'image : {image_path}\n{e}")
        return None

def click_image(target_pos, image_path):
    if image_path is None:
        print("Aucun chemin d'image fourni.")
        return
    if target_pos is None:
        print(f"Impossible de cliquer : aucune position trouvée pour l'image {image_path}")
        return
    # Fonction pour cliquer sur une image trouvée
    target_x, target_y = target_pos
    target_y += 10  # Décalage de 30 pixels vers le bas par rapport à l'image détectée
    # Utilise pyautogui pour déplacer et cliquer
    import pyautogui
    pyautogui.moveTo(target_x, target_y)
    pyautogui.click()
    time.sleep(0.1)
    keyboard.press_and_release('c')  # Simuler l'appui sur la touche 'c'
    print("Happyfarm")  # Message de confirmation de clic

def press_right_key():
    """ Fonction pour simuler l'appui sur la touche droite """
    import pyautogui
    pyautogui.keyDown('right')
    time.sleep(RIGHT_KEY_DURATION)
    pyautogui.keyUp('right')

def main():
    """ Fonction principale du script """
    unsuccessful_attempts = 0  # Initialisation du compteur de tentatives infructueuses
    while True:
        screenshot = capture_screen3()
        if screenshot is not None:
            image_found = False
            for image_path in IMAGE_PATHS:
                target_pos = locate_image(image_path, screenshot)
                if target_pos:
                    click_image(target_pos, image_path)
                    time.sleep(0.5)  # Attendre un peu après avoir cliqué sur l'image
                    unsuccessful_attempts = 0  # Réinitialiser les tentatives infructueuses
                    image_found = True
                    break  # Sortir de la boucle une fois une image trouvée
            if not image_found:
                print("Aucune des images n'a été trouvée ou les fichiers sont manquants.")
                time.sleep(DELAY_BETWEEN_ATTEMPTS)
                unsuccessful_attempts += 1
                if unsuccessful_attempts == MAX_FAILED_ATTEMPTS:
                    print("Appuyer sur la touche de droite pendant 1.5 seconde.")
                    press_right_key()  # Appuyer sur la touche droite en cas d'échecs répétés
                    unsuccessful_attempts = 0
        else:
            print("Capture écran 3 impossible!")
            break  # Sortir de la boucle si la capture échoue

        if keyboard.is_pressed('esc'):
            print("Boucle terminée.")
            break  # Sortir de la boucle si la touche 'esc' est pressée

if __name__ == "__main__":
    main()  # Exécuter la fonction principale si ce fichier est exécuté en tant que script
