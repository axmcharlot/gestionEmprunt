import sqlite3
from prettytable import PrettyTable
from termcolor import cprint

class Materiel:
    def __init__(self):
        self.conn = sqlite3.connect('emprunt.db')
        self.c = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()

    def ajouter_materiel(self, idMateriel, designation, stock):
        self.c.execute("INSERT INTO materiel VALUES (?, ?, ?)",(idMateriel, designation, stock))
        self.conn.commit()
        return True

    def afficher_materiel(self):
        self.c.execute("SELECT idMat, designation, stock FROM materiel")
        resultats = self.c.fetchall()
        if len(resultats) > 0:
            table = PrettyTable()
            table.field_names = ["ID Matériel", "Désignation", "Stock"]
            for resultat in resultats:
                table.add_row([resultat[0], resultat[1], resultat[2]])
            cprint(table, 'blue')
        else:
            cprint("[!] Aucune données n'a été trouvées",'yellow')

    def afficher_materiel_by_id(self, id):
        self.c.execute("SELECT idMat, designation, stock FROM materiel where idMat = ?",(id,))
        resultats = self.c.fetchall()
        if len(resultats) > 0:
            table = PrettyTable()
            table.field_names = ["ID Matériel", "Désignation", "Stock"]
            for resultat in resultats:
                table.add_row([resultat[0], resultat[1], resultat[2]])
            cprint(table, 'blue')
        else:
            cprint("[!] Aucune données n'a été trouvées",'yellow')

    def afficher_materiel_by_key(self, key):
        self.c.execute("SELECT idMat, designation, stock FROM materiel where idMat = ? or designation like ? or stock = ?",(key,'%'+key+'%',key))
        resultats = self.c.fetchall()
        if len(resultats) > 0:
            table = PrettyTable()
            table.field_names = ["ID Matériel", "Désignation", "Stock"]
            for resultat in resultats:
                table.add_row([resultat[0], resultat[1], resultat[2]])
            cprint(table, 'blue')
        else:
            cprint("[!] Aucune donnees n'a été trouvées",'yellow')

    def modifier_materiel(self, id_mat, designation, stock):
        self.c.execute("UPDATE materiel SET designation = ?, stock = ? WHERE idMat = ?", (designation, stock, id_mat))
        self.conn.commit()
        return True
        

    def supprimer_materiel(self, id_mat):
        self.c.execute("DELETE FROM materiel WHERE idMat = ?", (id_mat,))
        self.conn.commit()
        return True

