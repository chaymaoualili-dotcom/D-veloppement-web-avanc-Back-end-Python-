a = float(input("Nombre 1 : "))
b = float(input("Nombre 2 : "))

print("1: +")
print("2: -")
print("3: *")
print("4: /")

choix = input("Opération : ")

if choix == "1":
    print("Résultat :", a + b)

elif choix == "2":
    print("Résultat :", a - b)

elif choix == "3":
    print("Résultat :", a * b)

elif choix == "4":
    if b == 0:
        print("Erreur : division par zéro")
    else:
        print("Résultat :", a / b)

else:
    print("Choix invalide")