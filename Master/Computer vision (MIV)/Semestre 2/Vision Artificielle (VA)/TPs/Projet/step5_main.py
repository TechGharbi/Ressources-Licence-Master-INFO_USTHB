"""
╔══════════════════════════════════════════════════════╗
║   PROJET — STÉRÉOVISION SIFT                        ║
║   Master Informatique Visuelle — USTHB 2025/2026    ║
║   Prof. Slimane LARABI                               ║
╚══════════════════════════════════════════════════════╝

PIPELINE COMPLET :
    1. Calibration caméra
    2. Détection & matching SIFT
    3. Reconstruction 3D (triangulation)
    4. Visualisation nuage de points

UTILISATION :
    python step5_main.py --all          → pipeline complet (ordre correct)
    python step5_main.py --calib        → calibration seulement
    python step5_main.py --sift         → SIFT + matching seulement
    python step5_main.py --reconstruct  → reconstruction 3D (utilise matches.npz existant)
    python step5_main.py --viz          → visualisation seulement
"""

import argparse
import os
import sys

def check_dependencies():
    """Vérifie que toutes les librairies sont installées."""
    missing = []
    try:
        import cv2
        sift = cv2.SIFT_create()
    except ImportError:
        missing.append("opencv-python")
    except AttributeError:
        missing.append("opencv-contrib-python (pour SIFT)")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    try:
        import matplotlib
    except ImportError:
        missing.append("matplotlib")
    if missing:
        print(" Librairies manquantes :")
        for m in missing:
            print(f"   pip install {m}")
        sys.exit(1)
    print("✅ Toutes les dépendances sont installées.\n")

def check_files(mode):
    """Vérifie que les fichiers nécessaires existent."""
    if mode in ['sift', 'reconstruct', 'all']:
        # Accepter .png ou .jpg
        img1 = 'MES IMAGES/im1D.png'
        img2 = 'MES IMAGES/im2G.png'
        if not os.path.exists(img1):
            img1 = 'MES IMAGES/im1D.jpg'
        if not os.path.exists(img2):
            img2 = 'MES IMAGES/im2G.jpg'
        if not os.path.exists(img1) or not os.path.exists(img2):
            print(" Fichiers manquants : im1D et im2G (format .png ou .jpg)")
            sys.exit(1)
    if mode in ['reconstruct', 'viz']:
        if not os.path.exists('camera_params.npz'):
            print(" Fichier manquant : camera_params.npz")
            print("   Lancez d'abord : python step5_main.py --calib")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Stéréovision SIFT — USTHB 2025/2026')
    parser.add_argument('--all',         action='store_true', help='Pipeline complet (ordre 1→2→3→4)')
    parser.add_argument('--calib',       action='store_true', help='Calibration seulement')
    parser.add_argument('--sift',        action='store_true', help='SIFT + matching seulement')
    parser.add_argument('--reconstruct', action='store_true', help='Reconstruction 3D (utilise matches.npz)')
    parser.add_argument('--viz',         action='store_true', help='Visualisation seule')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        print("\n💡 Exemple : python step5_main.py --all")
        sys.exit(0)

    check_dependencies()

    # ── 1. CALIBRATION ────────────────────────────────────
    if args.calib or args.all:
        from step1_calibration import calibrate
        calibrate()
        print()

    # ── 2. SIFT + MATCHING ───────────────────────────────
    if args.sift or args.all:
        check_files('sift')
        from step2_sift_matching import detect_and_match
        detect_and_match()
        print()

    # ── 3. RECONSTRUCTION 3D ─────────────────────────────
    if args.reconstruct or args.all:
        check_files('reconstruct')
        from step3_reconstruction import reconstruct_3d
        # On ne passe pas de points → reconstruct_3d cherchera matches.npz (créé par step2)
        result = reconstruct_3d()
        print()
        if result:
            pts3d, colors = result
            from step4_visualization import visualize_3d
            visualize_3d(pts3d, colors)

    # ── 4. VISUALISATION SEULE ───────────────────────────
    if args.viz:
        check_files('viz')
        from step4_visualization import visualize_3d
        visualize_3d()

    print("\n" + "═" * 55)
    print("   ✅ Projet terminé avec succès !")
    print("═" * 55 + "\n")

if __name__ == '__main__':
    main()