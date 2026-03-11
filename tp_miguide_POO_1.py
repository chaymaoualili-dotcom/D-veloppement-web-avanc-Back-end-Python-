# ============================================================
# TP MI-GUIDÉ — CONSTRUCTION PROGRESSIVE D'UN SYSTÈME DE BOISSONS
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ============================================================
# PARTIE 1 : Classe abstraite Boisson
# ============================================================

class Boisson(ABC):

    @abstractmethod
    def cout(self):
        pass

    @abstractmethod
    def description(self):
        pass

    # PARTIE 4 : Combinaison de boissons avec l'opérateur +
    def __add__(self, other):
        desc_combinee = self.description() + " + " + other.description()
        prix_total = self.cout() + other.cout()

        # On crée une boisson anonyme combinée
        class BoissonCombinee(Boisson):
            def cout(self_inner):
                return prix_total
            def description(self_inner):
                return desc_combinee

        return BoissonCombinee()


# ============================================================
# PARTIE 2 : Boissons concrètes
# ============================================================

class Cafe(Boisson):

    def cout(self):
        return 2.0

    def description(self):
        return "Café simple"


class The(Boisson):

    def cout(self):
        return 1.5

    def description(self):
        return "Thé"


# ============================================================
# PARTIE 3 : Décorateurs d'ingrédients
# ============================================================

class DecorateurBoisson(Boisson):

    def __init__(self, boisson):
        self._boisson = boisson


class Lait(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.5

    def description(self):
        return self._boisson.description() + ", Lait"


class Sucre(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.2

    def description(self):
        return self._boisson.description() + ", Sucre"


# PARTIE 6 — Tâche 1 : Ingrédient supplémentaire Caramel
class Caramel(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.7

    def description(self):
        return self._boisson.description() + ", Caramel"


# ============================================================
# PARTIE 5 : Représentation d'un client (dataclass)
# ============================================================

@dataclass
class Client:
    nom: str
    numero: int
    points_fidelite: int = 0


# ============================================================
# PARTIE 6 — Tâche 3 : Méthode d'affichage d'une commande complète
# (intégrée dans la classe Commande ci-dessous)
# ============================================================

# ============================================================
# PARTIE 7 : Gestion des commandes
# ============================================================

# --- 7.1  Classe de base Commande ---
class Commande:

    def __init__(self, client):
        self.client = client
        self.boissons = []

    def ajouter_boisson(self, boisson):
        self.boissons.append(boisson)

    def prix_total(self):
        return sum(b.cout() for b in self.boissons)

    def afficher(self):
        print(f"Client       : {self.client.nom} (n°{self.client.numero})")
        for b in self.boissons:
            print(f"  Commande   : {b.description()}")
            print(f"  Prix       : {b.cout():.2f}€")
        print(f"Total        : {self.prix_total():.2f}€")


# --- 7.2  Types de commandes ---
class CommandeSurPlace(Commande):

    def afficher(self):
        print("===== COMMANDE SUR PLACE =====")
        super().afficher()
        print("==============================")


class CommandeEmporter(Commande):

    def afficher(self):
        print("===== COMMANDE À EMPORTER =====")
        super().afficher()
        print("  [Veuillez passer au comptoir pour récupérer votre commande]")
        print("===============================")


# --- 7.3  Programme de fidélité ---
class Fidelite:
    """1 point de fidélité par euro dépensé (arrondi à l'entier inférieur)."""

    def ajouter_points(self, client, montant):
        points_gagnes = int(montant)
        client.points_fidelite += points_gagnes
        print(f"  +{points_gagnes} point(s) de fidélité ajouté(s) "
              f"→ Total : {client.points_fidelite} point(s)")


# --- 7.4  Héritage multiple : CommandeFidele ---
class CommandeFidele(Commande, Fidelite):
    """Commande qui attribue automatiquement des points de fidélité."""

    def valider(self):
        total = self.prix_total()
        print(f"\n[Validation de la commande — montant : {total:.2f}€]")
        self.ajouter_points(self.client, total)


# ============================================================
# PARTIE 6 — Tâche 4 : Affichage attendu
# ============================================================

print("=" * 50)
print("PARTIE 6 — Affichage attendu")
print("=" * 50)

boisson = Cafe()
boisson = Lait(boisson)
boisson = Sucre(boisson)

print(f"Commande : {boisson.description()}")
print(f"Prix : {boisson.cout():.1f}€")


# ============================================================
# PARTIE 7 — Tâche 5 : Test complet du système
# ============================================================

print("\n" + "=" * 50)
print("PARTIE 7 — Test complet du système")
print("=" * 50)

# Créer un client
Chayma = Client(nom="Chayma", numero=42)

# Créer plusieurs boissons
cafe_caramel = Caramel(Lait(Cafe()))
the_sucre    = Sucre(The())
menu_combine = cafe_caramel + the_sucre   # combinaison avec +

# Créer une commande fidèle sur place
commande = CommandeFidele(Chayma)
commande.ajouter_boisson(cafe_caramel)
commande.ajouter_boisson(the_sucre)

# Afficher le contenu
print()
commande.afficher()

# Valider → attribution des points de fidélité
commande.valider()
print(f"\nPoints de fidélité de Chayma : {Chayma.points_fidelite}")

# Démonstration commande à emporter
print()
Manal = Client(nom="Manal", numero=7)
cmd_emporter = CommandeEmporter(Manal)
cmd_emporter.ajouter_boisson(Caramel(Cafe()))
cmd_emporter.afficher()


# ============================================================
# PARTIE 8 : Réponses aux questions de réflexion
# ============================================================

print("""
===== PARTIE 8 — Questions de réflexion =====

1. Quelle partie du code permet d'ajouter facilement de nouveaux ingrédients ?
   → Le patron de conception Décorateur (classe DecorateurBoisson).
     Pour ajouter un ingrédient, il suffit de créer une nouvelle sous-classe
     de DecorateurBoisson et d'y définir cout() et description().
     Aucune classe existante n'est modifiée (principe Ouvert/Fermé).

2. Si nous voulions ajouter une nouvelle boisson (chocolat chaud), quelles
   classes devraient être modifiées ?
   → Aucune classe existante ne doit être modifiée.
     Il suffit de créer une nouvelle classe ChocolatChaud(Boisson) qui
     implémente cout() et description(). Le reste du système (décorateurs,
     commandes, fidélité) fonctionne immédiatement avec cette nouvelle boisson.

3. Pourquoi séparer les responsabilités entre plusieurs classes rend le
   programme plus facile à maintenir ?
   → Chaque classe a un rôle unique et bien défini (principe SRP).
     Modifier la logique de fidélité n'impacte pas les boissons, et
     ajouter un type de commande n'impacte pas les ingrédients.
     Le code est plus lisible, testable et extensible sans risque de
     régression dans les autres parties du système.
""")