// //QUADRUPLES
// void quadr(char opr[], char op1[], char op2[], char res[]) {
//     Quadruplet *newQuad = malloc(sizeof(Quadruplet));  // Allouer de la mémoire pour un nouveau quadruplet

//     if (newQuad == NULL) {
//         // Gestion de l'erreur d'allocation de mémoire
//         fprintf(stderr, "Erreur d'allocation mémoire\n");
//         exit(EXIT_FAILURE);  // Ou tout autre traitement d'erreur approprié
//     }

//     // Copier les valeurs dans le nouveau quadruplet
//     strcpy(newQuad->oper, opr);
//     strcpy(newQuad->op1, op1);
//     strcpy(newQuad->op2, op2);
//     strcpy(newQuad->res, res);

//     newQuad->next = NULL;  // Initialiser le pointeur suivant à NULL car c'est le dernier élément de la liste

//     if (tete_quad == NULL) {
//         // Si la liste est vide, définir le nouveau quadruplet comme le début de la liste
//         tete_quad = newQuad;
//     } else {
//         // Trouver le dernier élément de la liste et ajouter le nouveau quadruplet à la fin
//         Quadruplet *temp = tete_quad;
//         while (temp->next != NULL) {
//             temp = temp->next;
//         }
//         temp->next = newQuad;  // Ajouter le nouveau quadruplet à la fin de la liste
//     }
// }

// //ajouter un quad
// void ajour_quad(int num_quad, int colon_quad, char val[]) {
//     Quadruplet *temp = tete_quad;
//     int i;
	
//     // Parcourir la liste jusqu'au quadruplet spécifié par num_quad
//     for (i = 0; i < num_quad && temp != NULL; i++) {
//         temp = temp->next;
//     }
    
//     // Vérifier si le quadruplet existe
//     if (temp == NULL) {
//         fprintf(stderr, "Erreur : Quadruplet non trouvé.\n");
//         return;
//     }

//     // Mettre à jour la valeur appropriée du quadruplet en fonction de colon_quad
//     switch (colon_quad) {
//         case 0:
//             strcpy(temp->oper, val);
//             break;
//         case 1:
//             strcpy(temp->op1, val);
//             break;
//         case 2:
//             strcpy(temp->op2, val);
//             break;
//         case 3:
//             strcpy(temp->res, val);
//             break;
//         default:
//             fprintf(stderr, "Erreur : Colonne de quadruplet non valide.\n");
//             break;
//     }
// }

// void afficher_qdr() {
//     printf("*********************Les Quadruplets***********************\n");

//     int i = 0;
//     Quadruplet *current = tete_quad;  // Commencer par le premier quadruplet de la liste

//     // Parcourir la liste jusqu'à la fin
//     while (current != NULL) {
//         printf("\n %d - ( %s  ,  %s  ,  %s  ,  %s )", i, current->oper, current->op1, current->op2, current->res);
//         printf("\n---------------------------------------------------\n");

//         // Passer au prochain quadruplet dans la liste
//         current = current->next;
//         i++;
//     }
// }


// pgm.h
#ifndef PGM_H
#define PGM_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ts.h"

// Déclarations des fonctions (prototypes seulement)
void quadr(char opr[], char op1[], char op2[], char res[]);
void ajour_quad(int num_quad, int colon_quad, char val[]);
void afficher_qdr();

#endif