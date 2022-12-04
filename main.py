from pyfirmata2 import Arduino
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import iir_filter
from scipy import signal
from time import perf_counter

# Realtime oscilloscope at a sampling rate of 100Hz
# It displays analog channel 0.
# You can plot multiple chnannels just by instantiating
# more RealtimePlotWindow instances and registering
# callbacks from the other channels.
# Copyright (c) 2018-2020, Bernd Porr <mail@berndporr.me.uk>
# see LICENSE file.

PORT = Arduino.AUTODETECT
# PORT = '/dev/ttyUSB0'

# Creates a scrolling data display
class RealtimePlotWindow:

    def __init__(self,title): #xlabel):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        # that's our plotbuffer
        self.plotbuffer = np.zeros(500)
        # create an empty line
        self.line, = self.ax.plot(self.plotbuffer)
        # axis
        self.ax.set_ylim(0, 1.2)
        self.ax.set_ylabel("Normalised Voltage (V) \nLight Intensity")
        self.ax.set_title(title)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)
        self.samp_freq = self.ax.text(0.9, 1.05, "Sample Rate:%d",
            bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 5},
            transform=self.ax.transAxes, ha="center")
        

    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(self.plotbuffer)
        self.samp_freq.set_text(f'Sample Rate: {self.samprate:.3f} Hz')
        
        return self.line,

    # appends data to the ringbuffer
    def addData(self, v,samp_rate): #xlabel):
        self.ringbuffer.append(v)
        self.samprate = samp_rate
        


# Create twp instances of an animated scrolling window (one for filtered data and one for unfiltered data)
realtimePlotWindow_unfiltereddata = RealtimePlotWindow("Unfiltered Data")
realtimePlotWindow_filtereddata = RealtimePlotWindow("Filtered Data")


# sampling rate: 1000Hz
samplingRate = 1000 #better sampling and getting all information in real time coming in


fc = 45 # lowpass cutoff freqeuncy
fs = 1000 # sampling frequency

sos1 = signal.butter(4, fc/fs*2, 'lowpass', output='sos') # creating IIR filter coefficients using Butterworth filter
iir1 = iir_filter.IIR_filter(sos1) # instanciating the IIR filter using the sos coefficients created using Butterworth


counter = 0 # used to find the sampling frequency
samplingFreq = 0 # start at zero and is the result of the first two counters as division is undefined
time_prev = perf_counter() # remove the transient response and to be considered as the initial value set outside which is 0
array_fft = np.empty([]) # filling an empty array with unfiltered input data to find its FFT response 
filtered_array_fft = np.empty([]) # filling an empty array with filtered input data to find its FFT response 

# called for every new sample which has arrived from the Arduino
def callBack(data):
    global array_fft
    global filtered_array_fft
    global samplingFreq
    global counter
    global time_prev

    # filling array with unfiltered data
    array_fft = np.append(array_fft,data)
    
    #if condition that works as a stopwatch and calculates the sampling frequency
    if counter == 100: # calculate sampling frequency every 100 samples
        counter = 0
        time_now = perf_counter()
        elapsedtime = time_now - time_prev
        time_prev = time_now
        samplingFreq = (100/(elapsedtime))

    counter = counter + 1 
    
    
    # filtering of input data:
    filtered_output = iir1.filter(data)

    # filling array with filtered data
    filtered_array_fft = np.append(filtered_array_fft,filtered_output)

    # send the sample to the plotwindow:
    realtimePlotWindow_unfiltereddata.addData(data,samplingFreq) # plotting unfiltered data
    realtimePlotWindow_filtereddata.addData(filtered_output,samplingFreq) # plotting filtered output

    
    
    #digital pin 10 --> green LED
    #digital pin 9 --> yellow LED
    #digital pin 6 --> red LED
    
    # light source far away
    if filtered_output < 0.4:
        board.digital[10].write(1) # green LED ON
        board.digital[9].write(0) # OFF
        board.digital[6].write(0) # OFF
        print("Enough Space")
    
    # light source getting closer
    elif 0.4 < filtered_output < 0.6:
        board.digital[10].write(0) # OFF
        board.digital[9].write(1) # yellow LED ON
        board.digital[6].write(0) # OFF
        print("Take Caution!")

    #light source really close
    elif filtered_output > 0.6:
        board.digital[10].write(0) # OFF
        board.digital[9].write(0) # OFF
        board.digital[6].write(1) # red LED ON
        print("STOP IMMEDIATELY!")


# Get the Ardunio board.
board = Arduino(PORT)

# Set the sampling rate in the Arduino
board.samplingOn(1000 / samplingRate)

# Register the callback which adds the data to the animated plot
board.analog[0].register_callback(callBack)

# Enable the callback
board.analog[0].enable_reporting()

# show the plot and start the animation
plt.show()

# needs to be called to close the serial port
board.exit()

print("Mission Parking: Successful!!")



# Finding the Fourier Transform of the unfiltered data and plotting it:
fourier_transform = np.fft.fft(array_fft) / len(array_fft)
x_axis = np.linspace(0,1000,len(array_fft))

plt.figure()
plt.title("Unfiltered Frequency Spectrum")
plt.xlim(-5,500)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.plot(x_axis,np.abs(fourier_transform))

# Finding the Fourier Transform of the filtered data and plotting it:
fourier_transform_filtered = np.fft.fft(filtered_array_fft) / len(filtered_array_fft)
x_axis_filtered = np.linspace(0,1000,len(filtered_array_fft))

plt.figure()
plt.title("Filtered Frequency Spectrum")
plt.xlim(-5,500)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.plot(x_axis_filtered,np.abs(fourier_transform_filtered))


plt.show()