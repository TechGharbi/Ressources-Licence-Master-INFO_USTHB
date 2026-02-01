"""
Lecteur et écrivain de fichiers au format DIMACS CNF
Format standard utilisé par SATLIB et les compétitions SAT
"""
def read_dimacs_cnf(filename):
    """
    Lit un fichier SATLIB au format DIMACS CNF
    
    Format DIMACS :
    c Commentaire (ligne ignorée)
    c Autre commentaire
    p cnf <nb_variables> <nb_clauses>
    1 -2 3 0
    -1 2 -3 0
    1 2 3 0
    
    Chaque clause se termine par 0
    
    Args:
        filename: chemin du fichier .cnf
    
    Returns:
        tuple: (clauses, num_variables)
            clauses: liste de listes d'entiers
            num_variables: nombre de variables
    """
    clauses = []
    num_variables = 0
    num_clauses = 0
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Ignorer les lignes vides
            if not line:
                continue
            
            # Ignorer les commentaires
            if line.startswith('c'):
                continue
            
            # Ligne de paramètres p cnf <vars> <clauses>
            if line.startswith('p'):
                parts = line.split()
                if len(parts) >= 4 and parts[1] == 'cnf':
                    num_variables = int(parts[2])
                    num_clauses = int(parts[3])
                continue
            
            # Ligne de clause
            try:
                literals = list(map(int, line.split()))
                
                # Retirer le 0 final (terminateur de clause en DIMACS)
                if literals and literals[-1] == 0:
                    literals = literals[:-1]
                
                # Ajouter la clause si elle n'est pas vide
                if literals:
                    clauses.append(literals)
                    
            except ValueError:
                # Ignorer les lignes mal formées
                continue
    
    # Si num_variables n'a pas été spécifié, le déduire des clauses
    if num_variables == 0 and clauses:
        max_var = max(abs(lit) for clause in clauses for lit in clause)
        num_variables = max_var
    
    return clauses, num_variables


def write_dimacs_cnf(clauses, num_variables, filename, comments=None):
    """
    Écrit une instance SAT/3-SAT au format DIMACS CNF
    
    Args:
        clauses: liste de clauses
        num_variables: nombre de variables
        filename: nom du fichier de sortie
        comments: liste de commentaires optionnels
    """
    with open(filename, 'w') as f:
        # Commentaires
        if comments:
            for comment in comments:
                f.write(f"c {comment}\n")
        else:
            f.write(f"c Instance SAT générée\n")
        
        f.write(f"c Nombre de variables: {num_variables}\n")
        f.write(f"c Nombre de clauses: {len(clauses)}\n")
        
        # Ligne de paramètres
        f.write(f"p cnf {num_variables} {len(clauses)}\n")
        
        # Clauses
        for clause in clauses:
            clause_str = ' '.join(map(str, clause))
            f.write(f"{clause_str} 0\n")


def read_3sat_dimacs(filename):
    """
    Lit un fichier DIMACS et vérifie que c'est du 3-SAT
    (toutes les clauses ont exactement 3 littéraux)
    
    Returns:
        tuple: (clauses, num_variables, is_3sat)
    """
    clauses, num_variables = read_dimacs_cnf(filename)
    
    # Vérifier si c'est du 3-SAT strict
    is_3sat = all(len(clause) == 3 for clause in clauses)
    
    if not is_3sat:
        # Filtrer pour ne garder que les clauses de taille 3
        clauses_3sat = [c for c in clauses if len(c) == 3]
        print(f"⚠️  Attention: {len(clauses) - len(clauses_3sat)} clauses ignorées (pas exactement 3 littéraux)")
        clauses = clauses_3sat
    
    return clauses, num_variables, is_3sat


