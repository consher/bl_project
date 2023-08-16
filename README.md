## BL 2023 Intern Project - Lightning on Uranus 

The following scripts were made to be used with a multi-site observation approach using the LOFAR (LOw Frequency ARray) telescopes.

**Command line util scripts**:  
- fil2npy.py - takes a filterbank file and outputs a numpy array file (.npy).  
- search.py - takes the .npy file and searches for a given SNR range using a certain boxcar size,  
            outputs an array of boolean values that are True if a 'hit' was detected and False if otherwise.  
- anti_coincidence - compares two 'hits' files from different LOFAR stations, if its appears in both it  
                    keeps them, otherwise it removes them from array.
