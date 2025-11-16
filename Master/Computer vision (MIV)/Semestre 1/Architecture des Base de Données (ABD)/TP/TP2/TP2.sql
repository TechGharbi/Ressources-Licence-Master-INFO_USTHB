-- 1. Configurations générale
-- a. Quel est le nom de l'instance Oracle, sa version et l'état de la base (v$instance)?
SELECT INSTANCE_NAME, VERSION, STATUS FROM V$INSTANCE;

-- b. Quel est le nom de la base et son mode d'ouverture (v$database)?
SELECT NAME, OPEN_MODE FROM V$DATABASE;

-- c. Localiser le fichier de paramètres d'initialisation: init.ora.xxxxx. Examiner le contenu de ce fichier. 
-- Voir aussi v$parameter ou exécuter show parameter;
-- Le fichier de paramètres d'initialisation (généralement un SPFILE) est souvent stocké dans un répertoire spécifique à l'instance.
-- La localisation exacte varie, mais la vue V$PARAMETER permet d'afficher les valeurs des paramètres d'initialisation en cours d'utilisation.
-- Afficher le chemin du fichier SPFILE (si utilisé)
SHOW PARAMETER SPFILE;
-- Afficher tous les paramètres d'initialisation
SHOW PARAMETER;

-- OU, en utilisant la vue du dictionnaire
SELECT NAME, VALUE, DESCRIPTION
FROM V$PARAMETER
ORDER BY NAME;

-- 2. Mémoire
-- a. Déterminer la taille de la SGA
-- taille globale (voir v$sga)
SELECT SUM(VALUE) / (1024 * 1024) AS SGA_TOTAL_MB FROM V$SGA;

-- taille détaillée (voir v$sgastat)
SELECT POOL, NAME, BYTES / (1024 * 1024) AS SIZE_MB FROM V$SGASTAT ORDER BY POOL, NAME;

-- b. Quelle est la taille du cache de données ?
-- La taille du cache de données (Buffer Cache) fait partie de la SGA.
SELECT NAME, VALUE/1024/1024 AS SIZE_MB
FROM V$SGA
WHERE NAME = 'Database Buffers';

-- 3. Processus
-- a. Afficher les processus utilisateur en cours d'exécution (v$session).
-- Les sessions utilisateur sont généralement celles qui ne sont pas des processus d'arrière-plan (background processes).
SELECT SID, SERIAL#, USERNAME, PROGRAM, STATUS
FROM V$SESSION WHERE TYPE = 'USER' AND USERNAME IS NOT NULL;

-- b. Afficher les processus système (Background) en cours d'exécution (v$session).
-- Les processus système ont généralement le type BACKGROUND.
SELECT SID, PROGRAM, STATUS FROM V$SESSION WHERE TYPE = 'BACKGROUND' ORDER BY SID;

-- 4. Fichiers
-- a. Quels sont les noms et les emplacements des fichiers de contrôle de la base (v$controlfile) ?
SELECT NAME, STATUS FROM V$CONTROLFILE;

-- b. Quels sont les noms et les emplacements des fichiers journaux (v$logfile)?
SELECT MEMBER, GROUP#, STATUS FROM V$LOGFILE;

-- c. Quels sont les noms des fichiers de données et la taille de leurs blocs (v$datafile)?
SELECT NAME, BLOCK_SIZE FROM V$DATAFILE;

-- 5. Pluggable database
-- Ces étapes sont des commandes administratives qui doivent être exécutées 
-- dans la base de données conteneur(CDB, après s'être connecté en tant que SYS ou SYSTEM).
-- a. Créer une base de données pluggable nommée AGRICOLPDB

 CREATE PLUGGABLE DATABASE AGRICOLPDB
        ADMIN USER agricol_adm IDENTIFIED BY agricol
        FILE_NAME_CONVERT = (
            'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\PDBSEED\',  -- Chemin source des fichiers SEED
            'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\AGRICOLPDB\' -- Chemin destination de la PDB
        );
--(Note: Le chemin exact dans FILE_NAME_CONVERT doit être ajusté pour correspondre à votre installation Oracle, souvent sous $ORACLE_BASE/oradata/CDB_NAME/).

-- b. Ouvrir la base de données.
connect sys as sysdba;

ALTER PLUGGABLE DATABASE AGRICOLPDB OPEN;

-- c. Connecter-vous à AGRICOLPDB en tant que SYSTEM.
CONNECT SYSTEM/mot_pass;

ALTER SESSION SET CONTAINER = AGRICOLPDB;

-- 6. Structure logique
-- Ces commandes doivent être exécutées dans la PDB AGRICOLPDB (après l'étape 5.c).

-- a. Quels sont les noms des tablespaces (dba_tablespaces) ?
SELECT TABLESPACE_NAME, STATUS, CONTENTS FROM DBA_TABLESPACES;

-- b. Dans quel tablespace est localisé chaque fichier de données (dba_data_files) ?
SELECT FILE_NAME, TABLESPACE_NAME FROM DBA_DATA_FILES ORDER BY TABLESPACE_NAME;

-- c. Créer un tablespace ayant un seul fichier de 2M auto extensible. Localiser le fichier dans le répertoire AGRICOLPDB. Vérifier.
CREATE TABLESPACE MonTablespace2M
DATAFILE 'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\AGRICOLPDB\MonTablespace2M_01.dbf'
SIZE 2M
AUTOEXTEND ON NEXT 1M MAXSIZE UNLIMITED;

-- Vérification :
SELECT TABLESPACE_NAME, FILE_NAME, BYTES / (1024 * 1024) AS SIZE_MB
FROM DBA_DATA_FILES
WHERE TABLESPACE_NAME = 'MONTABLESPACE2M';

-- d. Créer un tablespace temporaire ayant un seul fichier de 2M. Localiser le fichier dans le répertoire AGRICOLPDB. Vérifier.
CREATE TEMPORARY TABLESPACE MonTablespaceTemp2M
TEMPFILE 'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\AGRICOLPDB\MonTablespaceTemp2M_01.dbf'
SIZE 2M;

-- Vérification :
SELECT TABLESPACE_NAME, FILE_NAME, BYTES / (1024 * 1024) AS SIZE_MB
FROM DBA_TEMP_FILES
WHERE TABLESPACE_NAME = 'MONTABLESPACETEMP2M';

-- e. Créer un utilisateur et lui associer les deux tablespaces.
-- DEFAULT TABLESPACE pour le stockage permanent.
-- TEMPORARY TABLESPACE pour les opérations de tri.
CREATE USER feriel IDENTIFIED BY feriel11
DEFAULT TABLESPACE MonTablespace2M
TEMPORARY TABLESPACE MonTablespaceTemp2M
QUOTA UNLIMITED ON MonTablespace2M;

-- f. Supprimer les tablespaces crées dans les questions précédentes. Vérifier le résultat.
-- La suppression doit être faite avec l'option INCLUDING CONTENTS AND DATAFILES pour supprimer les données et les fichiers physiques.
-- Suppression du tablespace permanent
DROP TABLESPACE MonTablespace2M INCLUDING CONTENTS AND DATAFILES;

-- Suppression du tablespace temporaire
DROP TABLESPACE MonTablespaceTemp2M INCLUDING CONTENTS AND DATAFILES;

-- Vérification :
SELECT TABLESPACE_NAME
FROM DBA_TABLESPACES
WHERE TABLESPACE_NAME IN ('MONTABLESPACE2M', 'MONTABLESPACETEMP2M');
