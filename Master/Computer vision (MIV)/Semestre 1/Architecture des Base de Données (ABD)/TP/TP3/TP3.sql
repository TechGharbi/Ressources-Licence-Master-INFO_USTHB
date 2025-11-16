-- ***************************************************************
-- ÉTAPE I : PRÉPARATION DU SCHÉMA ET DES UTILISATEURS (SYSTEM/SYS)
-- ***************************************************************

-- 1. Connectez-vous en tant que SYSTEM à AGRICOLPDB.
-- (Assumons que cette connexion a été faite manuellement : CONNECT SYSTEM/motdepasse)
ALTER SESSION SET CONTAINER = AGRICOLPDB;

-- 2. Créer un tablespace agricolTBS et un tablespace temporaire agricolTempTBS.
-- ATTENTION : Remplacez le chemin du fichier (DATAFILE) par un chemin valide sur votre installation Oracle.
CREATE TABLESPACE agricolTBS
    DATAFILE 'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\AGRICOLPDB\agricolTBS.dbf' -- Chemin d'exemple à adapter
    SIZE 50M
    AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

CREATE TEMPORARY TABLESPACE agricolTempTBS
    TEMPFILE 'C:\APP\ORACLE21C\PRODUCT\21C\ORADATA\XE\AGRICOLPDB\agricolTempTBS.dbf' -- Chemin d'exemple à adapter
    SIZE 20M
    AUTOEXTEND ON;

-- 3. Créer un utilisateur DBAGRICOL et lui associer les tablespaces précédents. [cite_start]Donner lui tous les privilèges. [cite: 144]
-- Le rôle DBA donne le droit de session et la plupart des privilèges système.
CREATE USER DBAGRICOL IDENTIFIED BY dbagricol
    DEFAULT TABLESPACE agricolTBS
    TEMPORARY TABLESPACE agricolTempTBS
    QUOTA UNLIMITED ON agricolTBS;

-- 'Tous les privilèges' est interprété comme le rôle DBA (qui est très puissant).
GRANT CONNECT, RESOURCE, DBA TO DBAGRICOL;

-- ***************************************************************
-- ÉTAPE II : CRÉATION D'OBJETS ET D'UTILISATEURS (DBAGRICOL)
-- (CONNECT DBAGRICOL/dbagricol_pwd@AGRICOLPDB)
-- ***************************************************************

-- 4. Connectez-vous avec l'utilisateur DBAGRICOL@AGRICOLPDB. 
-- (Fait manuellement)
CONNECT DBAGRICOL/dbagricol@localhost:1521/AGRICOLPDB

-- a.Créer les tables du TP1 et y insérer les données (exécuter le fichier TP1.SQL). 
@ 'C:\Users\MICROSOFT PRO DZ\Documents\M1TPABD\TP1_P2'

-- b.Créez un autre utilisateur: Admin en lui donnant les mêmes tablespace que DBAGRICOL.
-- ATTENTION: Cette commande doit être exécutée par un utilisateur ayant le privilège CREATE USER,
-- généralement SYSTEM ou DBAGRICOL (qui a le rôle DBA).
CREATE USER Admin IDENTIFIED BY admin
    DEFAULT TABLESPACE agricolTBS
    TEMPORARY TABLESPACE agricolTempTBS
    QUOTA UNLIMITED ON agricolTBS;

-- c.Utiliser le dictionnaire de données pour vérifier la création des tablespaces, des utilisateurs et des tables.
-- Vérifier les tablespaces (Si connecté à SYSTEM ou DBAGRICOL/DBA)
SELECT TABLESPACE_NAME, STATUS, CONTENTS FROM DBA_TABLESPACES
WHERE TABLESPACE_NAME IN ('AGRICOLTBS', 'AGRICOLTEMPTBS');

-- Vérifier les utilisateurs (Si connecté à SYSTEM ou DBAGRICOL/DBA)
SELECT USERNAME, DEFAULT_TABLESPACE, ACCOUNT_STATUS FROM DBA_USERS
WHERE USERNAME IN ('DBAGRICOL', 'ADMIN');

-- Vérifier les tables créées par l'utilisateur courant (DBAGRICOL)
SELECT TABLE_NAME FROM USER_TABLES;

