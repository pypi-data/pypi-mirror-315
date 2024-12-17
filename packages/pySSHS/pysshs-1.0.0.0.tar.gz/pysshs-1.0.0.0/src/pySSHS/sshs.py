import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from scipy.special import ive
from scipy.special import erfinv, erf
from sklearn.cluster import KMeans




#======================================================
#                   MAIN FUNCTIONS
#======================================================

def SSHS_PlanGaussianScaleSpace(f):

    """Build the scale-space plane containing the detected local minima across the scales

    This function return a sparse lil_matrix where entries equal to 1 correspond to the position 
    of the detected lowest local minima across the different scales. The scale-space is built
    using the discrete Gaussian kernel based on the modified Bessel function of the first kind.

    Parameters
    ----------
    f : 1D array
        input vector

    Returns
    -------
    plane - 2D sparse lil_matrix (each column corresponds to a scale)
        1 for detected local minima, 0 otherwise

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/11/2024)
    """
    
    n=4         # kernel size
    t=1.6       # initial scale
    Niter=np.ceil(np.size(f)/n).astype(int)  # number of iteration through the scales
    ker=ive(np.linspace(-n,n,2*n+1),t)   # discrete Gaussian kernel via Bessel function
    plane = scipy.sparse.lil_matrix((np.size(f),Niter+1),dtype = np.int8)

    bounds = SSHS_LocalMaxMin2(f)
    plane[bounds,0] = 1

    N = np.zeros(Niter+1)
    N[0] = np.size(bounds)

    for i in range(0,Niter):
        f = np.convolve(f,ker,'same')
        bounds = SSHS_LocalMaxMin2(f)
        plane[bounds,i+1] = 1
        N[i+1] = np.size(bounds)
        if N[i+1] == 1:
            break

    return plane


def SSHS_MeaningfulScaleSpace(f,plane,type):

    """Extract meaningful boundaries from the scale-space plane with the selected method

    This function extracts the meaningful minima which will correspond to segmenting the 
    histogram f based on its scale-space representation in plane. It returns an array bounds 
    containing the indices of the boundaries, the set of length 
    of the scale-space curves L, and the detected threshold th.

    Parameters
    ----------
    f : 1D array
        input vector
    plane : lil_matrix
        scale-space plane representation
    type: string
        method to be used: "otsu", "halfnormal", "empiricallaw", "mean", "kmeans"

    Returns
    -------
    bounds - 1D array
        list of indices of the position of the detected local minima
    L - 1D array
        vector containing the length of the scale-space curves
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/11/2024)
    """

    # Compute the scale length of each curve in plane
    L, ind = SSHS_LengthScaleCurve(plane)

    # Detect the meaningful minima with the selected method
    if type.lower() == "otsu":
        bounds, th = SSHS_OtsuMethod(L,ind)
    elif type.lower() == "halfnormal":
        bounds, th = SSHS_HalfNormalLaw(L,ind,plane.shape[1])
    elif type.lower() == "empiricallaw":
        bounds, th = SSHS_EmpiricalLaw(L,ind)
    elif type.lower() == "mean":
        bounds, th = SSHS_MeanTh(L,ind)
    else:
        bounds, th = SSHS_kmeansDetect(L,ind)

    # Postprocessing: manage curves originating from several minima
    bounds = SSHS_RemoveMerge(f, plane, bounds, th)

    return bounds, L, th


def SSHS_GSS_BoundariesDetect(f,type):

    """Extract meaningful boundaries for histogram segmentation by scale-space method

    This function builds a scale-space representation of the provided histogram and then
    extract the meaningful minima which will correspond to segmenting the histogram. It 
    returns an array bounds containing the indices of the boundaries, the set of length 
    of the scale-space curves, and the detected threshold.

    Parameters
    ----------
    f : 1D array
        input vector
    type: string
        method to be used: "otsu", "halfnormal", "empiricallaw", "mean", "kmeans"

    Returns
    -------
    bounds - 1D array
        list of indices of the position of the detected local minima
    plane : lil_matrix
        scale-space plane representation
    L - 1D array
        vector containing the length of the scale-space curves
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/11/2024)
    """

    # Build the scale-space plane
    plane = SSHS_PlanGaussianScaleSpace(f)

    # Extract the meaningful minima, i.e. boundaries
    bounds, L, th = SSHS_MeaningfulScaleSpace(f,plane,type)

    return bounds, plane, L, th


