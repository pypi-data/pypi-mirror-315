import sys
sys.path.append("../src/pySSHS")
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

import sshs

# ====================================================
#                      MAIN
#
# Note: the whole process can be performed by directly
# by using the function SSHS_GSS_BoundariesDetect.
# In this file, we split the steps for illustrational
# purposes.
# ====================================================

# Load and plot our test histogram
hist = np.genfromtxt('histotest.csv', delimiter=',')
n=np.linspace(0,np.size(hist)-1,np.size(hist))

fig1, ax1 = plt.subplots(figsize=(5,3))
ax1.plot(n,hist)
ax1.set_title(r"Test Histogram")
plt.show()


# Build the scale-space plane
plane = sshs.SSHS_PlanGaussianScaleSpace(hist)

fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.matshow(plane.transpose().toarray(),cmap=plt.cm.gray_r)
ax2.set_title(r"Scale-space plane")
ax2.set_ylabel('Scales')
plt.show()


fig3, ax3 = plt.subplots(2, 3)

# Detect the meaningful minima with Otsu's method
bounds_otsu, L_otsu, th_otsu = sshs.SSHS_MeaningfulScaleSpace(hist,plane,"otsu")
print("=== OTSU'S METHOD ===")
print("Bounds:")
print(bounds_otsu)

ax3[0,0].plot(n,hist)
ax3[0,0].set_title(r"Otsu")
for i in range(0,np.size(bounds_otsu)):
    ax3[0,0].axvline(x=bounds_otsu[i], color='r', linestyle='--')

# Detect the meaningful minima with half normal law
bounds_hn, L_hn, th_hn = sshs.SSHS_MeaningfulScaleSpace(hist,plane,"halfnormal")
print("=== HALF-NORMAL LAW ===")
print("Bounds:")
print(bounds_hn)

ax3[0,1].plot(n,hist)
ax3[0,1].set_title(r"Half-Normal law")
for i in range(0,np.size(bounds_hn)):
    ax3[0,1].axvline(x=bounds_hn[i], color='r', linestyle='--')

# Detect the meaningful minima with empirical law
bounds_el, L_el, th_el = sshs.SSHS_MeaningfulScaleSpace(hist,plane,"halfnormal")
print("=== EMPIRICAL LAW ===")
print("Bounds:")
print(bounds_el)

ax3[0,2].plot(n,hist)
ax3[0,2].set_title(r"Empirical law")
for i in range(0,np.size(bounds_el)):
    ax3[0,2].axvline(x=bounds_el[i], color='r', linestyle='--')

# Detect the meaningful minima with mean
bounds_me, L_me, th_me = sshs.SSHS_MeaningfulScaleSpace(hist,plane,"mean")
print("=== MEAN ===")
print("Bounds:")
print(bounds_me)

ax3[1,0].plot(n,hist)
ax3[1,0].set_title(r"Mean")
for i in range(0,np.size(bounds_me)):
    ax3[1,0].axvline(x=bounds_me[i], color='r', linestyle='--')

# Detect the meaningful minima with kmeans
bounds_km, L_km, th_km = sshs.SSHS_MeaningfulScaleSpace(hist,plane,"kmeans")
print("=== KMEANS ===")
print("Bounds:")
print(bounds_km)

ax3[1,1].plot(n,hist)
ax3[1,1].set_title(r"Kmeans")
for i in range(0,np.size(bounds_km)):
    ax3[1,1].axvline(x=bounds_km[i], color='r', linestyle='--')

ax3[1,2].set_axis_off()
fig3.suptitle(r"Detected Boundaries with different methods", fontsize=18)
fig3.tight_layout()
plt.show()