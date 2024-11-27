DROP TABLE IF EXISTS Reduction;
DROP TABLE IF EXISTS Distance;
DROP TABLE IF EXISTS Collecte;
DROP TABLE IF EXISTS Benne;
DROP TABLE IF EXISTS Achete;
DROP TABLE IF EXISTS Depose;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Rang;
DROP TABLE IF EXISTS TypeVetement;
DROP TABLE IF EXISTS EntiteDate;



CREATE TABLE Rang(
   IdRang INT AUTO_INCREMENT,
   LibelleRang VARCHAR(20),
   PRIMARY KEY(IdRang)
);

CREATE TABLE TypeVetement(
   IdTypeVetement INT AUTO_INCREMENT,
   LibelleTypeVetement VARCHAR(20),
   PrixKilo DECIMAL(5,2),
   PRIMARY KEY(IdTypeVetement)
);

CREATE TABLE Benne(
   IdBenne INT AUTO_INCREMENT,
   Adresse VARCHAR(20),
   DistanceMagasinBenne INT,
   PRIMARY KEY(IdBenne)
);

CREATE TABLE Client(
   IdClient INT AUTO_INCREMENT,
   Nom VARCHAR(20),
   Prénom VARCHAR(20),
   AdresseMail VARCHAR(30),
   Téléphone VARCHAR(10),
   IdRang INT NOT NULL,
   PRIMARY KEY(IdClient),
   FOREIGN KEY(IdRang) REFERENCES Rang(IdRang)
);

CREATE TABLE Depose(
   IdClient INT,
   IdTypeVetement INT,
   JJ_MM_AAAA DATE,
   Quantite_Deposee INT,
   PRIMARY KEY(IdClient, IdTypeVetement, JJ_MM_AAAA),
   FOREIGN KEY(IdClient) REFERENCES Client(IdClient),
   FOREIGN KEY(IdTypeVetement) REFERENCES TypeVetement(IdTypeVetement)
);

CREATE TABLE Collecte(
   IdTypeVetement INT,
   IdBenne INT,
   JJ_MM_AAAA DATE,
   Quantite_Collectee INT,
   PRIMARY KEY(IdTypeVetement, IdBenne, JJ_MM_AAAA),
   FOREIGN KEY(IdTypeVetement) REFERENCES TypeVetement(IdTypeVetement),
   FOREIGN KEY(IdBenne) REFERENCES Benne(IdBenne)
);

CREATE TABLE Achete(
   IdClient INT,
   IdTypeVetement INT,
   JJ_MM_AAAA DATE,
   Quantite_Achetee INT,
   PRIMARY KEY(IdClient, IdTypeVetement, JJ_MM_AAAA),
   FOREIGN KEY(IdClient) REFERENCES Client(IdClient),
   FOREIGN KEY(IdTypeVetement) REFERENCES TypeVetement(IdTypeVetement)
);

CREATE TABLE Reduction(
   IdRang INT,
   IdTypeVetement INT,
   PourcentageReduction INT,
   PRIMARY KEY(IdRang, IdTypeVetement),
   FOREIGN KEY(IdRang) REFERENCES Rang(IdRang),
   FOREIGN KEY(IdTypeVetement) REFERENCES TypeVetement(IdTypeVetement)
);

CREATE TABLE Distance(
   IdBenne INT,
   IdBenne_1 INT,
   Distance INT,
   PRIMARY KEY(IdBenne, IdBenne_1),
   FOREIGN KEY(IdBenne) REFERENCES Benne(IdBenne),
   FOREIGN KEY(IdBenne_1) REFERENCES Benne(IdBenne)
);


INSERT INTO Rang (LibelleRang) VALUES
                                   ('Léger'),
                                   ('Lourd'),
                                   ('Méga lourd');


INSERT INTO TypeVetement (LibelleTypeVetement, PrixKilo) VALUES
                                                             ('T-shirt', 5.50),
                                                             ('Pantalon', 8.75),
                                                             ('Veste', 12.00);

INSERT INTO Benne (Adresse, DistanceMagasinBenne) VALUES
                                                      ('123 Rue Principale', 5),
                                                      ('456 Avenue du Centre', 12),
                                                      ('789 Boulevard Sud', 20);




