SET SERVEROUTPUT ON;
--------------------------------------------------------------------------------
-- 1. Bloc PL/SQL : infos sur Benali Ahmed
--------------------------------------------------------------------------------
DECLARE
    v_taille NUMBER;
    v_culture VARCHAR2(100);
    v_nom VARCHAR2(100) := 'Benali Ahmed';
BEGIN
    SELECT taille_exploitation, culture_principale
    INTO v_taille, v_culture
    FROM Agriculteur
    WHERE nom = v_nom;

    IF v_taille > 10 THEN
        dbms_output.put_line(v_nom || ' a une Grande exploitation (' || v_taille || ' hectares) de ' || v_culture);
    ELSE
        dbms_output.put_line(v_nom || ' a une Petite exploitation (' || v_taille || ' hectares) de ' || v_culture);
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
         dbms_output.put_line('Aucun agriculteur trouvé avec ce nom.');
END;
/
--------------------------------------------------------------------------------
-- 2. Bloc PL/SQL pour tous les agriculteurs avec curseur
--------------------------------------------------------------------------------
DECLARE
    CURSOR cr IS 
        SELECT nom, taille_exploitation, culture_principale
        FROM Agriculteur;
BEGIN
    FOR item IN cr LOOP
        IF item.taille_exploitation > 10 THEN
            dbms_output.put_line(item.nom || ' : Grande exploitation (' ||
                                  item.taille_exploitation || ' hectares) de ' ||
                                  item.culture_principale);
        ELSE
            dbms_output.put_line(item.nom || ' : Petite exploitation (' ||
                                  item.taille_exploitation || ' hectares) de ' ||
                                  item.culture_principale);
        END IF;
    END LOOP;
END;
/
--------------------------------------------------------------------------------
-- 3. Bloc PL/SQL : insertion, mise à jour et suppression
--------------------------------------------------------------------------------
BEGIN
    -- a. Insérer une nouvelle production
    INSERT INTO Production(production_id, agriculteur_id, produit_id, quantite_produite, saison)
    VALUES (6, 4, 3, 10000, 'hiver 2024');

    -- b. Mise à jour production_id = 3
    UPDATE Production
    SET quantite_produite = 15000
    WHERE production_id = 3;

    -- c. Suppression Approvisionnement avant 01-03-2024
    DELETE FROM Approvisionnement
    WHERE date_approvisionnement < TO_DATE('01-03-2024','DD-MM-YYYY');

    COMMIT;
END;
/
--------------------------------------------------------------------------------
-- 4.a Fonction total_production_agriculteur
--------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION total_production_agriculteur(id_agri NUMBER)
RETURN NUMBER
IS
    total NUMBER;
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM Agriculteur
    WHERE agriculteur_id = id_agri;

    IF v_count = 0 THEN
        raise_application_error(-20001, 'Agriculteur inexistant');
    END IF;

    SELECT NVL(SUM(quantite_produite),0)
    INTO total
    FROM Production
    WHERE agriculteur_id = id_agri;

    RETURN total;

END;
/
--------------------------------------------------------------------------------
-- 4.b Executer la fonction pour tous les agriculteurs
--------------------------------------------------------------------------------
DECLARE
    CURSOR cr IS SELECT agriculteur_id, nom FROM Agriculteur;
    total NUMBER;
BEGIN
    FOR i IN cr LOOP
        total := total_production_agriculteur(i.agriculteur_id);
        dbms_output.put_line('Total production de ' || i.nom || ' = ' || total);
    END LOOP;
END;
/
--------------------------------------------------------------------------------
-- 5. Procedure d'insertion securisee pour Production
--------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE inserer_production(
    p_production_id NUMBER,
    p_agriculteur_id NUMBER,
    p_produit_id NUMBER,
    p_quantite NUMBER,
    p_saison VARCHAR2
) IS
    v_count NUMBER;
BEGIN
    -- Verifier unicite cle 
    SELECT COUNT(*) INTO v_count
    FROM Production
    WHERE production_id = p_production_id;

    IF v_count > 0 THEN
        raise_application_error(-20002, 'Erreur : production_id deja utilise.');
    END IF;

    -- Verifier cle etrangere agriculteur
    SELECT COUNT(*) INTO v_count
    FROM Agriculteur
    WHERE agriculteur_id = p_agriculteur_id;

    IF v_count = 0 THEN
        raise_application_error(-20003, 'Erreur : agriculteur_id inexistant.');
    END IF;

    -- Vérifier cle etrangere produit
    SELECT COUNT(*) INTO v_count
    FROM Produit_Alimentaire
    WHERE produit_id = p_produit_id;

    IF v_count = 0 THEN
        raise_application_error(-20004, 'Erreur : produit_id inexistant.');
    END IF;

    -- Insertion finale
    INSERT INTO Production VALUES(
        p_production_id,
        p_agriculteur_id,
        p_produit_id,
        p_quantite,
        p_saison
    );

    dbms_output.put_line('Insertion reussie.');

EXCEPTION
    WHEN OTHERS THEN
        dbms_output.put_line('Erreur : ' || SQLERRM);
END;
/
--------------------------------------------------------------------------------
-- Exemple d’exécution :
-- EXEC inserer_production(10, 1, 2, 5000, 'printemps 2025');
--------------------------------------------------------------------------------
