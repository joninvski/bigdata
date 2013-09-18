import glob
import mincemeat
import pdb

text_files = glob.glob('gutenberg/*.txt*')

def file_contents(file_name):
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

source = dict((file_name, file_contents(file_name))
            for file_name in text_files)

f = open('outfile', 'w')
def final(key, value):
    f.write(str(key) + str(value) + "\n")

# client

#old version
# def mapfn(key, value):
#     for line in value.splitlines():
#         for word in line.split():
#             yield word.lower(), 1

def mapfn(key, value):
    w={}
    for line in value.splitlines():
        for word in line.split():
            if word.lower() in w.keys():
                w[word.lower()] = w[word.lower()] + 1
            else:
                w[word.lower()] = 1
        if(len(w) >= 10000):
            break

    for k in w.keys():
        yield k, w[k]


def reducefn(key, value):
    if(len(value) > 10):
        return len(value)
    else:
        return ""


s = mincemeat.Server()

# The data source can be any dictionary-like object
s.datasource = source
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="a")

for k in results:
    if results[k]:
        print k, results[k]
