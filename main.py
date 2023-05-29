import empruntMat
import cliennt
import materiel as M
from colorama import Fore, Style
import re
from termcolor import cprint

def client():
        print("-"*30)
        print("|"+" "*10+Fore.GREEN+"CLIENTS"+Style.RESET_ALL+" "*10+"|")
        print("-"*30)
        # Instructions pour client ici
        c = cliennt.Client()
        print("Entrez une commande ('a' pour afficher la liste des commandes disponibles, 'q' pour revenir au menu principal)")

        p = r"modifier\s(.+)"
        p1 = r"supprimer\s(.+)"
        p2 = r"chercher\s(.+)"

        while True:
            ch = input("[Client]>>> ").strip()

            if ch == 'a':
                print(Fore.GREEN+"a"+Style.RESET_ALL+" : lister tous les commandes disponibles")
                print(Fore.GREEN+"ajouter"+Style.RESET_ALL+" : lister tous les commandes disponibles")
                print(Fore.GREEN+"chercher"+Style.RESET_ALL+" [cle]: chercher des clients a partir id du client, nom, classe")
                print(Fore.GREEN+"lt"+Style.RESET_ALL+" : lister tous les materiels")
                print(Fore.GREEN+"modifier"+Style.RESET_ALL+" [id]: modifier les proprietes d'un client avec l'id entree")
                print(Fore.GREEN+"supprimer"+Style.RESET_ALL+" [id]: supprimer les donnees d'un client avec l'id entree")
                print(Fore.GREEN+"q"+Style.RESET_ALL+" : revenir au menu principal")
            elif ch == 'q':
                break
            elif ch == 'ajouter':
                id_client = input("Entrez l'idClient du nouveau client : ")
                nom_client = input("Entrez le nom du nouveau client : ")
                classe_client = input("Entrez la classe du nouveau client : ")
                if c.inserer_client(id_client, nom_client, classe_client):
                    cprint("[+]Ajout de client effectue avec succes.", 'green')
                    c.afficher_clients()
                else:
                    cprint("[-]Une erreur s'est produite", 'red')
            elif re.match(p, ch):
                id_materiel = (ch.split(" ")[1]).title()
                c.c.execute("SELECT idClient FROM client where idClient = ?",(id_materiel,))
                ids = c.c.fetchall()
                if (id_materiel,) in ids:
                    c.afficher_client_by_id(id_materiel)
                    nom_materiel = input("Entrez le nom du client : ").title()
                    classe_materiel = input("Entrez la classe du client : ").upper()
                    if c.modifier_client(id_materiel, nom_materiel, classe_materiel):
                        cprint("[+]Modification du client effectue avec succes.", 'green')
                    else:
                        cprint("[-]Une erreur s'est produite", 'red')
                else:
                    cprint("[-]Client non reconnu", 'red')
            elif re.match(p1, ch):
                id_materiel = (ch.split(" ")[1]).title()
                c.c.execute("SELECT idClient FROM client where idClient = ?",(id_materiel,))
                ids = c.c.fetchall()
                if (id_materiel,) in ids:
                    cprint("[!]Voulez-vous vraiment supprimer?(o/n)")
                    resp = input().lower()
                    if resp == 'o':
                        if c.supprimer_client(id_materiel):
                            cprint("[+]Le client a ete retire avec succes.", 'green')
                        else:
                            cprint("[-]Une erreur s'est produite", 'red')
                    else:
                        return
                else:
                    cprint("[-]Materiel non reconnu", 'red')
            elif re.match(p2, ch):
                key = (ch.split(" ")[1]).title()
                c.afficher_client_by_key(key)
            elif ch == 'lt':
                c.afficher_clients()
            else:
                cprint("[-]Commande introuvable ou incomplete.", 'red')
                cprint("[!]Taper 'a' pour voir la liste des commandes valides",'yellow')


