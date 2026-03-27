// ts.c
#include "ts.h"

// (definitions)
LISTE0* tete_liste0 = NULL; 
LISTE1* tete_liste1 = NULL; 
LISTE2* tete_liste2 = NULL;
Quadruplet* tete_quad = NULL;
char last_kw[20];
char last_sep[20];

// (definitions)
void insert(char entite[], char code[], char type[], float val, int y, char t[]) {
    switch (y) {
        case 0: // liste des idf et cst
            {
                LISTE0* temp = (LISTE0*)malloc(sizeof(LISTE0));
                temp->info.state = 1;
                strcpy(temp->info.name, entite);
                strcpy(temp->info.code, code);
                strcpy(temp->info.type, type);
                temp->info.val = val;
                strcpy(temp->info.taille, t);
                temp->svt = tete_liste0; 
                tete_liste0 = temp;
            }
            break;

        case 1: // liste des mots cles
            {
                LISTE1* temp = (LISTE1*)malloc(sizeof(LISTE1));
                temp->info.state = 1;
                strcpy(temp->info.name, entite);
                strcpy(temp->info.type, code);
                temp->svt = tete_liste1;
                tete_liste1 = temp;
            }
            break;

        case 2: // liste des separateurs
            {
                LISTE2* temp = (LISTE2*)malloc(sizeof(LISTE2));
                temp->info.state = 1;
                strcpy(temp->info.name, entite);
                strcpy(temp->info.type, code);
                temp->svt = tete_liste2;
                tete_liste2 = temp;
            }
            break;

        default:
            printf("ERREUR D'ALLOCATION DE TABLE \n");
            break;
    }
}

void research(char entite[], char code[], char type[], float val, int y, char t[]) {
    int exist = 0;
    switch (y) {
        case 0: // list idf / valeur / reel / entiere
            {
                LISTE0* tete0 = tete_liste0;

                if(strcmp(last_kw, "DIMENSION") == 0 || strcmp(last_kw, "CHARACTER") == 0)
                {
                    if(strcmp(last_sep, "(") == 0 && strcmp(tete0->info.taille, "") == 0)
                    {
                        strcat(tete0->info.taille, entite);
                    }
                    if(strcmp(last_sep, ",") == 0)
                    {
                        strcat(tete0->info.taille, "-");
                        strcat(tete0->info.taille, entite);
                    }
                    if(strcmp(last_sep, "*") == 0 && strcmp(tete0->info.taille, "") == 0)
                    {
                        strcat(tete0->info.taille, entite);
                    }
                }                
                else
                {
                    while (tete0 != NULL) {
                        if (strcmp(tete0->info.name, entite) == 0) {
                            exist = 1;
                            break;
                        } else {
                            tete0 = tete0->svt;
                        }
                    }
                    if (exist == 1)
                        printf("\nIDF '%s' EXISTE DEJA DANS LA TABLE DES SYMBOLE\n", entite);
                    else
                        insert(entite, code, type, val, y, t);
                }
            }
            break;
        case 1: // liste des mots cles
            {
                LISTE1* tete1 = tete_liste1;
                strcpy(last_kw, entite);
                while (tete1 != NULL) {
                    if (strcmp(tete1->info.name, entite) == 0) {
                        exist = 1;
                        break;
                    } else {
                        tete1 = tete1->svt;
                    }
                }
                if (exist == 1)
                    printf("\nMOT CLE '%s' EXIST DEJA DANS LA TABLE DES SYMBOLES\n", entite);
                else
                    insert(entite, code, type, val, y, t);
            }
            break;

        case 2: // liste des separateurs
            {
                LISTE2* tete2 = tete_liste2;
                strcpy(last_sep, entite);
                while (tete2 != NULL) {
                    if (strcmp(tete2->info.name, entite) == 0) {
                        exist = 1;
                        break;
                    } else {
                        tete2 = tete2->svt;
                    }
                }
                if (exist == 1)
                    printf("\nSEPARATEUR '%s' EXIST DEJA DANS LA TABLE DES SYMBOLES\n", entite);
                else
                    insert(entite, code, type, val, y, t);
            }
            break;
    }
}

