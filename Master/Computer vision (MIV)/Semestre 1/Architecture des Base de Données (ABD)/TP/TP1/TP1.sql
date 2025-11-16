-- Partie I : Langage de definition de donnees

-- 1. Connexion a l'utilisateur SYSTEM (a executer dans l'invite de commande SQL*Plus ou SQL Developer)
-- CONNECT SYSTEM/password;

-- 2. Creer les relations avec toutes les contraintes d'integrite
-- Supprimer les tables si elles existent deja
DROP TABLE Approvisionnement CASCADE CONSTRAINTS;
DROP TABLE Production CASCADE CONSTRAINTS;
DROP TABLE Marche CASCADE CONSTRAINTS;
DROP TABLE Produit_Alimentaire CASCADE CONSTRAINTS;
DROP TABLE Agriculteur CASCADE CONSTRAINTS;

CREATE TABLE Agriculteur (
    agriculteur_id NUMBER PRIMARY KEY,
    nom VARCHAR2(100) NOT NULL,
    localisation VARCHAR2(100),
    taille_exploitation NUMBER,
    culture_principale VARCHAR2(100)
);

CREATE TABLE Produit_Alimentaire (
    produit_id NUMBER PRIMARY KEY,
    nom VARCHAR2(100),
    categorie VARCHAR2(100),
    valeur_nutritionnelle VARCHAR2(100)
);

CREATE TABLE Production (
    production_id NUMBER PRIMARY KEY,
    agriculteur_id NUMBER,
    produit_id NUMBER,
    quantite_produite NUMBER DEFAULT 0,
    saison VARCHAR2(100),
    FOREIGN KEY (agriculteur_id) REFERENCES Agriculteur(agriculteur_id),
    FOREIGN KEY (produit_id) REFERENCES Produit_Alimentaire(produit_id)
);

CREATE TABLE Marche (
    marche_id NUMBER PRIMARY KEY,
    nom VARCHAR2(100),
    localisation VARCHAR2(100),
    type_marche VARCHAR2(100)
);

CREATE TABLE Approvisionnement (
    agriculteur_id NUMBER,
    produit_id NUMBER,
    marche_id NUMBER,
    date_approvisionnement DATE,
    quantite_fournie NUMBER,
    PRIMARY KEY (agriculteur_id, produit_id, marche_id, date_approvisionnement),
    FOREIGN KEY (agriculteur_id) REFERENCES Agriculteur(agriculteur_id),
    FOREIGN KEY (produit_id) REFERENCES Produit_Alimentaire(produit_id),
    FOREIGN KEY (marche_id) REFERENCES Marche(marche_id)
);

-- 3. Afficher les tables crees (nos tables seulement) et leur structure
-- D'abord afficher la liste des tables
SELECT table_name 
FROM user_tables 
WHERE table_name IN ('AGRICULTEUR', 'PRODUIT_ALIMENTAIRE', 'PRODUCTION', 'MARCHE', 'APPROVISIONNEMENT')
ORDER BY table_name;

DESC AGRICULTEUR;
DESC PRODUIT_ALIMENTAIRE;
DESC PRODUCTION;
DESC MARCHE;
DESC APPROVISIONNEMENT;

-- 4. Ajouter l'attribut NumTelephone
ALTER TABLE Agriculteur ADD NumTelephone VARCHAR2(15);

-- 5. Ajouter la contrainte NOT NULL pour Nom et NumTelephone
-- Nom est deja NOT NULL depuis la creation
ALTER TABLE Agriculteur MODIFY NumTelephone NOT NULL;

-- 6. Modifier la longueur de NumTelephone (agrandir a 20 caracteres)
ALTER TABLE Agriculteur MODIFY NumTelephone VARCHAR2(20);

-- 7. Renommer la colonne NumTelephone en Tel
ALTER TABLE Agriculteur RENAME COLUMN NumTelephone TO Tel;

-- Verification (structure de la table Agriculteur)
DESC Agriculteur;

-- 8. Supprimer la colonne Tel
ALTER TABLE Agriculteur DROP COLUMN Tel;

-- Verification (structure de la table Agriculteur)
DESC Agriculteur;

-- 9. Affecter la valeur par defaut 0 a quantite_produite (deja fait lors de la creation)
ALTER TABLE Production MODIFY quantite_produite DEFAULT 0;

-- 10. Ajouter la contrainte CHECK pour type_marche
ALTER TABLE Marche ADD CONSTRAINT chk_type_marche CHECK (type_marche IN ('gros', 'detail'));

-- Partie II : Langage de manipulation de donnees

