"""
Plotting a diagonal correlation matrix
======================================

_thumb: .3, .6
"""
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy

sns.set(style="white")

# Generate a large random dataset
rs = np.random.RandomState(33)
d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                 columns=list(ascii_letters[26:]))

# Compute the correlation matrix
corr = d.corr().to_numpy()

# Reordering the sparse matrix
corr_csr = scipy.sparse.csr_matrix(corr)
perm = list(scipy.sparse.csgraph.reverse_cuthill_mckee(corr_csr))

# Move the axis of matrix based on the permutation
perm_corr = np.zeros_like(corr)
for idx, p in enumerate(list(perm)):
    perm_corr[p] = corr[idx]

corr = perm_corr

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns_plot = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.savefig('corr_matrix.png', dpi=600)