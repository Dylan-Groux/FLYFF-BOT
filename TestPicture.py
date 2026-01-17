import cv2
import numpy as np
import os
import mss

image_folder = r"c:\wamp64\www\testrest\flyffbot\FLYFF-BOT\src\picture"

# Prendre un screenshot du deuxième écran
with mss.mss() as sct:
    monitor = sct.monitors[2]  # 2ème écran
    screenshot = np.array(sct.grab(monitor))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

# Parcourir toutes les images du dossier
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        template_path = os.path.join(image_folder, filename)
        template = cv2.imread(template_path)
        if template is None:
            print(f"Image non trouvée ou format non supporté : {template_path}")
            continue

        # Recherche de la correspondance
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7  # Ajuste selon la précision souhaitée
        loc = np.where(result >= threshold)

        # Dessine un rectangle autour de chaque correspondance trouvée
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screenshot, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
            print(f"Image trouvée : {filename} à la position {pt}")

# Affiche le résultat
cv2.imshow('Resultat', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()