def materiel():
    print("-"*30)
    print("|"+" "*10+Fore.GREEN+"MATERIELS"+Style.RESET_ALL+" "*10+"|")
    print("-"*30)
    # Instructions pour matériel ici
    m = M.Materiel()
    print("Entrez une commande ('a' pour afficher la liste des commandes disponibles, 'q' pour revenir au menu principal)")

    p = r"modifier\s(.+)"
    p1 = r"supprimer\s(.+)"
    p2 = r"chercher\s(.+)"

    while True:
        ch = input("[Materiel]>>> ").strip()

        if ch == 'a':
            print(Fore.GREEN+"a"+Style.RESET_ALL+" : lister tous les commandes disponibles")
            print(Fore.GREEN+"ajouter"+Style.RESET_ALL+" : lister tous les commandes disponibles")
            print(Fore.GREEN+"chercher"+Style.RESET_ALL+" [cle]: chercher des materiels a partir id du materiel, designation, nombre")
            print(Fore.GREEN+"lt"+Style.RESET_ALL+" : lister tous les materiels")
            print(Fore.GREEN+"modifier"+Style.RESET_ALL+" [id]: modifier les proprietes de l'emprunt avec l'id entree")
            print(Fore.GREEN+"supprimer"+Style.RESET_ALL+" [id]: supprimer les donnees d'un materiel avec l'id entree")
            print(Fore.GREEN+"q"+Style.RESET_ALL+" : revenir au menu principal")
        elif ch == 'q':
            break
        elif ch == 'ajouter':
            idM = input("Entrez l'ID du materiel: ").title()
            des = input("Entrez la designation du materiel: ").title()
            stock = int(input("Entrez le nombre de materiel a ajouter: "))
            if m.ajouter_materiel(idM,des,stock):
                cprint("[+]Ajout de materiel effectue avec succes.", 'green')
                m.afficher_materiel()
            else:
                cprint("[-]Une erreur s'est produite", 'red')
        elif re.match(p, ch):
            id_materiel = (ch.split(" ")[1]).title()
            m.c.execute("SELECT idMat FROM materiel where idMat = ?",(id_materiel,))
            ids = m.c.fetchall()
            if (id_materiel,) in ids:
                m.afficher_materiel_by_id(id_materiel)
                nom_materiel = input("Entrez la nouvelle designation du materiel : ")
                classe_materiel = input("Entrez le nouveau nombre en stock : ")
                if m.modifier_materiel(id_materiel, nom_materiel, classe_materiel):
                    cprint("[+]Modification du materiel effectue avec succes.", 'green')
                else:
                    cprint("[-]Une erreur s'est produite", 'red')
            else:
                cprint("[-]Materiel non reconnu", 'red')
        elif re.match(p1, ch):
            id_materiel = (ch.split(" ")[1]).title()
            m.c.execute("SELECT idMat FROM materiel where idMat = ?",(id_materiel,))
            ids = m.c.fetchall()
            if (id_materiel,) in ids:
                cprint("[!]Voulez-vous vraiment supprimer?(o/n)")
                resp = input().lower()
                if resp == 'o':
                    if m.supprimer_materiel(id_materiel):
                        cprint("[+]Suppression du materiel effectue avec succes.", 'green')
                    else:
                        cprint("[-]Une erreur s'est produite", 'red')
                else:
                    return
            else:
                cprint("[-]Materiel non reconnu", 'red')
        elif re.match(p2, ch):
            key = (ch.split(" ")[1]).title()
            m.afficher_materiel_by_key(key)
        elif ch == 'lt':
            m.afficher_materiel()
        else:
            cprint("[-]Commande introuvable ou incomplete.", 'red')
            cprint("[!]Taper 'a' pour voir la liste des commandes valides",'yellow')

