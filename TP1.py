# ============================================================
#  ANALYSEUR D'INSCRIPTIONS, DE NOTES ET DE COHERENCE PEDAGOGIQUE
#  Licence Développement Web Avancé – Back end Python 2025/2026
# ============================================================

donnees = [
    ("Sara",    "Math",     12,    "G1"),
    ("Sara",    "Info",     14,    "G1"),
    ("Ahmed",   "Math",     9,     "G2"),
    ("Adam",    "Chimie",   18,    "G1"),
    ("Sara",    "Math",     11,    "G1"),   # doublon partiel Sara/Math
    ("Bouchra", "Info",     "abc", "G2"),   # note invalide
    ("",        "Math",     10,    "G1"),   # nom vide
    ("Yassine", "Info",     22,    "G2"),   # note > 20
    ("Ahmed",   "Info",     13,    "G2"),
    ("Adam",    "Math",     None,  "G1"),   # note None
    ("Sara",    "Chimie",   16,    "G1"),
    ("Adam",    "Info",     7,     "G1"),
    ("Ahmed",   "Math",     9,     "G2"),   # doublon exact
    ("Hana",    "Physique", 15,    "G3"),
    ("Hana",    "Math",     8,     "G3"),
]

# ==============================================================
# PARTIE 1 : NETTOYAGE ET VALIDATION
# ==============================================================

def valider(enregistrement):
    """
    Vérifie si un enregistrement est valide.
    Retourne (True, "") si valide, sinon (False, "raison").
    """
    nom, matiere, note, groupe = enregistrement

    if not nom or not nom.strip():
        return (False, "nom vide")
    if not matiere or not matiere.strip():
        return (False, "matière vide")
    if not groupe or not groupe.strip():
        return (False, "groupe vide")
    if note is None:
        return (False, "note manquante (None)")
    if not isinstance(note, (int, float)):
        try:
            float(note)
        except (ValueError, TypeError):
            return (False, f"note non numérique : '{note}'")
    note_float = float(note)
    if not (0 <= note_float <= 20):
        return (False, f"note hors intervalle [0,20] : {note}")

    return (True, "")


# --- Séparation valides / erreurs / doublons_exact ---

valides        = []   # liste de tuples nettoyés (note en float)
erreurs        = []   # liste de dicts {"ligne": ..., "raison": ...}
doublons_exact = set()  # tuples répétés exactement

vus = {}  # tuple original -> nb d'occurrences (pour détecter les doublons exacts)

for enreg in donnees:
    vus[enreg] = vus.get(enreg, 0) + 1

for enreg in donnees:
    est_valide, raison = valider(enreg)
    if est_valide:
        nom, matiere, note, groupe = enreg
        tuple_nettoye = (nom.strip(), matiere.strip(), float(note), groupe.strip())
        valides.append(tuple_nettoye)
        # Doublon exact sur le tuple nettoyé
        if vus[enreg] > 1:
            doublons_exact.add(tuple_nettoye)
    else:
        erreurs.append({"ligne": enreg, "raison": raison})

# Dédupliquer les valides (on garde une seule copie des doublons exacts valides)
valides_dedup = list(dict.fromkeys(valides))

print("=" * 60)
print("PARTIE 1 – NETTOYAGE ET VALIDATION")
print("=" * 60)
print(f"\nEnregistrements valides   : {len(valides)}")
for v in valides:
    print("  ", v)

print(f"\nErreurs détectées         : {len(erreurs)}")
for e in erreurs:
    print(f"  {e['ligne']}  →  {e['raison']}")

print(f"\nDoublons exacts (set)     : {len(doublons_exact)}")
for d in doublons_exact:
    print("  ", d)


# ==============================================================
# PARTIE 2 : STRUCTURATION
# ==============================================================

# 2a. Matières distinctes (set → pas de doublon)
matieres_distinctes = set()
for nom, matiere, note, groupe in valides_dedup:
    matieres_distinctes.add(matiere)

# 2b. Hiérarchie étudiant → matière → liste de notes
notes_par_etudiant = {}
for nom, matiere, note, groupe in valides_dedup:
    if nom not in notes_par_etudiant:
        notes_par_etudiant[nom] = {}
    if matiere not in notes_par_etudiant[nom]:
        notes_par_etudiant[nom][matiere] = []
    notes_par_etudiant[nom][matiere].append(note)

# 2c. Étudiants par groupe (set par groupe → pas de répétition)
etudiants_par_groupe = {}
for nom, matiere, note, groupe in valides_dedup:
    if groupe not in etudiants_par_groupe:
        etudiants_par_groupe[groupe] = set()
    etudiants_par_groupe[groupe].add(nom)

print("\n" + "=" * 60)
print("PARTIE 2 – STRUCTURATION")
print("=" * 60)
print(f"\nMatières distinctes : {matieres_distinctes}")

print("\nNotes par étudiant par matière :")
for etudiant, matieres in notes_par_etudiant.items():
    print(f"  {etudiant} :")
    for mat, notes in matieres.items():
        print(f"      {mat} → {notes}")

print("\nÉtudiants par groupe :")
for groupe, etudiants in etudiants_par_groupe.items():
    print(f"  {groupe} : {etudiants}")


# ==============================================================
# PARTIE 3 : CALCULS ET STATISTIQUES
# ==============================================================

