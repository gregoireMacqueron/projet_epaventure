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

#Détection des scènes inaccessibles
def scenes_inaccessibles(scenes, depart="debut"):
    visites=set()
    file = deque([depart])
    while file:
        scene = file.popleft()
        if scene in visites:
            continue
        visites.add(scene)
        data = scenes.get(scene, {})
        
        if "suivant" in data:
            file.append(data["suivant"])

        if "choix" in data:
            for choix in data["choix"].values():
                file.append(choix["suivant"])
    return set(scenes.keys()) - visites                                        

#Détection de boucle
def detecter_boucles(scenes):
    boucles = []
    for depart in scenes:
        file = deque([(depart, [])])
        visites = set()
        
        while file:
            scene, chemin = file.popleft()

            if scene in chemin:
                boucles.append(chemin + [scene])
                break
            data = scenes.get(scene, {})
            transitions = []

            if "suivant" in data:
                transitions.append(data["suivant"])
            if "choix" in data:
                for choix in data["choix"].values():
                    transitions.append(data["suivant"])
            
            for t in transitions:
                file.append(t, chemin + [scene])
    return boucles


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

#Détection des scènes inexistantes ou inaccessibles
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

print("\nScènes inaccessibles :")
inaccessibles = scenes_inaccessibles(scenes)
if inaccessibles:
    for s in inaccessibles:
        print("⚠", s)
else:
    print("Aucune scène inaccessible.")        

#Détection de culs-de-sac (scènes sans choix, "suivant" ou fin)
print("\nCuls-de-sac potentiels :")
dead_ends = []
for nom_scene, scene in scenes.items():
    if nom_scene == "fin:"
        continue
    if "suivant" not in scene and "choix" not in scene:
        dead_ends.append(nom_scene)
if dead_ends:
    for s in dead_ends:
        print("⚠", s)
else:
    print("Aucun cul-de-sac.")

#Affichage des boucles
print("\nBoucles détectées :")

boucles = detecter_boucles(scenes)

if boucles:
    for b in boucles:
        print("⚠ boucle :", " -> ".join(b))
else:
    print("Aucune boucle détectée.") 