import os
anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data\\anode'
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data\\pmt'

anodeTimes = []     #store timestamps for anode files
#pmtTimes = []       #store timestamps for pmt files
numstring = []      #we will parse the numbers from the filename and we will store them in the time arrays. 
count = 0

for filename in os.listdir(anodeDir):
    print(os.path.join(anodeDir, filename))       #prints the name of the file in the directory
    
    name = os.path.join(anodeDir, filename)

    numString = [] #numString =         we will parse the numbers from the milliseconds section of the filename and we will store them in the anodeTimes array


    for word in name.split():
        if word.isdigit():
            numString.append(int(word))

    anodeTimes.append(numString)
    
    
    print('\n')

    count = count + 1



for i in range(anodeTimes.len()):  #there is an issue with len()
    print(anodeTimes[i])
    print('\n')
    
'''
for filename in os.listdir(anodeDir):
    print(os.path.join(anodeDir, filename))
'''