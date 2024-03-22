# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 08:56:47 2021

@author: localuser
"""
import matplotlib.pyplot as plt
import numpy as np
import time
import os.path

def printData(fn, st):
    fo = open(fn, 'a')
   
    print(st)
    fo.write(st+'\n')
    fo.close()
    
def plot(x,y):
    plt.figure()
    plt.plot(x,y)
    plt.show()

def calculate_signal_from_detector(data,freq):
    t = data['time']
    a = data['amplitude (a.u.)']

    
    ff = np.fft.fftfreq(len(t), d=t[1][0]-t[0][0])
    fourier = np.abs(np.fft.fft(a))
    #fourier = fourier-fourier[0]
# #   print(len(ff))
#    print(len(t))
    i=ff>=0
    f = ff[i]
    r = fourier[i]
#    print((f))
#    print(len(t))
#    
#    print((f[0]))
#    print((f[1]))
#    
#    print((t[0]))
#    print((t[1]))
#    plt.plot(f,r)
    res=[]
    for k in range(0,len(freq)):
        index=(f>(freq[k]*1e9-0.01e9))
        res.append(r[index][0])
       
    return np.array(res)
    
        

def calculate_signal(osc_data, Detector_bottom_name, freq, model):
    res = calculate_signal_from_detector(osc_data,freq)
    for i in range(0,len(Detector_bottom_name)):
        r = calculate_signal_from_detector(model.getresult("OSC_bottom_"+str(i), "signal"),freq)
        r[i]=0
        res = res+r

    return res #10*np.log10(res)


def BalancedDetector(model, name, x, y, f, position, start_time, ifLimitTimeRange,c):
    
    model.addelement('PIN Photodetector')
    model.set('name', 'PD')
    model.set('x position', -350)
    model.set('y position', -250)
    model.set('rotated',0)
    model.set("frequency at max power",0)
    model.set("frequency",c/1550e-9)
    
    model.addelement('LP Rectangular Filter')
    model.set('name', 'LPF')
    model.setexpression("LPF", "cutoff frequency", '');
    model.set("cutoff frequency", 100e9)
    model.set('x position', -250)
    model.set('y position', -250)
    model.set('rotated',0)
    
    
    model.addelement('DC block')
    model.set('name', 'HPF')
#    model.setexpression("HPF", "cutoff frequency", '');
#    model.set("cutoff frequency", 0.5e9)
    model.set('x position', -50)
    model.set('y position', -250)
    model.set('rotated',0)

    
    model.connect('PD', 'output', 'LPF', 'input')
    model.connect('LPF', 'output', 'HPF', 'input')
    
#    model.addelement('Electrical Multiplier')
#    model.set('name', 'MIX1')
#    model.set('x position', -150)
#    model.set('y position', -100)
#    model.set('rotated',0)
#    
#    model.connect('HPF', 'output', 'MIX1', 'input 2')
#    
#    model.addelement('Scripted Source')
#    model.set('name', 'ModulationSource')
#    model.set('x position', -400)
#    model.set('y position', -100)
#    model.set('rotated',0)
#    model.set('script', 'OUTPUT=sin(2*pi*'+str(f) +'e9*TIME);')
#    model.connect('ModulationSource', 'output', 'MIX1', 'input 1')
    
    model.select('PD')
#    model.shiftselect('MIX1')
#    model.shiftselect('ModulationSource')
    
    model.shiftselect('HPF')
    model.shiftselect('LPF')
    
    model.createcompound()
    
    model.set("name", name)
    model.set("x position", x)
    model.set("y position", y)
    model.set("rotated", position*3)
    
    model.addport(name, 'Detector_in', 'Bidirectional', 'Optical', 'Right', 0.5)
    model.select(name+'::RELAY_1')
    model.set('x position', -50)
    model.set('y position', -100)
    model.set('rotated',1)
    model.connect(name+'::PD', 'input', name+'::RELAY_1', 'port')
    
    
    model.addport(name, 'Detector_out', 'Bidirectional', 'Electrical', 'Left', 0.5)
    model.select(name+'::RELAY_2')
    model.set('x position', -450)
    model.set('y position', -250)
    model.set('rotated',1)
#    model.connect(name+'::MIX1', 'output', name+'::RELAY_2', 'port')
    model.connect(name+'::HPF', 'output', name+'::RELAY_2', 'port')
    
    t = name.split("_")
    if (position == 0):
        rot=2
        nm = t[1]
    else:
        rot=1
        nm = t[1]+"_"+t[2]
    
    model.addelement('Spectrum Analyzer')
    model.set('name', 'RFSA_'+nm)
    model.set('sensitivity', 1e-23)
    model.set('power unit', 'W')
    model.set('limit time range', ifLimitTimeRange)
    if (ifLimitTimeRange):
        model.set('start time', start_time)
    

    
    if (position == 0):
        model.set('x position', x-200)
        model.set('y position', y)
    else:
        model.set('y position', y+200)
        model.set('x position', x)
        
    model.set('rotated',rot)
    model.connect(name, 'Detector_out', 'RFSA_'+nm, 'input')
    
    model.addelement('Power Meter')
    model.set('name', 'PWM_'+nm)
    model.set('limit time range', ifLimitTimeRange)
    if (ifLimitTimeRange):
        model.set('start time', start_time)

    if (position == 0):
        model.set('x position', x-200)
        model.set('y position', y-60)
    else:
        model.set('y position', y+200)
        model.set('x position', x-60)
        
    model.set('rotated',rot)
    model.connect(name, 'Detector_out', 'PWM_'+nm, 'input')
    
    model.addelement('Oscilloscope')
    model.set('name', 'OSC_'+nm)
    model.set('limit time range', ifLimitTimeRange)
    if (ifLimitTimeRange):
        model.set('start time', start_time)
    if (position == 0):
        model.set('x position', x-200)
        model.set('y position', y+60)
    else:
        model.set('y position', y+200)
        model.set('x position', x+60)

    model.set('rotated',rot)
    model.connect(name, 'Detector_out', 'OSC_'+nm, 'input')
    
    
    
def MLD(model, name, x, y, f,c):
    
    model.addelement('CW Laser')
    model.set('name', 'LD')
    model.set('x position', -250)
    model.set('y position', -450)
    model.set('rotated',1)
    model.set('power',1)
    model.set("frequency", c/(1550)/1e-9)
    
    model.addelement('Optical Amplitude Modulator')
    model.set('name', 'AM')
    model.set('x position', -250)
    model.set('y position', -300)
    model.set('rotated',1)
    
    
    
    
    model.connect('AM', 'input', 'LD', 'Output')
    
    
    model.addelement('Scripted Source')
    model.set('name', 'ModulationSource')
    model.set('x position', 0)
    model.set('y position', -300)
    model.set('rotated',2)
    model.set('script', 'OUTPUT=0.5+0.5*sin(2*pi*'+str(f) +'e9*TIME);')
    model.connect('ModulationSource', 'output', 'AM', 'modulation')
    
#    model.addelement('Oscilloscope')
#    model.set('name', 'Osc2')
#    model.set('x position', -100)
#    model.set('y position', -200)
#    model.set('rotated',1)
#    model.connect('ModulationSource', 'output', 'Osc2', 'input')
    
    model.select('ModulationSource')
#    model.shiftselect('Osc2')
    model.shiftselect('AM')
    model.shiftselect('LD')
    
    model.createcompound()
    
    model.set("name", name)
    
    model.set("x position", x)
    model.set("y position", y)
    
    model.addport(name, 'LD_out', 'Bidirectional', 'Optical', 'Bottom', 0.5)
    model.select(name+'::RELAY_1')
    model.set('x position', -240)
    model.set('y position', -140)
    model.set('rotated',1)
    model.connect(name+'::AM', 'output', name+'::RELAY_1', 'port')

def Res(model, name, data1, x, y, start_time, ifLimitTimeRange):
    data='C:\\Users\\localuser\\Documents\\Interconnect\\filename_3000.ldf'
    model.addelement('Waveguide Coupler')
    model.set('name', 'WC1')
    model.set('x position', -200)
    model.set('y position', -200)
    model.set('coupling coefficient 1', 0.01)
    
    model.addelement('Waveguide Coupler')
    model.set('name', 'WC2')
    model.set('x position', -400)
    model.set('y position', 0)
    model.set('coupling coefficient 1', 0.2)
    model.set('rotated',1)
    
    model.addelement('MODE Waveguide')
    model.set('name', 'WG0')
    model.set('x position', 0)
    model.set('y position', 0)
    model.set('rotated',1)
    model.set('length',6.28*4e-6)
    model.set('ldf filename',data1)
    model.set('delay compensation',3)
    
    model.addelement('MODE Waveguide')
    model.set('name', 'WG4')
    model.set('x position', -400)
    model.set('y position', 150)
    model.set('rotated',1)
    model.set('length',10e-6)
    model.set('ldf filename',data)
    model.set('delay compensation',2)
    
    model.addelement('MODE Waveguide')
    model.set('name', 'WG3')
    model.set('x position', -550)
    model.set('y position', -325)
    model.set('rotated',1)
    model.set('length',10e-6)
    model.set('ldf filename',data)
    model.set('delay compensation',2)

    model.addelement('MODE Waveguide')
    model.set('name', 'WG2')
    model.set('x position', 0)
    model.set('y position', -200)
    model.set('length',10e-6)
    model.set('ldf filename',data)
    model.set('delay compensation',2)
    
    model.addelement('MODE Waveguide')
    model.set('name', 'WG1')
    model.set('x position', -650)
    model.set('y position', -200)
    model.set('length',10e-6)
    model.set('ldf filename',data)
    model.set('delay compensation',2)

    model.addelement('Waveguide crossing')
    model.set('name', 'WGX')
    model.set('x position', -500)
    model.set('y position', -200)
    #set('rotated',1)
    
    
    
    model.connect('WC1', 'port 2', 'WC2', 'port 1')
    model.connect('WC1', 'port 4', 'WG0', 'port 1')
    model.connect('WC2', 'port 3', 'WG0', 'port 2')
    
    model.connect('WC1', 'port 1', 'WGX', 'port 3')
    model.connect('WC2', 'port 2', 'WGX', 'port 4')
    model.connect('WC2', 'port 4', 'WG4', 'port 1')
    model.connect('WGX', 'port 1', 'WG3', 'port 2')
    model.connect('WC1', 'port 3', 'WG2', 'port 1')
    model.connect('WGX', 'port 2', 'WG1', 'port 2')
    
    model.select('WC1')
    model.shiftselect('WC2')
    model.shiftselect('WG0')
    model.shiftselect('WGX')
    model.shiftselect('WG1')
    model.shiftselect('WG2')
    model.shiftselect('WG3')
    model.shiftselect('WG4')
    
    
    model.createcompound()
    
    model.set("name", name)
    
    model.set("x position", x)
    model.set("y position", y)
    
    model.addport(name, 'PD_in', 'Bidirectional', 'Optical', 'Left', 0.1)
    model.select(name+'::RELAY_1')
    model.set('x position', -850)
    model.set('y position', -165)
    model.set('rotated',2)
    model.connect(name+'::WG1', 'port 1', name+'::RELAY_1', 'port')
    
    model.addport(name, 'PD_out', 'Bidirectional', 'Optical', 'Right', 0.1)
    model.select(name+'::RELAY_2')
    model.set('x position', 150)
    model.set('y position', -200)
    model.set('rotated',4)
    model.connect(name+'::WG2', 'port 2', name+'::RELAY_2', 'port')
    
    model.addport(name, 'LD_in', 'Bidirectional', 'Optical', 'Top', 0.1)
    model.select(name+'::RELAY_3')
    model.set('x position', -545)
    model.set('y position', -450)
    model.set('rotated',3)
    model.connect(name+'::WG3', 'port 1', name+'::RELAY_3', 'port')
    
    model.addport(name, 'LD_out', 'Bidirectional', 'Optical', 'Bottom', 0.1)
    model.select(name+'::RELAY_4')
    model.set('x position', -400)
    model.set('y position', 300)
    model.set('rotated',1)
    model.connect(name+'::WG4', 'port 2', name+'::RELAY_4', 'port')
    
    model.addelement('Optical Power Meter')
    model.set('limit time range', ifLimitTimeRange)
    if (ifLimitTimeRange):
        model.set('start time', start_time)
    t = name.split("_")
    model.set('name', 'PM_' + t[1] + "_" + t[2])
    model.set('x position', x-150)
    model.set('y position', y-100)
    model.set('rotated',2)
    model.connect(name, 'PD_in', 'PM_'+ t[1] + "_" + t[2], 'Input')

    model.addelement('Optical Power Meter')
    model.set('limit time range', ifLimitTimeRange)
    if (ifLimitTimeRange):
        model.set('start time', start_time)
    t = name.split("_")
    model.set('name', 'PM_LD_out_' + t[1] + "_" + t[2])
    model.set('x position', x-150)
    model.set('y position', y+100)
    model.set('rotated',2)
    model.connect(name, 'LD_out', 'PM_LD_out_'+ t[1] + "_" + t[2], 'Input')
    
def LWIRArray(lumapi, laserNumber = 4, detectorNumber = 1, wl_start = 1551, wl_stop = 1555, N=1):
    fname = "LWIRArray.icp" + str(laserNumber) + '_' + str(detectorNumber)
    c=299792458
    if os.path.isfile(fname):
        model = lumapi.INTERCONNECT("LWIRArray.icp")
    else:
        model = lumapi.INTERCONNECT()
    model.switchtodesign()
    initialCutOffTime=1e-10  
    ifLimitTimeRange=1
    desiredTimeWindow = 2e-9
    desiredNumberOfSamples = 2**15
    dt = desiredTimeWindow/(desiredNumberOfSamples-1)
    numberOfSamples = np.floor(initialCutOffTime/dt)+desiredNumberOfSamples
    startTime=np.floor(initialCutOffTime/dt)*dt
    timeWindow=startTime+dt*(desiredNumberOfSamples-1)
#    numberOfSamples = 3*2**14
#    startTime=1e-9+1*timeWindow/numberOfSamples
#    timeWindow=timeWindow-timeWindow/numberOfSamples
    model.set("number of threads", 8)
    model.set('time window', timeWindow)
    model.set('number of samples', numberOfSamples) 
    model.set('sample mode frequency band', "single") 
    model.set('bitrate', 2.5e9)
    
    
    freq = np.arange(30,30+laserNumber)
#    np.linspace(3,6, laserNumber) 
    Res_name = {}
    MLD_name = []
    Detector_name=[]
    Detector_bottom_name=[]
    cnt=0
    temperature_file_index=np.arange(0,100,10) #np.random.permutation(np.arange(0,100))
    
    for i in range(0,laserNumber):
        
        MLD_name.append("MLD_" + str(i))
        
        Detector_bottom_name.append("Detector_bottom_" +str(i))
        if (not os.path.isfile(fname)):
            MLD(model, MLD_name[i], -26+i*300, -200, freq[i],c)
        for j in range(0,detectorNumber):
            if (i==0):
                Detector_name.append("Detector_" +str(j))
            Res_name[i,j]="Res_" + str(j) + "_" + str(i)
            if (not os.path.isfile(fname)):
                Res(model, Res_name[i,j], 'C:\\Users\\localuser\\Documents\\Interconnect\\filename_' + str(3000+(temperature_file_index[cnt]))+'.ldf' , i*300, j*300, startTime, ifLimitTimeRange)
#            Res(model, Res_name[i,j], 'C:\\Users\\localuser\\Documents\\Interconnect\\filename_3010.ldf' , i*300, j*300)
           
                cnt=cnt+0
                if (j==0):
                    model.connect(Res_name[i,j], 'LD_in', MLD_name[i], 'LD_out')
                if (i > 0):
                    model.connect(Res_name[i,j], 'PD_in', Res_name[i-1,j], 'PD_out')
                if (j > 0):
                    model.connect(Res_name[i,j], 'LD_in', Res_name[i,j-1], 'LD_out')
                if (i==0):
                   
                    BalancedDetector(model, Detector_name[j], -250, -26+j*300, 3, 0, startTime, ifLimitTimeRange,c)
                    model.connect(Detector_name[j], 'Detector_in', Res_name[i,j], 'PD_in')
                
        if (not os.path.isfile(fname)):
            BalancedDetector(model, Detector_bottom_name[i], -26+i*300, -26+(j+1)*300, 3, 1, startTime, ifLimitTimeRange,c)
            model.connect(Detector_bottom_name[i], 'Detector_in', Res_name[i,j], 'LD_out')
 
    

    
#    wl_step = ((wl_stop-wl_start)/N)
    laserDistance=2 #spacing between lasers in nanometers to avoid interference in Interconnect
    wl_step = ((wl_stop-wl_start+2*laserDistance*(laserNumber-1))/N)
    shift = int(laserDistance/wl_step) if int(1/wl_step)>=1 else 1
#    shift=0
    file_name='Result\\LOG_' + str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '.txt'

    st="shift="+str(shift)
    printData(file_name, st)
    st= 'wl_step=' +str(wl_step)
    printData(file_name, st)
#    lam=np.append(np.linspace(wl_start,wl_stop,N), np.linspace(wl_start,wl_stop,N))*1e-9
    lam=(np.linspace(wl_start-laserDistance*(laserNumber-1),wl_stop+laserDistance*(laserNumber-1),N))*1e-9
    power= {}  #np.array([[0.0]*N]*detectorNumber)
    power_o= {} #np.array([[0.0]*N]*detectorNumber)
    power_e= {}
#    ii=np.append(np.arange(0,N),np.arange(0,N))
#    //file_name=('Result\\LOG_' + str(laserNumber) + '_' + str(detectorNumber) + '_' + str(wl_start) + '_' + str(wl_stop) + '_' + str(N) + '.txt', 'a')
    for i in range(0,N-shift*(laserNumber-1)):
        
        st= str(i)+"________________________________________"
        printData(file_name, st)
        st= 'sample mode center frequency=' +str(lam[i+int(shift*(laserNumber-1)/2)]*1e9)
        printData(file_name, st)

        
        model.switchtodesign()
#        model.unselectall()
#        model.set('sample mode center frequency', 3e8/lam[i+shift*int(detectorNumber/2)]) 
        model.setnamed('::Root Element', 'sample mode center frequency', c/lam[i+int(shift*(laserNumber-1)/2)]);
        for k in range(0,laserNumber):
            st= '      Wavelength:   ' + str(lam[i+shift*k]*1e9)
            printData(file_name, st)
            model.select(MLD_name[k]+"::LD")
            model.set("frequency", c/lam[i+shift*k])
          
#        for j in Detector_name:
##            print(j)
#            model.select(j+"::PD")
#            model.set("frequency", 3e8/lam[i])
        model.run()

#        time.sleep(1)
        for j in range(0,detectorNumber):
            res = calculate_signal(model.getresult("OSC_"+str(j), "signal"), Detector_bottom_name, freq, model)
            res1 = model.getresult("RFSA_"+str(j), "signal")
            am = res1['power (W)']
            fr = res1['frequency']

#            plt.plot(fr, am)
            st= '     FFT data........................'
            printData(file_name, st)
            for k in range(0, laserNumber):
                ind=[]
                ind=(fr>(freq[k]*1e9-0.01e9))

                st= '     Frequency=' + str((fr[ind])[0]/1e9)
                printData(file_name, st)
                
                ind=list(np.squeeze(ind))
       
                
                st= "     Detector =" + str(j)+ "       Laser = " + str(k)  +'       '+'Wavelength=' + str(lam[i+shift*k]*1e9)
                printData(file_name, st)
#                index=[f>(freq[k]*1e9-1)][0]
                if (j,k,0) in power:
                    power[j,k,0] = np.append(power[j,k,0], res[k])
                    power[j,k,1] = np.append(power[j,k,1], lam[i+shift*k])
                else:
                    power[j,k,0] =  res[k]
                    power[j,k,1] = lam[i+shift*k]
                
                
                
                st= '          FFT Power=         ' + str(res[k]) +'       '+ str(10*np.log10(res[k]) if 10*np.log10(res[k])>0 else 0) 
                printData(file_name, st)
                
                if (j,k,0) in power_o:
                    power_o[j,k,0] = np.append(power_o[j,k,0], model.getresult("PM_"+str(j)+"_"+str(k),"sum/power"))
                    power_o[j,k,1] = np.append(power_o[j,k,1], lam[i+shift*k])
                else:
                    power_o[j,k,0] =  model.getresult("PM_"+str(j)+"_"+str(k),"sum/power")
                    power_o[j,k,1] = lam[i+shift*k]
                    
                st= '          Optical Power=     ' + str(model.getresult("PM_"+str(j)+"_"+str(k),"sum/power")) 
                printData(file_name, st)

                
                if (j,k,0) in power_e:
                    power_e[j,k,0] = np.append(power_e[j,k,0], np.sqrt(am[ind][0]))
                    power_e[j,k,1] = np.append(power_e[j,k,1], lam[i+shift*k])
                else:
                    power_e[j,k,0] =  np.sqrt(am[ind][0])
                    power_e[j,k,1] = lam[i+shift*k]
                st= '          RFSA Power=        ' +str((am[ind][0])) +'       '+ str(np.sqrt(am[ind][0])) +'       '+ str(10*np.log10(np.sqrt(am[ind][0]))) 
                printData(file_name, st)
#                
#    for i in range(0,detectorNumber):
#        for j in range(0,laserNumber):
#            arg=np.argsort(power[i,j,1])
#            power[i,j,1] = power[i,j,1][arg]
#            power[i,j,0] = power[i,j,0][arg]
#            
#            power_o[i,j,1] = power_o[i,j,1][arg]
#            power_o[i,j,0] = power_o[i,j,0][arg]

        
    model.save("LWIRArray.icp")
    
    return power_o, power, power_e
    
