import os
import statistics
import matplotlib.pyplot as plt
import numpy as np


anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data\\anode'
pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data\\pmt'

anodeTimes = []     #store timestamps for anode files
pmtTimes = []       #store timestamps for pmt files



for filename in os.listdir(anodeDir):
    #print(os.path.join(anodeDir, filename))       #prints the name of the file in the directory
    
    name = os.path.join(anodeDir, filename)
    index = len(name) - 7 
  
    timeStampVal = int(name[index - 6]) * 600000 + int(name[index - 5]) * 60000 + int(name[index - 3]) * 10000 + int(name[index - 2]) * 1000 + int(name[index]) * 100 + int(name[index + 1]) * 10 + int(name[index + 2]) #taking the last three number in the timestamp (milliseconds) and adding it to anodeTimes

    #this method may be inaccurate when timing things near a change in hour

    anodeTimes.append(timeStampVal) 
     
    
    #print('\n')

    

for filename in os.listdir(pmtDir):
    #print(os.path.join(pmtDir, filename))       #prints the name of the file in the directory
    
    name = os.path.join(pmtDir, filename)
    index = len(name) - 7
  
    timeStampVal = int(name[index - 6]) * 600000 + int(name[index - 5]) * 60000 + int(name[index - 3]) * 10000 + int(name[index - 2]) * 1000 + int(name[index]) * 100 + int(name[index + 1]) * 10 + int(name[index + 2]) #taking the last three number in the timestamp (milliseconds) and adding it to anodeTimes


    pmtTimes.append(timeStampVal) 
     
    
    #print('\n')

   
print("-------------------- now displaying anodeTimes --------------") 

for i in range(len(anodeTimes)):  
    print(anodeTimes[i])
    print('\n')

print("-------------------- now displaying pmtTimes --------------")

for i in range(len(pmtTimes)):  
    print(pmtTimes[i])
    print('\n')


timeDifs = [] #difference between timestamps is stored here


count = 0

for a, p in zip(anodeTimes, pmtTimes): 
    timeDifs.append( abs(a - p) )
    print(abs( a - p ), count)
    count = count + 1

#also do standard deviation
#make sure to include 


print("The average time difference between the two oscilloscopes is: ")
print(sum(timeDifs) / len(timeDifs))
print("\n")
print("the standard deviation is:")
print(statistics.stdev(timeDifs))

np.histogram(timeDifs, bins=20, range=None, normed=None, weights=None, density=None)   #these lines create a histogram
plt.hist(timeDifs, bins ='auto')
plt.title("time differences")
plt.show()

#pmt folder usually has one more acquisition than the anode folder. This can cause large discrepancies when 
#multiple acquisitions runs are kept in the same folder as non-corresponding acquisitions are subtracted
#resulting in huge differences. 