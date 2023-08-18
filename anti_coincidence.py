#command line script to compare 
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f1',  dest = 'file1',   type = str,   help = '1st file in .npy format')
parser.add_argument('-f2',  dest = 'file2',   type = str,   help = '2nd file in .npy format to compare with 1st')
parser.add_argument('-o',   dest = 'output',  type = str,   help = 'output file name')
parser.add_argument('-err', dest = 'error',   type = int,   help = 'error value for anti-coincidence (default = 0)', default = 0)

args = parser.parse_args()
f1 = args.file1
f2 = args.file2
output = args.output
err = args.error

print('Comparing {0} and {1} potential hits.'.format(f1, f2))

hits1 = np.load(f1, allow_pickle=True)
hits2 = np.load(f2, allow_pickle=True)

if(hits1.shape != hits2.shape):
    raise ValueError('Array files must have same shape')

tally = 0

for i in range(0, hits1.shape[0]):      #iterates through each value of hit1 and hit2
    for j in range(0, hits1.shape[1]):
        #begins test if hits1[i][j] is True
        if(hits1[i][j] == True):

                if(err > 0):        
                    #if the error margin is greater than 1
                    #it checks the box around hits1[i][j]

                    check = False

                    for p in range(-err, err + 1):
                        for q in range(-err, err + 1):
                            
                            if(hits1[i][j] == hits2[i + p][j + q]):
                                check = True    
                                #if the box around hits1[i][j] contains a match check is True

                    #passes anti-coincidence test
                    if(check == True):
                        tally += 1

                    #otheriwse sets both to false
                    else:
                        hits1[i][j] = False
                        hits2[i][j] = False        

                #if the error value is 1, just compares the exact corresponding hits2 value
                elif(err == 0):
                    if(hits1[i][j] == hits2[i][j]):
                        tally += 1

                    else:
                        hits1[i][j] = False
                        hits2[i][j] = False

        #if hits1 is False, simply sets both to zero
        else:
            hits1[i][j] = False
            hits2[i][j] = False

if(tally == 0):
    print('{0} hits appear in both {1} and {2} :('.format(tally, f1, f2),'\n')
else: 
    print('{0} hits appear in both {1} and {2}!'.format(tally, f1, f2),'\n')
    np.save(output, hits1) #as hits1 and hits2 are now idendical it doesn't matter which is saved