def somme_recursive(liste):
    """Calcule la somme d'une liste de nombres par récursivité."""
    if len(liste) == 0:
        return 0
    return liste[0] + somme_recursive(liste[1:])

def moyenne(liste):
    """Calcule la moyenne d'une liste via la somme récursive."""
    if len(liste) == 0:
        return None
    return somme_recursive(liste) / len(liste)


# Moyennes générales et par matière pour chaque étudiant
moyennes_generales   = {}
moyennes_par_matiere = {}

for etudiant, matieres in notes_par_etudiant.items():
    toutes_les_notes = []
    moyennes_par_matiere[etudiant] = {}
    for mat, notes in matieres.items():
        moy_mat = moyenne(notes)
        moyennes_par_matiere[etudiant][mat] = round(moy_mat, 2)
        toutes_les_notes.extend(notes)
    moyennes_generales[etudiant] = round(moyenne(toutes_les_notes), 2)

print("\n" + "=" * 60)
print("PARTIE 3 – CALCULS ET STATISTIQUES")
print("=" * 60)
print("\nMoyennes générales :")
for etudiant, moy in moyennes_generales.items():
    print(f"  {etudiant} : {moy}/20")

print("\nMoyennes par matière :")
for etudiant, matieres in moyennes_par_matiere.items():
    print(f"  {etudiant} :")
    for mat, moy in matieres.items():
        print(f"      {mat} : {moy}/20")


# ==============================================================
# PARTIE 4 : ANALYSE AVANCÉE ET DÉTECTION D'ANOMALIES
# ==============================================================

SEUIL_MOYENNE_FAIBLE = 10.0   # seuil groupe faible
SEUIL_ECART          = 8.0    # seuil écart min/max instable

alertes = {
    "notes_multiples":  [],   # étudiant avec >1 note pour une même matière
    "profil_incomplet": [],   # étudiant sans note dans toutes les matières
    "groupe_faible":    [],   # groupe dont la moyenne < seuil
    "ecart_important":  [],   # étudiant avec grand écart min/max
}

# 4.1 – Étudiants avec plusieurs notes pour une même matière
for etudiant, matieres in notes_par_etudiant.items():
    for mat, notes in matieres.items():
        if len(notes) > 1:
            alertes["notes_multiples"].append({
                "etudiant": etudiant,
                "matiere":  mat,
                "notes":    notes
            })

# 4.2 – Profil incomplet (manque au moins une matière du catalogue)
for etudiant, matieres in notes_par_etudiant.items():
    matieres_etudiant = set(matieres.keys())
    matieres_manquantes = matieres_distinctes - matieres_etudiant
    if matieres_manquantes:
        alertes["profil_incomplet"].append({
            "etudiant":  etudiant,
            "manquantes": matieres_manquantes
        })

# 4.3 – Groupes avec moyenne générale faible
moyennes_groupes = {}
for groupe, etudiants in etudiants_par_groupe.items():
    notes_groupe = []
    for etudiant in etudiants:
        for mat, notes in notes_par_etudiant[etudiant].items():
            notes_groupe.extend(notes)
    moy_groupe = moyenne(notes_groupe)
    moyennes_groupes[groupe] = round(moy_groupe, 2)
    if moy_groupe is not None and moy_groupe < SEUIL_MOYENNE_FAIBLE:
        alertes["groupe_faible"].append({
            "groupe":  groupe,
            "moyenne": round(moy_groupe, 2)
        })

# 4.4 – Étudiants avec écart min/max important
for etudiant, matieres in notes_par_etudiant.items():
    toutes = []
    for notes in matieres.values():
        toutes.extend(notes)
    ecart = max(toutes) - min(toutes)
    if ecart >= SEUIL_ECART:
        alertes["ecart_important"].append({
            "etudiant": etudiant,
            "min":      min(toutes),
            "max":      max(toutes),
            "ecart":    round(ecart, 2)
        })

print("\n" + "=" * 60)
print("PARTIE 4 – ANOMALIES ET ALERTES")
print("=" * 60)

print(f"\n[1] Notes multiples pour une même matière :")
if alertes["notes_multiples"]:
    for a in alertes["notes_multiples"]:
        print(f"    {a['etudiant']} / {a['matiere']} → notes : {a['notes']}")
else:
    print("  Aucune")

print(f"\n[2] Profils incomplets (matières manquantes) :")
if alertes["profil_incomplet"]:
    for a in alertes["profil_incomplet"]:
        print(f"    {a['etudiant']} → manque : {a['manquantes']}")
else:
    print("  Aucun")

print(f"\n[3] Groupes avec moyenne < {SEUIL_MOYENNE_FAIBLE} :")
print(f"  Moyennes des groupes : {moyennes_groupes}")
if alertes["groupe_faible"]:
    for a in alertes["groupe_faible"]:
        print(f"    {a['groupe']} → moyenne : {a['moyenne']}/20")
else:
    print("  Aucun groupe faible")

print(f"\n[4] Étudiants avec écart min/max ≥ {SEUIL_ECART} :")
if alertes["ecart_important"]:
    for a in alertes["ecart_important"]:
        print(f"    {a['etudiant']} → min={a['min']} / max={a['max']} / écart={a['ecart']}")
else:
    print("  Aucun")

print("\n" + "=" * 60)
print("FIN DE L'ANALYSE")
print("=" * 60)