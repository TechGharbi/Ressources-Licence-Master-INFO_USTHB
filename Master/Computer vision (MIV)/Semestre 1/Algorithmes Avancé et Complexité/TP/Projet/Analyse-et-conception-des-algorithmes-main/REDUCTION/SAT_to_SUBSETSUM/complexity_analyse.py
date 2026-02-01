"""
Analyse empirique de la complexité de la réduction SAT → SUBSETSUM
Génère des graphiques de performance (temps, mémoire, taille)
"""
import time
import sys
import os
import random
import tracemalloc
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict

# Importer votre module de réduction (NOM CORRIGÉ)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importer depuis reductionSAT_SUBSETSUM.py
    from reductionSAT_SUBSETSUM import encode_sat_to_subsetsum
    IMPORTS_OK = True
    print("Module de réduction importé")
except ImportError as e:
    print(f" Erreu {e}")
    IMPORTS_OK = False
    sys.exit(1)


# Génère des instances SAT de différentes tailles
class SATInstanceGenerator:

    """
        Génère une formule SAT aléatoire
        Returner la liste de clauses   
        """
    @staticmethod
    def generate_random_sat(n_vars: int, n_clauses: int, 
                           clause_size: int = 3) -> List[List[int]]:
    
        formula = []
        for _ in range(n_clauses):
            clause = []
            # Choisir clause_size variables aléatoires différentes
            vars_in_clause = random.sample(range(1, n_vars + 1), 
                                          min(clause_size, n_vars))
            for var in vars_in_clause:
                # Ajouter le littéral positif ou négatif aléatoirement
                literal = var if random.random() > 0.5 else -var
                clause.append(literal)
            formula.append(clause)
        return formula

 # Effectue la réduction avec mesures de performance
class SATtoSUBSETSUMReducer:
  
    def __init__(self):
        self.stats = {}
   #  Encode SAT vers SUBSETSUM avec mesures de performance
    def encode_with_metrics(self, formula: List[List[int]]) -> Tuple[List[int], int, Dict, Dict]:
        
        # Démarrer les mesures
        tracemalloc.start()
        start_time = time.perf_counter()
        memory_start = tracemalloc.get_traced_memory()[0]
        
        # Effectuer la réduction 
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            S, T, mapping = encode_sat_to_subsetsum(formula)
        
        # Mesurer les ressources
        end_time = time.perf_counter()
        memory_current, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Calculer les statistiques
        variables = set(abs(lit) for clause in formula for lit in clause)
        self.stats = {
            'time': end_time - start_time,
            'memory_peak': memory_peak / (1024 * 1024),  # MB
            'memory_used': (memory_peak - memory_start) / (1024 * 1024),  # MB
            'size_S': len(S),
            'max_number_size': max(S) if S else 0,
            'n_vars': len(variables),
            'n_clauses': len(formula),
            'total_literals': sum(len(clause) for clause in formula)
        }
        
        return S, T, mapping, self.stats

  # Système pour effectuer les benchmarks
