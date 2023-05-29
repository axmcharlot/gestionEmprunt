import sqlite3
from prettytable import PrettyTable
from datetime import datetime
from colorama import Fore, Style
from termcolor import cprint
import cliennt
import materiel as MM

class emprunt:
    def __init__(self, nom_bdd):
        # Connexion à la base de données
        self.connexion = sqlite3.connect(nom_bdd)
        self.curseur = self.connexion.cursor()

    def afficheTablee(self, nom_table):
        self.curseur.execute(f"SELECT * FROM {nom_table}")
        resultat = self.curseur.fetchall()
        if len(resultat) > 0:
            # Création du tableau
            table = PrettyTable()

            # Ajout des titres de colonnes
            table.field_names = ["ID", "ID Client", "ID Matériel", "Nombre de matériel", "Date et heure emprunté", "Date et heure rendu", "Observation"]

            # Ajout des données dans le tableau
            for row in resultat:
                table.add_row(row)

            # Affichage du tableau
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')

    def afficheNonRendus(self, nom_table):
        self.curseur.execute(f"SELECT * FROM {nom_table} where dateRen is null")
        resultat = self.curseur.fetchall()

        if len(resultat) > 0:

            # Création du tableau
            table = PrettyTable()

            # Ajout des titres de colonnes
            table.field_names = ["ID", "ID Client", "ID Matériel", "Nombre de matériel", "Date et heure emprunté", "Date et heure rendu", "Observation"]

            # Ajout des données dans le tableau
            for row in resultat:
                table.add_row(row)

            # Affichage du tableau
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')
    
    def afficheRendus(self, nom_table):
        self.curseur.execute(f"SELECT * FROM {nom_table} where dateRen is not null")
        resultat = self.curseur.fetchall()
        if len(resultat) > 0:
            # Création du tableau
            table = PrettyTable()

            # Ajout des titres de colonnes
            table.field_names = ["ID", "ID Client", "ID Matériel", "Nombre de matériel", "Date et heure emprunté", "Date et heure rendu", "Observation"]

            # Ajout des données dans le tableau
            for row in resultat:
                table.add_row(row)

            # Affichage du tableau
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')
    
    def rendreMateriel(self, nom_table, id):
        maintenant = datetime.now().strftime("%d %B %Y %H:%M:%S")
        #id = int(id)
        self.curseur.execute("select * from emprunt where id = ? and dateRen is null", (id,))
        res = self.curseur.fetchone()

        if len(res) == 0:
            cprint("[!]ID inconnu ou materiel deja rendu",'yellow')
            return
        
        obs = input("Observations sur le materiel a rendre: ")

        c = self.connexion.cursor()
        c.execute(f"UPDATE {nom_table} SET dateRen = ?, observation = ? where id = ? and dateRen is null", (maintenant, obs, id))
        self.connexion.commit()

        # Mise à jour de la valeur de la colonne stock dans la table materiel
        self.curseur.execute("select nombre, idMat from emprunt where id = ?", (id,))
        r = self.curseur.fetchone()
        nomb = r[0]
        idMat = r[1]

        self.curseur.execute(f"UPDATE materiel SET stock = stock + ? WHERE idMat = ?", (nomb,idMat,))
        self.connexion.commit()

        cprint("[+]Succes", 'green')


    def empruntmat(self, nom_table):
        # Saisie des données utilisateur
        cObj = cliennt.Client()
        cObj.afficher_clients()
        client = input("Entrez l'ID du client : ").title()

        # Vérification de l'existence du client dans la table client
        self.curseur.execute("SELECT idClient from client where idClient=?", (client,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Le client n'apparait pas dans la base de donnees" + Style.RESET_ALL)
            return

        self.curseur.execute("SELECT emprunt.idClient FROM client join emprunt on client.idClient=emprunt.idClient WHERE client.idClient = ? and client.idClient not in (select idClient from emprunt where dateRen is null) ", (client,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.YELLOW + "[!]Ce client  n'a pas encore rendu un materiel" + Style.RESET_ALL)

        # Saisie des données utilisateur
        mObj = MM.Materiel()
        mObj.afficher_materiel()
        materielID= input("Entrez l'ID du matériel emprunté : ").title()

        # Vérification de l'existence du matériel dans la table materiel
        self.curseur.execute("SELECT * FROM materiel WHERE idMat = ?", (materielID,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Matériel spécifié n'existe pas dans la Base de données." + Style.RESET_ALL)
            return


        # Vérification de l'existence du matériel si encore disponible dans la table materiel
        self.curseur.execute("SELECT * FROM materiel WHERE idMat = ? AND stock > 0", (materielID,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Matériel spécifié n'est plus disponnible." + Style.RESET_ALL)
            return

        nomb = int(input("Entrez le nombre: "))

        self.curseur.execute("select stock from materiel where idMat = ?", (materielID,))
        res = self.curseur.fetchone()
        if int(res[0]) < nomb:
            cprint("[!]Materiel insufisant pour effectuer l'emprunt",'yellow')
            return

        maintenant = datetime.now().strftime("%d %B %Y %H:%M:%S")

        # Insertion des données dans la table
        self.curseur.execute(f"INSERT INTO {nom_table} (idClient, idMat, nombre, dateEmp, dateRen, observation) "
                             "VALUES (?, ?, ?, ?, NULL, '')", (client, materielID, nomb, maintenant))
        self.connexion.commit()

        # Mise à jour de la valeur de la colonne stock dans la table materiel
        self.curseur.execute(f"UPDATE materiel SET stock = stock - ? WHERE idMat = ?", (nomb,materielID,))
        self.connexion.commit()

        print("------------------------------------")
        print(Fore.GREEN + "[+]Emprunt effectue succès." + Style.RESET_ALL)
        

    def modifierempruntmat(self, nom_table,id_emprunt):
        # Saisie de l'ID de l'emprunt à modifier
    
        # Vérification de l'existence de l'emprunt dans la table emprunt
        self.curseur.execute("SELECT * FROM emprunt WHERE id = ?", (id_emprunt,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Emprunt spécifié n'existe pas dans la Base de données." + Style.RESET_ALL)
            return

        # Vérification si la colonne dateRen est NULL et observation est vide
        if result[5] is not None or result[6]:
            print("------------------------------------")
            print(
                Fore.RED + "[-]Impossible de modifier l'emprunt car la matériel spécifié a déja ete rendu." + Style.RESET_ALL)
            return

        # Saisie des nouvelles données utilisateur
        client = input("Entrez le nouvel ID du client : ").title()


        # Vérification de l'existence du client dans la table client
        self.curseur.execute("SELECT * FROM client WHERE idClient = ?", (client,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Client spécifié n'existe pas dans la Base de données." + Style.RESET_ALL)
            return

        materiel = input("Entrez le nouvel ID du matériel emprunté : ").title()
        # Vérification de l'existence du matériel dans la table materiel
        self.curseur.execute("SELECT * FROM materiel WHERE idMat = ?", (materiel,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Matériel spécifié n'existe pas dans la Base de données." + Style.RESET_ALL)
            return

        # Modification des données dans la table
        self.curseur.execute(f"UPDATE {nom_table} SET idClient = ?, idMat = ? WHERE id = ?",
                             (client, materiel, id_emprunt))
        self.connexion.commit()

        print("------------------------------------")
        print(Fore.GREEN + "[+]Enregistrement modifié avec succès." + Style.RESET_ALL)

    def supprimerempruntmat(self, nom_table,id_emprunt):
        
        # Saisie de l'ID de l'emprunt à supprimer

        # Vérification de l'existence de l'emprunt dans la table emprunt
        self.curseur.execute(f"SELECT * FROM {nom_table} WHERE id = ?", (id_emprunt,))
        result = self.curseur.fetchone()
        if result is None:
            print("------------------------------------")
            print(Fore.RED + "[-]Emprunt spécifié n'existe pas dans la Base de données." + Style.RESET_ALL)
            return
        # Suppression de l'emprunt dans la table
        self.curseur.execute(f"DELETE FROM {nom_table} WHERE id = ?", (id_emprunt))
        self.connexion.commit()

        print("------------------------------------")
        print(Fore.GREEN + "[+]Emprunt supprimé avec succès." + Style.RESET_ALL)

    def chercherEmpruntNonRendu(self, key, nom_table):
        self.curseur.execute(f"SELECT * FROM {nom_table} where (idMat = ? or idClient = ? or dateEmp = ? or nombre = ?) and dateRen is null",(key.title(),key.title(),key,key,))
        resultat = self.curseur.fetchall()

        if len(resultat) > 0:
            
            # Création du tableau
            table = PrettyTable()

            # Ajout des titres de colonnes
            table.field_names = ["ID", "ID Client", "ID Matériel", "Nombre de matériel", "Date et heure emprunté", "Date et heure rendu", "Observation"]

            # Ajout des données dans le tableau
            for row in resultat:
                table.add_row(row)

            # Affichage du tableau
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouve", "yellow")
