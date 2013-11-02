import sqlite3


# Create database for Bayesian network (page 16 of the slides)

def create_database():
    db = sqlite3.connect(':memory:')
    return db

# Original
# +------+     +-----+
# | Rain | --> | Wet |
# +------+     +-----+

# Now with thunder
# +------+     +---------+
# | Rain | --> | Thunder |
# +------+     +---------+
#   |
#   |
#   v
# +------+
# | Wet  |
# +------+

# Now with sprinkler and hose
# +------+     +-----------+
# | Rain | --> |  Thunder  |
# +------+     +-----------+
#   |
#   |
#   v
# +------+     +-----------+     +------+
# | Wet  | <-- | Sprinkler | --> | Hose |
# +------+     +-----------+     +------+
#   ^            |
#   +------------+


# --------------
# |    RAIN    |
# --------------
# | Y    | 0.2 |
# | N    | 0.8 |
# --------------

# ----------------
# | Wet  |  Rain |
# ----------------
# | Y | Y | 0.90 |
# | Y | N | 0.20 |
# | N | Y | 0.10 |
# | N | N | 0.80 |
# ----------------

# ------------------------
# | Thunder | Rain | %   |
# | Y       | Y    | 0.8 |
# | Y       | N    | 0.1 |
# | N       | Y    | 0.2 |
# | N       | N    | 0.9 |
# ------------------------


def insert_values(db):
    c = db.cursor()
    c.execute('CREATE TABLE rain (R text, P float)')
    c.execute('INSERT INTO rain VALUES ("Y", 0.2)')
    c.execute('INSERT INTO rain VALUES ("N", 0.8)')
    db.commit()

    c.execute('CREATE TABLE wet (W text, R text, P float)')
    c.execute('INSERT INTO wet VALUES ("Y", "Y", 0.90)')
    c.execute('INSERT INTO wet VALUES ("Y", "N", 0.20)')
    c.execute('INSERT INTO wet VALUES ("N", "Y", 0.10)')
    c.execute('INSERT INTO wet VALUES ("N", "N", 0.80)')
    db.commit()

    # Slide 21
    c.execute('CREATE TABLE newWet (W text, S text, R text, P float)')
    c.execute('INSERT INTO newWet VALUES ("Y", "Y", "Y", 0.90)')
    c.execute('INSERT INTO newWet VALUES ("Y", "Y", "N", 0.70)')
    c.execute('INSERT INTO newWet VALUES ("Y", "N", "Y", 0.80)')
    c.execute('INSERT INTO newWet VALUES ("Y", "N", "N", 0.10)')
    c.execute('INSERT INTO newWet VALUES ("N", "Y", "Y", 0.10)')
    c.execute('INSERT INTO newWet VALUES ("N", "Y", "N", 0.30)')
    c.execute('INSERT INTO newWet VALUES ("N", "N", "Y", 0.20)')
    c.execute('INSERT INTO newWet VALUES ("N", "N", "N", 0.90)')
    db.commit()

    c.execute('CREATE TABLE thunder (T text, R text, P float)')
    c.execute('INSERT INTO thunder VALUES ("Y", "Y", 0.80)')
    c.execute('INSERT INTO thunder VALUES ("Y", "N", 0.10)')
    c.execute('INSERT INTO thunder VALUES ("N", "Y", 0.20)')
    c.execute('INSERT INTO thunder VALUES ("N", "N", 0.90)')
    db.commit()

    c.execute('CREATE TABLE sprinkler (S text, P text)')
    c.execute('INSERT INTO sprinkler VALUES ("Y", 0.3)')
    c.execute('INSERT INTO sprinkler VALUES ("N", 0.7)')
    db.commit()

def ask_question_knowing_wet_and_sprinkler(db):
    c = db.cursor()
    c.execute('SELECT rain.R, rain.P || " * " || newWet.P || " * " || sprinkler.P\
               FROM rain, newWet, sprinkler\
               WHERE newWet.W = "Y" and sprinkler.S = "Y" and rain.R = newWet.R and sprinkler.S = newWet.S\
               -- GROUP BY rain.R\
               ')
    result = c.fetchall()
    return result

def ask_question_knowing_wet_but_dont_know_sprinkler(db):
    c = db.cursor()
    c.execute('SELECT rain.R, rain.P || " * " || newWet.P || " * " || sprinkler.P\
               FROM rain, newWet, sprinkler\
               WHERE newWet.W = "Y" and rain.R = newWet.R and sprinkler.S = newWet.S\
               -- GROUP BY rain.R\
               ')
    result = c.fetchall()
    return result

def ask_question_knowing_wet_and_thunder(db):
    c = db.cursor()
    c.execute('SELECT rain.R, SUM(rain.P * wet.P * thunder.P)\
               FROM rain, wet, thunder\
               WHERE thunder.T = "Y" AND wet.W = "Y" and rain.R = wet.R and wet.R = thunder.R\
               GROUP BY rain.R\
               ')
    result = c.fetchall()
    return result

def ask_question_knowing_wet(db):
    c = db.cursor()
    # Question is probability of raining knowing the ground is wet
    c.execute('SELECT rain.R, SUM(rain.P * wet.P) \
               FROM rain, wet \
               WHERE wet.W="Y" AND rain.R=wet.R \
               GROUP BY rain.R')
    result = c.fetchall()
    return result
print "######################################"

db = create_database()
insert_values(db)
result = ask_question_knowing_wet(db)
result = ask_question_knowing_wet_and_thunder(db)
result = ask_question_knowing_wet_but_dont_know_sprinkler(db)
result = ask_question_knowing_wet_and_sprinkler(db)

print "Result: "
for p in result:
    print p
print ""

n = result[0][1]
y = result[1][1]

print "Ponderated result (Y) = " + str(y / (y + n))
print "Ponderated result (N) = " + str(n / (y + n))
