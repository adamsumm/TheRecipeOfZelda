
import sys
import xmltodict
from os import listdir
from os.path import isfile, join


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


mypath = sys.argv[1]

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

all_data = []
for filename in onlyfiles:

    with open(filename) as fd:
        doc = xmltodict.parse(fd.read())
    doc = doc['root']

    data = {key:[] for key in doc}
    numeric = {key:False for key in doc}
    onePer = []
    numPer = 0
    for key,val in doc.items():
        if ';' in val:
            vals = val.split(';')
            numPer = len(vals)
            numeric[key] = is_number(vals[0])
            v_ = []
            for v in vals:
                if v == '-1':
                    v_.append('nan')
                else:
                    v_.append(v)
            vals = v_
            data[key] = vals
        else:
            if val == '-1':
                val = 'nan'
            onePer.append((key,val))
            numeric[key] = is_number(val)


    for k,v in onePer:
        data[k] = [v]*numPer

    continuous = [key for key in numeric if (numeric[key]) ]
    discrete = [key for key in numeric if (not numeric[key]) ]
    all_data.append( (data, continuous, discrete))
    #outstr = '\t' + '\t'.join(['EXP{}'.format(ii) for ii in range(numPer)]) + '\n'
    #for c in continuous:
    #    outstr += '\t'.join([c] + data[c]) + '\n'
    #for c in regulators:
    #    outstr += '\t'.join([c] + data[c]) + '\n'
    #print outstr

categories = [k for k in all_data[0][0]]

all_categories = {'k':'k',
                  'b':'b',
                  'l':'l',
                  'S':'s',
                  'K':'bosskey',
                  'I':'keyitem',
                  'p':'p',}
                  

actual_cats = []
for cat in categories:
    if cat in discrete:
        for c in [all_categories[k] for k in sorted(all_categories)]:
            actual_cats.append('{}_{}'.format(cat,c))
    else:
        actual_cats.append(cat)    
print ','.join(actual_cats)
for data,continuous,discrete in all_data:
    for ii in range(len(data[categories[0]])):
        line = []
        for cat in categories:
            if cat in discrete:
                 for k in sorted(all_categories):
                     line.append(str(data[cat][ii].count(all_categories[k])))
            else:
                line.append(data[cat][ii])
        print ','.join(line)
        
    