class BenchmarkSystem:
    
    def __init__(self):
        self.results = []
        self.generator = SATInstanceGenerator()
        self.reducer = SATtoSUBSETSUMReducer()
    
    def run_benchmark(self, sizes: List[Tuple[int, int]], 
                     repetitions: int = 5) -> List[Dict]:
        results = []
        
        print("=" * 70)
        print("DÉMARRAGE DU BENCHMARK")
        print("=" * 70)
        
        for i, (n_vars, n_clauses) in enumerate(sizes, 1):
            print(f"\n[{i}/{len(sizes)}] Test : {n_vars} variables, {n_clauses} clauses")
            
            times = []
            memories = []
            sizes_S = []
            max_nums = []
            
            for rep in range(repetitions):
                # Générer instance
                formula = self.generator.generate_random_sat(n_vars, n_clauses)
                
                # Effectuer la réduction avec mesures
                S, T, mapping, stats = self.reducer.encode_with_metrics(formula)
                
                times.append(stats['time'])
                memories.append(stats['memory_peak'])
                sizes_S.append(stats['size_S'])
                max_nums.append(stats['max_number_size'])
                
                print(f"  Rep {rep+1}/{repetitions}: {stats['time']*1000:.2f}ms", end='\r')
            
            # Calculer moyennes
            result = {
                'n_vars': n_vars,
                'n_clauses': n_clauses,
                'time_mean': np.mean(times),
                'time_std': np.std(times),
                'memory_mean': np.mean(memories),
                'memory_std': np.std(memories),
                'size_S': int(np.mean(sizes_S)),
                'max_number': int(np.mean(max_nums))
            }
            
            results.append(result)
            print(f"  Moyenne: {result['time_mean']*1000:.2f}ms ± {result['time_std']*1000:.2f}ms")
        
        self.results = results
        return results
    # Test de scalabilité : augmentation progressive
    def run_scalability_test(self):
        
        print("\n" + "=" * 70)
        print("TEST DE SCALABILITÉ")
        print("=" * 70)
        
        # Différentes tailles à tester
        sizes = [
            (5, 10),      
            (10, 20),    
            (15, 30),     
            (20, 40),    
            (25, 50),   
            (30, 60),     
        ]
        
        return self.run_benchmark(sizes, repetitions=5)
    # Génère les graphiques d'analyse   
