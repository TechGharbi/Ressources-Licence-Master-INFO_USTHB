%{
    /* Partie Declaration en c*/
    int nb_ligne=1;
    char yytext_buffer[50];

    #include <stdio.h>
    #include <string.h>
    #include "syn.tab.h"
    
    extern int nb_mots_cles;
    extern int nb_identifiants;
    extern int nb_nombres;
    extern int nb_chaines;
    extern int nb_commentaires;
    extern int nb_symboles;
    extern int nb_erreurs;

    void add_token(const char *type, const char *value, int line);

%}

%option noyywrap 

IDF     [a-zA-Z_][a-zA-Z0-9_]*
chaine  \'[^\']*\' 
Nbr     [0-9]+

commentaire "//*"(.)*"*//"

%%

Program     { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return PROGRAM; }
DEC         { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return DEC; }
FinDEC      { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return FINDEC; }
DebutProg   { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return DEBUTPROG; }
FinProg     { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return FINPROG; }
If          { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return IF; }
Else        { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return ELSE; }
Do          { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return DO; }
printWindow { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return PRINTWINDOW; }
equal       { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return EQUAL; }

"int"       { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return INT; }
"float"     { strcpy(yytext_buffer, yytext); add_token("Mot cle", yytext, nb_ligne); nb_mots_cles++; return FLOAT; }

{IDF}         { strcpy(yytext_buffer, yytext); add_token("IDF", yytext, nb_ligne); nb_identifiants++; return IDF; }
{chaine}      { strcpy(yytext_buffer, yytext); add_token("Chaine", yytext, nb_ligne); nb_chaines++; return CHAINE;}
{Nbr}         { strcpy(yytext_buffer, yytext); add_token("Nombre", yytext, nb_ligne); nb_nombres++; return NOMBRE;}
{commentaire} { strcpy(yytext_buffer, yytext); add_token("Comment", yytext, nb_ligne); nb_commentaires++; return COMMENTAIRE;}

[#|]        { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return SEPARATOR; }
"("         { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return G_PARENTHESE; }
")"         { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return D_PARENTHESE; }
"{"         { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return G_ACCOLADE; }
"}"         { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return D_ACCOLADE; }
[,]         { strcpy(yytext_buffer, yytext); add_token("Symbole", yytext, nb_ligne); nb_symboles++; return SEPARATOR; }

[ \t]     ;
\n        {nb_ligne++;}

.         { strcpy(yytext_buffer, yytext);
    add_token("Erreur", yytext, nb_ligne); 
    return ERROR;
    }

%%
