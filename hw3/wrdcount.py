import glob

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
    print key, value
    f.write(str(key,value))

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

    for k in w.keys():
        yield k, w[k]


def reducefn(key, value):
    return key, len(value)
