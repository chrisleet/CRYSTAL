import matplotlib.pyplot as plt
import numpy as np

def normalize(shards):

    '''
    Normalizes each spectrum.

    Fits a polynomial to each spectrum's baseline, and then divides this 
    polynomial out. We make sure that the polynomial fit isn't affected by
    the lines in the spectrum by dividing the spectrum up into sets,
    fitting a line to each set, and then only fitting the polynomial to 
    the pixels above each line.
    '''

    for shard in shards.itervalues():
        remove_baseline(shard)

def remove_baseline(shard):

    '''
    Normalizes a shard.

    Worker function function of normalize.
    '''

    for spectrum in shard.spectra.itervalues():

        set_len = 100
        set_x, set_f, rdat_x, rdat_y = [], [], [], []
        set_no = int(len(spectrum.log_y)/set_len)

        for set_i in range(set_no+1):

            #Select set of data points
            x = np.array(spectrum.lin_x[set_i*set_len:(set_i+1)*set_len])
            y = np.array(spectrum.log_y[set_i*set_len:(set_i+1)*set_len])

            if len(x) == 0:
                break 

            #Fit and store linear fit to data points
            f = np.poly1d(np.polyfit(x, y, 1))
            set_x.append(x)
            set_f.append(f)
            
            #Filter out data points below linear fit
            for i in range(len(x)):
                if(y[i] >= f(x[i])):
                    rdat_x.append(x[i])
                    rdat_y.append(y[i])

        rdat_x = np.array(rdat_x)
        rdat_y = np.array(rdat_y)
        median_x = np.median(rdat_x)
        rdat_x -= median_x

        polyfit = np.poly1d(np.polyfit(rdat_x, rdat_y, 5))

        # This plots the baseline fit. Useful for debugging
        plot_baseline_fitter = False
        if plot_baseline_fitter:
            plot_baseline_fit(spectrum, set_x, set_f, median_x, rdat_x, rdat_y, polyfit, shardloc)
        
        baselineY = polyfit(spectrum.lin_x - median_x)
        spectrum.log_y -= baselineY

def plot_baseline_fit(self, spectrum, set_x, set_f, median_x, rdat_x, rdat_y, polyfit, shardloc):

    '''
    Plots the baseline fitter's fitting process.
    '''

    fig = plt.figure(facecolor='white')
    plt.title("Logged data for order {}, px:({},{}) w/ baselines fitted".format(shardloc[0], shardloc[1], shardloc[2]))
    plt.xlabel("Wavelength (Angstroms)")
    plt.ylabel("Log(Signal strength)")

    for set_i in range(len(set_x)):
        plt.plot(set_x[set_i], set_f[set_i](set_x[set_i]), color="red")
        
    plt.plot(spectrum.lin_x, spectrum.log_y, color="blue")
    plt.plot(rdat_x + median_x, rdat_y, color="green")
    plt.plot(rdat_x + median_x, polyfit(rdat_x), color="orange")
        
    plt.show()            
