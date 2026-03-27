%{
	#include <stdio.h>
	#include <string.h>
	#include <stdlib.h>
	#include "ts.h"
	#include "pgm.h"

	extern int yyleng;
	int err = 0; 
	extern int nb_ligne;
	extern int nb_colonne;

	char   sauvType[20];//variable pour sauvegareder le type
	char   sauvType1[20];
	char temp1[25] = "TEMP"; //temporaire 
	char sauvOpr[20]; //sauvegareder l'operation
	char sauvIDF1[20]; //sauvegarder un idf 
	char sauvIDF[20]; //sauvegarder un idf 
	char sauvLOG[20]; //sauvegarder operateur logique ou comperateur
	char medType[30];
	char s[25]; //stocker le premier idf pour les operation de comparaison (kayn probleme fih)
	char saveCst[20]; //sauvegarder un idf ou un var (kima ENTIER REEL ett)
	int qc=0; //indice de matrice quadr
	char tmp[25];//temporaire apres nchof wsh ndir bih pour stocker fih le contenu du temporaire et pas juste print le mot temp1
	char op1[25];//variable pour stocker l'operande 1
	char op2[25];//variable pour stocker l'operande 1
	int AND_or_OR = 1; //pour voir si on a un "ou" ou un "et"  AND=1 OR=0
	int eval=0;//varibale boolen pour stocker sois la premiere operande sois la deuxieme dans op1 et op2 respectivement
	int aritm=0; //kima eval mais pour les operations arithmetiques 
	int sauv_BZ=0,sauv_deb=0,sauv_BR; //etiquette
	int comp=0; //kont 7aba n'utilisiha kima eval et arithm pour les comparaison mzl ma mchat
	char s2[20];
	char Routinenom[10];

	void yyerror(const char *s);
	int yylex(void);
%}


%union {
	float reel;
	int entier;
	char charachter;
	char* str;
}

%token <str>mc_pgm <str>mc_entier <str>mc_reel <str>mc_char <str>mc_END <str>mc_ENDR <str>mc_routine  <str>mc_if <str>mc_then <str>mc_endif 
<str>mc_else <str>mc_dowhile <str>mc_enddo <str>mc_call <str>mc_equivalence <str>mc_read <str>mc_write <str>mc_ou <str>mc_et <str>mc_Dimension 
idf <str>aff <str>parou <str>parfer <str>pvg <str>vrg  <str>chaine <reel>REEL <entier>ENTIER  <str>add <str>sous <str>mult
<str>divi <str>mc_GT <str>mc_LT <str>mc_EQ <str>mc_NE <str>mc_LE <str>mc_GE <str>mc_TRUE <str>mc_FALSE <str>mc_logical
%token <str> guillemet

%left mult divi
%left add sous 
%left mc_GT mc_LT mc_EQ mc_NE mc_LE mc_GE
%left mc_et
%left mc_ou

%%

S :  FONCTION   mc_pgm  idf  DEC  INST  mc_END {printf("CE PROGRAMME EST SYNTAXIQUEMENT CORRECT !\n\n"); YYACCEPT;} 
;
FONCTION : TYPE mc_routine  idf PARAMETRE  DEC  INSTR  mc_ENDR FONCTION {strcpy(Routinenom,$3);}
			| 
;
DEC : TYPE idf  { 
			if (rechercheNonDeclare($2)==0) {insererTYPE($2,sauvType);}
else {printf("\nErreur semantique 'double declaration' a la ligne %d,la variable %s est deja declaree \n", nb_ligne-1, $2);}}
D
| 
;

D : mc_Dimension TAILLE SUITE | SUITE | mult VAL SUITE |
;
SUITE : pvg DEC | vrg idf {  
			if (rechercheNonDeclare($2)==0) {insererTYPE($2,sauvType);}
			else {printf("\nErreur semantique 'double declaration' a la ligne %d,la variable %s est deja declaree \n", nb_ligne, $2);}
			} D 
