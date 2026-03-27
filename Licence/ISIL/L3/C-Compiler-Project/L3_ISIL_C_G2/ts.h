
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>


// //Partie 1: definition des types et declaration des tetes de liste
// typedef struct struct1
// {
//    int state;
//    char name[20];
//    char code[20];
//    char type[20];
//    float val;
//    char taille[10];
//  } struct1;

// typedef struct struct2
// { 
//    int state; 
//    char name[20];
//    char type[20];
// } struct2;

// typedef struct LISTE0
// {
//     struct1 info;
//     struct LISTE0* svt;
// }LISTE0;

// typedef struct LISTE1
// {
//     struct2 info;
//     struct LISTE1* svt;
// }LISTE1;

// typedef struct LISTE2
// {
//     struct2 info;
//     struct LISTE2* svt;
// }LISTE2;
// // Structure pour stocker les signes de formatage
// typedef struct {
//     char signFormatage;
// 	char idf[20];
// } compatibilite;

// typedef struct Quadruplet {
//     char oper[50];
//     char op1[50];
//     char op2[50];
//     char res[50];
//     struct Quadruplet *next;  // Pointeur vers le prochain quadruplet dans la liste
// } Quadruplet;


// LISTE0* tete_liste0 = NULL; 
// LISTE1* tete_liste1 = NULL; 
// LISTE2* tete_liste2 = NULL;
// Quadruplet* tete_quad = NULL;
// char last_kw[20];
// char last_sep[20];

// //Partie 2: insertion des entite dans les listes des symboles
// void insert(char entite[], char code[], char type[], float val, int y, char t[]) {
//     switch (y) {
//         case 0: // liste des idf et cst
//             {
//                 LISTE0* temp = (LISTE0*)malloc(sizeof(LISTE0));
//                 temp->info.state = 1;
//                 strcpy(temp->info.name, entite);
//                 strcpy(temp->info.code, code);
//                 strcpy(temp->info.type, type);
//                 temp->info.val = val;
//                 strcpy(temp->info.taille, t);
//                 temp->svt = tete_liste0; 
//                 tete_liste0 = temp;
//             }
//             break;

//         case 1: // liste des mots cles
//             {
//                 LISTE1* temp = (LISTE1*)malloc(sizeof(LISTE1));
//                 temp->info.state = 1;
//                 strcpy(temp->info.name, entite);
//                 strcpy(temp->info.type, code);
//                 temp->svt = tete_liste1;
//                 tete_liste1 = temp;
//             }
//             break;

//         case 2: // liste des separateurs
//             {
//                 LISTE2* temp = (LISTE2*)malloc(sizeof(LISTE2));
//                 temp->info.state = 1;
//                 strcpy(temp->info.name, entite);
//                 strcpy(temp->info.type, code);
//                 temp->svt = tete_liste2;
//                 tete_liste2 = temp;
//             }
//             break;

//         default:
//             printf("ERREUR D'ALLOCATION DE TABLE \n");
//             break;
//     }
// }

// //Partie 3 : rechercher l'existance dans la ts

// void research(char entite[], char code[], char type[], float val, int y, char t[]) {
//     int exist = 0;
//     switch (y) {
//             case 0: // list idf / valeur / reel / entiere
//             {
//                 LISTE0* tete0 = tete_liste0;

//                 if(strcmp(last_kw, "DIMENSION") == 0 || strcmp(last_kw, "CHARACTER") == 0)
//                 {
//                     if(strcmp(last_sep, "(") == 0 && strcmp(tete0->info.taille, "") == 0)
//                     {
//                         strcat(tete0->info.taille, entite);
//                     }
//                     if(strcmp(last_sep, ",") == 0)
//                     {
//                         strcat(tete0->info.taille, "-");
//                         strcat(tete0->info.taille, entite);
//                     }
//                     if(strcmp(last_sep, "*") == 0 && strcmp(tete0->info.taille, "") == 0)
//                     {
//                         strcat(tete0->info.taille, entite);
//                     }
//                 }                
//                 else
//                 {
//                     while (tete0 != NULL) {
//                     if (strcmp(tete0->info.name, entite) == 0) {
//                         exist = 1;
//                         break;
//                     } else {
//                         tete0 = tete0->svt;
//                     }
//                     }
//                     if (exist == 1)
//                         printf("\nIDF '%s' EXISTE DEJA DANS LA TABLE DES SYMBOLE\n",entite );
//                     else
//                         insert(entite, code, type, val, y, t);
//                 }
                
