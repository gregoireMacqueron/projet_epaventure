#Import des librairies/Libraries import
import random

#Ordre de genèse conseillé:
##génération des salles : FAIT via generer_graphe
##branches : FAIT via intégration à generer_graphe
##obstacles TO DO
##butin TO DO
##sas FAIT via ajouter_sas
#Scènes & évènements : conversion en scènes JSON
    
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
    else:
        raise ValueError(f"Taille inconnue : {taille!r} (attendu : petite, grande, behemoth)")
    
    graphe = generer_graphe(nb_salles, branches)
    scenes = generer_scenes(graphe)
    ajouter_sas(scenes, nb_sas)
    return scenes

def generer_scenes(graphe):
    """Stub : version minimale pour les tests, à compléter."""
    scenes = {}
    for nom in graphe:
        scenes[nom] = {
            "description": "Une salle de l'épave, parmi tant d'autres.",  #description générique
            "suivants": graphe[nom]
        }
    return scenes

def enrichir_aventure(scenes):
    for nom, scene in scenes.items():
        if random.random() < 0.3:
            scene["test"] = random.choice(["combat", "fute"])
        if random.random() < 0.2:
            scene["type"] = "sas"
        if random.random() < 0.4:
            scene.setdefault("effets", {})
            scene["effets"]["reussite"] = {"loot": "ferraille"}

