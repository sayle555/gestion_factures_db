import sqlite3
import sqlite3 as lite
from pathlib import Path

conn = lite.connect("fournisseur_db")

cursor = conn.cursor()

liste_fournisseur_path = Path().cwd() / "liste_fournisseur.txt"





while True:
    choix = input("voulez vous ajouter un fournisseur ? y/n").lower()
    if choix in ["y","yes","oui","ok"]:
        nom_fournisseur=input("quel est le nom du fournisseur ?")

        with open(liste_fournisseur_path, "a") as f_0:
            f_0.write(f"{nom_fournisseur} ")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nom_fournisseur}(Date, N_facture, nombre_de_produits, montant_HT, montant_TTC, fichier)")
        conn.commit()
    else:
        break


while True:
    choix_ajouter_facture=input("Voulez vous ajouter une facture ?")

    if choix_ajouter_facture in ["y","yes","oui","ok"]:

        """renvoie une liste de tuples des noms des tables / ex: [('table1',), ('table2'), ('table3')]
        cependant lorsque je tape "table1" pour y acceder, ca ne marche pas"""
        # cursor.execute("SELECT name FROM sqlite_master WHERE type ='table'")
        # conn.commit()
        # lines = cursor.fetchall()
        # print(lines)

        with open(liste_fournisseur_path, "r") as f_1:
            fourn = f_1.read()
            fourn_split=fourn.split()

        print(fourn_split)

        choix_fournisseur = input("sur quel fournisseur voulez inserer une facture ?")
        if choix_fournisseur in fourn_split:
            date=input("quelle est la date de la facture ?")
            num_facture = input("quel est le numero de la facture ?")
            n_produit = input("combien de produit la facture contient-elle ?")
            montant_ht = input("quel est le montant de la facture HT ?")
            montant_ttc = input("quel est le montant de la facture TTC ?")

            cursor.execute(f"INSERT INTO {choix_fournisseur}(Date, N_facture, nombre_de_produits, montant_HT, montant_TTC) VALUES(?,?,?,?,?)", (date, num_facture, n_produit, montant_ht, montant_ttc))
            conn.commit()

            ajouter_fichier=input("voulez vous ajouter un fichier de la facture ?")
            if ajouter_fichier in ["y","yes","oui","ok"]:
                choix_path = input(str("quel est le chemin du fichier a ajouter ?"))
                my_path = Path(choix_path)

                with open(my_path, "rb") as f:
                    my_file = f.read()
                    cursor.execute(f"UPDATE {choix_fournisseur} SET fichier=? WHERE N_facture=?",(my_file,num_facture))
                    conn.commit()

            else:
                break


        elif choix_fournisseur not in fourn_split:
            print("aucun fournisseur de ce nom existe.")

    else:
        break

