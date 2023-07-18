from maser.data import Data
import  matplotlib.pyplot as plt
import numpy as np

class ued:
    def __init__(self):
        self.hits=None
        self.xarray=None
        self.nparray=None
        self.medmad=None


    def reader(self,lbl_file):
        #uses MASER library to read voyager data
        data=Data(filepath=lbl_file)

        #uses xarray library to convert it to xarray
        data_array=data.as_xarray()

        #data kept as right and left polarisation, added squared for total intensity
        dataR=data_array['R']
        dataL=data_array['L']
        dataTI=(dataR)**2+(dataL)**2

        nparry=np.array(dataTI)

        self.xarray=dataTI          #xarray maintains much more metadata than a numpy array so it is kept
        self.nparray=nparry         #numpy array easier to work with so a copy is converted from xarray


    def medmad(self,nchans):
        #function to compute median and MAD, takes nchans, the number of requency channesls
        ur_array=self.nparray

        #computing the median of each frequency channel (70 in lowband data)
        medians=[]
        for j in range(nchans):
            temp=[]
            for i in ur_array:
                temp.append(i[j])
            temp.sort()
            l=len(temp)
            if l%2==0:
                medians.append((temp[l//2-1]+temp[l//2])/2)
            else:
                medians.append(temp[l//2])

        #compute the Median Absolute Deviation
        mads=[]
        for j in range(nchans):
            temp=[]
            for i in ur_array:
                temp.append(i[j])
            temp=abs(temp-medians[j])
            temp.sort()
            l=len(temp)
            if l%2==0:
                mads.append((temp[l//2-1]+temp[l//2])/2)
            else:
                mads.append(temp[l//2])


        #list containing both median and MAD
        medmad=[]
        for i in range(len(medians)):
            medmad.append([medians[i],mads[i]])
        self.medmad=medmad
    
    def search(self,nchans,sigma):
        #searches nparray for a given sigma, if value > median + sigma * MAD it is counted as a hit
        nparray=self.nparray
        xarray=self.xarray
        medmad=self.medmad
        hits=[]

        #searches data and records location of all data above x sigma
        for j in range(nchans):
            for i in range(len(nparray)):
                if nparray[i][j]>(medmad[j][0]+sigma*medmad[j][1]):
                    hits.append([i,j])

        #converts hits from i,j position values to time,frequency coordinates for plotting
        n=len(hits)
        p=0 #progress variable
        for k in range(n):
            f=float(xarray[hits[k][0]][hits[k][1]].frequency)
            t=np.datetime64(np.array(xarray[hits[k][0]][hits[k][1]].time))      #this takes a while but datetime format is cool imo
            hits[k]=[t,f]

            #quick progress bar so I don't lose my mind
            if abs(k/n-p)>=0.01:
                print(np.floor(k/n*100),'% complete')
                p=k/n

        self.hits=hits

    def save_hits(self,filename):
        #saves np array of hit locations to .npy file
        hits=self.hits
        np.save('{0}.npy'.format(filename),hits)
    
    def load_hits(self,filename):
        #loads a previously saved .npy array
        self.hits=np.load('{0}.npy'.format(filename),allow_pickle=True)


    def plot_hits(self,min_time='1986-01-19T00:00:03.900000000',max_time='1986-01-31T23:59:56.900000000',min_f=1.2,max_f=1326,save=False):
        #plots the good stuff
        #note for adding time axis limits must be in 'YYYY-MM-DDT00:00:00 where 00:00:00 is whatever time of the day and T is just a delimiter between the date and time
        hits=self.hits
        f=[]
        t=[]
        for i in hits:
            t.append(i[0])
            f.append(i[1])

        plt.plot(t,f,'k,')
        plt.xlabel('datetime')
        plt.ylabel('frequency (Hz)')
        plt.ylim(min_f,max_f)                                             #minimum and maximum frequencies in Hz
        plt.xlim(np.datetime64(min_time),np.datetime64(max_time)  )       #min max times in datetime64
        #plt.show()
        if(save==True):
            plt.savefig('hit_plot')

inst=ued()
inst.load_hits('hits')
inst.plot_hits(save=True)