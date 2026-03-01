
flex Lex.L
bison -d syn.y -o syn.tab.c
gcc lex.yy.c syn.tab.c -o analseur.exe
chcp 65001
analseur.exe <test.txt