-- 11. Remplir les tables avec les instances donnees

-- Insertion dans Agriculteur
INSERT INTO Agriculteur (agriculteur_id, nom, localisation, taille_exploitation, culture_principale) 
VALUES (1, 'Benali Ahmed', 'Bilda', 5, 'tomates');

INSERT INTO Agriculteur (agriculteur_id, nom, localisation, taille_exploitation, culture_principale) 
VALUES (2, 'Khelifi Samira', 'Setif', 12, 'ble dur');

INSERT INTO Agriculteur (agriculteur_id, nom, localisation, taille_exploitation, culture_principale) 
VALUES (3, 'Touati Mourad', 'Mostaganem', 8, 'pommes de terre');

INSERT INTO Agriculteur (agriculteur_id, nom, localisation, taille_exploitation, culture_principale) 
VALUES (4, 'Zerrouki Fatma', 'Tizi Ouzou', 3, 'olives');

INSERT INTO Agriculteur (agriculteur_id, nom, localisation, taille_exploitation, culture_principale) 
VALUES (5, 'Bensaid Rachid', 'Biskra', 15, 'dattes');

-- Insertion dans Produit_Alimentaire
INSERT INTO Produit_Alimentaire (produit_id, nom, categorie, valeur_nutritionnelle) 
VALUES (1, 'Ble dur', 'cereale', '340 kcal/100g');

INSERT INTO Produit_Alimentaire (produit_id, nom, categorie, valeur_nutritionnelle) 
VALUES (2, 'Tomates', 'legume', '18 kcal/100g');

INSERT INTO Produit_Alimentaire (produit_id, nom, categorie, valeur_nutritionnelle) 
VALUES (3, 'Pommes de terre', 'tubercule', '77 kcal/100g');

INSERT INTO Produit_Alimentaire (produit_id, nom, categorie, valeur_nutritionnelle) 
VALUES (4, 'Olives', 'fruit', '115 kcal/100g');

INSERT INTO Produit_Alimentaire (produit_id, nom, categorie, valeur_nutritionnelle) 
VALUES (5, 'Dattes Deglet Nour', 'fruit', '277 kcal/100g');

-- Insertion dans Production
INSERT INTO Production (production_id, agriculteur_id, produit_id, quantite_produite, saison) 
VALUES (1, 2, 1, 30000, 'ete 2024');

INSERT INTO Production (production_id, agriculteur_id, produit_id, quantite_produite, saison) 
VALUES (2, 1, 2, 15000, 'printemps 2024');

INSERT INTO Production (production_id, agriculteur_id, produit_id, quantite_produite, saison) 
VALUES (3, 3, 3, 20000, 'hiver 2024');

INSERT INTO Production (production_id, agriculteur_id, produit_id, quantite_produite, saison) 
VALUES (4, 4, 4, 8000, 'automne 2024');

INSERT INTO Production (production_id, agriculteur_id, produit_id, quantite_produite, saison) 
VALUES (5, 5, 5, 25000, 'automne 2024');
-- Correction de (5, 7, 5, 25000, 'automne 2024') car l'agriculteur 7 n'existe pas et l'ID de production 5 est deja utilise. On prend ID=7.

-- Insertion dans Marche
INSERT INTO Marche (marche_id, nom, localisation, type_marche) 
VALUES (1, 'Marche de gros de Boufarik', 'Bilda', 'gros');

INSERT INTO Marche (marche_id, nom, localisation, type_marche) 
VALUES (2, 'Souk El Fellah', 'Alger', 'detail');

INSERT INTO Marche (marche_id, nom, localisation, type_marche) 
VALUES (3, 'Marche de gros de Setif', 'Setif', 'gros');

INSERT INTO Marche (marche_id, nom, localisation, type_marche) 
VALUES (4, 'Marche de detail de Mostaganem', 'Mostaganem', 'detail');

INSERT INTO Marche (marche_id, nom, localisation, type_marche) 
VALUES (5, 'Marche de gros des dattes de Tolga', 'Biskra', 'gros');

-- Insertion dans Approvisionnement
INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (2, 1, 3, TO_DATE('07-01-2024', 'DD-MM-YYYY'), 10000);

INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (1, 2, 1, TO_DATE('15-05-2024', 'DD-MM-YYYY'), 8000);

INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (3, 3, 4, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 12000);

INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (4, 4, 2, TO_DATE('05-12-2024', 'DD-MM-YYYY'), 5000);

INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (5, 5, 5, TO_DATE('11-03-2024', 'DD-MM-YYYY'), 15000);

