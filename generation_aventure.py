#Import des librairies/Libraries import
import random

#Ordre de genèse conseillé:
##génération des salles
##branches
##obstacles
##butin
##sas
##équilibrage danger

#Structure : générer le graphe des salles
def generer_graphe(nb_salles, branches):
    graphe = {}
    graphe["debut"] = ["room_0"]
    for i in range(nb_salles):
        sorties = []
        sorties.append(f"room_{i+1}")
        if random.random() < branches:
            sorties.append(f"side_{i}")
        graphe[f"room_{i}"] = sorties
    graphe[f"room_{nb_salles}"] = ["fin"]
    return graphe

def ajouter_sas(scenes, nb_sas):
    salles = list(scenes.keys())
    candidats = [s for s in salles if s not in ("debut", "fin")]
    sas = random.sample(candidats, nb_sas)
    for s in sas:
        scenes[s]["type"] = "sas"
        scenes[s]["description"] += "\n\nUn sas intact mène vers l'extérieur."

def generer_aventure(taille="grande"):
    #Paramètres de dimension de l'épave
    if taille == "petite":
        nb_salles = random.randint(8, 10)
        branches = 0.25
        nb_sas = 1
    elif taille == "grande":
        nb_salles = random.randint(14, 18)
        branches = 0.4
        nb_sas = 2
    elif taille == "behemoth":
        nb_salles = random.randint(22, 30)
        branches = 0.6
        nb_sas = random.randint(3, 4)

    graphe = generer_graphe(nb_salles, branches)

    scenes = generer_scenes(graphe)

    ajouter_sas(scenes, nb_sas)

    return scenes

    #Habillage : générer le type des salles (description & ambiance)
TYPES_SALLES = [
    "couloir",
    "cabine",
    "soute",
    "atelier",
    "infirmerie"
]

SALLES_RARES = [
    "passerelle",
    "coffre",
    "salle_reacteur",
    "salle_machines"
]

DESCRIPTIONS = {
    "couloir": "Un couloir étroit envahi par les câbles.",
    "cabine": "Une cabine abandonnée flotte dans le silence.",
    "soute": "La soute est remplie de caisses dérivantes.",
    "atelier": "Un atelier technique aux machines éventrées.",
    "infirmerie": "Une infirmerie dont les instruments flottent."
}

    #Ajouter des obstacles

    #Ajouter du butin

    #Scènes & évènements : conversion en scènes JSON


    #########################ancienne version
    scenes = {}
    scenes["debut"] = {
        "description":"Tu entres dans l'épave.",
        "suivant": "salle_1"
    }
    for i in range(1, nb_salles):
        scenes[f"salle_{i}"] = {
            "description":"Une salle abandonnée.",
            "suivant": f"salle_{i+1}"
        }
    scenes[f"salle_{nb_salles}"]= {
        "description":"Un sas vers l'extérieur.",
        "suivant": "fin"        
    }

   # branche aléatoire
    if random.random() < 0.4:

        scenes["salle_3"] = {
            "description": "Une salle technique.",
            "choix": {
                "1": {"texte": "Couloir principal", "suivant": "salle_4"},
                "2": {"texte": "Conduit secondaire", "suivant": "salle_6"}
            }
        }
        
    scenes["fin"] = {
        "description": "Tu quittes l'épave."
    }
    return scenes

def enrichir_aventure(scenes):
    for nom, scene in scenes.items():
        if random.random() < 0.3:
            scene["test"] = random.choice(["combat", "fute"])
        if random.random() < 0.2:
            scene["type"] = "sas"
        if random.random() < 0.4:
            scene.setdefault("effects", {})
            scene["effets"]["reussite"] = {"loot": "ferraille"}

enrichir_aventure()
generer_obstacles()
generer_butin()