INSERT INTO Client (Nom, Prénom, AdresseMail, Téléphone, IdRang) VALUES
                                                                     ('Dupont', 'Jean', 'jean.dupont@example.com', '0612345678', 1),
                                                                     ('Martin', 'Sophie', 'sophie.martin@example.com', '0623456789', 2),
                                                                     ('Lemoine', 'Paul', 'paul.lemoine@example.com', '0634567890', 3);


INSERT INTO Depose (IdClient, IdTypeVetement, JJ_MM_AAAA, Quantite_Deposee) VALUES
                                                                                (1, 1, '2024-11-15', 10847),
                                                                                (1, 2, '2024-11-15', 5672),
                                                                                (2, 2, '2024-11-16', 5847),
                                                                                (2, 2, '2024-12-14', 1568),
                                                                                (3, 3, '2024-11-17', 8124);


INSERT INTO Collecte (IdTypeVetement, IdBenne, JJ_MM_AAAA, Quantite_Collectee) VALUES
                                                                                   (1, 1, '2024-11-15', 20126),
                                                                                   (1, 1, '2024-11-16', 13876),
                                                                                   (2, 1, '2024-11-15', 1964),
                                                                                   (2, 1, '2024-11-17', 19819),
                                                                                   (3, 1, '2024-11-14', 2123),
                                                                                   (2, 2, '2024-11-16', 15542),
                                                                                   (3, 3, '2024-11-17', 12124);


INSERT INTO Achete (IdClient, IdTypeVetement, JJ_MM_AAAA, Quantite_Achetee) VALUES
                                                                                (2, 2, '2024-11-15', 314),
                                                                                (2, 2, '2024-11-16', 257),
                                                                                (3, 1, '2024-11-15', 224),
                                                                                (3, 2, '2024-11-20', 678),
                                                                                (3, 3, '2024-11-21', 892);


INSERT INTO Reduction (IdRang, IdTypeVetement, PourcentageReduction) VALUES
                                                                         (1, 1, 5),
                                                                         (2, 2, 10),
                                                                         (3, 3, 15);


INSERT INTO Distance (IdBenne, IdBenne_1, Distance) VALUES
                                                        (1, 2, 7154),
                                                        (1, 3, 15147),
                                                        (2, 3, 10234);


SELECT Client.Nom AS NomClient, Client.Prénom AS PrenomClient, Rang.LibelleRang AS Rang, TypeVetement.LibelleTypeVetement AS TypeVetement, SUM(Depose.Quantite_Deposee) AS TotalDeposee
FROM Depose JOIN Client ON Depose.IdClient = Client.IdClient
    JOIN Rang ON Client.IdRang = Rang.IdRang
    JOIN TypeVetement ON Depose.IdTypeVetement = TypeVetement.IdTypeVetement
GROUP BY Client.Nom, Client.Prénom, TypeVetement.LibelleTypeVetement, Rang.LibelleRang
ORDER BY NomClient, PrenomClient, TypeVetement;

SELECT Benne.Adresse AS AdresseBenne, TypeVetement.LibelleTypeVetement AS TypeVetement, SUM(Recupere.Quantite_Collectee) AS TotalCollectee
FROM Collecte JOIN Benne ON Collecte.IdBenne = Benne.IdBenne = Benne.IdBenne
    JOIN TypeVetement ON Collecte.IdTypeVetement = TypeVetement.IdTypeVetement
GROUP BY Benne.Adresse, TypeVetement.LibelleTypeVetement
ORDER BY AdresseBenne, TypeVetement;

SELECT Client.Nom AS NomClient, Client.Prénom AS PrenomClient, Rang.LibelleRang AS Rang, SUM(Achete.Quantite_Achetee) AS TotalAchetee
FROM Achete  RIGHT JOIN Client ON Achete.IdClient = Client.IdClient
            JOIN Rang ON Client.IdRang = Rang.IdRang
GROUP BY Client.Nom, Client.Prénom, Rang.LibelleRang
ORDER BY NomClient, PrenomClient;