// pgm.c
#include "pgm.h"

void quadr(char opr[], char op1[], char op2[], char res[]) {
    Quadruplet *newQuad = malloc(sizeof(Quadruplet));

    if (newQuad == NULL) {
        fprintf(stderr, "Erreur d'allocation mémoire\n");
        exit(EXIT_FAILURE);
    }

    strcpy(newQuad->oper, opr);
    strcpy(newQuad->op1, op1);
    strcpy(newQuad->op2, op2);
    strcpy(newQuad->res, res);

    newQuad->next = NULL;

    if (tete_quad == NULL) {
        tete_quad = newQuad;
    } else {
        Quadruplet *temp = tete_quad;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newQuad;
    }
}

void ajour_quad(int num_quad, int colon_quad, char val[]) {
    Quadruplet *temp = tete_quad;
    int i;
    
    for (i = 0; i < num_quad && temp != NULL; i++) {
        temp = temp->next;
    }
    
    if (temp == NULL) {
        fprintf(stderr, "Erreur : Quadruplet non trouvé.\n");
        return;
    }

    switch (colon_quad) {
        case 0:
            strcpy(temp->oper, val);
            break;
        case 1:
            strcpy(temp->op1, val);
            break;
        case 2:
            strcpy(temp->op2, val);
            break;
        case 3:
            strcpy(temp->res, val);
            break;
        default:
            fprintf(stderr, "Erreur : Colonne de quadruplet non valide.\n");
            break;
    }
}

void afficher_qdr() {
    printf("*********************Les Quadruplets***********************\n");

    int i = 0;
    Quadruplet *current = tete_quad;

    while (current != NULL) {
        printf("\n %d - ( %s  ,  %s  ,  %s  ,  %s )", i, current->oper, current->op1, current->op2, current->res);
        printf("\n---------------------------------------------------\n");

        current = current->next;
        i++;
    }
}