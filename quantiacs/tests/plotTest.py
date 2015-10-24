import matplotlib.pyplot as plt
import numpy as np

# Define the event
def ontype(event):
    if event.key == '1':
        print 'It is working'
        plt.clf()

# Create figure an connect the event to it
fig=plt.figure(figsize=(16,8))
plt.gcf().canvas.mpl_connect('key_press_event',ontype)

# Loop
for element in xrange(10):
    #This mimicks the "array of arrays" generating a random array in each loop
    vector = np.random.random(10)  
    plt.plot(vector)
    plt.show()

