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
    c.execute('INSERT INTO Tuberculosis VALUES ("Y", "N", 0.01)')
    c.execute('INSERT INTO Tuberculosis VALUES ("N", "Y", 0.95)')
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
    c.execute('INSERT INTO Lungcancer VALUES ("Y", "N", 0.01)')
    c.execute('INSERT INTO Lungcancer VALUES ("N", "Y", 0.90)')
    c.execute('INSERT INTO Lungcancer VALUES ("N", "N", 0.99)')
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
    c.execute('INSERT INTO Bronchitis VALUES ("Y", "N", 0.30)')
    c.execute('INSERT INTO Bronchitis VALUES ("N", "Y", 0.40)')
    c.execute('INSERT INTO Bronchitis VALUES ("N", "N", 0.70)')
    db.commit()

    # ---------------------------------------------------------
    # | EitherTubOrLungcancer | Lungcancer | Tuberculosis | % |
    # | Y                     | Y          | Y            | 1 |
    # | Y                     | Y          | N            | 1 |
    # | Y                     | N          | Y            | 1 |
    # | Y                     | N          | N            | 0 |
    # | N                     | Y          | Y            | 0 |
    # | N                     | Y          | N            | 0 |
    # | N                     | N          | Y            | 0 |
    # | N                     | N          | N            | 1 |
    # ---------------------------------------------------------
    c.execute('CREATE TABLE EitherTubOrLungcancer(E text, T text, L text, P float)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("Y", "Y", "Y", 1)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("Y", "Y", "N", 1)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("Y", "N", "Y", 1)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("Y", "N", "N", 0)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("N", "Y", "Y", 0)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("N", "Y", "N", 0)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("N", "N", "Y", 0)')
    c.execute('INSERT INTO EitherTubOrLungcancer VALUES ("N", "N", "N", 1)')

    # ---------------------------------------
    # | Xray | EitherTubOrLungcancer | %    |
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
    # | Dyspnoea | EitherTubOrLungcancer | Bronchitis | %    |
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


def test_question_tuberculosis(db):
    # patient who did not go to Asia, did not smoke, did not have a positive X-ray and did not have Dyspnoea
    # tuberculosis
    # yes: 0.00007470 no: 0.99992530
    cr = db.cursor()

            # SELECT Tuberculosis.T HasT, Tuberculosis.P TuberP, Asia.P AsiaP, EitherTubOrLungcancer.P EitherP, Xray.P XrayP, Smoking.P Smoke, Lungcancer.P Lung,  Bronchitis.P Bronc,  Dyspnoea.P Dyspnoea \
    cr.execute('\
            SELECT Tuberculosis.T HasT, SUM(Tuberculosis.P * Asia.P * EitherTubOrLungcancer.P * Xray.P * Smoking.P * Lungcancer.P *  Bronchitis.P * Dyspnoea.P ) \
            FROM Tuberculosis, Asia, EitherTubOrLungcancer, Xray, Smoking, Lungcancer, Bronchitis, Dyspnoea\
            WHERE \
            Asia.A = "N" \
            AND Smoking.S = "N" \
            AND Xray.X = "N" \
            AND Dyspnoea.D = "N" \
            AND Asia.A = Tuberculosis.A \
            AND Smoking.S = Lungcancer.S \
            AND Smoking.S = Bronchitis.S \
            AND Tuberculosis.T = EitherTubOrLungcancer.T \
            AND Lungcancer.L = EitherTubOrLungcancer.L \
            AND Bronchitis.B = Dyspnoea.B \
            AND EitherTubOrLungcancer.E = Dyspnoea.E \
            AND EitherTubOrLungcancer.E = Xray.E \
            GROUP BY HasT \
            ORDER BY HasT' \
            )

    result = cr.fetchall()
    desc = [d[0] for d in cr.description]
    return (desc, result)

def test_question_lung_cancer(db):
    # lung cancer
    # yes: 0.00007470 no: 0.99992530
    cr = db.cursor()

    # SELECT Tuberculosis.T HasT, Tuberculosis.P TuberP, Asia.P AsiaP, EitherTubOrLungcancer.P EitherP, Xray.P XrayP, Smoking.P Smoke, Lungcancer.P Lung,  Bronchitis.P Bronc,  Dyspnoea.P Dyspnoea \
    cr.execute('\
        SELECT Lungcancer.L HasL, SUM(Tuberculosis.P * Asia.P * EitherTubOrLungcancer.P * Xray.P * Smoking.P * Lungcancer.P *  Bronchitis.P * Dyspnoea.P ) \
        FROM Tuberculosis, Asia, EitherTubOrLungcancer, Xray, Smoking, Lungcancer, Bronchitis, Dyspnoea\
        WHERE \
        Asia.A = "N" \
        AND Smoking.S = "N" \
        AND Xray.X = "N" \
        AND Dyspnoea.D = "N" \
        AND Asia.A = Tuberculosis.A \
        AND Smoking.S = Lungcancer.S \
        AND Smoking.S = Bronchitis.S \
        AND Tuberculosis.T = EitherTubOrLungcancer.T \
        AND Lungcancer.L = EitherTubOrLungcancer.L \
        AND Bronchitis.B = Dyspnoea.B \
        AND EitherTubOrLungcancer.E = Dyspnoea.E \
        AND EitherTubOrLungcancer.E = Xray.E \
        GROUP BY HasL \
        ORDER BY HasL' \
        )

    result = cr.fetchall()
    desc = [d[0] for d in cr.description]
    return (desc, result)


def test_question_bronchitis(db):
    # Bronchitis
    # yes: 0.08696218 no: 0.91303782
    cr = db.cursor()

    # SELECT Tuberculosis.T HasT, Tuberculosis.P TuberP, Asia.P AsiaP, EitherTubOrLungcancer.P EitherP, Xray.P XrayP, Smoking.P Smoke, Lungcancer.P Lung,  Bronchitis.P Bronc,  Dyspnoea.P Dyspnoea \
    cr.execute('\
        SELECT Bronchitis.B HasB, SUM(Tuberculosis.P * Asia.P * EitherTubOrLungcancer.P * Xray.P * Smoking.P * Lungcancer.P *  Bronchitis.P * Dyspnoea.P ) \
        FROM Tuberculosis, Asia, EitherTubOrLungcancer, Xray, Smoking, Lungcancer, Bronchitis, Dyspnoea\
        WHERE \
        Asia.A = "N" \
        AND Smoking.S = "N" \
        AND Xray.X = "N" \
        AND Dyspnoea.D = "N" \
        AND Asia.A = Tuberculosis.A \
        AND Smoking.S = Lungcancer.S \
        AND Smoking.S = Bronchitis.S \
        AND Tuberculosis.T = EitherTubOrLungcancer.T \
        AND Lungcancer.L = EitherTubOrLungcancer.L \
        AND Bronchitis.B = Dyspnoea.B \
        AND EitherTubOrLungcancer.E = Dyspnoea.E \
        AND EitherTubOrLungcancer.E = Xray.E \
        GROUP BY HasB \
        ORDER BY HasB' \
        )

    result = cr.fetchall()
    desc = [d[0] for d in cr.description]
    return (desc, result)



db = create_database()
insert_values(db)
desc, result = test_question_bronchitis(db)

print "##############################################"
for d in desc:
    print str(d) + "\t\t",
print ""

for r in result:
    for x in r:
        print str(x) + "\t\t",
    print ""

print ""

n = result[0][1]
y = result[1][1]

print "Ponderated result (Y) = {0:.10f}".format(y / (y + n)), 
print " (N) = {0:.10f}".format(n / (y + n))
