#Les imports
import json
import os

from collections import deque

#Afficher la distance jusqu’à la sortie (fin)
def distance_sortie(scenes, scene_depart, scene_fin="fin"):

    file = deque([(scene_depart, 0)])
    visites = set()

    while file:
        scene, dist = file.popleft()

        if scene == scene_fin:
            return dist

        if scene in visites:
            continue

        visites.add(scene)

        data = scenes[scene]

        if "suivant" in data:
            file.append((data["suivant"], dist + 1))

        if "choix" in data:
            for choix in data["choix"].values():
                file.append((choix["suivant"], dist + 1))

    return None

#Graphe des scènes du jeu
chemin = os.path.join(os.path.dirname(__file__),"Aventure_scenes.json")
with open(chemin, "r", encoding="utf-8") as fichier:
    scenes = json.load(fichier) 

print("Carte de l'aventure : \n")

for nom_scene, scene in scenes.items():

    #Transitions simples
    if "suivant" in scene:
        dist = distance_sortie(scenes, scene["suivant"])
        print(f"{nom_scene} - > {scene['suivant']} (distance sortie : {dist})")
    #Transition par choix
    if "choix" in scene:
        for numero, choix_data in scene["choix"].items():
            dist = distance_sortie(scenes, choix_data["suivant"])
            print(f"{nom_scene} -> {choix_data['suivant']} (distance sortie : {dist})")

#Détection des scènes inexistantes
print("\nVérification des scènes :\n")
erreur_trouvee = False

for nom_scene, scene in scenes.items():

    if "suivant" in scene and scene["suivant"] not in scenes:
        print("⚠ scène inconnue :", scene["suivant"])
        erreur_trouvee = True

    if "choix" in scene:
        for choix_data in scene["choix"].values():
            if choix_data["suivant"] not in scenes:
                print("⚠ scène inconnue :", choix_data["suivant"])
                erreur_trouvee = True
if not erreur_trouvee:
    print("Toutes les scènes référencées existent. Aucun problème détecté.\ns")

