#Import des librairies/Libraries import
import random

#Ordre de genèse conseillé:
##génération des salles
##branches
##obstacles
##butin
##sas
##équilibrage danger

def generer_aventure(nb_salles=10):
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