def convert_simple_to_dimacs(input_file, output_file):
    """
    Convertit un fichier au format simple vers DIMACS
    
    Format simple:
    3
    3
    1 -2 3
    -1 2 -3
    1 2 3
    
    Format DIMACS:
    p cnf 3 3
    1 -2 3 0
    -1 2 -3 0
    1 2 3 0
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    num_variables = int(lines[0].strip())
    num_clauses = int(lines[1].strip())
    
    clauses = []
    for i in range(2, 2 + num_clauses):
        literals = list(map(int, lines[i].strip().split()))
        clauses.append(literals)
    
    write_dimacs_cnf(clauses, num_variables, output_file)


def print_dimacs_info(filename):
    """
    Affiche les informations d'un fichier DIMACS
    """
    try:
        clauses, num_vars = read_dimacs_cnf(filename)
        
        print(f"\n{'='*60}")
        print(f"Informations du fichier: {filename}")
        print('='*60)
        print(f"Variables: {num_vars}")
        print(f"Clauses: {len(clauses)}")
        
        # Statistiques sur les tailles de clauses
        clause_sizes = {}
        for clause in clauses:
            size = len(clause)
            clause_sizes[size] = clause_sizes.get(size, 0) + 1
        
        print(f"\nDistribution des tailles de clauses:")
        for size in sorted(clause_sizes.keys()):
            count = clause_sizes[size]
            print(f"  Taille {size}: {count} clauses ({count/len(clauses)*100:.1f}%)")
        
        # Vérifier si c'est du 3-SAT
        is_3sat = all(len(c) == 3 for c in clauses)
        print(f"\n3-SAT strict: {'✓ OUI' if is_3sat else '✗ NON'}")
        
        # Afficher quelques clauses
        print(f"\nPremières clauses:")
        for i, clause in enumerate(clauses[:5], 1):
            print(f"  C{i}: {clause}")
        
        if len(clauses) > 5:
            print(f"  ... ({len(clauses) - 5} clauses supplémentaires)")
        
        print('='*60 + '\n')
        
    except FileNotFoundError:
        print(f"⚠️  Erreur: Fichier '{filename}' non trouvé")
    except Exception as e:
        print(f"⚠️  Erreur lors de la lecture: {e}")


if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("LECTEUR/ÉCRIVAIN DIMACS CNF")
    print("="*60)
    
    # Test 1: Créer un fichier DIMACS exemple
    print("\n1. Création d'un fichier DIMACS exemple...")
    
    test_clauses = [
        [1, -2, 3],
        [-1, 2, -3],
        [1, 2, 3]
    ]
    
    test_file = "example_3sat.cnf"
    comments = [
        "Exemple de fichier 3-SAT",
        "F = (x1 v -x2 v x3) ^ (-x1 v x2 v -x3) ^ (x1 v x2 v x3)"
    ]
    
    write_dimacs_cnf(test_clauses, 3, test_file, comments)
    print(f"✓ Fichier créé: {test_file}")
    
    # Test 2: Lire le fichier créé
    print("\n2. Lecture du fichier créé...")
    clauses, num_vars = read_dimacs_cnf(test_file)
    print(f"✓ Lecture réussie")
    print(f"  Variables: {num_vars}")
    print(f"  Clauses: {len(clauses)}")
    
    # Test 3: Afficher les informations détaillées
    print("\n3. Informations détaillées:")
    print_dimacs_info(test_file)
    
    # Test 4: Vérification 3-SAT
    print("4. Vérification 3-SAT...")
    clauses_3sat, num_vars_3sat, is_3sat = read_3sat_dimacs(test_file)
    if is_3sat:
        print("✓ Le fichier contient une instance 3-SAT valide")
    else:
        print("⚠️  Le fichier contient des clauses qui ne sont pas du 3-SAT")
    
    # Instructions pour utiliser avec d'autres fichiers
    if len(sys.argv) > 1:
        print("\n5. Analyse du fichier fourni:")
        print_dimacs_info(sys.argv[1])
    else:
        print("\n" + "="*60)
        print("UTILISATION:")
        print("="*60)
        print("  python dimacs_reader.py <fichier.cnf>")
        print("\nExemple:")
        print("  python dimacs_reader.py satlib_instances/uf20-01.cnf")

        print("="*60)