//             }
//             break;
//         case 1: // liste des mots cles
//             {
//                 LISTE1* tete1 = tete_liste1;
//                 strcpy(last_kw, entite);
//                 while (tete1 != NULL) {
//                     if (strcmp(tete1->info.name, entite) == 0) {
//                         exist = 1;
//                         break;
//                     } else {
//                         tete1 = tete1->svt;
//                     }
//                 }
//                 if (exist == 1)
//                     printf("\nMOT CLE '%s' EXIST DEJA DANS LA TABLE DES SYMBOLES\n",entite);
//                 else
//                     insert(entite, code, type, val, y, t);
//             }
//             break;

//         case 2: // liste des separateurs
//             {
//                 LISTE2* tete2 = tete_liste2;
//                 strcpy(last_sep, entite);
//                 while (tete2 != NULL) {
//                     if (strcmp(tete2->info.name, entite) == 0) {
//                         exist = 1;
//                         break;
//                     } else {
//                         tete2 = tete2->svt;
//                     }
//                 }
//                 if (exist == 1)
//                      printf("\nSEPARATEUR '%s' EXIST DEJA DANS LA TABLE DES SYMBOLES\n",entite);
//                 else
//                     insert(entite, code, type, val, y, t);
//             }
//             break;
//     }
// }


// //Partie 4: afficher la TS
// void afficher()
// {
//     printf("/***************IDF - REEL - ENTIER TS*************/\n");
//     printf("_________________________________________________________________________________________________________\n");
//     printf("\t| Nom Entite    |      Code Entite        |    Type Entite     |   Val Entite     |    Taille Entite \n");
//     printf("_________________________________________________________________________________________________________\n");
//     LISTE0* temp_liste0 = tete_liste0;
//         while (temp_liste0 != NULL) {
//             printf(" %20s  %20s  %20s  %20f  %20s \n", temp_liste0->info.name, temp_liste0->info.code, temp_liste0->info.type, temp_liste0->info.val, temp_liste0->info.taille);
//             temp_liste0 = temp_liste0->svt;
//         }
    
//     printf("\n/***************MOT CLE TS*************/\n");
//     printf("______________________________________________________\n");
//     printf("\t| Nom Entite    |  Code Entite | \n");
//     printf("______________________________________________________\n");
//     LISTE1* temp_liste1 = tete_liste1;
//     while (temp_liste1 != NULL) {
//         printf(" %20s %20s\n", temp_liste1->info.name, temp_liste1->info.type);
//         temp_liste1 = temp_liste1->svt;
//     }


//     printf("\n/***************SEPARATEURS TS*************/\n");
//     printf("_______________________________________________________\n");
//     printf("\t|   Nom Entite  |  Code Entite | \n");
//     printf("________________________________________________________\n");
//     LISTE2* temp_liste2 = tete_liste2;
//     while (temp_liste2 != NULL) {
//         printf("\t %10s \t\t %10s\n", temp_liste2->info.name, temp_liste2->info.type);
//         temp_liste2 = temp_liste2->svt;
//     }

// }



// // Fonction rechercherIDF avec liste
// int rechercherIDF(char entite[]) {
//     int position = 0;
//     LISTE0* temp = tete_liste0;
    
//     while (temp != NULL) {
//         if (strcmp(entite, temp->info.name) == 0) {
//             return position;  // Retourne la position de l'IDF si trouvé
//         }
//         temp = temp->svt;
//         position++;
//     }
//     return -1;  // Si l'IDF n'est pas trouvé
// }



// //la fonction qui permet d'inserer un type à une variable (IDF) 
// void insererTYPE(char entite[], char type[]) {
//     int i;
// 	int pos = rechercherIDF(entite);  // Recherche la position de l'entité
//     if (pos != -1) {
//         // Si l'entité est trouvée, modifiez son type
//         LISTE0* temp_liststruct1 = tete_liste0;
//         for ( i = 0; i < pos; i++) {
//             //printf("\nposition %d of %d\n",i,pos);
//             temp_liststruct1 = temp_liststruct1->svt;
//         }
//         strcpy( temp_liststruct1->info.type, type);
//     } else {
//         // Si l'entité n'est pas trouvée, vous pouvez choisir d'insérer ici ou d'afficher un message d'erreur.
//         printf("IDF '%s' non trouvé\n", entite);
//     }
// }





// // Fonction qui sauvegarde la valeur des variables dans la liste
// void SaveValue(char entite[], float val) {
//     int position = rechercherIDF(entite); // Trouver la position de l'IDF dans la liste
//     int i;
//     if (position != -1) {
//         // Parcourir la liste jusqu'à la position de l'IDF
//         LISTE0* temp = tete_liste0;
//         for (i = 0; i < position; i++) {
//             temp = temp->svt;
//         }
        
