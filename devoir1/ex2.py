contacts = []

while True:
    print("\n1. Ajouter contact")
    print("2. Afficher contacts")
    print("3. Quitter")

    choix = input("Choix : ")

    if choix == "1":
        nom = input("Nom : ")
        contacts.append(nom)

    elif choix == "2":
        if len(contacts) == 0:
            print("Aucun contact.")
        else:
            for i, c in enumerate(contacts, 1):
                print(i, "-", c)

    elif choix == "3":
        print("Au revoir !")
        break

    else:
        print("Choix invalide")
