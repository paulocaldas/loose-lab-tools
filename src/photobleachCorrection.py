from PyQt5 import QtWidgets
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob
import re
from scipy.optimize import curve_fit
   
def OpenFileDialog():
    '''this opens multiple dialogs to select n files
    returns a list of all path/to/file/filename'''
             
    app = QtWidgets.QApplication([dir])
    
    dialog = QtWidgets.QFileDialog()
    
    # filename are saved in a list according with the order of selection
    files, _  = dialog.getOpenFileNames(None, "Select Multiple Files in the Proper Order ", '', filter = "All files (*)")
    
    # use one of the files to save directory
    dirname = os.path.dirname(files[0]) 
    
    # remove path from filenames
    files = [os.path.basename(file) for file in files]
        
    return files, dirname

def GetAcqTimes(files, dirname, thres = 0, cutoff = 100, col = 'TRACK_DURATION', unit = 'seconds'):
    
    '''extract acquistion time (from filename) and lifetimes (from 'col' table) 
    for each file (and filename). Returns a list of lists with all info 
    input units (from trackmate) are assumed to be in seconds '''

    acq_times = [] # list to save filename, acquistion time and lifetimes distribution

    for file in files:
        
        # get acquistion time from file name
        
        file_wo = os.path.splitext(file)[0] # file name without extention
        
        for elem in re.split('[_,-, ]' , file_wo):

            if 'msec' in elem:
                acq_time = re.sub('msec', '', elem)
                acq_time = float(acq_time)/1000
                
            elif 'ms' in elem:
                acq_time = re.sub('ms', '', elem)
                acq_time = float(acq_time)/1000
                
            elif 'sec' in elem:
                acq_time = float(re.sub('sec', '', elem))
                
        # get lifetimes from the right column on the table (values are in frames by default)
        lifetimes = pd.read_csv(dirname + '/' + file)[col].values
        lifetimes = [value for value in lifetimes if value < cutoff and value > thres * acq_time]
        
        # save all info
        file_w_directory = dirname + '/' + file
        acq_times.append([file_w_directory, acq_time, lifetimes])
        
        #print('File:{} ; acq time: {} sec/frame'.format(file, acq_time))
        
    return acq_times

def ComputePhotobleachCorrection(t_exp = 0.5, thres = 1, cutoff = 100, bin_width = 2, plot_xlim = 6, col = 'TRACK_DURATION'):
    ''' this function fits a monoexponential decay to each distribution and saves all 
    parameters in a table'''
    
    AcqTimes = GetAcqTimes(*OpenFileDialog(), thres = thres, cutoff = cutoff, col = col)
    
    param_list = []

    fig, ax = plt.subplots(1,2,figsize = (8,3), dpi = 120)
    colors = plt.cm.viridis

    for n, file in enumerate(AcqTimes):
        
        acq_time = file[1]
        lifetimes = file[2]

        #format bin size
        binsize = bin_width * acq_time # bin_width in frames 
        binning = np.arange(min(lifetimes), max(lifetimes) + binsize, binsize) # creates an array with bins

        exp_decay = lambda x, amp, tau: amp * np.exp(-x/tau) #define expression for exponential fit
        counts, bins = np.histogram(lifetimes, bins = binning, density = True) # get bins and counts from the distribution

        bins = bins[:-1] + np.diff(bins/2) # compute bin center, instead of edges for fitting procedure
        param, cov = curve_fit(exp_decay, bins, counts, p0 = (counts[1], 1)) # fit exponential to datapoints

        x_fit = np.linspace(bins[0],bins[-1], 500) # create array to fit the data
        ax[0].plot(bins, counts, 'o', markeredgecolor = colors(n*50), markersize = 4, color = 'w') #plot original datapoints
        ax[0].plot(x_fit, exp_decay(x_fit, *param), '--', color = colors(n*50), label = str(acq_time) + ' s') #plot fitting result
        
        # print summary
        print('file:{} rate:{:.2}s/frame binsize:{:.2}s AppTau:{:.2}s'.format(os.path.basename(file[0]),acq_time, binsize, param[1]))
        
        # save all parameters
        param_list.append([acq_time, param[1]])

        ax[0].legend(frameon = False, fontsize = 10)
        ax[0].set_ylabel('normalized counts'); ax[0].set_xlabel('lifetimes (s)')
        ax[0].set_xlim([-0.1, plot_xlim])

    table_param = pd.DataFrame(param_list, columns = ['acq_time','tau_app']).sort_values('acq_time')

    x_axis = table_param.acq_time
    y_axis = table_param.tau_app * (table_param.acq_time)

    linear_reg = lambda x, m, b: m*x + b #linear regression
    linear_param, linear_cov = curve_fit(linear_reg, x_axis, y_axis)

    c_pb = linear_param[1]/t_exp #photobleaching constant
    tau  = 1/linear_param[0]

    #plt.figure(figsize = (4,3), dpi = 120)
    ax[1].plot(x_axis, y_axis, 'o', markeredgecolor = 'black', markersize = 6)
    
    x_fit_lin = np.linspace(0, np.max(x_axis) + 0.2,500)
    ax[1].plot(x_fit_lin, linear_reg(x_fit_lin, *linear_param), '--', color = 'crimson', 
               label = 'tau = {:.3} sec \npb_k = {:4.2}'.format(tau,c_pb))

    ax[1].set_ylabel('acq_time * tau_app'); ax[1].set_xlabel('acq_time(s)')
    ax[1].legend(frameon = False, fontsize = 10)

    'tau = {:.3} sec, C_pb = {:.3}'.format(tau,c_pb)
    
    return table_param
	
def ComputeLifetimeDistributions(t_exp = 0.5, thres = 1, cutoff = 100, bin_width = 2, col = 'TRACK_DURATION'):
    
    AcqTimes = GetAcqTimes(*OpenFileDialog(), thres = thres, cutoff = cutoff, col = col)
    
    for n, file in enumerate(AcqTimes):

            acq_time = file[1]
            lifetimes = file[2]

            #format bin size
            binsize = bin_width * acq_time # bin_width in frames 
            binning = np.arange(min(lifetimes), max(lifetimes) + binsize, binsize) # creates an array with bins

            exp_decay = lambda x, amp, tau: amp * np.exp(-x/tau) #define expression for exponential fit
            counts, bins = np.histogram(lifetimes, bins = binning, density = True) # get bins and counts from the distribution

            bins = bins[:-1] + np.diff(bins/2) # compute bin center, instead of edges for fitting procedure
            param, cov = curve_fit(exp_decay, bins, counts, p0 = (counts[1], 1)) # fit exponential to datapoints
            
            tau_app = round(param[1],1)
        
            plt.figure(figsize = (4,3), dpi = 120)
            x_axis_limit = np.median(lifetimes) * 6
            x_fit = np.linspace(bins[0],bins[-1], 1000) # create array to fit the data

            plt.hist(lifetimes, bins = binning, edgecolor = 'w', density = True, label = 'acq_time='+str(acq_time) + ' s')
            #plt.plot(bins, counts, 'o', markeredgecolor = 'black', markersize = 4, color = 'w') #plot original datapoints
            plt.plot(x_fit, exp_decay(x_fit, *param), '--', color = 'red', #plot fitting result
                       label = 'tau_app='+str(tau_app) + ' s') 
            plt.legend(frameon = False)
            plt.xlim([0,x_axis_limit])
            plt.ylabel('PDF')
            plt.xlabel('lifetime(s)')