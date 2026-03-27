%{ 
   #include "ts.h"
   #include "pgm.h"
   #include "syntaxique.tab.h"
   
   int nb_ligne=1; 
   int nb_colonne=1;    
%}


lettre [a-zA-Z]
chiffre [0-9]
IDF {lettre}({lettre}|{chiffre})* 
ENTIER [+-]?{chiffre}+
REEL  [+-]?{chiffre}+[\.]{chiffre}*[1-9]
guillemet ["]
chaine {guillemet}[^"]*{guillemet}
com [%](.)*
%%

PROGRAM   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_pgm\n"); nb_colonne=nb_colonne +strlen(yytext);return mc_pgm;}
INTEGER   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_entier\n");nb_colonne=nb_colonne +strlen(yytext);return mc_entier;}
CHARACTER { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_char\n");nb_colonne=nb_colonne +strlen(yytext);return mc_char;}
LOGICAL      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_logical\n");nb_colonne=nb_colonne +strlen(yytext);return mc_logical;}
REAL      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_reel\n");nb_colonne=nb_colonne +strlen(yytext);return mc_reel;}
END       { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_END\n\n\n");nb_colonne=nb_colonne +strlen(yytext);;return mc_END;}
ENDR      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_ENDR\n");nb_colonne=nb_colonne +strlen(yytext);return mc_ENDR;}
ROUTINE   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_routine\n");nb_colonne=nb_colonne +strlen(yytext);return mc_routine;}
IF        { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_if\n");nb_colonne=nb_colonne +strlen(yytext);return mc_if;}
THEN      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_then\n");nb_colonne=nb_colonne +strlen(yytext);return mc_then;}
ENDIF    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_endif\n");nb_colonne=nb_colonne +strlen(yytext);return mc_endif;}
ELSE      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_else\n");nb_colonne=nb_colonne +strlen(yytext);return mc_else;}
DOWHILE   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_dowhile\n");nb_colonne=nb_colonne +strlen(yytext);return mc_dowhile;}
ENDDO     { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_enddo\n");nb_colonne=nb_colonne +strlen(yytext);return mc_enddo;}
CALL      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,"");  printf ("Entite lexical reconnue : mc_call\n");nb_colonne=nb_colonne +strlen(yytext);return mc_call;}
EQUIVALENCE { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_equivalence\n");nb_colonne=nb_colonne +strlen(yytext);return mc_equivalence;}
READ      { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_read\n");nb_colonne=nb_colonne +strlen(yytext);return mc_read;}
WRITE     { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_write\n");nb_colonne=nb_colonne +strlen(yytext);return mc_write;}
DIMENSION { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_Dimension\n");nb_colonne=nb_colonne +strlen(yytext);return mc_Dimension;}
".OR."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_or\n");nb_colonne=nb_colonne +strlen(yytext);return mc_ou;}
".AND."   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : mc_and\n");nb_colonne=nb_colonne +strlen(yytext);return mc_et;}
".GT."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_GT;}
".EQ."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_EQ;}
".NE."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_NE;}
".LE."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_LE;}
".GE."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_GE;}
".LT."    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_LT;}
"TRUE"    { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_TRUE;}
"FALSE"   { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue :  comparator\n");nb_colonne=nb_colonne +strlen(yytext);return mc_FALSE;}
{guillemet}  { yylval.str=strdup(yytext); research(yytext, "KEY WORD","",0,1,""); printf ("Entite lexical reconnue : guillemet %s \n", yytext);nb_colonne=nb_colonne +strlen(yytext);return guillemet;}
{chaine}  {printf ("Entite lexical reconnue : CHAINE %s \n", yytext);nb_colonne=nb_colonne +strlen(yytext);return chaine;}
{IDF}     { yylval.str=strdup(yytext); 
if (yyleng>10)
{printf("IDF %s NON ACCEPTER : TAILLE MAXIMALE DEPASSE, \n",yytext);}
else{research(yytext, "IDF","",0,0,""); 
printf ("Entite lexical reconnue : idf %s \n", yytext);
nb_colonne=nb_colonne +strlen(yytext);
nb_colonne=nb_colonne +strlen(yytext);
return idf;} }
{ENTIER}  { yylval.entier=atoi(yytext);if (atoi(yytext) <= -32768 || atoi(yytext)>= 32767) {printf("NOMBRE ENTIER %d NON ACCEPTER : NON INCLUE DANS L'INTERVALLE\n",atoi(yytext));}else { research(yytext, "INTEGER","",0,0,"");printf ("Entite lexical reconnue : ENTIER %s \n", yytext);nb_colonne=nb_colonne +strlen(yytext);return ENTIER;}}
{REEL}    { yylval.reel=atof(yytext);if (atof(yytext) <= -32768.32768 || atof(yytext)>= 32767.32768) {printf("NOMBRE REEL %d NON ACCEPTER :NON INCLUE DANS L'INTERVALLE\n",atoi(yytext));}else { research(yytext, "REAL","",0,0,"");printf ("Entite lexical reconnue : REEL %s \n", yytext);nb_colonne=nb_colonne +strlen(yytext);return REEL;}}
"-"       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : op\n");nb_colonne=nb_colonne +strlen(yytext);return sous;}
"+"       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : op\n");nb_colonne=nb_colonne +strlen(yytext);return add;}
"/"       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,"");printf ("Entite lexical reconnue : op\n");nb_colonne=nb_colonne +strlen(yytext);return divi;}
"*"       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : op\n");nb_colonne=nb_colonne +strlen(yytext);return mult;}
"="       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : aff\n");nb_colonne=nb_colonne +strlen(yytext);return aff;}
"("       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : parou\n");nb_colonne=nb_colonne +1," ";return parou;}
")"       { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : parfer\n");nb_colonne=nb_colonne +strlen(yytext);return parfer;}
,         { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : vrg\n");nb_colonne=nb_colonne +strlen(yytext);return vrg;}
;         { yylval.str=strdup(yytext); research(yytext, "SEPARATOR","",0,2,""); printf ("Entite lexical reconnue : pvg\n");nb_colonne=nb_colonne +strlen(yytext);return pvg;}
{com}     { printf (" This is a comment :  %s \n", yytext);nb_colonne=1," ";}
[ \t]    
\n        { nb_ligne++; nb_colonne=1," ";} 
.    {printf("Lexical error, Unrecognized entity '%s' in file : '%s' , line : %d , column : %d \n\n",yytext,__FILE__,nb_ligne,nb_colonne); nb_colonne=nb_colonne +strlen(yytext);} 

%%

