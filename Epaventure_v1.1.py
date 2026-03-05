#Minimum viable product du jeu "Epaventure spatiale"
# Contenu : Description d’ambiance et début du jeu
# Choix (1 seul)
# Obstacle (fixe) 1 ou 2
# Gain (fixe) 1 ou 2
# Description d’ambiance et début du jeu

#Import des librairies/Libraries import
import random
import os

#Variables
nom_perso = "Alain Connu"
score = 0
coriace = "o"
fute = 0
und6 = 0
deuxd6 = 0
jet = 0

class Epaventure:
#Classe pour manipuler le jeu
    def ecran_propre(self):
        #Effacer le terminal
        os.system('cls' if os.name == 'nt' else 'clear')

    def __init__(self):
        #Lance le jeu
        self.ecran_propre()
        print("Bienvenue dans Epaventure spatiale, le jeu où vous incarnez un pill... heu, un explorateur et sauveteur de l'espace.")
        #Création du personnage
        print("Qui est votre personnage, que sait-il faire ?")
        self.nom_perso = input("Quel est son nom ?\n")
        score = input("\nEst-il plutôt coriace (C) ou futé (F) ? Si tu tapes C, il sera bon en combat et activités physiques, F il sera bon dans les aspects techniques et analytiques.\n").upper()
        self.coriace = 0
        self.fute = 0
        #Verification
        #print("verif score :", score)
        #Boucle d'acquisition des stats des capacités
        while True:
            if score == "C":
                self.coriace += 1
                break
            elif score == "F":
                self.fute += 1
                break
            else:
                score = input("Réponse invalide, indiquez C ou F :")
        
        #print(type(self.coriace)) #verif type score coriace
        
        print("\n====================================")
        print("\nFélicitation, vous êtes", self.nom_perso, "l'intrépide explorateur·rice et serviable sauveteur·euse de l'espace (officiellement du moins...).")
        print("\nVotre score de coriace est de", self.coriace, "et votre score de futé est", self.fute, ".")
        print("\n====================================")
        
        #Intro première scène
        print("\nVous venez de quitter le havre de votre vaisseau de récupération et vous êtes désormais devant l'un des sas de l'énorme épave qui dérive dans le vide spatial.\n")

    def start(self):
        #Débuter l'aventure avec un premier choix
        print("Vous avez pénétré dans le couloir attenant au sas. Sur votre droite, il vous semble percevoir un mouvement dans l'obscurité, plus loin dans le couloir. A gauche, une porte fermée donne sur le couloir, qui continue plus loin dans l'obscurité.")
        
        print("1 : aller à droite pour découvrir ce qu'était le mouvement.")
        print("2 : tenter d'ouvrir la porte de gauche.")
        choix_1 = input("Que faites-vous ? Prenez-vous l'option 1 ou l'option 2 ?\n")
        self.premier_choix(choix_1)

    def premier_choix(self, choix):
        #Gérer le premier choix de l'aventure
        if choix == '1':
            self.explorer_couloir()
        elif choix == '2':
            self.crochetage_porte()
        else:
            print("\nChoix invalide. Boucle à implémenter.")

    #def test(): #factoriser le test et le résultat ternaire
        #Générer un nb entier aléatoire 



    def crochetage_porte(self):
        #Gère le choix d'entrer dans la pièce derrière la porte du couloir
        print("\nLe mécanisme de la porte de sécurité est bloqué en position fermée. Tu démontes le panneau de la commande et tentes de réactiver son fonctionnement.\n")
        und6 = random.randint(1,6)
        deuxd6 = random.randint(1,6)
        jet = und6 + deuxd6 + self.fute
        print("Tu obtiens un", jet, "en crochetage.")
        if jet >= 10:
            print("Tu parviens à ouvrir la porte mécanique. De l'autre côté, tu découvres une soute remplie de rubémeraudes !")
        elif jet < 10 and jet >=7:
            print("Le corps d'un officier de pont flotte dans la pièce de l'autre côté. En fouillant sa combinaison, tu récupères sa montre en platine céleste.")
        else:
            print("Tu déclenches un court-circuit et tu te brûles ! Quant à la porte, elle est définitivement bloquée...")


    def explorer_couloir(self):
        #Gère le choix d'explorer le couloir
        print("\nTu avances lentement et précautionneusement dans le couloir obscur, le faisceau de ta lampe torche déchirant les ombres. Tu arrives à un embranchement et là, soudain, une créature te saute dessus et tente de déchirer ta combinaison !\n")
        und6 = random.randint(1,6)
        deuxd6 = random.randint(1,6)
        jet = und6 + deuxd6 + self.coriace
        print("Tu obtiens un", jet, "en combat, avec un modificateur de Coriace de :", self.coriace)
        if jet >= 10:
            print("Tu parviens à tuer cette créature avec ton cutter à plasma. A tes pieds se trouve le corps de la créature et un corps, sans doute sa victime. Le corps en combinaison agrippe toujours un fusil énergétique que tu récupères.")
        elif jet < 10 and jet >=7:
            print("Tu lui enfonces dans le flanc la lame-plasma de ton cutter, et elle s'enfuit dans le noir.")
        else:
            print("La créature déchire ta combinaison et ton abdomen avant de disparaître à nouveau. Tu es blessé et perd de l'oxygène.")

# Crée une instance de la classe Jeu
jeu = Epaventure()

# Début de l'aventure
jeu.start()


#Fin de jeu
print("\nLa démo de ce jeu est terminée, merci d'avoir joué et au revoir !")
print("=====================================================")
quit()