//         // Mettre à jour la valeur de l'IDF
//         temp->info.val = val;
//     } else {
//         printf("IDF '%s' non trouvé. Impossible de sauvegarder la valeur.\n", entite);
//     }
// }



// int doubleDeclaration(char entite[]) {
//     LISTE0* temp_liststruct1 = tete_liste0;  // Commencez par le début de la liste

//     while (temp_liststruct1 != NULL) {
//         if (strcmp(temp_liststruct1->info.name, entite) == 0) {
//             // Si l'entité est trouvée et son type n'est pas une chaîne vide
//             if (strcmp(temp_liststruct1->info.type, "") != 0) {
//                 return -1;  // La variable est doublement déclarée
//             } else {
//                 return 0;   // La variable n'est pas doublement déclarée
//             }
//         }
//         temp_liststruct1 = temp_liststruct1->svt;  // Passez au prochain élément de la liste
//     }
    
//     return 0;  // Si l'entité n'est pas trouvée, elle n'est pas considérée comme doublement déclarée
// }









// // Fonction qui vérifie la compatibilité des types pour un IDF donné
// int CompType(char entite[], char type[]) {
//     int position = rechercherIDF(entite); // Trouver la position de l'IDF dans la liste
//     int i;
//     if (position != -1) {
//         // Parcourir la liste jusqu'à la position de l'IDF
//         LISTE0* temp = tete_liste0;
//         for (i = 0; i < position; i++) {
//             temp = temp->svt;
//         }
        
//         // Comparer le type de l'IDF avec le type donné
//         if (strcmp(temp->info.type, type) == 0) {
//             return 1;  // Le type est compatible
//         } else {
//             return 0;  // Le type n'est pas compatible
//         }
//     } else {
//         printf("IDF '%s' non trouvé. Impossible de vérifier la compatibilité des types.\n", entite);
//         return -1;  // Retourne -1 si l'IDF n'est pas trouvé
//     }
// }




// int rechercheNonDeclare(char entite[]) {
//     LISTE0* temp_liststruct1 = tete_liste0;  // Commencez par le début de la liste

//     while (temp_liststruct1 != NULL) {
//         if (strcmp(temp_liststruct1->info.name, entite) == 0) {
//             // Si l'IDF est trouvé et son type est vide
//             if (strcmp(temp_liststruct1->info.type, "") == 0) {
//                 return 0;  // La variable n'est pas déclarée
//             } else {
//                 return 1;  // La variable est déclarée
//             }
//         }
//         temp_liststruct1 = temp_liststruct1->svt;  // Passez au prochain élément de la liste
//     }
    
//     return 1;  // Si l'IDF n'est pas trouvé, il est considéré comme déclaré
// }



#ifndef TS_H
#define TS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Partie 1: definition des types et declaration des tetes de liste
typedef struct struct1
{
   int state;
   char name[20];
   char code[20];
   char type[20];
   float val;
   char taille[10];
} struct1;

typedef struct struct2
{ 
   int state; 
   char name[20];
   char type[20];
} struct2;

typedef struct LISTE0
{
    struct1 info;
    struct LISTE0* svt;
} LISTE0;

typedef struct LISTE1
{
    struct2 info;
    struct LISTE1* svt;
} LISTE1;

typedef struct LISTE2
{
    struct2 info;
    struct LISTE2* svt;
} LISTE2;

// Structure pour stocker les signes de formatage
typedef struct {
    char signFormatage;
    char idf[20];
} compatibilite;

typedef struct Quadruplet {
    char oper[50];
    char op1[50];
    char op2[50];
    char res[50];
    struct Quadruplet *next;
} Quadruplet;

// Declaration des variables globales (extern)
extern LISTE0* tete_liste0; 
extern LISTE1* tete_liste1; 
extern LISTE2* tete_liste2;
extern Quadruplet* tete_quad;
extern char last_kw[20];
extern char last_sep[20];
extern int yyleng;

// Declaration des fonctions
void insert(char entite[], char code[], char type[], float val, int y, char t[]);
void research(char entite[], char code[], char type[], float val, int y, char t[]);
void afficher();
int rechercherIDF(char entite[]);
void insererTYPE(char entite[], char type[]);
void SaveValue(char entite[], float val);
int doubleDeclaration(char entite[]);
int CompType(char entite[], char type[]);
int rechercheNonDeclare(char entite[]);
void quadr(char opr[], char op1[], char op2[], char res[]);
void ajour_quad(int num_quad, int colon_quad, char val[]);
void afficher_qdr();

#endif