class GraphGenerator:
    
    @staticmethod
    def plot_time_complexity(results: List[Dict], title: str = "Complexité Temporelle"):
        """Graphique temps vs taille"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Extraire données
        n_total = [r['n_vars'] * r['n_clauses'] for r in results]
        times_ms = [r['time_mean'] * 1000 for r in results]
        times_std = [r['time_std'] * 1000 for r in results]
        
        # Graphique 1 : Temps vs (n × m)
        ax1.errorbar(n_total, times_ms, yerr=times_std, 
                    marker='o', capsize=5, linewidth=2, markersize=8,
                    color='#2E86AB', ecolor='#A23B72')
        ax1.set_xlabel('Taille (n_vars × n_clauses)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Temps (ms)', fontsize=12, fontweight='bold')
        ax1.set_title(f'{title}\nTemps vs Taille totale', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Ajouter régression linéaire
        if len(n_total) > 2:
            z = np.polyfit(n_total, times_ms, 1)
            p = np.poly1d(z)
            x_smooth = np.linspace(min(n_total), max(n_total), 100)
            ax1.plot(x_smooth, p(x_smooth), '--', color='red', linewidth=2,
                    label=f'Régression: y = {z[0]:.4f}x + {z[1]:.2f}')
            ax1.legend(loc='best')
        
        # Graphique 2 : Temps vs nombre de variables
        n_vars = [r['n_vars'] for r in results]
        ax2.errorbar(n_vars, times_ms, yerr=times_std,
                    marker='s', capsize=5, linewidth=2, markersize=8, 
                    color='#F18F01', ecolor='#C73E1D')
        ax2.set_xlabel('Nombre de variables', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Temps (ms)', fontsize=12, fontweight='bold')
        ax2.set_title('Temps vs Nombre de variables', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_memory_complexity(results: List[Dict]):
     
        fig, ax = plt.subplots(figsize=(10, 6))
        
        n_total = [r['n_vars'] * r['n_clauses'] for r in results]
        memory = [r['memory_mean'] for r in results]
        memory_std = [r['memory_std'] for r in results]
        
        ax.errorbar(n_total, memory, yerr=memory_std,
                   marker='D', capsize=5, linewidth=2, markersize=8, 
                   color='#6A4C93', ecolor='#C5299B')
        ax.set_xlabel('Taille (n_vars × n_clauses)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Mémoire (MB)', fontsize=12, fontweight='bold')
        ax.set_title('Complexité Spatiale\nMémoire vs Taille', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Régression linéaire
        if len(n_total) > 2:
            z = np.polyfit(n_total, memory, 1)
            p = np.poly1d(z)
            x_smooth = np.linspace(min(n_total), max(n_total), 100)
            ax.plot(x_smooth, p(x_smooth), '--', color='red', linewidth=2,
                   label=f'Régression: y = {z[0]:.6f}x + {z[1]:.2f}')
            ax.legend(loc='best')
        
        plt.tight_layout()
        return fig
    
     # Analyse de la taille de S et des nombres
    @staticmethod
    def plot_size_analysis(results: List[Dict]):
       
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        n_vars = [r['n_vars'] for r in results]
        n_clauses = [r['n_clauses'] for r in results]
        size_S = [r['size_S'] for r in results]
        max_nums = [r['max_number'] for r in results]
        
        # Graphique 1 : Taille de S
        ax1.plot(n_vars, size_S, marker='o', linewidth=2, markersize=8, 
                label='Taille observée de S', color='#06AED5')
        
        # Théorique : 2n + 2m
        theoretical = [2*n + 2*m for n, m in zip(n_vars, n_clauses)]
        ax1.plot(n_vars, theoretical, '--', linewidth=2, 
                label='Théorique: 2n + 2m', color='#DD1C1A')
        
        ax1.set_xlabel('Nombre de variables', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Taille de S', fontsize=12, fontweight='bold')
        ax1.set_title('Taille de l\'ensemble S', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Graphique 2 : Taille maximale des nombres (échelle log)
        ax2.semilogy(n_vars, max_nums, marker='s', linewidth=2, markersize=8, 
                    color='#F77F00')
        ax2.set_xlabel('Nombre de variables', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Taille max des nombres (échelle log)', fontsize=12, fontweight='bold')
        ax2.set_title('Croissance des nombres\n(Exponentielle: 10^(n+m))', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, which='both', linestyle='--')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_comprehensive_report(results: List[Dict], save_path: str = None):
        """Rapport complet avec tous les graphiques"""
        fig = plt.figure(figsize=(18, 12))
        
        # Extraire données
        n_total = [r['n_vars'] * r['n_clauses'] for r in results]
        times_ms = [r['time_mean'] * 1000 for r in results]
        memory = [r['memory_mean'] for r in results]
        size_S = [r['size_S'] for r in results]
        n_vars = [r['n_vars'] for r in results]
        
        # 1. Temps d'exécution
        ax1 = plt.subplot(2, 3, 1)
        ax1.plot(n_total, times_ms, marker='o', linewidth=2, markersize=8, color='#2E86AB')
        ax1.set_xlabel('Taille (n × m)', fontweight='bold')
        ax1.set_ylabel('Temps (ms)', fontweight='bold')
        ax1.set_title('Complexité Temporelle', fontweight='bold', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 2. Mémoire
        ax2 = plt.subplot(2, 3, 2)
        ax2.plot(n_total, memory, marker='s', linewidth=2, markersize=8, color='#6A4C93')
        ax2.set_xlabel('Taille (n × m)', fontweight='bold')
        ax2.set_ylabel('Mémoire (MB)', fontweight='bold')
        ax2.set_title('Complexité Spatiale', fontweight='bold', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # 3. Taille de S
        ax3 = plt.subplot(2, 3, 3)
        ax3.plot(n_vars, size_S, marker='D', linewidth=2, markersize=8, color='#06AED5')
        ax3.set_xlabel('Nombre de variables', fontweight='bold')
        ax3.set_ylabel('Taille de S', fontweight='bold')
        ax3.set_title('Taille de l\'ensemble S', fontweight='bold', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # 4. Comparaison temps/mémoire
        ax4 = plt.subplot(2, 3, 4)
        ax4_twin = ax4.twinx()
        line1 = ax4.plot(n_total, times_ms, 'b-o', label='Temps', linewidth=2)
        line2 = ax4_twin.plot(n_total, memory, 'r-s', label='Mémoire', linewidth=2)
        ax4.set_xlabel('Taille (n × m)', fontweight='bold')
        ax4.set_ylabel('Temps (ms)', color='b', fontweight='bold')
        ax4_twin.set_ylabel('Mémoire (MB)', color='r', fontweight='bold')
        ax4.set_title('Temps vs Mémoire', fontweight='bold', fontsize=12)
        ax4.grid(True, alpha=0.3)
        
        # 5. Efficacité (temps par élément)
        ax5 = plt.subplot(2, 3, 5)
        efficiency = [t / n if n > 0 else 0 for t, n in zip(times_ms, n_total)]
        ax5.plot(n_total, efficiency, marker='^', linewidth=2, markersize=8, color='#F18F01')
        ax5.set_xlabel('Taille (n × m)', fontweight='bold')
        ax5.set_ylabel('Temps par élément (ms)', fontweight='bold')
        ax5.set_title('Efficacité', fontweight='bold', fontsize=12)
        ax5.grid(True, alpha=0.3)
        
        # 6. Tableau de statistiques
        ax6 = plt.subplot(2, 3, 6)
        ax6.axis('off')
        
        stats_text = "STATISTIQUES GLOBALES\n" + "="*30 + "\n\n"
        stats_text += f"Instances testées: {len(results)}\n\n"
        stats_text += f"Temps:\n"
        stats_text += f"  Moyen: {np.mean(times_ms):.2f} ms\n"
        stats_text += f"  Min:   {np.min(times_ms):.2f} ms\n"
        stats_text += f"  Max:   {np.max(times_ms):.2f} ms\n\n"
        stats_text += f"Mémoire:\n"
        stats_text += f"  Moyenne: {np.mean(memory):.2f} MB\n"
        stats_text += f"  Max:     {np.max(memory):.2f} MB\n\n"
        stats_text += f"Complexité observée:\n"
        stats_text += f"  Temps:   O(n × m)\n"
        stats_text += f"  Mémoire: O(n + m)\n"
        stats_text += f"  Taille S: 2n + 2m"
        
        ax6.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        plt.suptitle('RAPPORT COMPLET - Réduction SAT → SUBSETSUM',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n✅ Graphique sauvegardé: {save_path}")
        
        return fig


def main():
   
    
    # Créer le système de benchmark
    benchmark = BenchmarkSystem()
    
    # Test de scalabilité
    print("\n[1/1] Exécution du test de scalabilité...")
    results = benchmark.run_scalability_test()
    
    # Créer dossier output si nécessaire
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\n Dossier créé: {output_dir}/")
    

    
    grapher = GraphGenerator()
    
    # Complexité temporelle
    fig1 = grapher.plot_time_complexity(results, "Analyse de Complexité Temporelle")
    fig1.savefig(f'{output_dir}/1_time_complexity.png', dpi=300, bbox_inches='tight')
    print(f" {output_dir}/1_time_complexity.png")
    
    # 2. Complexité spatiale
    fig2 = grapher.plot_memory_complexity(results)
    fig2.savefig(f'{output_dir}/2_memory_complexity.png', dpi=300, bbox_inches='tight')
    print(f" {output_dir}/2_memory_complexity.png")
    
    # 3. Analyse de taille
    fig3 = grapher.plot_size_analysis(results)
    fig3.savefig(f'{output_dir}/3_size_analysis.png', dpi=300, bbox_inches='tight')
    print(f" {output_dir}/3_size_analysis.png")
    
    # 4. Rapport complet
    fig4 = grapher.plot_comprehensive_report(results)
    fig4.savefig(f'{output_dir}/4_rapport_complet.png', dpi=300, bbox_inches='tight')
    print(f" {output_dir}/4_rapport_complet.png")
    
    # Afficher les graphiques
   
    plt.show()
    
    

    print(f"\n{output_dir}/")
    
    print(f"  • {output_dir}/1_time_complexity.png")
    print(f"  • {output_dir}/2_memory_complexity.png")
    print(f"  • {output_dir}/3_size_analysis.png")
    print(f"  • {output_dir}/4_rapport_complet.png")
    

if __name__ == "__main__":
    main()