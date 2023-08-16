#command util script to search a .npy file

import numpy as np
import argparse

parser = argparse.ArgumentParser(prog = 'A script to search numpy arrays',
                                 description = 'Reads a .npy file with (x, y) dimensions (time, frequency) respectively')
parser.add_argument('-f',   dest = 'filename', type = str, help = 'filename, must be .npy numpy array file', default = None)
parser.add_argument('-tb',  dest = 'time_box', type = int, help = 'number of time samples per box (default = 4)', default = 4)
parser.add_argument('-fb',  dest = 'freq_box', type = int, help = 'number of frequency channels to per box (default = 16)', default = 16)
parser.add_argument('-min', dest = 'snr_min',  type = float, help = 'minimum SNR search value (default = 2)', default = 2)
parser.add_argument('-max', dest = 'snr_max',  type = float, help = 'maximum SNR search value (default = 5)', default = 5)
parser.add_argument('-o',   dest = 'output',   type = str, help = 'output filename (if none given names it filename_{boxdata}_hits)', default = None)

args = parser.parse_args()
filename = args.filename
station = args.station
time_box = args.time_box
freq_box = args.freq_box
chunks = args.chunks
snr_min = args.snr_min
snr_max = args.snr_max
output = args.output

#searches array along the time axis for a given boxcar size
def time_boxcar(data, box_size):

    if(type(data) != np.ndarray):
        raise TypeError('data must be of type numpy.ndarray')
    
    nsamps = data.shape[0]
    nchans = data.shape[1]

    boxed_sums = np.zeros((nsamps - box_size + 1,nchans))   #we lose (box_size - 1) data entries

    for j in range(0, nchans):  #iterates through each frequency bin

        run_sum = 0

        for i in range(0, box_size):        #sums first 4 entries of data

            run_sum += data[i][j]

        boxed_sums[0][j] = run_sum

        for i in range(box_size, nsamps):   #subtracts the last element and adds the next element as the box moves along the array
            run_sum -= data[i - box_size][j]
            run_sum += data[i][j]

            boxed_sums[i - box_size + 1][j] = run_sum

    return boxed_sums

#same process as for time_boxcar, acting on other axis
def freq_boxcar(data, box_size):

    if(type(data) != np.ndarray):
        raise TypeError('data must be of type numpy.ndarray')
    
    nsamps = data.shape[0]
    nchans = data.shape[1]

    boxed_sums = np.zeros((nsamps,nchans - box_size +1))

    for i in range(0, nsamps):  #iterates through each time sample

        run_sum = 0

        for j in range(0, box_size):        #sums first 4 entries of data

            run_sum += data[i][j]

        boxed_sums[i][0] = run_sum

        for j in range(box_size, nchans):   #subtracts the last element and adds the next element as the box moves along the array
            run_sum -= data[i][j - box_size]
            run_sum += data[i][j]

            boxed_sums[i][j -box_size + 1] = run_sum

    return boxed_sums

#calculates frequency channel medians of array
def get_medians(data):

    if(type(data) != np.ndarray):
        raise TypeError('"data" must be of type numpy.ndarray')

    nsamps = data.shape[0]
    nchans = data.shape[1]

    medians = np.zeros(nchans)
    temp = np.zeros(nsamps)

    for j in range(0, nchans):
        for i in range(0, nsamps):
            temp[i] = data[i][j]

        temp.sort()         #sorts data

        if(nsamps % 2 == 1):         
            #if array is odd length picks out middle one, otherwise if even averages the middle two 
            median = temp[nsamps // 2]
        
        else:
            median = (temp[nsamps // 2] + temp[nsamps // 2 + 1])/2

        medians[j] = median

    return medians


data = np.load(filename, allow_pickle = True)

#boxes time samples and frequency channels
boxed_data = time_boxcar(data, time_box)          
boxed_data = freq_boxcar(boxed_data, freq_box)


nsamps_boxed = boxed_data.shape[0]
nchans_boxed = boxed_data.shape[1]

print('Original data array =', data.shape, ', Boxed data array =', boxed_data.shape)

medians = get_medians(boxed_data)       #computes medians

#hits are recorded in a binary numpy array of the same size as the boxed data
#if snr matches the location is given the value True, otherwise False
hits = np.zeros((nsamps_boxed,nchans_boxed), dtype = bool)
tally = 0

#calculates the snr of each value
#if its in a desired range change its corresponding value in hits to True
for j in range(0, nchans_boxed):           
    for i in range(0, nsamps_boxed):
        snr = 10*np.log10(boxed_data[i][j] / medians[j])

        if(snr > snr_min and snr < snr_max):
            hits[i][j] = True
            tally += 1

print('Found {0} potenital hits'.format(tally))

if(output != None):
    np.save(output, hits)

else:
    np.save('{0}_box_t{1}_f{2}_hits'.format(filename, time_box, freq_box), hits)