import sqlite3

homework = sqlite3.connect(':memory:')
c = homework.cursor()

# Create database for Bayesian network (page 16 of the slides)

c.execute('CREATE TABLE rain (R text, P float)')
c.execute('INSERT INTO rain VALUES ("Y", 0.2)')
c.execute('INSERT INTO rain VALUES ("N", 0.8)')
homework.commit()

c.execute('CREATE TABLE wet (W text, R text, P float)')
c.execute('INSERT INTO wet VALUES ("Y", "Y", 0.90)')
c.execute('INSERT INTO wet VALUES ("N", "Y", 0.10)')
c.execute('INSERT INTO wet VALUES ("Y", "N", 0.20)')
c.execute('INSERT INTO wet VALUES ("N", "N", 0.80)')
homework.commit()

# SQL query
c.execute('SELECT rain.R, SUM(rain.P * wet.P) \
           FROM rain, wet \
           WHERE wet.W="Y" AND rain.R=wet.R \
           GROUP BY rain.R')

result = c.fetchall()
print result
n = result[0][1]
y = result[1][1]
print y / (y + n)
