"""
ÉTAPE 4 : Visualisation 3D
============================
- Export .ply pour MeshLab
- Affichage matplotlib (3 vues)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_3d(pts3d=None, colors=None):
    print("=" * 50)
    print("   ÉTAPE 4 — Visualisation 3D")
    print("=" * 50)

    if pts3d is None:
        try:
            pts3d = np.load('points3d.npy')
            colors = np.load('colors3d.npy')
        except FileNotFoundError:
            print(" Fichiers introuvables. Lancez d'abord step3_reconstruction.py")
            return

    # Conversion en tableaux numpy si nécessaire
    pts3d = np.asarray(pts3d)
    colors = np.asarray(colors)
    
    print(f"\n🌐 {len(pts3d)} points 3D chargés.")

    # Filtrage des outliers (optionnel)
    if len(pts3d) > 3:
        median = np.median(pts3d, axis=0)
        dists = np.linalg.norm(pts3d - median, axis=1)
        mask = dists < np.percentile(dists, 95)
        pts3d = pts3d[mask]
        colors = colors[mask]
        print(f"   Après filtrage : {len(pts3d)} points")
    else:
        print("   Trop peu de points pour le filtrage, on conserve tout.")

    if len(pts3d) == 0:
        print("⚠️ Aucun point à afficher.")
        return

    X, Y, Z = pts3d[:, 0], pts3d[:, 1], pts3d[:, 2]

    # 1) Export PLY pour MeshLab
    export_ply(pts3d, colors, 'pointcloud.ply')

    # 2) Visualisation Matplotlib : 3 vues
    fig = plt.figure(figsize=(15, 5))
    fig.suptitle('Reconstruction 3D — Stéréovision SIFT', fontsize=14, fontweight='bold')

    ax1 = fig.add_subplot(141, projection='3d')
    ax1.scatter(X, Z, -Y, c=colors, s=10)
    ax1.set_title('Vue perspective')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Z (m)')
    ax1.set_zlabel('Y (m)')

    ax2 = fig.add_subplot(142)
    ax2.scatter(X, Z, c=colors, s=10)
    ax2.set_title('Vue de dessus (X-Z)')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Z (m)')
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(143)
    ax3.scatter(X, -Y, c=colors, s=10)
    ax3.set_title('Vue de face (X-Y)')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.grid(True, alpha=0.3)
    
    ax4 = fig.add_subplot(144)
    ax4.scatter(Z, Y, c=colors, s=10)
    ax4.set_title('Vue de face (Z-Y)')
    ax4.set_xlabel('Z (m)')
    ax4.set_ylabel('Y (m)')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('result_pointcloud_3views.png', dpi=150)
    plt.show()
    print("💾 Sauvegardé : result_pointcloud_3views.png")

    # 3) Vue 3D unique avec couleur = profondeur Z
    fig2 = plt.figure(figsize=(8, 6))
    ax = fig2.add_subplot(111, projection='3d')
    sc = ax.scatter(X, Z, -Y, c=Z, cmap='viridis', s=20)
    ax.set_title(f'Nuage de points 3D — {len(pts3d)} points (couleur = Z)')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Z (m)')
    ax.set_zlabel('Y (m)')
    plt.colorbar(sc, label='Profondeur Z (m)')
    plt.tight_layout()
    plt.savefig('result_pointcloud_3d.png', dpi=150)
    plt.show()
    
    print("💾 Sauvegardé : result_pointcloud_3d.png")
    print("\n🖱️  Faites pivoter la figure avec la souris !")


def export_ply(pts3d, colors, filename='pointcloud.ply'):
    """Exporte le nuage de points au format PLY pour MeshLab."""
    pts3d = np.asarray(pts3d)
    colors = np.asarray(colors)
    if colors.max() <= 1.0:
        colors_255 = (colors * 255).astype(np.uint8)
    else:
        colors_255 = colors.astype(np.uint8)

    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(pts3d)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        for i in range(len(pts3d)):
            x, y, z = pts3d[i]
            r, g, b = colors_255[i]
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\n")
    print(f"\n💾 Fichier MeshLab exporté : {filename}")
    print("   → Ouvrez MeshLab → File → Import Mesh → choisissez pointcloud.ply")


if __name__ == '__main__':
    visualize_3d()