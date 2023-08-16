#converts a filterbank to a numpy array file for easier manipulation (will lose metadata)
#note: requires Your reader
from your import Your
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-fil', dest = 'filterbank', type = str, help = 'filterbank file to read')
parser.add_argument('-o',   dest = 'output',     type = str, help = 'output filename')
parser.add_argument('-c',   dest = 'chunks',     type = int, help = 'number of chunks to split the data into (default = 1)', default = 1)
parser.add_argument('-h',   dest = 'header',     help = 'print header of fil file (default = do not)', action = 'store_const', const = 'y', default = 'n')

args = parser.parse_args()
fil_file = args.filterbank
n = args.chunks
output = args.output
header = args.header

#your reader
fil = Your(fil_file)
nsamp = fil.your_header.nspectra
step = int(nsamp/n)

if(header == 'y'):
    print(fil.your_header)


#dprint(step,c_len)

for i in range(0,n):
    if(n > 1):
        print('reading chunk {0}'.format(i))

    data = fil.get_data(nstart=i*step, nsamp=step)        #read a chunk
    
    #if only 1 chunk saves file as output name
    if(n == 1):
        np.save(output, data)

    #otherwise saves it with chunk number appended
    else:
        np.save('{0}_{1}'.format(output, i), data)