--5. Connectez-vous à l'aide de l'utilisateur Admin. Que remarquez-vous ?
-- Action : Tenter de se connecter manuellement : 
connect admin/admin @localhost:1521/AGRICOLPDB
-- Remarque : L'utilisateur Admin ne peut pas se connecter. Il reçoit l'erreur ORA-01045: user ADMIN lacks CREATE SESSION privilege; logon denied.
-- Un utilisateur nouvellement créé n'a, par défaut, aucun privilège système, même pas celui d'ouvrir une sessio

-- 6. Donnez le droit de création d'une session et reconnectez-vous.
CONNECT DBAGRICOL/dbagricol@localhost:1521/AGRICOLPDB
GRANT CREATE SESSION TO Admin;
-- Vérification : Tenter la connexion en tant qu'Admin devrait maintenant réussir.
-- 7. Donnez les privilèges suivants à Admin: créer des tables, des utilisateurs. Vérifier.
GRANT CREATE TABLE TO Admin;
GRANT CREATE USER TO Admin; 
GRANT UNLIMITED TABLESPACE TO Admin; -- Nécessaire pour que Admin puisse assigner de l'espace à d'autres utilisateurs.
-- Vérification : En tant qu'Admin :
connect admin/admin @localhost:1521/AGRICOLPDB
SELECT * FROM SESSION_PRIVS; -- Affiche les privilèges système (CREATE TABLE, CREATE USER, CREATE SESSION).

-- 8. Exécutez la requête Q1 : 
Select * from DBAGRICOL.AGRICULTEUR; --Que remarquez-vous ?
-- Remarque : La requête échoue avec l'erreur ORA-00942: table or view does not exist.
-- Même si Admin peut créer ses propres tables, il n'a pas reçu le privilège d'objet SELECT sur la table AGRICULTEUR qui appartient au schéma DBAGRICOL.

-- 9. Donnez le droit de lecture... Exécutez la requête Q1 maintenant.
CONNECT DBAGRICOL/dbagricol@localhost:1521/AGRICOLPDB
GRANT SELECT ON AGRICULTEUR TO Admin;
connect admin/admin @localhost:1521/AGRICOLPDB
-- Vérification : En tant qu'Admin, la requête réussit maintenant. 
SELECT * FROM DBAGRICOL.AGRICULTEUR;

-- 10 On veut créer une vue AGRI_PROD... Que faut-il faire ?
-- Pour permettre à Admin de créer une vue (AGRI_PROD) basée sur des tables appartenant à DBAGRICOL, il faut : 
-- Donner le privilège système de créer une vue. (Exécuté par DBAGRICOL).
CONNECT DBAGRICOL/dbagricol@localhost:1521/AGRICOLPDB
GRANT CREATE VIEW TO Admin;
-- Donner le privilège d'objet SELECT sur toutes les tables sources (AGRICULTEUR, PRODUCTION, PRODUIT_ALIMENTAIRE). (Exécuté par DBAGRICOL).
GRANT SELECT ON PRODUCTION TO Admin;
GRANT SELECT ON PRODUIT_ALIMENTAIRE TO Admin;
-- Création de la vue (Par Admin) 
-- Connecté en tant que Admin
connect admin/admin @localhost:1521/AGRICOLPDB
CREATE VIEW AGRI_PROD AS
SELECT A.nom AS Agriculteur_Nom, P.quantite_produite, PA.nom AS Produit_Nom
FROM DBAGRICOL.Agriculteur A
JOIN DBAGRICOL.Production P ON A.agriculteur_id = P.agriculteur_id
JOIN DBAGRICOL.Produit_Alimentaire PA ON P.produit_id = PA.produit_id;


-- 11. Créez un index NAMEPROD_IX... Que remarquez-vous ?
-- Connecté en tant que Admin
CREATE INDEX NAMEPROD_IX ON DBAGRICOL.PRODUIT_ALIMENTAIRE (NOM); 
-- Remarque : La commande échoue avec ORA-01031: insufficient privileges.
-- Admin n'a pas le droit de créer un index sur une table qu'il ne possède pas, même s'il a le droit de lecture.
-- Il manque le privilège d'objet INDEX.

-- 12. Donnez le droit de création d'index à Admin... réessayez. Que se passe-t-il ?
GRANT INDEX ON PRODUIT_ALIMENTAIRE TO Admin;
-- Vérification : En tant qu'Admin, l'exécution de la commande réussit maintenant.
-- Connecté en tant que Admin
CREATE INDEX NAMEPROD_IX ON DBAGRICOL.PRODUIT_ALIMENTAIRE (NOM); 
-- L'index est créé.

