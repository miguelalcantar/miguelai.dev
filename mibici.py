import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def mode_graph(dataset):
    """print the graph of the most concurrent station
    """
    # sorting data
    sorted_data = dataset.sort_values(by=['Inicio_del_viaje'])
    # mode
    orig_mode = sorted_data.Origen_Id.mode()[0]

    # Two lists, which filter the data by the mode value
    orig_mode_data = sorted_data.loc[sorted_data['Origen_Id'] == orig_mode]
    dest_mode_data = sorted_data.loc[sorted_data['Destino_Id'] == orig_mode]

    # Counting the concurrence of use in batches of hours
    orig = orig_mode_data.Inicio_del_viaje.str[:13].value_counts(sort=False).sort_index()
    dest = dest_mode_data.Fin_del_viaje.str[:13].value_counts(sort=False).sort_index()

    # Getting their mean and difference
    orig_mean, dest_mean = orig.mean(), dest.mean()
    diff = dest_mean - orig_mean

    # finally printing and visualizing the data
    orig.plot(label=f"Orig: {orig_mean}")
    dest.plot(label=f"Dest: {dest_mean}, Difference:{diff}")
    plt.legend(loc='upper left')
    print('done')
    plt.show()

def stations_stabiliy(dataset,diff=1,min_gradient=12):
    """get list of unstable bases where:
    dataset is the data to be analized in mibici format,
    diff is the minimun difference between origin and destiny averge,
    min_gradient is the minimum amount in order to save the data in a list when gradient function is used
    """
    
    # Sorting data by time
    data_sorted = data.sort_values(by=['Inicio_del_viaje'])
    
    # Sorted descendent list of Origen_Id concurrence
    stations = data_sorted.Origen_Id.value_counts().index.tolist()
    
    bases = []
    
    for base in stations:
    # Filtering for origin and destiny stations
        base_orig = data_sorted.loc[data_sorted['Origen_Id'] == base]
        base_dest = data_sorted.loc[data_sorted['Destino_Id'] == base]
        
        # Counting concurrence by hour
        orig = base_orig.Inicio_del_viaje.str[:13].value_counts(sort=False).sort_index()
        dest = base_dest.Fin_del_viaje.str[:13].value_counts(sort=False).sort_index()
        # getting their averages
        orig_mean,dest_mean = orig.mean(), dest.mean()
    
        # differnces between av
        base_diff = dest_mean - orig_mean
    
        # if acutal difference is greater than diff 
        if abs(base_diff) > diff:
            bases.append({
                'Station':base,
                'avOrig': orig_mean,
                'avDest': dest_mean,
                'Diff':base_diff,
                 # Get all those values greater than min_gradient on a list
                'peak_orig':[(i,j) for i,j in zip(list(orig.index),np.gradient(orig)) if j > min_gradient],
                'peak_dest':[(i,j) for i,j in zip(list(dest.index),np.gradient(dest)) if j > min_gradient]
            })
            
    # Lastly, sort by their difference
    bases.sort(key = lambda i:i['Diff'])
    
    return bases