def emprunte():
    print("-"*30)
    print("|"+" "*10+Fore.GREEN+"EMPRUNTS"+Style.RESET_ALL+" "*10+"|")
    print("-"*30)
    print(Fore.CYAN + "-> Ici, vous pouvez rechercher, effectuer des emprunts ou rendre des materiels" + Style.RESET_ALL)
    # Instructions pour emprunt matériel ici
    m = empruntMat.emprunt("emprunt.db")
    print("Entrez une commande ('a' pour afficher la liste des commandes disponibles, 'q' pour revenir au menu principal)")
    p = r'^rendre \d+$'
    p2 = r'^modifier \d+$'
    p3 = r'^supprimer \d+$'
    p4 = r"chercher\s(.+)"
    while True:
        sub_choice = input("[Emprunt]>>> ").strip()
        if sub_choice == 'a':
            print(Fore.GREEN+"a"+Style.RESET_ALL+" : lister tous les commandes disponibles")
            print(Fore.GREEN+"chercher"+Style.RESET_ALL+" [cle]: chercher des materiels non rendus a partir id du client, date d'emprunt, nombre, id du materiel")
            print(Fore.GREEN+"emprunter"+Style.RESET_ALL+" : effectuer un nouvel emprunt")
            print(Fore.GREEN+"lt"+Style.RESET_ALL+" : lister tous les emprunts")
            print(Fore.GREEN+"lr"+Style.RESET_ALL+" : lister les emprunts rendus")
            print(Fore.GREEN+"lnr"+Style.RESET_ALL+" : lister les emprunts non rendus")
            print(Fore.GREEN+"modifier"+Style.RESET_ALL+" [id]: modifier les proprietes de l'emprunt avec l'id entree")
            print(Fore.GREEN+"rendre"+Style.RESET_ALL+" [id]: rendre le materiel avec l'id entree")
            print(Fore.GREEN+"supprimer"+Style.RESET_ALL+" [id]: supprimer les donnees d'emprunt avec l'id entree")
            print(Fore.GREEN+"q"+Style.RESET_ALL+" : revenir au menu principal")
        elif sub_choice == 'q':
            break
        elif sub_choice == 'lt':
            m.afficheTablee("emprunt")
        elif sub_choice == 'lnr':
            m.afficheNonRendus("emprunt")
        elif sub_choice == 'lr':
            m.afficheRendus("emprunt")
        elif sub_choice == 'emprunter':
            m.empruntmat("emprunt")
            m.afficheNonRendus()
        elif re.match(p4, sub_choice):
            id = sub_choice.split(" ")[1]
            m.chercherEmpruntNonRendu(id,"emprunt")
        elif re.match(p3, sub_choice):
            id = sub_choice.split(" ")[1]
            cprint("[!]Voulez-vous vraiment supprimer?(o/n)")
            resp = input().lower()
            if resp == 'o':
                m.supprimerempruntmat("emprunt",id)
            else:
                return
        elif re.match(p2, sub_choice):
            id = sub_choice.split(" ")[1]
            m.modifierempruntmat("emprunt",id)
        elif re.match(p, sub_choice):
            id = sub_choice.split(" ")[1]
            m.rendreMateriel("emprunt",id)
        else:
            cprint("[-]Commande introuvable ou incomplete.", 'red')
            cprint("[!]Taper 'a' pour voir la liste des commandes valides", 'yellow')



def quit_program():
    print("------------------------------------")
    print(Fore.CYAN + "Au revoir !" + Style.RESET_ALL)
    quit()


if __name__ == '__main__':
    print("Bienvenue dans le logiciel de gestion d'emprunt de materiels")

    options = {
        "1": emprunte,
        "2": materiel,
        "3": client,
        "4": quit_program,
    }

    while True:
        print('-'*38)
        print("|"+Fore.GREEN + "            MENU PRINCIPAL" + Style.RESET_ALL + "          |")
        print("|"+Fore.BLUE + "1. Emprunts" + Style.RESET_ALL + "                         |")
        print("|"+Fore.BLUE + "2. Matériels" + Style.RESET_ALL + "                         |")
        print("|"+Fore.BLUE + "3. Clients" + Style.RESET_ALL + "                          |")
        print("|"+Fore.RED + "4. Quitter" + Style.RESET_ALL + "                          |")
        print('-'*38)

        choice = input("Entrez votre choix (1-4): ")
        action = options.get(choice)
        if action:
            action()
        else:
            print(Fore.LIGHTRED_EX + "Choix invalide. Réessayez.\n" + Style.RESET_ALL)