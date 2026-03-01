%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_TOKENS 500
extern char yytext_buffer[];

typedef struct {
    char type[20];
    char value[50];
    int line;
} TokenEntry;

TokenEntry token_table[MAX_TOKENS];
int token_count = 0;

void add_token(const char *type, const char *value, int line) {
    if(token_count < MAX_TOKENS) {
        strcpy(token_table[token_count].type, type);
        strcpy(token_table[token_count].value, value);
        token_table[token_count].line = line;
        token_count++;
    }
}
extern int nb_ligne;
extern int yylex();
void yyerror(const char *msg);

int nb_mots_cles = 0;
int nb_identifiants = 0;
int nb_nombres = 0;
int nb_chaines = 0;
int nb_commentaires = 0;
int nb_symboles = 0;
int nb_erreurs = 0;
%}

%token PROGRAM DEC FINDEC DEBUTPROG FINPROG IF ELSE DO
%token INT FLOAT EQUAL PRINTWINDOW
%token IDF NOMBRE CHAINE COMMENTAIRE
%token SEPARATOR G_PARENTHESE D_PARENTHESE G_ACCOLADE D_ACCOLADE
%token ERROR

%left EQUAL
%left ELSE

%%

programme: 
    PROGRAM IDF declaration_programme corps_programme FINPROG
    ;

declaration_programme:
    DEC liste_declarations FINDEC
    ;

liste_declarations:
    declaration
    | liste_declarations declaration
    ;

declaration:
    type liste_identifiants 
    ;

type:
    INT   { nb_mots_cles++; }
    | FLOAT { nb_mots_cles++; }
    ;

liste_identifiants:
    IDF SEPARATOR { nb_identifiants++; }
    | liste_identifiants IDF SEPARATOR { nb_identifiants++; }
    ;

corps_programme:
    DEBUTPROG liste_instructions
    ;

liste_instructions:
    instruction
    | liste_instructions instruction
    ;

instruction:
    affectation
    | condition
    | boucle
    | affichage
    | commentaire
    | bloc
    | error SEPARATOR {         
        yyerror("syntax error"); 
        yyerrok; 
    }    ;

affectation:
    IDF EQUAL expression SEPARATOR { nb_identifiants++; }
    ;

expression:
    IDF { nb_identifiants++; }
    | NOMBRE { nb_nombres++; }
    | CHAINE { nb_chaines++; }
    ;

condition:
    IF G_PARENTHESE expression EQUAL expression D_PARENTHESE instruction ELSE instruction
    {
        nb_mots_cles += 2; 
    }
    ;

boucle:
    DO G_ACCOLADE liste_instructions D_ACCOLADE
    {
        nb_mots_cles++; 
    }
    ;

affichage:
    PRINTWINDOW G_PARENTHESE CHAINE D_PARENTHESE SEPARATOR
    {
        nb_mots_cles++;
        nb_chaines++;
    }
    ;

bloc:
    G_ACCOLADE liste_instructions D_ACCOLADE
    ;

commentaire:
    COMMENTAIRE { nb_commentaires++; }
    ;

%%

void yyerror(const char *msg) {
    fprintf(stderr, "\n Erreur syntaxique a la ligne %d : %s->'%s'\n", nb_ligne, msg, yytext_buffer);
    nb_erreurs++;
}

void print_token_table() {

    printf("\n╔════════════╦════════════════════╦═══════╗\n");
    printf("║ %-10s ║ %-18s ║ %-5s ║\n", "TYPE", "VALEUR", "LIGNE");
    printf("╠════════════╬════════════════════╬═══════╣\n");

    for(int i=0; i<token_count; i++) {
        printf("║ %-10s ║ %-18s ║ %-5d ║\n",
                token_table[i].type,
                token_table[i].value,
                token_table[i].line);
    }

    printf("╚════════════╩════════════════════╩═══════╝\n");
}

int main(int argc, char *argv[]) {

    extern FILE *yyin; 
    printf("=== DEBUT ANALYSE SYNTAXIQUE ===\n\n");
    yyparse();
    if (nb_erreurs == 0) {
        printf("CE PROGRAMME EST SYNTAXIQUEMENT CORRECT !\n\n");
    }
    print_token_table();
    printf("\n=== FIN ANALYSE SYNTAXIQUE ===\n");
    
    printf(" RESUME DE L'ANALYSE\n");
    printf("    Mots-cles    : %d\n", nb_mots_cles);
    printf("    Identifiants : %d\n", nb_identifiants);
    printf("    Nombres      : %d\n", nb_nombres);
    printf("    Chaines      : %d\n", nb_chaines);
    printf("    Commentaires : %d\n", nb_commentaires);
    printf("    Symboles     : %d\n", nb_symboles);
    if (nb_erreurs > 0) {
        printf("   Erreurs : %d\n", nb_erreurs);
    } else {
        printf("   Analyse reussie - Aucune erreur\n");
    }
    printf("______________________________________\n");

    
    return 0;
} 