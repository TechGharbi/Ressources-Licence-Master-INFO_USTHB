'''
    Ce programme résout le problème SUBSETSUM en utilisant des datasets
    aléatoires stockés dans des fichiers S.txt pour l'ensemble et T.txt pour la cible 
    il génère tous les sous-ensembles possibles d'un ensemble S et trouve une solution dont la somme = T si elle existe
'''

from typing import List, Tuple, Optional     
import os                                  
import random                               


'''
  cette fonction résout le problème de SUBSETSUM avec une méthode récursive telle que il  genrer des sous ensemble 
  et vérifie si la somme de chaque sous ensemble est égale à T 
  il  retourner true si une solution existe et false sinon
    
'''
def solve_subsetsum_backtracking_recursif(S: List[int], T: int,  
                                    index: int = 0,         
                                    sous_ensemble_actuel: List[int] = None,  
                                    somme_actuelle: int = 0) -> Tuple[bool, Optional[List[int]]]: 
  
   
         #  Initialisation 
    if sous_ensemble_actuel is None:         
        sous_ensemble_actuel = []           
    
    # Vérification de la solution
    if somme_actuelle == T:             
        return True, sous_ensemble_actuel.copy()  
    
    #  Si o n a traité tous les éléments on retourne false 
    if index == len(S):                     
        return False, None                  

    element_actuel = S[index]        
    
    
    sous_ensemble_actuel.append(element_actuel)  
    # Appel récursif avec l'élément inclus
    resultat, solution =solve_subsetsum_backtracking_recursif(  
        S, T, index + 1, sous_ensemble_actuel, 
        somme_actuelle + element_actuel     
    )
            # Si on a trouvé une solution, retourner 
    if resultat:                        
        return resultat, solution        
    

    sous_ensemble_actuel.pop()   #  BACKTRACK    
    resultat, solution = solve_subsetsum_backtracking_recursif(  
        S, T, index + 1, sous_ensemble_actuel, 
        somme_actuelle                       
    )
      # Retourner le résultat final
    return resultat, solution                

"""
    Lit un dataset  depuis Data
    ici en utilise seulement les ficheir S ET T 
        S : L'ensemble
        T : La cible
"""
def lire_dataset(numero: int) -> Tuple[List[int], int]:
  
    # Lire S
    with open(f'data/dataset_{numero}_S.txt', 'r') as f:  
        S = [int(x) for x in f.read().split()]  
    
    # Lire T
    with open(f'data/dataset_{numero}_T.txt', 'r') as f:  
        T = int(f.read())                    
    
    return S, T                           

  
   

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
    
    print("RÉSOLUTION SUBSETSUM ")  
                             
    # Choisir un dataset
    numero_dataset = choisir_dataset()       
    
    if numero_dataset is None:              
        exit()                              
    
    # Lire le dataset
    try:                                     
        S, T = lire_dataset(numero_dataset)  
    except FileNotFoundError:                
        print("Erreur")  
        exit()                              
    
   

    

    
    resultat, solution = solve_subsetsum_backtracking_recursif(S, T)  
    
    print(f"\n dataset numero : {numero_dataset}") 
    print(f" S = {S}")           
    print(f" T = {T}")              
    
    
    if resultat:                             
        print(f"Solution trouvée: {solution}")  
        # Vérifier que la somme est correcte
        print(f"   Vérification: {' + '.join(map(str, solution))} = {sum(solution)} = {T} ✓")  
    else:                                    
        print("Aucune solution trouvée") 