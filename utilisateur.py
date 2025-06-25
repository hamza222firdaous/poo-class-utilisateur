from datetime import datetime

class Utilisateur:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.livres_empruntes = {}  # isbn: date_emprunt
        self.historique_emprunts = []
        self.penalise = False
        self.nb_retards = 0

    def emprunter_livre(self, bibliotheque, isbn):
        if self.penalise or len(self.livres_empruntes) >= 3:
            print("Limite atteinte ou utilisateur pénalisé.")
            return
        livre = bibliotheque.livres.get(isbn)
        if livre and livre.emprunter():
            self.livres_empruntes[isbn] = datetime.now()
            print(f"Livre {livre.titre} emprunté.")
        else:
            print("Livre indisponible.")

    def retourner_livre(self, bibliotheque, isbn):
        if isbn in self.livres_empruntes:
            livre = bibliotheque.livres.get(isbn)
            date_emprunt = self.livres_empruntes.pop(isbn)
            livre.retourner()
            self.historique_emprunts.append((isbn, date_emprunt, datetime.now()))

            if (datetime.now() - date_emprunt).days > 15:
                self.nb_retards += 1
                if self.nb_retards >= 3:
                    self.penalise = True
                    print("Utilisateur pénalisé pour retards répétés.")
            print(f"Livre {livre.titre} retourné.")

    def afficher_emprunts(self):
        for isbn, date in self.livres_empruntes.items():
            print(f"{isbn} emprunté le {date.date()}")

    def afficher_historique(self):
        for isbn, debut, fin in self.historique_emprunts:
            print(f"{isbn} : du {debut.date()} au {fin.date()}")