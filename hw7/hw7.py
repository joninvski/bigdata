import Orange
import pdb

train = Orange.data.Table("genestrain")
test = Orange.data.Table("genesblind")

naive = Orange.classification.bayes.NaiveLearner(train)
naive.name = "name"


learners= [naive]

N = len(test)

res = [''] * N
for i in range(N):
    print(learners[0](test[i]))
    res[i] = (learners[0](test[i]))

