'''
    Ce programme vérifie si un sous ensemble donné est une solution valide pour le problème SUBSETSUM en utilisant des datasets
    aléatoires stockés dans des fichiers S.txt pour l'ensemble et T.txt pour la cible  et V.txt pour le sous-ensemble proposé
'''


from typing import List
import os
import random

"""
    Cette fonction vérifier si un sous-ensemble donné est 
    une solution valide pour le problème SUBSETSUM
    retourner true c'est correcte et false sinon
"""
def verifier_solution(S: List[int], sous_ensemble: List[int], T: int) -> bool:
  
    

    # verfifer si tous les éléments de V sont dans S ?
    for element in sous_ensemble:
        if element not in S:
            print(f"{element} n'est pas dans S")
            return False
        else:
            print(f"{element} est dans S")
    
    print("tous les éléments sont dans S ")
    
    # verifier l'agilité de la somme de sous-ensemble et T  
    
    somme = sum(sous_ensemble)
    print(f"somme = {' + '.join(map(str, sous_ensemble))} = {somme}")
    print(f"T = {T}")
    
    if somme == T:
        print(f" {somme} == {T} ")
        return True
    else:
        print(f"{somme} != {T} ")
        return False

"""
    Lit un dataset complet depuis Data
        S : L'ensemble
        T : La cible
        v : Le sous-ensemble à vérifier
"""
def lire_dataset(numero: int) -> tuple:
    
    # Lire S
    with open(f'data/dataset_{numero}_S.txt', 'r') as f:
        S = [int(x) for x in f.read().split()]
    
    # Lire T
    with open(f'data/dataset_{numero}_T.txt', 'r') as f:
        T = int(f.read())
    
    # Lire V
    with open(f'data/dataset_{numero}_V.txt', 'r') as f:
        contenu = f.read().strip()
        V = [int(x) for x in contenu.split()] if contenu else []
    
    return S, T, V


#  Choisir un dataset aléatoirement
def choisir_dataset() -> int:            
    

    nb_datasets = 50 
    
    if nb_datasets == 0:                    
        print("erreur")  
        return None          

    numero = random.randint(1, nb_datasets)  
    print(f"data num : {numero}")  
    return numero                           


if __name__ == "__main__":
    
  
    print("VÉRIFICATION SUBSETSUM AVEC DATASETS")
    
    
    # Choisir un dataset aléatoirement
    
    numero_dataset = choisir_dataset()
    
    if numero_dataset is None:
        exit()
    
    # Lire le dataset complet
    try:
        S, T, V = lire_dataset(numero_dataset)
    except FileNotFoundError:
        print(f"\n Erreur")
        exit()
    
    # Vérifier la solution
    resultat = verifier_solution(S, V, T)
    
    
    print(f"\ndataset numéro : {numero_dataset}")
    print(f"S = {S}")
    print(f" T = {T}")
    print(f"V = {V}")
    print()
    
    if resultat:
        print(f"Le sous-ensemble est une solution valide")
        print(f" verefication: {' + '.join(map(str, V))} = {sum(V)} = {T} ✓")
    else:
        somme_v = sum(V) if V else 0
        print(f"Le sous-ensemble n'est PAS une solution valide")
        if V:
            print(f" somme de V: {' + '.join(map(str, V))} = {somme_v} ≠ {T}")
    
    