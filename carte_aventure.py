#Les imports
import json

#Graphe des scènes du jeu
with open("Aventure_scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

print("Carte de l'aventure : \n")

for nom_scene, scene in scenes.items():

    #Transitions simples
    if "suivant" in scene:
        print(f"{nom_scene} - > {scene['suivant']}")
    #Transition par choix
    if "choix" in scene:
        for numero, choix_data in scene["choix"].items():
            print(f"{nom_scene} - > {choix_data['suivant']}")

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