;  
INSTR : mc_read parou idf {if (rechercheNonDeclare($3)==0) {printf("Erreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1); insererTYPE($3,sauvType);}} parfer pvg  INSTR 
											
|mc_write parou CH parfer pvg INSTR 
|idf  aff mc_call idf {if (rechercheNonDeclare($1)==0){printf("La fonction n'est pas declare\n");}} PARAMETRE pvg INSTR

|mc_equivalence PARAMETRE vrg  PARAMETRE pvg INSTR 
|mc_dowhile {sauv_deb=qc;}CON {quadr("BZ","FIN","COND.TEMP","VIDE"); sauv_BZ=qc; qc=qc+1;} INST {qc=qc+1; ajour_quad(sauv_BZ+1,1,tmp); quadr("BR","debut","VIDE","VIDE");} mc_enddo INSTR
|mc_if parou COND {if(AND_or_OR==1) {quadr("BZ","ELSE","COND.TEMP","VIDE" );} else {quadr("BNZ","deb.then","COND.TEMP","VIDE" );quadr("=",saveCst,op1,temp1); quadr("BZ","ELSE","VIDE","VIDE");} sauv_BZ=qc; qc=qc+1;}
mc_then  
INST {
quadr("BR","FIN" ,"VIDE" ,"VIDE"); sauv_BR=qc; qc=qc+1;ajour_quad(sauv_BZ+1,1,tmp);}  I INSTR  { sauv_BR=qc; qc=qc+1;ajour_quad(sauv_BZ+1,1,tmp);}
|AFF pvg INSTR 
|idf  aff VAL {strcpy(sauvIDF,$1);
				if(strcmp(sauvIDF,Routinenom)!=0){printf("\nERREUR SEMENTIQUE A LA LIGNE %d : RETOUR DE LA FONCTION INCORRECT IDF INCOMPATIBLE\n",nb_ligne-1);}
				sprintf(saveCst,"%d",$1);quadr("=",sauvIDF1,"VIDE",sauvIDF);
			if (rechercheNonDeclare($1)==1) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);insererTYPE($1,sauvType);}}
;
INST : mc_read parou idf {if (rechercheNonDeclare($3)==0) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$3);insererTYPE($3,sauvType);}} parfer pvg INST 

|mc_write parou CH parfer pvg  INST 
|idf  aff mc_call idf PARAMETRE pvg INST {if (rechercheNonDeclare($1)==0) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);insererTYPE($1,sauvType);}
										if (rechercheNonDeclare($4)==0) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$4);insererTYPE($4,sauvType);}						             
										}
|mc_equivalence PARAMETRE vrg  PARAMETRE  pvg INST
|mc_dowhile {sauv_deb=qc;}CON {quadr("BZ","FIN","COND.TEMP","VIDE"); sauv_BZ=qc; qc=qc+1;} INST {qc=qc+1; ajour_quad(sauv_BZ+1,1,tmp); quadr("BR","debut","VIDE","VIDE");} mc_enddo INST
|mc_if parou COND{if(AND_or_OR==1) {quadr("BZ","ELSE","COND.TEMP","VIDE" );} else {quadr("BR","deb.cond2","COND.TEMP","VIDE" );} sauv_BZ=qc; qc=qc+1;}
mc_then {quadr(sauvOpr,saveCst,op2,temp1);}
INST {quadr("BR","VIDE" ,"VIDE" ,"VIDE"); sauv_BZ=qc; qc=qc+1;ajour_quad(sauv_BZ+1,1,tmp);}  I INST  { sauv_BR=qc; qc=qc+1;ajour_quad(sauv_BZ+1,1,tmp);}


|AFF pvg INST  { sauv_BR=qc; qc=qc+1;ajour_quad(sauv_BZ+1,1,tmp);}
|
; 
I : {ajour_quad(sauv_BR+1,1,tmp);}  mc_endif 
	| mc_else  INST {ajour_quad(sauv_BR+1,1,tmp);} mc_endif
;

AFF : idf  aff EXP{if (rechercheNonDeclare($1)==0 ){printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);insererTYPE($1,sauvType);
					if((strcmp(sauvOpr,"/")==0)&&(strcmp(sauvIDF1,"0")==0))
					{printf(" \nErreur semantique 'division par zero' a la ligne %d\n",nb_ligne);}}
				strcpy(sauvIDF1,$1); 
				if(aritm==1){quadr("=",temp1,"VIDE",sauvIDF1);} else {  quadr("=",saveCst,"VIDE",sauvIDF1); }		
				if ((CompType($1,sauvType)==0) && (CompType(sauvIDF1,sauvType)==0)) {{printf("\nErreur semantique a la ligne %d : ICOMPATIBILITE DE TYPE de la variable %s %s \n", nb_ligne, sauvIDF1 , saveCst);}}}
				;

EXP : VAL1  EXP1  {if(strcmp(sauvOpr,"+")==0 ||strcmp(sauvOpr,"*")==0 || strcmp(sauvOpr,"/")==0 || strcmp(sauvOpr,"-")==0)
{ quadr(sauvOpr,op1,saveCst,temp1); aritm=1;}}
; 
EXP1 : { aritm=1; eval=1;aritm=1;}OPERATION VAL1  {  
				if((strcmp(sauvOpr,"/")==0)&&(strcmp(sauvIDF1,"0")==0))
					{printf("\nErreur semantique 'division par zero' a la ligne %d \n",nb_ligne);}}        
