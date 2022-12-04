# Assignment 3 - IIR Filters
## Kerolos Ikladeos (2432195i) and Anirudh Garikapati (2480291g)


## Application
- Indoor Garage Parking Sensor using LDR wih 3 LEDs reacting to different values on how far or close the light source is.

## YouTube Video Link
> https://youtu.be/2AZ1obUZoQc

## Features
- IIR filtering using Butterworth and IIR filter module
- DAQ using Arduino Uno and PyFirmata2 on Python
- Detecting sampling rate **real time**


## Contents

 <a name="desc"></a>
## 1. main.py

Code containing filtering and realtime callback from Arduino and FFT analysis of the filtered and unfiltered signal

<a name="usage"></a>
## 2. report.pdf

report describing everything for this project

<a name="usage"></a>
## 3. rearlights.ino

Arduino sketch to turn on the LED lights for rear car lights used for the video demo

<a name="usage"></a>
## 4. qt_graphs.py

QT plots with live FFT transformation that were used to verify the FFT results of the main code.


## Credits

 - [PyFirmata2](https://github.com/berndporr/pyFirmata2/tree/master/examples) for event driven real time callbacks 

 - [IIR Filter Module](https://github.com/berndporr/py-iir-filter) for IIR filtering using second order structures (sos)

