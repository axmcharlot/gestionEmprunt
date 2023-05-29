import sqlite3
from prettytable import PrettyTable
from termcolor import cprint

class Client:
    def __init__(self):
        self.conn = sqlite3.connect('emprunt.db')
        self.c = self.conn.cursor()
        
    def __del__(self):
        self.conn.close()
    
    def afficher_clients(self):
        self.c.execute("SELECT * FROM client")
        clients = self.c.fetchall()
        if len(clients) > 0:

            # Création du tableau
            table = PrettyTable()

            # Ajout des titres de colonnes
            table.field_names = ["ID Client", "Nom", "Classe"]

            # Ajout des données dans le tableau
            for row in clients:
                table.add_row(row)

            # Affichage du tableau
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')

    def afficher_client_by_id(self, id):
        self.c.execute("SELECT idClient, nomClient, classeClient FROM client where idClient = ?",(id,))
        resultats = self.c.fetchall()
        if len(resultats) > 0:
            table = PrettyTable()
            table.field_names = ["ID Client", "Nom", "Classe"]
            for resultat in resultats:
                table.add_row([resultat[0], resultat[1], resultat[2]])
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')
    
    def afficher_client_by_key(self, key):
        self.c.execute("SELECT idClient, nomClient, classeClient FROM client where idClient = ? or nomClient like ? or classeClient like ?",(key,'%'+key+'%','%'+key+'%'))
        resultats = self.c.fetchall()
        if len(resultats) > 0:
            table = PrettyTable()
            table.field_names = ["ID Client", "Nom", "Classe"]
            for resultat in resultats:
                table.add_row([resultat[0], resultat[1], resultat[2]])
            cprint(table, 'blue')
        else:
            cprint("[!]Aucune donnees n'a ete trouvees",'yellow')
    
    def inserer_client(self, id_client, nom_client, classe_client):
        self.c.execute("INSERT INTO client VALUES (?, ?, ?)", (id_client, nom_client, classe_client))
        self.conn.commit()
        return True
        
    def modifier_client(self, id_client, nom_client, classe_client):
        self.c.execute("UPDATE client SET nomClient = ?, classeClient = ? WHERE idClient = ?", (nom_client, classe_client, id_client))
        self.conn.commit()
        return True
    
    def supprimer_client(self, id_client):
        self.c.execute("DELETE FROM client WHERE idClient = ?", (id_client,))
        self.conn.commit()
        return True
    