void afficher()
{
    printf("/***************IDF - REEL - ENTIER TS*************/\n");
    printf("_________________________________________________________________________________________________________\n");
    printf("\t| Nom Entite    |      Code Entite        |    Type Entite     |   Val Entite     |    Taille Entite \n");
    printf("_________________________________________________________________________________________________________\n");
    LISTE0* temp_liste0 = tete_liste0;
    while (temp_liste0 != NULL) {
        printf(" %20s  %20s  %20s  %20f  %20s \n", temp_liste0->info.name, temp_liste0->info.code, temp_liste0->info.type, temp_liste0->info.val, temp_liste0->info.taille);
        temp_liste0 = temp_liste0->svt;
    }
    
    printf("\n/***************MOT CLE TS*************/\n");
    printf("______________________________________________________\n");
    printf("\t| Nom Entite    |  Code Entite | \n");
    printf("______________________________________________________\n");
    LISTE1* temp_liste1 = tete_liste1;
    while (temp_liste1 != NULL) {
        printf(" %20s %20s\n", temp_liste1->info.name, temp_liste1->info.type);
        temp_liste1 = temp_liste1->svt;
    }

    printf("\n/***************SEPARATEURS TS*************/\n");
    printf("_______________________________________________________\n");
    printf("\t|   Nom Entite  |  Code Entite | \n");
    printf("________________________________________________________\n");
    LISTE2* temp_liste2 = tete_liste2;
    while (temp_liste2 != NULL) {
        printf("\t %10s \t\t %10s\n", temp_liste2->info.name, temp_liste2->info.type);
        temp_liste2 = temp_liste2->svt;
    }
}

int rechercherIDF(char entite[]) {
    int position = 0;
    LISTE0* temp = tete_liste0;
    
    while (temp != NULL) {
        if (strcmp(entite, temp->info.name) == 0) {
            return position;
        }
        temp = temp->svt;
        position++;
    }
    return -1;
}

void insererTYPE(char entite[], char type[]) {
    int i;
    int pos = rechercherIDF(entite);
    if (pos != -1) {
        LISTE0* temp_liststruct1 = tete_liste0;
        for (i = 0; i < pos; i++) {
            temp_liststruct1 = temp_liststruct1->svt;
        }
        strcpy(temp_liststruct1->info.type, type);
    } else {
        printf("IDF '%s' non trouvé\n", entite);
    }
}

void SaveValue(char entite[], float val) {
    int position = rechercherIDF(entite);
    int i;
    if (position != -1) {
        LISTE0* temp = tete_liste0;
        for (i = 0; i < position; i++) {
            temp = temp->svt;
        }
        temp->info.val = val;
    } else {
        printf("IDF '%s' non trouvé. Impossible de sauvegarder la valeur.\n", entite);
    }
}

int doubleDeclaration(char entite[]) {
    LISTE0* temp_liststruct1 = tete_liste0;

    while (temp_liststruct1 != NULL) {
        if (strcmp(temp_liststruct1->info.name, entite) == 0) {
            if (strcmp(temp_liststruct1->info.type, "") != 0) {
                return -1;
            } else {
                return 0;
            }
        }
        temp_liststruct1 = temp_liststruct1->svt;
    }
    return 0;
}

int CompType(char entite[], char type[]) {
    int position = rechercherIDF(entite);
    int i;
    if (position != -1) {
        LISTE0* temp = tete_liste0;
        for (i = 0; i < position; i++) {
            temp = temp->svt;
        }
        if (strcmp(temp->info.type, type) == 0) {
            return 1;
        } else {
            return 0;
        }
    } else {
        printf("IDF '%s' non trouvé. Impossible de vérifier la compatibilité des types.\n", entite);
        return -1;
    }
}

int rechercheNonDeclare(char entite[]) {
    LISTE0* temp_liststruct1 = tete_liste0;

    while (temp_liststruct1 != NULL) {
        if (strcmp(temp_liststruct1->info.name, entite) == 0) {
            if (strcmp(temp_liststruct1->info.type, "") == 0) {
                return 0;
            } else {
                return 1;
            }
        }
        temp_liststruct1 = temp_liststruct1->svt;
    }
    return 1;
}

// // QUADRUPLES
// void quadr(char opr[], char op1[], char op2[], char res[]) {
//     Quadruplet *newQuad = malloc(sizeof(Quadruplet));

//     if (newQuad == NULL) {
//         fprintf(stderr, "Erreur d'allocation mémoire\n");
//         exit(EXIT_FAILURE);
//     }

//     strcpy(newQuad->oper, opr);
//     strcpy(newQuad->op1, op1);
//     strcpy(newQuad->op2, op2);
//     strcpy(newQuad->res, res);

//     newQuad->next = NULL;

//     if (tete_quad == NULL) {
//         tete_quad = newQuad;
//     } else {
//         Quadruplet *temp = tete_quad;
//         while (temp->next != NULL) {
//             temp = temp->next;
//         }
//         temp->next = newQuad;
//     }
// }

// void ajour_quad(int num_quad, int colon_quad, char val[]) {
//     Quadruplet *temp = tete_quad;
//     int i;
    
//     for (i = 0; i < num_quad && temp != NULL; i++) {
//         temp = temp->next;
//     }
    
//     if (temp == NULL) {
//         fprintf(stderr, "Erreur : Quadruplet non trouvé.\n");
//         return;
//     }

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
//     Quadruplet *current = tete_quad;

//     while (current != NULL) {
//         printf("\n %d - ( %s  ,  %s  ,  %s  ,  %s )", i, current->oper, current->op1, current->op2, current->res);
//         printf("\n---------------------------------------------------\n");

//         current = current->next;
//         i++;
//     }
// }