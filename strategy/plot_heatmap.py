#!/usr/bin/python
# -*- coding: utf-8 -*-
# plot_heatmap.py

from sys import path
import os
path.append(os.getcwd() + '/../engine')
path.append(os.getcwd() + '/../')

import matplotlib.pyplot as plt
import numpy as np

def create_data_matrix(csv_ref, col_index):
    data = np.zeros((3,3))
    for i in range(0,3):
        for j in range (0,3):
            data[i][j] = float(csv_ref[i*3+j][col_index])
    return data

def create_heatmap(data, color, title):
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(data, cmap=color)
    row_labels = [0.5, 1.0, 1.5]
    column_labels = [2.0, 3.0, 4.0]
    
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x+0.5, y+0.5, '%.2f' % data[y,x],
                    horizontalalignment = 'center',
                    verticalalignment= 'center',
                    )
    
    plt.colorbar(heatmap)
    
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor = False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor = False)
    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    
    plt.suptitle(title, fontsize=18)
    plt.xlabel('Z-Score Exit Threshold', fontsize=14)
    plt.ylabel('Z-Score Entry Threshold', fontsize=14)
    plt.show()

if __name__ == "__main__":
    # Open the csv and obtain only the lines with a lookback of N
    N = 100
    csv_file = open("output.csv", "r").readlines()
    csv_ref = [
            c.replace('%','').strip().split(',')
            for c in csv_file if c.strip().split(',')[-2:-1] == [str(N)]
            ]
        
    """ col_index 2 for sharpe (
        		0 'Total Return',1 'CC Total Return',2'Sharpe Ratio',
        		3 'Sortino Ratio',4'Annualised MAR',5'Total Return MAR',
	    		6'Max Drawdown',7'Drawdown Duration',8'Average DD Duration', 
        		9'Average Drawdown', 10'Number of Drawdowns'
        		) + end_col 
    """
    sharpe_matrix = create_data_matrix(csv_ref, 2)
    maxdd_matrix = create_data_matrix(csv_ref, 6)
    
    create_heatmap(sharpe_matrix, plt.cm.Blues, 
                    title = 'N=%d Sharpe Ratio Heatmap' % N)
    create_heatmap(maxdd_matrix, plt.cm.Reds,
                    title = 'N=%d Max Drawdown Heatmap' % N)
    

    