def SSHS_PlotBoundaries(f,bounds,title):

    """Plot the position of the meaningful minima on top of the original histogram

    Parameters
    ----------
    f : 1D array
        input vector which contains the histogram
    bounds : 1D array
        list of indices of the position of the detected local minima
    title : string
        title to be added to the plot

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/11/2024)
    """

    n=np.linspace(0,np.size(f)-1,np.size(f))
    figb, axb = plt.subplots(figsize=(5,3))
    axb.plot(n,f)
    for i in range(0,np.size(bounds)):
        axb.axvline(x=bounds[i], color='r', linestyle='--')
    
    axb.set_title(title)
    plt.show()


#======================================================
#                 AUXILARY FUNCTIONS
#======================================================
def SSHS_LocalMaxMin2(f):

    """Detect the lowest local minima between two consecutive local maxima

    This function return an array bounds containing the indices of the lowest local minima
    between two consecutive local maxima in a vector f

    Parameters
    ----------
    f : 1D array
        input vector

    Returns
    -------
    bounds - 1D array
        list of indices of the position of the detected local minima

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/11/2024)
    """

    locmax = np.zeros(np.size(f))
    locmin = np.max(f) * np.ones(np.size(f))

    # find the local maximum
    for i in range(1, np.size(f)-1):
        if (f[i-1] < f[i]) and (f[i] > f[i+1]):
            locmax[i] = f[i]
    
    i = 1
    while i < (np.size(f)-1):
        if (f[i-1] > f[i]) and (f[i] < f[i+1]):
            locmin[i] = f[i]
            i = i+1
        elif (f[i-1] > f[i]) and (f[i] == f[i+1]):
            i0 = i
            while (i < np.size(f)-2) and (f[i] == f[i+1]):
                i = i+1
            if f[i] < f[i+1]:   # end of flat minimum
                locmin[np.round((i0+i)/2).astype(int)] = f[np.round((i0+i)/2).astype(int)]
            i = i+1
        else:
            i = i+1

    bounds = np.zeros(np.size(f))
    nb = 0
    for i in range(0,np.size(locmin)-1):
        if locmin[i] < np.max(f):
            bounds[nb] = i
            nb = nb + 1

    bounds = bounds[0:nb].astype(int)

    return bounds

def SSHS_LengthScaleCurve(plane):

    """Compute the length of the curves in the scale-space plane

    This function returns a vector containing the length of each scale-space
    curves (in terms of scale lifespan) and a vector containing the indices 
    corresponding to the position of the original local minima (i.e. scale 0)

    Parameters
    ----------
    plane : lil_matrix
        scale-space plane representation

    Returns
    -------
    Length - 1D array
        list of the length of each curve
    Indices - 1D array
        list of indices of the position of the original local minima

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    nr = plane.shape[0]
    nc = plane.shape[1]

    Ncurve = 0
    for i in range(0,nr):
        if plane[i,0] == 1:
            Ncurve = Ncurve + 1

    Length = np.ones(Ncurve)
    Indices = np.zeros(Ncurve)
    ic = 0

    for i in range(0,nr):
        if plane[i,0] == 1:
            Indices[ic] = i
            i0 = i
            j0 = 1
            stop = 0
            if i0 == 0:
                while stop == 0:
                    if plane[i0,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        if j0 > nc-1:
                            stop = 1
                    elif plane[i0+1,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        i0 = i0 + 1
                        if (i0 == 0) or (j0 > nc-1):
                            stop = 1
                    else:
                        stop = 1
                
                ic = ic + 1
            elif i0 == nr-1:
                while stop == 0:
                    if plane[i0,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        if j0 > nc-1:
                            stop = 1
                    elif plane[i0-1,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        i0 = i0 - 1
                        if (i0 == nr-1) or (j0 > nc-1):
                            stop = 1
                    else:
                        stop = 1
                
                ic = ic + 1
            else:
                while stop == 0:
                    if plane[i0,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        if j0 > nc-1:
                            stop = 1
                    elif plane[i0-1,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        i0 = i0 - 1
                        if (i0 == 0) or (j0 > nc-1):
                            stop = 1
                    elif plane[i0+1,j0] == 1:
                        Length[ic] = Length[ic] +1
                        j0 = j0 + 1
                        i0 = i0 + 1
                        if (i0 == nr-1) or (j0 > nc-1):
                            stop = 1
                    else:
                        stop = 1
                
                ic = ic + 1

    return Length.astype(int), Indices.astype(int)

def SSHS_OtsuMethod(L, ind):

    """Detect the meaningful minima using Otsu's method

    This function classifies the set of minima curve lengths stored
    in L into two classes by using Otsu's method. It returns the 
    meaninful ones and the detected threshold.

    Parameters
    ----------
    L : 1D array
        vector of the length of the minima curves
    ind: 1D array
        vector containing the indices of the position of the original
        minima

    Returns
    -------
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    histo, be = np.histogram(L,np.max(L))
    Nt = histo.sum()
    histo = histo/Nt

    muT = 0.0
    for i in range(0,np.size(histo)):
        muT = muT + (i+1) * histo[i]

    sigbcv = np.zeros(np.size(histo)-1)

    for k in range(0,np.size(sigbcv)):
        wb = 0.0
        mu = 0.0
        for i in range(0,k+1):
            wb = wb + histo[i]
            mu = mu + (i+1) * histo[i]

        wf = 1 - wb
        mub = mu / wb
        muf = (muT - mu) / wf
        sigbcv[k] = wb * wf * (mub - muf) ** 2

    th = np.argmax(sigbcv)

    Lb = np.ones(np.size(L))
    for i in range(0,np.size(L)):
        if L[i] < th:
            Lb[i] = 0

    bounds = ind[np.where(Lb==1)[0]]

    return bounds, th


