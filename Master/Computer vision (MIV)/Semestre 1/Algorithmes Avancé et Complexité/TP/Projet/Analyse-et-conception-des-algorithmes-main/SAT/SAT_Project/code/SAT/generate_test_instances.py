# generate_test_instances.py
import random
import os

def generate_test_instances():
    """Génère des instances de test de différentes tailles."""
    
    test_dir = os.path.join( "data", "test_cases", "sat_tests")
    os.makedirs(test_dir, exist_ok=True)
    
    instances = [
        (3, 5, "small"),
        (5, 10, "medium"),
        (7, 14, "large"),
        (10, 20, "xlarge"),
    ]
    
    print("Génération d'instances de test SAT...")
    
    for n_vars, n_clauses, size in instances:
        filename = os.path.join(test_dir, f"random_{n_vars}_{n_clauses}.cnf")
        
        with open(filename, 'w') as f:
            # En-tête DIMACS
            f.write(f"c Instance SAT {size} - {n_vars} variables, {n_clauses} clauses\n")
            f.write(f"p cnf {n_vars} {n_clauses}\n")
            
            # Générer les clauses
            for _ in range(n_clauses):
                # Choisir 2-3 variables aléatoires
                k = random.randint(2, 3)
                chosen_vars = random.sample(range(1, n_vars + 1), k)
                
                clause_literals = []
                for var in chosen_vars:
                    if random.choice([True, False]):
                        clause_literals.append(str(var))
                    else:
                        clause_literals.append(f"-{var}")
                
                clause_line = " ".join(clause_literals) + " 0\n"
                f.write(clause_line)
        
        print(f"   {filename} généré ({n_vars}v/{n_clauses}c)")
    
    # Générer aussi un fichier toujours satisfaisable
    filename = os.path.join(test_dir, "always_satisfiable.cnf")
    with open(filename, 'w') as f:
        f.write("c Toujours satisfaisable (chaque clause contient x1)\n")
        f.write("p cnf 3 3\n")
        f.write("1 2 0\n")
        f.write("1 -3 0\n")
        f.write("-1 2 3 0\n")
    
    print(f"   {filename} généré (toujours satisfaisable)")
    
    # Générer un fichier impossible
    filename = os.path.join(test_dir, "unsatisfiable.cnf")
    with open(filename, 'w') as f:
        f.write("c Non satisfaisable\n")
        f.write("p cnf 2 4\n")
        f.write("1 0\n")
        f.write("-1 2 0\n")
        f.write("-1 -2 0\n")
        f.write("-2 0\n")
    
    print(f"  {filename} généré (non satisfaisable)")
    
    print(f"\nTotal: {len(instances) + 2} instances générées dans {test_dir}")

if __name__ == "__main__":
    generate_test_instances()