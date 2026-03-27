flex lexical.l
bison -d syntaxique.y -o syntaxique.tab.c
gcc lex.yy.c syntaxique.tab.c ts.c pgm.c -o ts.exe
ts.exe <ex.txt