def SSHS_HalfNormalLaw(L, ind, Lmax):

    """Detect the meaningful minima using the epsilon-meaningful method
    (half-normal law)

    This function classifies the set of minima curve lengths stored
    in L into the ones which are epsilon-meaningful for an half-normal 
    law fitted to the data. It returns the meaninful ones and the detected 
    threshold.

    Parameters
    ----------
    L : 1D array
        vector of the length of the minima curves
    ind: 1D array
        vector containing the indices of the position of the original
        minima
    Lmax: number
        maximum possible length of a minima curve (i.e. number of 
        columns in the scale-space plane)

    Returns
    -------
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    # estimate sigma
    sigma = np.sqrt(np.pi/2) * np.mean(L)

    # compute the threshold
    th = np.sqrt(2) * sigma * erfinv(erf(Lmax / (np.sqrt(2) * sigma)) - 1/np.size(L))

    # keep the meaningful minima
    Lth = L
    for i in range(0,np.size(L)):
        if L[i] <= th:
            Lth[i] = 0

    bounds = ind[np.where(Lth != 0)[0]]

    return bounds, th


def SSHS_EmpiricalLaw(L,ind):

    """Detect the meaningful minima using the epsilon-meaningful method
    (empirical law)

    This function classifies the set of minima curve lengths stored
    in L into the ones which are epsilon-meaningful for an empirical 
    law fitted. It returns the meaninful ones and the detected threshold.

    Parameters
    ----------
    L : 1D array
        vector of the length of the minima curves
    ind: 1D array
        vector containing the indices of the position of the original
        minima

    Returns
    -------
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    histo, be = np.histogram(L,np.max(L))
    chisto = np.cumsum(histo / np.sum(histo))
    
    th = np.where(chisto > (1-1/np.size(L)))[0][0]

    Lth = np.ones(np.size(L))
    for i in range(0,np.size(L)):
        if L[i] < th:
            Lth[i] = 0

    bounds = ind[np.where(Lth == 1)[0]]

    return bounds, th


