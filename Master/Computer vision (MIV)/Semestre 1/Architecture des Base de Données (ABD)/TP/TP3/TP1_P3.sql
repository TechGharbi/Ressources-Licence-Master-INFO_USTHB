-- Creation de la table Agriculteur
CREATE TABLE Agriculteur (
    agriculteur_id INT PRIMARY KEY,
    nom VARCHAR(100) ,
    localisation VARCHAR(100),
    taille_exploitation INT,
    culture_principale VARCHAR(100)
);

-- Creation de la table Produit_Alimentaire
CREATE TABLE Produit_Alimentaire (
    produit_id INT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    categorie VARCHAR(50),
    valeur_nutritionnelle VARCHAR(100)
);

-- Creation de la table Marche
CREATE TABLE Marche (
    marche_id INT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    localisation VARCHAR(100),
    type_marche VARCHAR(50)
);

-- Creation de la table Production
CREATE TABLE Production (
    production_id INT PRIMARY KEY,
    agriculteur_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite_produite INT,
    saison VARCHAR(50),
    -- Cle etrangere vers Agriculteur
    FOREIGN KEY (agriculteur_id) REFERENCES Agriculteur(agriculteur_id),
    -- Cle etrangere vers Produit_Alimentaire
    FOREIGN KEY (produit_id) REFERENCES Produit_Alimentaire(produit_id)
);

-- Creation de la table Approvisionnement
CREATE TABLE Approvisionnement (
    agriculteur_id INT NOT NULL,
    produit_id INT NOT NULL,
    marche_id INT NOT NULL,
    date_approvisionnement DATE,
    quantite_fournie INT,
    PRIMARY KEY (agriculteur_id, produit_id, marche_id, date_approvisionnement),
    FOREIGN KEY (agriculteur_id) REFERENCES Agriculteur(agriculteur_id),
    FOREIGN KEY (produit_id) REFERENCES Produit_Alimentaire(produit_id),
    FOREIGN KEY (marche_id) REFERENCES Marche(marche_id)
);


-- Agriculteur
INSERT INTO Agriculteur VALUES (1, 'Benali Ahmed', 'Blida', 5, 'tomates');
INSERT INTO Agriculteur VALUES (2, 'Khelifi Samira', 'Setif', 12, 'ble dur');
INSERT INTO Agriculteur VALUES (3, 'Touati Mourad', 'Mostaganem', 8, 'pommes de terre''');
INSERT INTO Agriculteur VALUES (4, 'Zerrouki Fatma', 'Tizi Ouzou', 3, 'olives');
INSERT INTO Agriculteur VALUES (5, 'Bensaid Rachid', 'Biskra', 15, 'dattes');

-- Produit_Alimentaire
INSERT INTO Produit_Alimentaire VALUES (1, 'Ble dur', 'cereale', '340 kcal/100g');
INSERT INTO Produit_Alimentaire VALUES (2, 'Tomates', 'legume', '18 kcal/100g');
INSERT INTO Produit_Alimentaire VALUES (3, 'Pommes de terre', 'tubercule', '77 kcal/100g');
INSERT INTO Produit_Alimentaire VALUES (4, 'Olives', 'fruit', '115 kcal/100g');
INSERT INTO Produit_Alimentaire VALUES (5, 'Dattes Deglet Nour', 'fruit', '277 kcal/100g');

-- Marche
INSERT INTO Marche VALUES (1, 'Marche de gros de Boufarik', 'Blida', 'gros');
INSERT INTO Marche VALUES (2, 'Souk El Fellah', 'Alger', 'detail');
INSERT INTO Marche VALUES (3, 'Marche de gros de Setif', 'Setif', 'grosss');
INSERT INTO Marche VALUES (4, 'Marche de detail de Mostaganem', 'Mostaganem', 'detail');
INSERT INTO Marche VALUES (5, 'Marche de gros des dattes de Tolga', 'Biskra', 'gros');

-- Production
INSERT INTO Production VALUES (1, 2, 1, 30000, 'ete 2024');
INSERT INTO Production VALUES (2, 1, 2, 15000, 'printemps 2024');
INSERT INTO Production VALUES (3, 3, 3, 20000, 'hiver 2024');
INSERT INTO Production VALUES (4, 4, 4, 8000, 'automne 2024');
INSERT INTO Production VALUES (5, 5, 5, 25000, 'automne 2024');
INSERT INTO Production VALUES (5, 7, 5, 25000, 'automne 2024'); -- Correction de (5, 7, 5, 25000, 'automne 2024') car l'agriculteur 7 n'existe pas et l'ID de production 5 est dejà utilise. On prend ID=7.

-- Approvisionnement
INSERT INTO Approvisionnement VALUES (1, 2, 1, DATE '2024-05-15', 8000);
INSERT INTO Approvisionnement VALUES (2, 1, 3, DATE '2024-01-07', 10000);
INSERT INTO Approvisionnement VALUES (3, 3, 4, DATE '2024-01-20', 12000);
INSERT INTO Approvisionnement VALUES (4, 4, 2, DATE '2024-12-05', 5000);
INSERT INTO Approvisionnement VALUES (5, 5, 5, DATE '2024-03-11', 15000);
INSERT INTO Approvisionnement VALUES (6, 5, 5, DATE '2025-12-30', 15000);