EXP1 
| 
; 
VAL1:VAL 
|idf {strcpy(sauvIDF1,$1); sprintf(saveCst,"%d",$1);
if (rechercheNonDeclare($1)==0) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);
insererTYPE($1,sauvType);}
} parou VAL O parfer 
| parou EXP parfer 
;
O:  vrg VAL |
;
CH : chaine CH1 | idf CH1 
;
CH1 : vrg CH | 
;             
VAL :ENTIER { 
insererTYPE(sauvIDF1,sauvType);sprintf(sauvIDF1,"%d",$1);
sprintf(saveCst,"%d",$1); 

}
|idf {if(rechercheNonDeclare($1)==0 ) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);insererTYPE($1,sauvType);}
strcpy(saveCst,$1); 
if(eval==0) {strcpy(op1,$1);} else{strcpy(op2,$1);} eval=0;
if(comp==0) {strcpy(s,$1);} else {strcpy(s2,$1);}; 
}
| REEL  {insererTYPE(sauvIDF1,sauvType);sprintf(saveCst,"%0.5f",$1); }
| chaine {strcpy(saveCst,$1);}
| BOOL 
;
P4: P1 | P2 
;
P1 : VAL P3 
; 
P2 : idf {if (rechercheNonDeclare($1)==0) {printf("\nErreur semantique a la ligne  %d : la variable %s n'est pas declaree !!\n",nb_ligne,$1);insererTYPE($1,sauvType);}} TAILLE P3 
;
P3 : vrg P4 |
;
PARAMETRE: parou PAR1
;
PAR1 : P4 parfer | parfer
;
TAILLE : parou ENTIER T1 
;
T1 : parfer | vrg ENTIER parfer 
;
OPERATION :  mult {strcpy(sauvOpr,$1);  } | divi {strcpy(sauvOpr,$1);} | sous {strcpy(sauvOpr,$1);} | add { strcpy(sauvOpr,$1);} {aritm=0;}
;
COMPARATOR : mc_GT {strcpy(sauvLOG,$1);comp=1;} | mc_LT {strcpy(sauvLOG,$1);comp=1;} | mc_EQ {strcpy(sauvLOG,$1);comp=1;} | mc_NE {strcpy(sauvLOG,$1);comp=1;} | mc_LE {strcpy(sauvLOG,$1);comp=1;} | mc_GE {strcpy(sauvLOG,$1);comp=1;}
;
TYPE : mc_reel {strcpy(sauvType,$1);}
| chaine  {strcpy(sauvType,$1);}
| mc_entier {strcpy(sauvType,$1);}  
| mc_char {strcpy(sauvType,$1);} 
| mc_logical  {strcpy(sauvType,$1);}
;

COND : parou CON parfer parfer;
CON :  parou E1  MC {comp=1;}  E1  
{if(strcmp(sauvLOG,".GT.")==0){quadr(".GT.",s,s2,temp1);}
if(strcmp(sauvLOG,".EQ.")==0){quadr(".EQ.",s,s2,temp1);}
if(strcmp(sauvLOG,".GE.")==0){quadr(".GE.",s,s2,temp1);}
if(strcmp(sauvLOG,".LT.")==0){quadr(".LT.",s,s2,temp1);}
if(strcmp(sauvLOG,".LE.")==0){quadr(".LE.",s,s2,temp1);}
if(strcmp(sauvLOG,".NE.")==0){quadr(".NE.",s,s2,temp1);}
comp=0;
}  parfer  CND 
;
CND : MC CON |
;
E1 : VAL | parou  VAL  OPERATION   { if((strcmp(sauvOpr,"/")==0)&&(strcmp(sauvIDF1,"0")==0)){printf("\nErreur semantique 'division par zero' a la ligne %d \n",nb_ligne);}}
VAL E2 parfer 

				
					
; 
E2 :  OPERATION  Z {
					if((strcmp(sauvOpr,"/")==0)&&(strcmp(sauvIDF1,"0")==0))
					{printf(" \nErreur semantique 'division par zero' a la ligne %d\n",nb_ligne);}
}
| 
; 
Z : parou VAL parfer E2 | VAL E2
;

MC : mc_et {AND_or_OR=1; }
| mc_ou {AND_or_OR=0;} 		
|   COMPARATOR   
; 




BOOL : mc_TRUE {insererTYPE(sauvType,sauvIDF); {strcpy(sauvType,"LOGICAL");strcpy(saveCst,"TRUE");}} 
| mc_FALSE  {insererTYPE(sauvType,sauvIDF1);{strcpy(sauvType,"LOGICAL");strcpy(saveCst,"FALSE");}}
;

%%
void yyerror(const char *s)
{
	
	printf("\n ERREUR SYNTAXIQUE DANS : %s, LIGNEline: %d, COLONNE : %d\n\n", __FILE__, nb_ligne, nb_colonne- yyleng );
}

int main()
{
	yyparse();
	afficher();
	afficher_qdr();
	return 0;
}

int yywrap()
{
	return 1;
}