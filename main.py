import sqlite3
import sqlite3 as lite
from pathlib import Path

conn = lite.connect("fournisseur_db")

cursor = conn.cursor()

liste_fournisseur_path = Path().cwd() / "liste_fournisseur.txt"

is_running = True
while is_running:
    choice = input("\n1: add a supplier \n2: add a bill \n3: edit a bill\n4: exit")

    #add supplier choice
    if choice.lower() == "supplier":
        nom_fournisseur = input("quel est le nom du fournisseur ?")

        with open(liste_fournisseur_path, "a") as f_0:
            f_0.write(f"{nom_fournisseur} ")

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nom_fournisseur}(N_facture, Date, nombre_de_produits, montant_HT, montant_TTC, fichier)")
        conn.commit()

    #add bill choice
    elif choice.lower() == "add bill":

        with open(liste_fournisseur_path, "r") as f_1:
            fourn = f_1.read()
            fourn_split = fourn.split()

        print(fourn_split)

        choix_fournisseur = input("sur quel fournisseur voulez inserer une facture ?")
        if choix_fournisseur in fourn_split:
            num_facture = input("quel est le numero de la facture ?")
            date = input("quelle est la date de la facture ?")
            n_produit = input("combien de produit la facture contient-elle ?")
            montant_ht = input("quel est le montant de la facture HT ?")
            montant_ttc = input("quel est le montant de la facture TTC ?")
            print(type(num_facture), type(date), type(n_produit), type(montant_ht), type(montant_ttc))

            cursor.execute(
                f"INSERT INTO {choix_fournisseur}(N_facture, Date, nombre_de_produits, montant_HT, montant_TTC) VALUES(?,?,?,?,?)",
                (num_facture, date, n_produit, montant_ht, montant_ttc))
            conn.commit()


            ajouter_fichier = input("voulez vous ajouter un fichier de la facture ?")
            if ajouter_fichier in ["y", "yes", "oui", "ok"]:
                choix_path = input(str("quel est le chemin du fichier a ajouter ?"))
                my_path = Path(choix_path)

                with open(my_path, "rb") as f:
                    my_file = f.read()
                    cursor.execute(f"UPDATE {choix_fournisseur} SET fichier=? WHERE N_facture=?",
                                   (my_file, num_facture))
                    conn.commit()
                    conn.close()

            else:
                print("vous n'ajoutez pas de fichier")


        else:
            print("aucun fournisseur de ce nom existe.")

    # edit bill choice
    elif choice.lower() =="edit bill":

            with open(liste_fournisseur_path, "r") as f_1:
                fourn = f_1.read()
                fourn_split = fourn.split()

            print(fourn_split)

            choix_fournisseur = input("sur quel fournisseur voulez modifier une facture ?")

            if choix_fournisseur in fourn_split:
                #on recupere les factures existantes dans une variable afin de l afficher
                cursor.execute(f"SELECT * FROM {choix_fournisseur}")
                row = cursor.fetchall()
                print(row)

                choix_facture = input("sur quel facture voulez vous modifier (en selectionant le numero de la facture)")
                print(type(choix_facture))
                choix_case_a_modifier = input("quel case modifier ? (N_facture, Date, nombre_de_produits, montant_HT, montant_TTC)")
                new_value = input("new value: ")
                cursor.execute(f"UPDATE {choix_fournisseur} SET {choix_case_a_modifier}={new_value} WHERE N_facture='{choix_facture}'")
                conn.commit()


            elif choix_fournisseur not in fourn_split:
                print("aucun fournisseur a ce nom")

    #exit choice
    elif choice.lower() == "exit":
        print("you leave the programm")
        is_running = False

    else:
        print(f"{choice} is not in inputs's choices")