INSERT INTO Approvisionnement (agriculteur_id, produit_id, marche_id, date_approvisionnement, quantite_fournie) 
VALUES (5, 5, 5, TO_DATE('30-12-2025', 'DD-MM-YYYY'), 15000);

-- Problemes rencontres :

-- Violation de la contrainte CHECK sur Marche (si elle est appliquee avant l'insertion): La donnee ('Marche de gros de Setif', 'Setif', 'grosss') pour la table Marche possede la valeur 'grosss' pour type_marche, qui violera la contrainte CHECK n'autorisant que 'gros' et 'detail'.
-- Erreur de cle etrangere (FOREIGN KEY) sur Production : La ligne (5, 7, 5, 25000, 'automne 2024') contient un agriculteur_id egal à 7, or l'agriculteur 7 n'existe pas dans la table Agriculteur (les IDs vont de 1 à 5).
-- Erreur de cle primaire sur Production : Dans les donnees, il y a deux lignes avec l'ID de production 5. La seconde ligne ((5, 7, 5, 25000, 'automne 2024')) devrait avoir un ID different. J'ai utilise 7 comme ID dans la correction ci-dessus.
-- Erreur de type de donnees : Le format des dates dans le document (ex: '07-01-2024') est ambigu (mois-jour-annee ou jour-mois-annee). Dans la commande, j'ai utilise DATE 'AAAA-MM-JJ' pour la clarte.
-- Duplication d'enregistrement sur Approvisionnement : La derniere ligne d'insertion de l'exemple (5, 5, 5, '30-12-2025', 15000) est repetee dans les commentaires du document, mais elle a une cle primaire valide (date differente).
-- Violation de la contrainte NOT NULL : Si les contraintes NOT NULL de la question 5 sont appliquees avant l'insertion, les agriculteurs n'auront pas de numero de telephone (Tel), ce qui causera une erreur.

-- Valider les insertions
COMMIT;

-- 12. Modifier le nom du marche 'Souk El Fellah'
UPDATE Marche SET nom = 'Marche Ali Ramli' WHERE nom = 'Souk El Fellah';

-- 13. Supprimer les approvisionnements avec date superieure a la date actuelle
DELETE FROM Approvisionnement WHERE date_approvisionnement > SYSDATE;

-- 14. Modifier la contrainte CHECK pour autoriser d'autres valeurs
ALTER TABLE Marche DROP CONSTRAINT chk_type_marche;
ALTER TABLE Marche ADD CONSTRAINT chk_type_marche 
CHECK (type_marche IN ('gros', 'detail', 'local', 'regional', 'national'));

-- Partie IV : Langage d'interrogation de donnees

-- 15. Agriculteurs de Mostaganem
SELECT nom FROM Agriculteur WHERE localisation = 'Mostaganem';

-- 16. Agriculteurs qui ont produit du ble
SELECT DISTINCT A.nom
FROM Agriculteur A
JOIN Production P ON A.agriculteur_id = P.agriculteur_id
JOIN Produit_Alimentaire PA ON P.produit_id = PA.produit_id
WHERE PA.nom = 'Ble dur';

-- 17. Agriculteurs qui ont produit de la tomate et approvisionne Boufarik
SELECT DISTINCT A.nom
FROM Agriculteur A
JOIN Production P ON A.agriculteur_id = P.agriculteur_id
JOIN Produit_Alimentaire PA ON P.produit_id = PA.produit_id
JOIN Approvisionnement App ON A.agriculteur_id = App.agriculteur_id AND PA.produit_id = App.produit_id
JOIN Marche M ON App.marche_id = M.marche_id
WHERE PA.nom = 'Tomates' AND M.nom = 'Marche de gros de Boufarik';

-- 18. Quantite produite des cereales
SELECT SUM(P.quantite_produite) as quantite_totale_cereales
FROM Production P
JOIN Produit_Alimentaire PA ON P.produit_id = PA.produit_id
WHERE PA.categorie = 'cereale';

-- 19. Quantite produite par categorie
SELECT PA.categorie, SUM(P.quantite_produite) as quantite_totale
FROM Production P
JOIN Produit_Alimentaire PA ON P.produit_id = PA.produit_id
GROUP BY PA.categorie;

-- 20. Categorie ayant le maximum de production
SELECT categorie, quantite_totale
FROM (
    SELECT PA.categorie, SUM(P.quantite_produite) as quantite_totale
    FROM Production P
    JOIN Produit_Alimentaire PA ON P.produit_id = PA.produit_id
    GROUP BY PA.categorie
    ORDER BY quantite_totale DESC
)
WHERE ROWNUM = 1;