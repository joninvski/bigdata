import sqlite3


# Create database for Bayesian network (page 16 of the slides)

def create_database():
    db = sqlite3.connect(':memory:')
    return db







def insert_values(db):
    c = db.cursor()

    # --------------
    # |    Asia    |
    # --------------
    # | Y   | 0.01 |
    # | N   | 0.99 |
    # --------------
    c.execute('CREATE TABLE Asia (A text, P float)')
    c.execute('INSERT INTO Asia VALUES ("Y", 0.01)')
    c.execute('INSERT INTO Asia VALUES ("N", 0.99)')
    db.commit()

    # ------------------------------
    # | Tuberculosis | Asia | %    |
    # | Y            | Y    | 0.05 |
    # | Y            | N    | 0.01 |
    # | N            | Y    | 0.95 |
    # | N            | N    | 0.99 |
    # ------------------------------
    c.execute('CREATE TABLE Tuberculosis (T text, A text, P float)')
    c.execute('INSERT INTO Tuberculosis VALUES ("Y", "Y", 0.05)')
    c.execute('INSERT INTO Tuberculosis VALUES ("N", "Y", 0.01)')
    c.execute('INSERT INTO Tuberculosis VALUES ("Y", "N", 0.95)')
    c.execute('INSERT INTO Tuberculosis VALUES ("N", "N", 0.99)')
    db.commit()

    # ------------------
    # | Smoking | %    |
    # | Y       | 0.50 |
    # | N       | 0.50 |
    # ------------------
    c.execute('CREATE TABLE Smoking(S text, P float)')
    c.execute('INSERT INTO Smoking VALUES ("Y", 0.50)')
    c.execute('INSERT INTO Smoking VALUES ("N", 0.50)')
    db.commit()

    # -------------------------------
    # | Lungcancer | Smoking | %    |
    # | Y          | Y       | 0.10 |
    # | Y          | N       | 0.01 |
    # | N          | Y       | 0.90 |
    # | N          | N       | 0.10 |
    # -------------------------------
    c.execute('CREATE TABLE Lungcancer(L text, S text, P float)')
    c.execute('INSERT INTO Lungcancer VALUES ("Y", "Y", 0.10)')
    c.execute('INSERT INTO Lungcancer VALUES ("N", "Y", 0.01)')
    c.execute('INSERT INTO Lungcancer VALUES ("Y", "N", 0.90)')
    c.execute('INSERT INTO Lungcancer VALUES ("N", "N", 0.10)')
    db.commit()

    # -------------------------------
    # | Bronchitis | Smoking | %    |
    # | Y          | Y       | 0.60 |
    # | Y          | N       | 0.30 |
    # | N          | Y       | 0.40 |
    # | N          | N       | 0.70 |
    # -------------------------------
    c.execute('CREATE TABLE Bronchitis(B text, S text, P float)')
    c.execute('INSERT INTO Bronchitis VALUES ("Y", "Y", 0.60)')
    c.execute('INSERT INTO Bronchitis VALUES ("N", "Y", 0.30)')
    c.execute('INSERT INTO Bronchitis VALUES ("Y", "N", 0.40)')
    c.execute('INSERT INTO Bronchitis VALUES ("N", "N", 0.70)')
    db.commit()

    # ---------------------------------------------------------
    # | EitherTubOrLungCancer | LungCancer | Tuberculosis | % |
    # | Y                     | Y          | Y            | 1 |
    # | Y                     | Y          | N            | 1 |
    # | Y                     | N          | Y            | 1 |
    # | Y                     | N          | N            | 0 |
    # | N                     | Y          | Y            | 0 |
    # | N                     | Y          | N            | 0 |
    # | N                     | N          | Y            | 0 |
    # | N                     | N          | N            | 1 |
    # ---------------------------------------------------------
    c.execute('CREATE TABLE EitherTubOrLungCancer(E text, T text, L text, P float)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("Y", "Y", "Y", 1)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("Y", "Y", "N", 1)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("Y", "N", "Y", 1)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("Y", "N", "N", 0)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("N", "Y", "Y", 0)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("N", "Y", "N", 0)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("N", "N", "Y", 0)')
    c.execute('INSERT INTO EitherTubOrLungCancer VALUES ("N", "N", "N", 1)')

    # ---------------------------------------
    # | Xray | EitherTubOrLungCancer | %    |
    # | Y    | Y                     | 0.98 |
    # | Y    | N                     | 0.05 |
    # | N    | Y                     | 0.02 |
    # | N    | N                     | 0.95 |
    # ---------------------------------------
    c.execute('CREATE TABLE Xray (X text, E text, P float)')
    c.execute('INSERT INTO Xray VALUES ("Y", "Y", 0.98)')
    c.execute('INSERT INTO Xray VALUES ("Y", "N", 0.05)')
    c.execute('INSERT INTO Xray VALUES ("N", "Y", 0.02)')
    c.execute('INSERT INTO Xray VALUES ("N", "N", 0.95)')

    # --------------------------------------------------------
    # | Dyspnoea | EitherTubOrLungCancer | Bronchitis | %    |
    # | Y        | Y                     | Y          | 0.90 |
    # | Y        | Y                     | N          | 0.70 |
    # | Y        | N                     | Y          | 0.80 |
    # | Y        | N                     | N          | 0.10 |
    # | N        | Y                     | Y          | 0.10 |
    # | N        | Y                     | N          | 0.30 |
    # | N        | N                     | Y          | 0.20 |
    # | N        | N                     | N          | 0.90 |
    # --------------------------------------------------------
    c.execute('CREATE TABLE Dyspnoea (D text, E text, B text, P float)')
    c.execute('INSERT INTO Dyspnoea VALUES ("Y", "Y", "Y", 0.90)')
    c.execute('INSERT INTO Dyspnoea VALUES ("Y", "Y", "N", 0.70)')
    c.execute('INSERT INTO Dyspnoea VALUES ("Y", "N", "Y", 0.80)')
    c.execute('INSERT INTO Dyspnoea VALUES ("Y", "N", "N", 0.10)')
    c.execute('INSERT INTO Dyspnoea VALUES ("N", "Y", "Y", 0.10)')
    c.execute('INSERT INTO Dyspnoea VALUES ("N", "Y", "N", 0.30)')
    c.execute('INSERT INTO Dyspnoea VALUES ("N", "N", "Y", 0.20)')
    c.execute('INSERT INTO Dyspnoea VALUES ("N", "N", "N", 0.90)')


def ask_question(db):
    c = db.cursor()
    # SQL query
    c.execute('SELECT rain.R, SUM(rain.P * wet.P) \
               FROM rain, wet \
               WHERE wet.W="Y" AND rain.R=wet.R \
               GROUP BY rain.R')
    result = c.fetchall()
    return result

def test_question(db):
    # patient who did not go to Asia, did not smoke, did not have a positive X-ray and did not have dyspnoea
    # tuberculosis
    # yes: 0.00007470 no: 0.99992530
    # lung cancer
    # yes: 0.00007470 no: 0.99992530
    # bronchitis
    # yes: 0.08696218 no: 0.91303782
    c = db.cursor()
    c.execute('SELECT Tuberculosis.T, SUM(Tuberculosis.P * Asia.P) \
               FROM Tuberculosis, Asia\
               WHERE Asia.A="N" AND Tuberculosis.A=Asia.A \
               GROUP BY Tuberculosis.T')
    result = c.fetchall()
    return result


db = create_database()
insert_values(db)
result = test_question(db)
# result = ask_question(db)

print result
print ""

n = result[0][1]
y = result[1][1]

print "Ponderated result (Y) = " + str(y / (y + n))
print "Ponderated result (N) = " + str(n / (y + n))