def SSHS_MeanTh(L, ind):

    """Detect the meaningful minima using a mean threshold

    This function classifies the set of minima curve lengths stored
    in L into the ones which meaningful based on a threshold computed
    as the mean of L. It returns the meaninful ones and the detected threshold.

    Parameters
    ----------
    L : 1D array
        vector of the length of the minima curves
    ind: 1D array
        vector containing the indices of the position of the original
        minima

    Returns
    -------
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    th = np.ceil(np.mean(L))

    Lth = np.ones(np.size(L))
    for i in range(0,np.size(L)):
        if L[i] < th:
            Lth[i] = 0

    bounds = ind[np.where(Lth == 1)[0]]

    return bounds, th


def SSHS_kmeansDetect(L, ind):

    """Detect the meaningful minima using kmeans

    This function classifies the set of minima curve lengths stored
    in L into the ones which meaningful based on a kmeans clustering. 
    It returns the meaninful ones and the detected threshold.

    Parameters
    ----------
    L : 1D array
        vector of the length of the minima curves
    ind: 1D array
        vector containing the indices of the position of the original
        minima

    Returns
    -------
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    LL = np.zeros([np.size(L), 2])
    LL[:,1] = L
    km_model = KMeans(n_clusters=2, n_init="auto").fit(LL)
    clusters = km_model.fit_predict(LL)

    Lmax = np.where(L == np.max(L))[0][0]
    cln = clusters[Lmax]

    bounds = ind[np.where(clusters == cln)[0]]
    th = np.min(L[np.where(clusters == cln)[0]])

    
    return bounds, th


def SSHS_RemoveMerge(f, plane, bounds, th):

    """Detect the meaningful minima using kmeans

    This function manage local minima which merge at some point in the
    scale-space plane according to the following rules:
        - if the mergin occur before the scale th then we keep only one minima
          (the lowest one) as they are not individually meaningful
        - if the mergin occur after the scale th then we consider that each 
          initial minima is meaningful and we keep them

    Parameters
    ----------
    f : 1D array
        histogram to be segmented
    plane : lil_matrix
        scale-space plane representation
    bounds - 1D array
        list of the indices of the position of the meaningful minima
    th - number
        detected scale threshold

    Returns
    -------
    bounds - 1D array
        updated list of the indices of the position of the meaningful minima

    Author: Jerome Gilles
    Institution: San Diego State University
    Version: 1.0 (12/12/2024)
    """

    tagplane = scipy.sparse.lil_matrix(plane.shape,dtype = np.int8)
    indrem = np.zeros(np.size(bounds))

    # tag the first curve
    tag = bounds[0]
    stop = 0
    i = tag
    j = 0
    while stop != 1:
        tagplane[i,j] = tag
        if i > 0:
            if plane[i-1,j+1] == 1:
                i = i-1
                j = j+1
            elif plane[i,j+1] == 1:
                j = j+1
            elif plane[i+1,j+1] == 1:
                i = i+1
                j = j+1
            else:
                stop = 1
        else:
            if plane[i,j+1] == 1:
                j = j+1
            elif plane[i+1,j+1] == 1:
                i = i+1
                j = j+1
            else:
                stop = 1
        
        if (j > th) or (j == plane.shape[1]-2):
            stop = 1

    # we address the other curves
    for k in range(1,np.size(bounds)):
        tag = bounds[k]
        i = tag
        j = 0
        stop = 0
        retag = 0

        while stop != 1:
            tagplane[i,j] = tag
            if i >1:
                if plane[i-1,j+1] == 1:
                    if (tagplane[i-1,j+1] == bounds[k-1]) and (retag == 0):
                        if f[bounds[k-1]] < f[bounds[k]]:
                            indrem[k] = 1
                            stop =1
                        else:
                            indrem[k-1] = 1
                            retag = 1
                    i = i-1
                    j = j+1
                elif plane[i,j+1] == 1:
                    if (tagplane[i,j+1] == bounds[k-1]) and (retag == 0):
                        if f[bounds[k-1]] < f[bounds[k]]:
                            indrem[k] = 1
                            stop =1
                        else:
                            indrem[k-1] = 1
                            retag = 1
                    j = j+1
                elif plane[i+1,j+1] == 1:
                    i = i+1
                    j = j+1
                else:
                    stop = 1
            else:
                if plane[i,j+1] == 1:
                    if (tagplane[i,j+1] == bounds[k-1]) and (retag == 0):
                        if f[bounds[k-1]] < f[bounds[k]]:
                            indrem[k] = 1
                            stop =1
                        else:
                            indrem[k-1] = 1
                            retag = 1
                    j = j+1
                elif plane[i+1,j+1] == 1:
                    i = i+1
                    j = j+1
                else:
                    stop = 1
            
            if (j >  th) or (j == plane.shape[1]-2):
                stop = 1
        
    bounds = bounds[np.where(indrem == 0)[0]]

    return bounds