-- 13. Afficher tous les privilèges attribués à Admin.
-- Privilèges système accordés directement
SELECT * FROM SESSION_PRIVS;
-- Privilèges objet reçus
SELECT * FROM USER_TAB_PRIVS_RECD; 
-- Rôles accordés (sera utile pour la Q19)
SELECT * FROM USER_ROLE_PRIVS; 


-- 14. Enlevez les privilèges précédemment accordés.
-- Privilèges objet (par DBAGRICOL) 
REVOKE SELECT ON AGRICULTEUR FROM Admin;
REVOKE SELECT ON PRODUCTION FROM Admin;
REVOKE SELECT ON PRODUIT_ALIMENTAIRE FROM Admin;
REVOKE INDEX ON PRODUIT_ALIMENTAIRE FROM Admin;

-- Privilèges système (par DBAGRICOL/SYS) 
REVOKE CREATE SESSION FROM Admin;
REVOKE CREATE TABLE FROM Admin;
REVOKE CREATE USER FROM Admin;
REVOKE CREATE VIEW FROM Admin;


-- 15. Vérifiez que les privilèges ont bien été supprimés.
SELECT * FROM SESSION_PRIVS;
SELECT * FROM USER_TAB_PRIVS_RECD;
-- Normalement, les résultats sont vides ou ne contiennent que les privilèges publics/par défaut.

-- 16. Créez un profil << AGRICOL_Profil >> avec les caractéristiques spécifiées.
CREATE PROFILE AGRICOL_Profil LIMIT
    SESSIONS_PER_USER 3                         -- 3 sessions simultanés 
    CPU_PER_CALL 3500                           -- 35 secondes de CPU (3500 centièmes) 
    CONNECT_TIME 90                             -- 90 minutes de session 
    LOGICAL_READS_PER_CALL 1200                 -- 1200 blocs lus par appel 
    PRIVATE_SGA 25K                             -- 25 ko de SGA 
    IDLE_TIME 30                                -- 30 minutes d'inactivité 
    FAILED_LOGIN_ATTEMPTS 5                     -- 5 tentatives avant blocage 
    PASSWORD_LIFE_TIME 50                       -- 50 jours de validité du mot de passe 
    PASSWORD_REUSE_TIME 40                      -- 40 jours avant réutilisation 
    PASSWORD_LOCK_TIME 1                        -- 1 jour d'interdiction d'accès 
    PASSWORD_GRACE_TIME 5;                      -- Période de grâce de 5 jours 

-- 17. Affectez ce profil à l'utilisateur Admin. 
ALTER USER Admin PROFILE AGRICOL_Profil;

-- 18. Créez le rôle : <<< MARCHE_MANAGER » qui peut voir les tables AGRICULTEUR, PRODUCTION et peut modifier les lignes de la table MARCHE. [cite: 164]
CREATE ROLE MARCHE_MANAGER;
-- (À exécuter en tant que DBAGRICOL pour accorder les droits sur les objets)
GRANT SELECT ON AGRICULTEUR TO MARCHE_MANAGER;
GRANT SELECT ON PRODUCTION TO MARCHE_MANAGER;
GRANT UPDATE ON MARCHE TO MARCHE_MANAGER;


-- 19. Assignez ce rôle à Admin. [cite_start]Vérifier que les autorisations assignées au rôle MARCHE_MANAGER, ont été bien transférées à l'utilisateur à Admin. [cite: 165]
-- (À exécuter en tant que SYSTEM ou DBAGRICOL)
GRANT MARCHE_MANAGER TO Admin;

-- Vérification : (En tant que Admin)
-- 1. Vérifie que le rôle est actif :
-- SELECT * FROM USER_ROLE_PRIVS WHERE GRANTED_ROLE = 'MARCHE_MANAGER';
-- 2. Test de lecture (doit réussir) :
-- SELECT * FROM DBAGRICOL.AGRICULTEUR;
-- 3. Test de modification (doit réussir) :
-- UPDATE DBAGRICOL.MARCHÉ SET localisation = 'Centre' WHERE marche_id = 1;
-- 4. Test d'une action non permise (doit échouer) :
-- INSERT INTO DBAGRICOL.AGRICULTEUR VALUES (99, 'Test', 'Lieu', 1, 'Rien'); -- ORA-01031: privileges insuffisants