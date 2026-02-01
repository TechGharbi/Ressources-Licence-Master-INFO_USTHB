import os
import random
from typing import List, Tuple

# Chemin de base : dossier SUBSETSUM
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def generer_ensemble_aleatoire(taille: int, valeur_min: int, valeur_max: int) -> List[int]:
    """
    Génère un ensemble S d'entiers aléatoires de taille fixe AVEC POSSIBILITÉ DE DOUBLONS
    """
    ensemble = [random.randint(valeur_min, valeur_max) for _ in range(taille)]
    return ensemble


def generer_sous_ensemble_aleatoire(S: List[int], taille_max: int = 5) -> List[int]:
    """
    Génère un sous-ensemble V aléatoire à partir de l'ensemble S
    """
    taille = random.randint(1, min(len(S), taille_max))
    indices = random.sample(range(len(S)), taille)
    return [S[i] for i in indices]


def generer_dataset_meilleur_cas(S: List[int]) -> Tuple[int, List[int], str]:
    """
    CAS 1 : MEILLEUR CAS
    T est le premier élément de S
    → Le backtracking trouve la solution IMMÉDIATEMENT (1ère branche)
    """
    T = S[0]
    V = [S[0]]
    return T, V, "MEILLEUR"


def generer_dataset_pire_cas(S: List[int]) -> Tuple[int, List[int], str]:
    """
    CAS 2 : VRAI PIRE CAS pour backtracking
    
    ⚠️ CORRECTION MAJEURE :
    Le pire cas survient quand le backtracking doit explorer TOUTES les branches
    
    Stratégie :
    - T = sum(S) - 1 (impossible mais très proche du maximum)
    - Force l'algorithme à essayer TOUTES les 2^n combinaisons
    - Aucune branche ne peut être élaguée tôt
    
    Complexité : O(2^n) garantie
    """
    
    somme_totale = sum(S)
    
    
    
    T = somme_totale - 1
    
   
    if T <= 0:
        T = somme_totale + 1
    
 
    V = []
    
    return T, V, "PIRE"


def creer_dossier_data():
    """Crée le dossier data s'il n'existe pas"""
    os.makedirs(DATA_DIR, exist_ok=True)


def sauvegarder_dataset(numero: int, S: List[int], T: int, V: List[int], type_cas: str):
    """Sauvegarde un dataset dans 4 fichiers séparés"""
    base_path = os.path.join(DATA_DIR, f"dataset_{numero}")

    with open(f"{base_path}_S.txt", "w") as f:
        f.write(" ".join(map(str, S)))

    with open(f"{base_path}_T.txt", "w") as f:
        f.write(str(T))

    with open(f"{base_path}_V.txt", "w") as f:
        f.write(" ".join(map(str, V)) if V else "")

    with open(f"{base_path}_TYPE.txt", "w") as f:
        f.write(type_cas)

"""
    Génère des datasets UNIQUEMENT pour le meilleur cas et pire cas 
    avec une augmentation progressive de la taille n
    
    tq on a :
        nombre_par_type: Nombre de datasets par catégorie (50 par défaut)
        n_min: Taille minimale de l'ensemble S (5 par défaut)
        n_max: Taille maximale de l'ensemble S (20 par défaut)
        valeur_min: Valeur minimale des éléments (1 par défaut)
        valeur_max: Valeur maximale des éléments (1000 par défaut)
    """
    
def generer_datasets_meilleur_pire(
    nombre_par_type: int = 50,
    n_min: int = 5,
    n_max: int = 20,
    valeur_min: int = 1,
    valeur_max: int = 1000
):
   
    
  
    creer_dossier_data()
    
    # Calculer combien de datasets par taille n
    range_n = n_max - n_min + 1
    datasets_par_taille = nombre_par_type // range_n
    datasets_restants = nombre_par_type % range_n
    
    numero = 1
    
   
    
    for n in range(n_min, n_max + 1):
      
        nb_datasets = datasets_par_taille
        if n - n_min < datasets_restants:
            nb_datasets += 1
        
        print(f"   n = {n:2d} : ", end="", flush=True)
        
        for i in range(nb_datasets):
          
            S = generer_ensemble_aleatoire(n, valeur_min, valeur_max)
            
            #  meilleur cas
            T, V, type_cas = generer_dataset_meilleur_cas(S)
            
           
            sauvegarder_dataset(numero, S, T, V, type_cas)
            numero += 1
            
            if (i + 1) % 5 == 0:
                print("█", end="", flush=True)
        
    for n in range(n_min, n_max + 1):
        # Nombre de datasets pour cette taille n
        nb_datasets = datasets_par_taille
        if n - n_min < datasets_restants:
            nb_datasets += 1
        
        print(f"   n = {n:2d} : ", end="", flush=True)
        
        for i in range(nb_datasets):
            
            S = generer_ensemble_aleatoire(n, valeur_min, valeur_max)
            
            # pire
            T, V, type_cas = generer_dataset_pire_cas(S)
          
            sauvegarder_dataset(numero, S, T, V, type_cas)
            numero += 1
            
            if (i + 1) % 5 == 0:
                print("█", end="", flush=True)
        
       
    
    print(f"\n✅ Total PIRE : {nombre_par_type} datasets")
  
    
   


def afficher_exemple_dataset():
    
   
    
    print("\n🟢 CAS MEILLEUR (T = S[0]) :")
    print("-" * 80)
    for n in range(5, 11):
        S = generer_ensemble_aleatoire(n, 1, 100)
        T, V, _ = generer_dataset_meilleur_cas(S)
       
    for n in range(5, 11):
        S = generer_ensemble_aleatoire(n, 1, 100)
        T, V, _ = generer_dataset_pire_cas(S)
       

"""
    Vérifie que la correction est bien appliquée
    Compare l'ancien et le nouveau comportement
    """
def verifier_correction():
   
   
    S = [10, 20, 30, 40, 50]
   
    # Cas MEILLEUR
    T_meilleur, V_meilleur, _ = generer_dataset_meilleur_cas(S)
   
    
    # Cas PIRE (CORRIGÉ)
    T_pire, V_pire, _ = generer_dataset_pire_cas(S)
   
    for i in range(min(5, len(S))):
        subset_size = i + 1
        combos = 2**subset_size
        


if __name__ == "__main__":
    
    afficher_exemple_dataset()
    
    
    verifier_correction()
    
    # Générer les datasets
    generer_datasets_meilleur_pire(
        nombre_par_type=50,  
        n_min=5,             
        n_max=20,           
        valeur_min=1,
        valeur_max=1000
    )