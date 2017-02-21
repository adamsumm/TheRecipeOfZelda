import sklearn
from sklearn import mixture
import sys
import numpy as np
from sklearn.manifold import TSNE

with open(sys.argv[1]) as infile:
    cats = infile.readline().rstrip().split(',')
    data = []
    for line in infile:
        data.append([float(c) for c in line.rstrip().split(',')])


data = np.array(data)
data = np.nan_to_num(data)

dpgmm = mixture.BayesianGaussianMixture(n_components=50,
                                        weight_concentration_prior=1e-3,
                                        covariance_type='tied').fit(data)

cats =  dpgmm.predict(data)

model = TSNE(n_components=2, random_state=0,learning_rate=100)
transformed = model.fit_transform(data) 

colors = ['r','g','b','c','m','y','k']
shapes = ['x','+','o','v','.','^']

import itertools
prods = [''.join(a) for a in itertools.product(*[colors,shapes])]
print prods


import matplotlib.pyplot as plt

print len(np.unique(cats))
for c in np.unique(cats):
    ind = np.where(cats == c)
    plt.plot(transformed[ind,0],transformed[ind,1],prods[c])

plt.show()

